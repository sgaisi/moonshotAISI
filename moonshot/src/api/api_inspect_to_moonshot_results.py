from datetime import datetime
import json
from typing import Union
from pydantic import validate_call

@validate_call
def api_inspect_to_moonshot_results(inspect_json: str) -> Union[str, None]:
    """
    Transforms Inspect evaluation result JSON into Moonshot-compatible format.

    This function extracts and normalizes evaluation metadata, sample conversations,
    predicted results, and scoring from the Inspect tool format into the expected
    format for use with the Moonshot evaluation UI.

    Args:
        inspect_json (str): JSON string from Inspect evaluation logs.

    Returns:
        Union[str, None]: JSON string in Moonshot format, or None if an error occurs.
    """
    try:
        data = json.loads(inspect_json)

        start_time = data.get("stats", {}).get("started_at")
        end_time = data.get("stats", {}).get("completed_at")
        duration = None
        if start_time and end_time:
            try:
                start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                duration = (end - start).total_seconds()
            except ValueError:
                pass

        model = data.get("eval", {}).get("model", "")
        dataset = data.get("eval", {}).get("dataset", {})
        dataset_name = dataset.get("name", "unknown")
        total_samples = data.get("results", {}).get("total_samples", "")

        # Try to extract accuracy
        accuracy = 0
        try:
            accuracy = data.get("results", {}).get("scores", [])[0].get("metrics", {}).get("accuracy", {}).get("value", 0)
        except (IndexError, TypeError):
            pass

        def calculate_sample_duration(sample):
            try:
                events = sample.get("transcript", {}).get("events", [])
                if not events:
                    return None
                start_time = datetime.fromisoformat(events[0]["timestamp"].replace('Z', '+00:00'))
                end_time = datetime.fromisoformat(events[-1]["timestamp"].replace('Z', '+00:00'))
                return (end_time - start_time).total_seconds()
            except (KeyError, ValueError, IndexError):
                return None

        def calculate_grade(score):
            if score >= 80: return "A"
            elif score >= 60: return "B"
            elif score >= 40: return "C"
            elif score >= 20: return "D"
            else: return "E"

        processed_samples = []
        for sample in data.get("samples", []):
            sample_duration = calculate_sample_duration(sample)
            events = sample.get("transcript", {}).get("events", [])
            prompt = []
            context = []

            for event in events:
                role = event.get("role")
                content = event.get("content", "")
                if role == "user":
                    prompt.append({"role": "user", "content": content, "source": "input"})
                elif role == "system":
                    prompt.insert(0, {"role": "system", "content": content, "source": "system"})
                else:
                    context.append({"role": role, "content": content, "source": "context"})

            processed_sample = {
                "prompt": sample.get("input", [{}])[0].get("content", ""),
                "predicted_result": {
                    "response": sample.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "context": context
                },
                "target": sample.get("target", ""),
                "duration": sample_duration
            }

            if "score" in sample or "explanation" in sample:
                processed_sample["evaluation"] = {
                    "grade": sample.get("score", ""),
                    "explanation": sample.get("explanation", ""),
                    "score_type": "model_graded_fact"
                }

            processed_samples.append(processed_sample)

        metrics = data.get("results", {}).get("scores", "")
        metrics_dict = {}
        if metrics and isinstance(metrics, list):
            for item in metrics:
                if isinstance(item, list) and len(item) == 2:
                    key, value = item
                    metrics_dict[key] = value
                elif isinstance(item, dict):
                    metrics_dict.update(item)

        metrics_dict.update({
            "accuracy": accuracy * 100,
            "grading_criteria": {"accuracy": accuracy * 100}
        })

        transformed_data = {
            "metadata": {
                "id": data.get("eval", {}).get("run_id", "unknown"),
                "start_time": start_time,
                "end_time": end_time,
                "duration": duration,
                "status": data.get("status", "completed"),
                "recipes": [dataset_name] if dataset_name else [],
                "cookbooks": None,
                "endpoints": [model] if model else [],
                "prompt_selection_percentage": 100,
                "random_seed": 0,
                "system_prompt": data.get("plan", {}).get("steps", [{}])[0].get("params", {}).get("template", "")
            },
            "results": {
                "recipes": [
                    {
                        "id": dataset_name,
                        "details": [
                            {
                                "model_id": model,
                                "dataset_id": dataset_name,
                                "prompt_template_id": dataset_name,
                                "data": processed_samples,
                                "metrics": metrics_dict
                            }
                        ],
                        "evaluation_summary": [
                            {
                                "model_id": model,
                                "num_of_prompts": total_samples,
                                "avg_grade_value": accuracy * 100,
                                "grade": calculate_grade(accuracy * 100)
                            }
                        ],
                        "grading_scale": {
                            "A": [80, 100],
                            "B": [60, 79],
                            "C": [40, 59],
                            "D": [20, 39],
                            "E": [0, 19]
                        },
                        "total_num_of_prompts": total_samples
                    }
                ]
            }
        }

        return json.dumps(transformed_data, indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error: {e}"
