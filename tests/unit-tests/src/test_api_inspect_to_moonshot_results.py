import os
import json
import pytest
from typer.testing import CliRunner

from moonshot.api import api_inspect_to_moonshot_results

runner = CliRunner()


@pytest.fixture
def valid_inspect_json():
    return json.dumps(
        {
            "version": 2,
            "status": "success",
            "eval": {
                "run_id": "3LGUy5TqXU3Usmu6vAY7Xj",
                "created": "2025-06-09T19:48:49+08:00",
                "task": "theory_of_mind",
                "task_id": "H8vAi9vPJpjCWRYSVZyMJz",
                "task_version": 0,
                "task_file": "inspect.py",
                "task_attribs": {},
                "task_args": {},
                "dataset": {
                    "name": "theory_of_mind",
                    "location": "example://theory_of_mind",
                    "samples": 100,
                    "sample_ids": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                        27,
                        28,
                        29,
                        30,
                        31,
                        32,
                        33,
                        34,
                        35,
                        36,
                        37,
                        38,
                        39,
                        40,
                        41,
                        42,
                        43,
                        44,
                        45,
                        46,
                        47,
                        48,
                        49,
                        50,
                        51,
                        52,
                        53,
                        54,
                        55,
                        56,
                        57,
                        58,
                        59,
                        60,
                        61,
                        62,
                        63,
                        64,
                        65,
                        66,
                        67,
                        68,
                        69,
                        70,
                        71,
                        72,
                        73,
                        74,
                        75,
                        76,
                        77,
                        78,
                        79,
                        80,
                        81,
                        82,
                        83,
                        84,
                        85,
                        86,
                        87,
                        88,
                        89,
                        90,
                        91,
                        92,
                        93,
                        94,
                        95,
                        96,
                        97,
                        98,
                        99,
                        100,
                    ],
                    "shuffled": False,
                },
                "model": "openai/gpt-4o",
                "model_args": {},
                "config": {},
                "revision": {
                    "type": "git",
                    "origin": "https://github.com/NagaNikshith-SGAISI/Inspect2Moonshot.git",
                    "commit": "7d5d1ed",
                },
                "packages": {"inspect_ai": "0.3.50"},
            },
            "plan": {
                "name": "plan",
                "steps": [
                    {"solver": "prompt_template", "params": {"template": "{prompt}"}},
                    {"solver": "generate", "params": {}},
                    {"solver": "self_critique", "params": {}},
                ],
                "config": {},
            },
            "results": {
                "total_samples": 100,
                "completed_samples": 100,
                "scores": [
                    {
                        "name": "model_graded_fact",
                        "scorer": "model_graded_fact",
                        "params": {},
                        "metrics": {
                            "accuracy": {
                                "name": "accuracy",
                                "value": 0.81,
                                "options": {},
                            },
                            "stderr": {
                                "name": "stderr",
                                "value": 0.03942772444036625,
                                "options": {},
                            },
                        },
                    }
                ],
            },
            "stats": {
                "started_at": "2025-06-09T19:48:49+08:00",
                "completed_at": "2025-06-09T19:50:40+08:00",
                "model_usage": {
                    "openai/gpt-4o": {
                        "input_tokens": 89254,
                        "output_tokens": 43878,
                        "total_tokens": 133132,
                    }
                },
            },
            "samples": [
                {
                    "id": 1,
                    "epoch": 1,
                    "input": [
                        {
                            "content": "Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?",
                            "source": "input",
                            "role": "user",
                        }
                    ],
                    "target": "bathtub",
                    "messages": [
                        {
                            "content": "Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?",
                            "source": "input",
                            "role": "user",
                        },
                        {
                            "content": "At the beginning, the boots were in the bathtub.",
                            "source": "generate",
                            "role": "assistant",
                        },
                        {
                            "content": '\nGiven the following question, initial answer and critique please generate an improved answer to the question:\n\n[BEGIN DATA]\n***\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n***\n[Answer]: At the beginning, the boots were in the bathtub.\n***\n[Critique]: The original answer is fully correct.\n***\n[END DATA]\n\nIf the original answer is already correct, just repeat the original answer exactly. Provide your answer at the end on its own line in the form "ANSWER: $ANSWER" (without quotes) where $ANSWER is the answer to the question.\n',
                            "role": "user",
                        },
                        {
                            "content": "ANSWER: At the beginning, the boots were in the bathtub.",
                            "source": "generate",
                            "role": "assistant",
                        },
                    ],
                    "output": {
                        "model": "gpt-4o-2024-08-06",
                        "choices": [
                            {
                                "message": {
                                    "content": "ANSWER: At the beginning, the boots were in the bathtub.",
                                    "source": "generate",
                                    "role": "assistant",
                                },
                                "stop_reason": "stop",
                            }
                        ],
                        "usage": {
                            "input_tokens": 221,
                            "output_tokens": 13,
                            "total_tokens": 234,
                        },
                        "time": 0.5431496999954106,
                    },
                    "scores": {
                        "model_graded_fact": {
                            "value": "C",
                            "answer": "ANSWER: At the beginning, the boots were in the bathtub.",
                            "explanation": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                            "metadata": {
                                "grading": [
                                    {
                                        "content": "\nYou are comparing a submitted answer to an expert answer on a given question. Here is the data:\n\n[BEGIN DATA]\n************\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n************\n[Expert]: bathtub\n************\n[Submission]: ANSWER: At the beginning, the boots were in the bathtub.\n************\n[END DATA]\n\nCompare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.\n\nDoes the submission contain the content in the expert answer?\n\n\nAfter assessing the submitted answer, reply with 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.  Please choose ONE option for the grade: either \"C\" for correct answers, or \"I\" for incorrect answers.\n\nFor example, after reviewing a correct answer you might write 'GRADE: C' or after reviewing an incorrect answer you might write 'GRADE: I'.\n\nFirst, write out in a step by step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then, end with your answer formatted as 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.\n\n",
                                        "role": "user",
                                    },
                                    {
                                        "content": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                                        "source": "generate",
                                        "role": "assistant",
                                    },
                                ]
                            },
                        }
                    },
                    "metadata": {},
                    "store": {},
                    "events": [
                        {
                            "timestamp": "2025-06-09T19:48:49.305509+08:00",
                            "event": "sample_init",
                            "sample": {
                                "input": [
                                    {
                                        "content": "attachment://cf0ef11e103a389b2fbab8855294a035",
                                        "source": "input",
                                        "role": "user",
                                    }
                                ],
                                "target": "bathtub",
                                "id": 1,
                            },
                            "state": {
                                "messages": [
                                    {
                                        "content": "attachment://cf0ef11e103a389b2fbab8855294a035",
                                        "source": "input",
                                        "role": "user",
                                    }
                                ],
                                "tools": [],
                                "tool_choice": None,
                                "store": {},
                                "output": {"model": "openai/gpt-4o", "choices": []},
                                "completed": False,
                                "metadata": {},
                            },
                        },
                        {
                            "timestamp": "2025-06-09T19:48:49.305509+08:00",
                            "event": "step",
                            "action": "begin",
                            "type": "solver",
                            "name": "prompt_template",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:49.305509+08:00",
                            "event": "step",
                            "action": "end",
                            "type": "solver",
                            "name": "prompt_template",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:49.305509+08:00",
                            "event": "step",
                            "action": "begin",
                            "type": "solver",
                            "name": "generate",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:49.305509+08:00",
                            "event": "model",
                            "model": "openai/gpt-4o",
                            "input": [
                                {
                                    "content": "attachment://cf0ef11e103a389b2fbab8855294a035",
                                    "source": "input",
                                    "role": "user",
                                }
                            ],
                            "tools": [],
                            "tool_choice": "none",
                            "config": {},
                            "output": {
                                "model": "gpt-4o-2024-08-06",
                                "choices": [
                                    {
                                        "message": {
                                            "content": "At the beginning, the boots were in the bathtub.",
                                            "source": "generate",
                                            "role": "assistant",
                                        },
                                        "stop_reason": "stop",
                                    }
                                ],
                                "usage": {
                                    "input_tokens": 51,
                                    "output_tokens": 11,
                                    "total_tokens": 62,
                                },
                                "time": 1.0453971999959322,
                            },
                            "call": {
                                "request": {
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": "attachment://cf0ef11e103a389b2fbab8855294a035",
                                        }
                                    ],
                                    "tools": None,
                                    "tool_choice": None,
                                    "model": "gpt-4o",
                                },
                                "response": {
                                    "id": "chatcmpl-BgVHs3vDOLPgeOoE8GjUAj1hDQew4",
                                    "choices": [
                                        {
                                            "finish_reason": "stop",
                                            "index": 0,
                                            "logprobs": None,
                                            "message": {
                                                "content": "At the beginning, the boots were in the bathtub.",
                                                "refusal": None,
                                                "role": "assistant",
                                                "audio": None,
                                                "function_call": None,
                                                "tool_calls": None,
                                                "annotations": [],
                                            },
                                        }
                                    ],
                                    "created": 1749469744,
                                    "model": "gpt-4o-2024-08-06",
                                    "object": "chat.completion",
                                    "service_tier": "default",
                                    "system_fingerprint": "fp_a288987b44",
                                    "usage": {
                                        "completion_tokens": 11,
                                        "prompt_tokens": 51,
                                        "total_tokens": 62,
                                        "completion_tokens_details": {
                                            "accepted_prediction_tokens": 0,
                                            "audio_tokens": 0,
                                            "reasoning_tokens": 0,
                                            "rejected_prediction_tokens": 0,
                                        },
                                        "prompt_tokens_details": {
                                            "audio_tokens": 0,
                                            "cached_tokens": 0,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            "timestamp": "2025-06-09T19:48:50.358601+08:00",
                            "event": "state",
                            "changes": [
                                {
                                    "op": "add",
                                    "path": "/output/usage",
                                    "value": {
                                        "input_tokens": 51,
                                        "output_tokens": 11,
                                        "total_tokens": 62,
                                    },
                                },
                                {
                                    "op": "add",
                                    "path": "/output/time",
                                    "value": 1.0453971999959322,
                                },
                                {
                                    "op": "replace",
                                    "path": "/output/model",
                                    "value": "gpt-4o-2024-08-06",
                                    "replaced": "openai/gpt-4o",
                                },
                                {
                                    "op": "add",
                                    "path": "/output/choices/0",
                                    "value": {
                                        "message": {
                                            "content": "At the beginning, the boots were in the bathtub.",
                                            "source": "generate",
                                            "role": "assistant",
                                        },
                                        "stop_reason": "stop",
                                    },
                                },
                                {
                                    "op": "add",
                                    "path": "/messages/1",
                                    "value": {
                                        "content": "At the beginning, the boots were in the bathtub.",
                                        "source": "generate",
                                        "role": "assistant",
                                    },
                                },
                            ],
                        },
                        {
                            "timestamp": "2025-06-09T19:48:50.358601+08:00",
                            "event": "step",
                            "action": "end",
                            "type": "solver",
                            "name": "generate",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:50.358601+08:00",
                            "event": "step",
                            "action": "begin",
                            "type": "solver",
                            "name": "self_critique",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:50.358601+08:00",
                            "event": "model",
                            "model": "openai/gpt-4o",
                            "input": [
                                {
                                    "content": "attachment://e04cf62be4778fba9279477c67f89cb5",
                                    "role": "user",
                                }
                            ],
                            "tools": [],
                            "tool_choice": "none",
                            "config": {},
                            "output": {
                                "model": "gpt-4o-2024-08-06",
                                "choices": [
                                    {
                                        "message": {
                                            "content": "The original answer is fully correct.",
                                            "source": "generate",
                                            "role": "assistant",
                                        },
                                        "stop_reason": "stop",
                                    }
                                ],
                                "usage": {
                                    "input_tokens": 131,
                                    "output_tokens": 7,
                                    "total_tokens": 138,
                                },
                                "time": 0.7737504999968223,
                            },
                            "call": {
                                "request": {
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": "attachment://e04cf62be4778fba9279477c67f89cb5",
                                        }
                                    ],
                                    "tools": None,
                                    "tool_choice": None,
                                    "model": "gpt-4o",
                                },
                                "response": {
                                    "id": "chatcmpl-BgVHtdsivdeNchEEXIaD1RXC3PabH",
                                    "choices": [
                                        {
                                            "finish_reason": "stop",
                                            "index": 0,
                                            "logprobs": None,
                                            "message": {
                                                "content": "The original answer is fully correct.",
                                                "refusal": None,
                                                "role": "assistant",
                                                "audio": None,
                                                "function_call": None,
                                                "tool_calls": None,
                                                "annotations": [],
                                            },
                                        }
                                    ],
                                    "created": 1749469745,
                                    "model": "gpt-4o-2024-08-06",
                                    "object": "chat.completion",
                                    "service_tier": "default",
                                    "system_fingerprint": "fp_a288987b44",
                                    "usage": {
                                        "completion_tokens": 7,
                                        "prompt_tokens": 131,
                                        "total_tokens": 138,
                                        "completion_tokens_details": {
                                            "accepted_prediction_tokens": 0,
                                            "audio_tokens": 0,
                                            "reasoning_tokens": 0,
                                            "rejected_prediction_tokens": 0,
                                        },
                                        "prompt_tokens_details": {
                                            "audio_tokens": 0,
                                            "cached_tokens": 0,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            "timestamp": "2025-06-09T19:48:51.123832+08:00",
                            "event": "model",
                            "model": "openai/gpt-4o",
                            "input": [
                                {
                                    "content": "attachment://cf0ef11e103a389b2fbab8855294a035",
                                    "source": "input",
                                    "role": "user",
                                },
                                {
                                    "content": "At the beginning, the boots were in the bathtub.",
                                    "source": "generate",
                                    "role": "assistant",
                                },
                                {
                                    "content": "attachment://1763074a72813091d1dc7d8726fd8089",
                                    "role": "user",
                                },
                            ],
                            "tools": [],
                            "tool_choice": "none",
                            "config": {},
                            "output": {
                                "model": "gpt-4o-2024-08-06",
                                "choices": [
                                    {
                                        "message": {
                                            "content": "ANSWER: At the beginning, the boots were in the bathtub.",
                                            "source": "generate",
                                            "role": "assistant",
                                        },
                                        "stop_reason": "stop",
                                    }
                                ],
                                "usage": {
                                    "input_tokens": 221,
                                    "output_tokens": 13,
                                    "total_tokens": 234,
                                },
                                "time": 0.5431496999954106,
                            },
                            "call": {
                                "request": {
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": "attachment://cf0ef11e103a389b2fbab8855294a035",
                                        },
                                        {
                                            "role": "assistant",
                                            "content": "At the beginning, the boots were in the bathtub.",
                                        },
                                        {
                                            "role": "user",
                                            "content": "attachment://1763074a72813091d1dc7d8726fd8089",
                                        },
                                    ],
                                    "tools": None,
                                    "tool_choice": None,
                                    "model": "gpt-4o",
                                },
                                "response": {
                                    "id": "chatcmpl-BgVHu3Ww5kEITwPTOZvKRLE4N5R6K",
                                    "choices": [
                                        {
                                            "finish_reason": "stop",
                                            "index": 0,
                                            "logprobs": None,
                                            "message": {
                                                "content": "ANSWER: At the beginning, the boots were in the bathtub.",
                                                "refusal": None,
                                                "role": "assistant",
                                                "audio": None,
                                                "function_call": None,
                                                "tool_calls": None,
                                                "annotations": [],
                                            },
                                        }
                                    ],
                                    "created": 1749469746,
                                    "model": "gpt-4o-2024-08-06",
                                    "object": "chat.completion",
                                    "service_tier": "default",
                                    "system_fingerprint": "fp_a288987b44",
                                    "usage": {
                                        "completion_tokens": 13,
                                        "prompt_tokens": 221,
                                        "total_tokens": 234,
                                        "completion_tokens_details": {
                                            "accepted_prediction_tokens": 0,
                                            "audio_tokens": 0,
                                            "reasoning_tokens": 0,
                                            "rejected_prediction_tokens": 0,
                                        },
                                        "prompt_tokens_details": {
                                            "audio_tokens": 0,
                                            "cached_tokens": 0,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            "timestamp": "2025-06-09T19:48:51.674088+08:00",
                            "event": "state",
                            "changes": [
                                {
                                    "op": "replace",
                                    "path": "/output/usage/total_tokens",
                                    "value": 234,
                                    "replaced": 62,
                                },
                                {
                                    "op": "replace",
                                    "path": "/output/usage/input_tokens",
                                    "value": 221,
                                    "replaced": 51,
                                },
                                {
                                    "op": "replace",
                                    "path": "/output/usage/output_tokens",
                                    "value": 13,
                                    "replaced": 11,
                                },
                                {
                                    "op": "replace",
                                    "path": "/output/choices/0/message/content",
                                    "value": "ANSWER: At the beginning, the boots were in the bathtub.",
                                    "replaced": "At the beginning, the boots were in the bathtub.",
                                },
                                {
                                    "op": "replace",
                                    "path": "/output/time",
                                    "value": 0.5431496999954106,
                                    "replaced": 1.0453971999959322,
                                },
                                {
                                    "op": "add",
                                    "path": "/messages/2",
                                    "value": {
                                        "content": "attachment://1763074a72813091d1dc7d8726fd8089",
                                        "role": "user",
                                    },
                                },
                                {
                                    "op": "add",
                                    "path": "/messages/3",
                                    "value": {
                                        "content": "ANSWER: At the beginning, the boots were in the bathtub.",
                                        "source": "generate",
                                        "role": "assistant",
                                    },
                                },
                            ],
                        },
                        {
                            "timestamp": "2025-06-09T19:48:51.674088+08:00",
                            "event": "step",
                            "action": "end",
                            "type": "solver",
                            "name": "self_critique",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:51.674088+08:00",
                            "event": "step",
                            "action": "begin",
                            "type": "scorer",
                            "name": "model_graded_fact",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:51.674088+08:00",
                            "event": "model",
                            "model": "openai/gpt-4o",
                            "input": [
                                {
                                    "content": "attachment://dc4732730f019805c1f9353fbdcef987",
                                    "role": "user",
                                }
                            ],
                            "tools": [],
                            "tool_choice": "none",
                            "config": {},
                            "output": {
                                "model": "gpt-4o-2024-08-06",
                                "choices": [
                                    {
                                        "message": {
                                            "content": "attachment://4936e8846a77b3770761615cd60b158f",
                                            "source": "generate",
                                            "role": "assistant",
                                        },
                                        "stop_reason": "stop",
                                    }
                                ],
                                "usage": {
                                    "input_tokens": 287,
                                    "output_tokens": 227,
                                    "total_tokens": 514,
                                },
                                "time": 4.819278300004953,
                            },
                            "call": {
                                "request": {
                                    "messages": [
                                        {
                                            "role": "user",
                                            "content": "attachment://dc4732730f019805c1f9353fbdcef987",
                                        }
                                    ],
                                    "tools": None,
                                    "tool_choice": None,
                                    "model": "gpt-4o",
                                },
                                "response": {
                                    "id": "chatcmpl-BgVHuKkfm4nYl1qUrL2Vaq6FHr5Hw",
                                    "choices": [
                                        {
                                            "finish_reason": "stop",
                                            "index": 0,
                                            "logprobs": None,
                                            "message": {
                                                "content": "attachment://4936e8846a77b3770761615cd60b158f",
                                                "refusal": None,
                                                "role": "assistant",
                                                "audio": None,
                                                "function_call": None,
                                                "tool_calls": None,
                                                "annotations": [],
                                            },
                                        }
                                    ],
                                    "created": 1749469746,
                                    "model": "gpt-4o-2024-08-06",
                                    "object": "chat.completion",
                                    "service_tier": "default",
                                    "system_fingerprint": "fp_a288987b44",
                                    "usage": {
                                        "completion_tokens": 227,
                                        "prompt_tokens": 287,
                                        "total_tokens": 514,
                                        "completion_tokens_details": {
                                            "accepted_prediction_tokens": 0,
                                            "audio_tokens": 0,
                                            "reasoning_tokens": 0,
                                            "rejected_prediction_tokens": 0,
                                        },
                                        "prompt_tokens_details": {
                                            "audio_tokens": 0,
                                            "cached_tokens": 0,
                                        },
                                    },
                                },
                            },
                        },
                        {
                            "timestamp": "2025-06-09T19:48:56.487895+08:00",
                            "event": "score",
                            "score": {
                                "value": "C",
                                "answer": "ANSWER: At the beginning, the boots were in the bathtub.",
                                "explanation": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                                "metadata": {
                                    "grading": [
                                        {
                                            "content": "\nYou are comparing a submitted answer to an expert answer on a given question. Here is the data:\n\n[BEGIN DATA]\n************\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n************\n[Expert]: bathtub\n************\n[Submission]: ANSWER: At the beginning, the boots were in the bathtub.\n************\n[END DATA]\n\nCompare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.\n\nDoes the submission contain the content in the expert answer?\n\n\nAfter assessing the submitted answer, reply with 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.  Please choose ONE option for the grade: either \"C\" for correct answers, or \"I\" for incorrect answers.\n\nFor example, after reviewing a correct answer you might write 'GRADE: C' or after reviewing an incorrect answer you might write 'GRADE: I'.\n\nFirst, write out in a step by step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then, end with your answer formatted as 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.\n\n",
                                            "role": "user",
                                        },
                                        {
                                            "content": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                                            "source": "generate",
                                            "role": "assistant",
                                        },
                                    ]
                                },
                            },
                            "target": "bathtub",
                        },
                        {
                            "timestamp": "2025-06-09T19:48:56.487895+08:00",
                            "event": "step",
                            "action": "end",
                            "type": "scorer",
                            "name": "model_graded_fact",
                        },
                    ],
                    "model_usage": {
                        "openai/gpt-4o": {
                            "input_tokens": 690,
                            "output_tokens": 258,
                            "total_tokens": 948,
                        }
                    },
                    "attachments": {
                        "cf0ef11e103a389b2fbab8855294a035": "Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?",
                        "e04cf62be4778fba9279477c67f89cb5": "\nGiven the following question and answer, please critique the answer. A good answer comprehensively answers the question and NEVER refuses to answer. If the answer is already correct do not provide critique - simply respond 'The original answer is fully correct'.\n\n[BEGIN DATA]\n***\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n***\n[Answer]: At the beginning, the boots were in the bathtub.\n***\n[END DATA]\n\nCritique: ",
                        "1763074a72813091d1dc7d8726fd8089": '\nGiven the following question, initial answer and critique please generate an improved answer to the question:\n\n[BEGIN DATA]\n***\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n***\n[Answer]: At the beginning, the boots were in the bathtub.\n***\n[Critique]: The original answer is fully correct.\n***\n[END DATA]\n\nIf the original answer is already correct, just repeat the original answer exactly. Provide your answer at the end on its own line in the form "ANSWER: $ANSWER" (without quotes) where $ANSWER is the answer to the question.\n',
                        "dc4732730f019805c1f9353fbdcef987": "\nYou are comparing a submitted answer to an expert answer on a given question. Here is the data:\n\n[BEGIN DATA]\n************\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n************\n[Expert]: bathtub\n************\n[Submission]: ANSWER: At the beginning, the boots were in the bathtub.\n************\n[END DATA]\n\nCompare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.\n\nDoes the submission contain the content in the expert answer?\n\n\nAfter assessing the submitted answer, reply with 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.  Please choose ONE option for the grade: either \"C\" for correct answers, or \"I\" for incorrect answers.\n\nFor example, after reviewing a correct answer you might write 'GRADE: C' or after reviewing an incorrect answer you might write 'GRADE: I'.\n\nFirst, write out in a step by step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then, end with your answer formatted as 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.\n\n",
                        "4936e8846a77b3770761615cd60b158f": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                    },
                },
            ],
            "reductions": [
                {
                    "scorer": "model_graded_fact",
                    "samples": [
                        {
                            "value": 1.0,
                            "answer": "ANSWER: At the beginning, the boots were in the bathtub.",
                            "explanation": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                            "metadata": {
                                "grading": [
                                    {
                                        "content": "\nYou are comparing a submitted answer to an expert answer on a given question. Here is the data:\n\n[BEGIN DATA]\n************\n[Question]: Jackson entered the hall. Chloe entered the hall. The boots is in the bathtub. Jackson exited the hall. Jackson entered the dining_room. Chloe moved the boots to the pantry. Where was the boots at the beginning?\n************\n[Expert]: bathtub\n************\n[Submission]: ANSWER: At the beginning, the boots were in the bathtub.\n************\n[END DATA]\n\nCompare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.\n\nDoes the submission contain the content in the expert answer?\n\n\nAfter assessing the submitted answer, reply with 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.  Please choose ONE option for the grade: either \"C\" for correct answers, or \"I\" for incorrect answers.\n\nFor example, after reviewing a correct answer you might write 'GRADE: C' or after reviewing an incorrect answer you might write 'GRADE: I'.\n\nFirst, write out in a step by step manner your reasoning about the criterion to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then, end with your answer formatted as 'GRADE: $LETTER' (without quotes) where LETTER is one of CI.\n\n",
                                        "role": "user",
                                    },
                                    {
                                        "content": 'To evaluate the submitted answer against the expert answer, we need to examine their factual content and determine if they convey the same information regarding the location of the boots at the beginning of the scenario described in the question.\n\nStep 1: Identify the factual content in the expert answer.\n- The expert answer states that "bathtub" is where the boots were at the beginning.\n\nStep 2: Identify the factual content in the submitted answer.\n- The submitted answer states: "At the beginning, the boots were in the bathtub."\n\nStep 3: Compare the factual content of both answers.\n- Both answers convey the same key information: that the boots were located in the bathtub at the beginning of the scenario.\n\nStep 4: Determine if there is any discrepancy in the factual content.\n- There is no discrepancy. Both answers provide the same factual information about the location of the boots at the beginning.\n\nStep 5: Conclusion based on the comparison.\n- Since the submitted answer contains the same factual content as the expert answer, it meets the criterion for a correct answer.\n\nTherefore, the submitted answer should be graded as correct.\n\nGRADE: C',
                                        "source": "generate",
                                        "role": "assistant",
                                    },
                                ]
                            },
                            "sample_id": 1,
                        }
                    ],
                }
            ],
        }
    )


def test_api_inspect_to_moonshot_results(valid_inspect_json):
    """
    Test the convertion of inspect results to moonshot via the API.

    This test function simulates the convertion of results from Inspect to Moonshot by calling the
    api_inspect_to_moonshot_results function with a given dataset_id. It then verifies that
    the output or exception raised matches the expected result as defined in
    expected_dict.

    Args:
        valid_inspect_json (_type_): _description_
    """
    output = api_inspect_to_moonshot_results(valid_inspect_json)
    assert output is not None

    data = json.loads(output)
    assert data["metadata"]["id"] == "3LGUy5TqXU3Usmu6vAY7Xj"

    prompt = data["results"]["recipes"][0]["details"][0]["data"][0]["prompt"]
    assert isinstance(prompt, str)
    assert prompt.startswith("Jackson entered the hall")