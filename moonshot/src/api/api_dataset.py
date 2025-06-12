import json
import os

from pydantic import validate_call

from moonshot.src.datasets.dataset import Dataset
from moonshot.src.datasets.dataset_arguments import DatasetArguments


# ------------------------------------------------------------------------------
# Datasets APIs
# ------------------------------------------------------------------------------
@validate_call
def api_delete_dataset(ds_id: str) -> bool:
    """
    Deletes a dataset identified by its unique dataset ID.

    Args:
        ds_id (str): The unique identifier for the dataset to be deleted.

    Returns:
        bool: True if the dataset was successfully deleted, False otherwise.

    Raises:
        Exception: If the deletion process encounters an error.
    """
    return Dataset.delete(ds_id)


def api_get_all_datasets() -> list[dict]:
    """
    This function retrieves all available datasets and returns them as a list of dictionaries. Each dictionary
    represents a dataset and contains its information.

    Returns:
        list[dict]: A list of dictionaries, each representing a dataset.
    """
    _, datasets = Dataset.get_available_items()
    return [dataset.to_dict() for dataset in datasets]


def api_get_all_datasets_name() -> list[str]:
    """
    This function retrieves all available dataset names and returns them as a list.

    Returns:
        list[str]: A list of dataset names.
    """
    datasets_name, _ = Dataset.get_available_items()
    return datasets_name


def api_download_dataset(
    name: str, description: str, reference: str, license: str, **kwargs
) -> str:
    """
    Downloads a dataset from Hugging Face and creates a new dataset with the provided details.

    This function takes the name, description, reference, and license for a new dataset as input, along with additional
    keyword arguments for downloading the dataset from Hugging Face. It then creates a new DatasetArguments object with
    these details and an empty id. The id is left empty because it will be generated from the name during the creation
    process. The function then calls the Dataset's create method to create the new dataset.

    Args:
        name (str): The name of the new dataset.
        description (str): A brief description of the new dataset.
        reference (str): A reference link for the new dataset.
        license (str): The license of the new dataset.
        kwargs: Additional keyword arguments for downloading the dataset from Hugging Face.

    Returns:
        str: The ID of the newly created dataset.
    """
    examples = Dataset.download_hf(**kwargs)
    ds_args = DatasetArguments(
        id="",
        name=name,
        description=description,
        reference=reference,
        license=license,
        examples=examples,
    )
    return Dataset.create(ds_args)


def normalize_examples(raw_examples: list[dict]) -> list[dict]:
    sample_fields = {
        "input": ("input", "question", "prompt"),
        "target": ("target", "answer", "label"),
    }

    converted = []
    for idx, item in enumerate(raw_examples):
        input_data = None
        for field in sample_fields["input"]:
            if field in item and item[field]:
                input_data = item[field]
                break
        if isinstance(input_data, list):
            input_data = " ".join(part.get("content", "") for part in input_data)
            
        target_data = None
        for field in sample_fields["target"]:
            if field in item and item[field]:
                target_data = item[field]
                break
        if isinstance(target_data, list):
            if target_data and target_data[0]:
                target_data = target_data[0]
        if isinstance(target_data, dict):
            target_data = target_data.get("content", "")

        converted.append({
            "id": item.get("id", str(idx)),
            "input": input_data,
            "target": target_data,
        })

    return converted

def api_convert_dataset(
    name: str, description: str, reference: str, license: str, file_path: str
) -> str:
    """
    Converts a JSON, JSONL (Inspect-style), or CSV file to a Moonshot dataset and registers it.

    Args:
        name (str): The name of the new dataset.
        description (str): A brief description of the new dataset.
        reference (str): A reference link for the new dataset.
        license (str): The license of the new dataset.
        file_path (str): Path to .json, .jsonl, or .csv file.

    Returns:
        str: The ID of the newly created dataset.
    """
    if not (file_path.endswith(".json") or file_path.endswith(".jsonl") or file_path.endswith(".csv")):
        raise ValueError("Unsupported file format. Please provide a JSON, JSONL, or CSV file.")

    if os.path.getsize(file_path) == 0:
        raise ValueError("The uploaded file is empty.")

    try:
        if file_path.endswith(".json"):
            with open(file_path, encoding='utf-8') as f:
                json_data = json.load(f)
                
            raw_examples = json_data if isinstance(json_data, list) else json_data.get("examples", [])
            examples = normalize_examples(raw_examples)

        elif file_path.endswith(".csv"):
            raw_examples = Dataset.convert_data(file_path)
            examples = normalize_examples(raw_examples)

        elif file_path.endswith(".jsonl"):
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_examples = [json.loads(line) for line in f]
            examples = normalize_examples(raw_examples)

        if not examples:
            raise ValueError("No valid examples found in the dataset.")

        ds_args = DatasetArguments(
            id="",
            name=name,
            description=description,
            reference=reference,
            license=license,
            examples=iter(examples),
        )
        return Dataset.create(ds_args)

    except Exception as e:
        raise RuntimeError(f"Failed to convert dataset: {e}")