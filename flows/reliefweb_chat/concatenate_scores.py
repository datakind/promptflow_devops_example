import re

import numpy as np
from promptflow import tool


@tool
def concat_results(groundesness_score: str):
    """
    Concatenates the results of groundedness scores.

    Args:
        deep_eval results (str): The evaluation score

    Returns:
        dict: A dictionary containing the concatenated
        results of groundedness scores.
    """

    load_list = [{"name": "gpt_groundedness", "score": groundesness_score}]
    score_list = []
    errors = []
    for item in load_list:
        try:
            score = item["score"]
            match = re.search(r"\d", score)
            if match:
                score = match.group()
            score = float(score)
        except Exception as e:
            score = np.nan
            item = item["name"]
            errors.append({"name": item, "msg": str(e), "data": item["score"]})
        score_list.append({"name": item["name"], "score": score})

    variant_level_result = {}
    for item in score_list:
        score = item["score"]
        pass_rate = 1 if score > 3 else 0
        item_name = str(item["name"])
        variant_level_result[item_name] = item["score"]
        variant_level_result[item_name + "_pass_rate"] = pass_rate

    return variant_level_result
