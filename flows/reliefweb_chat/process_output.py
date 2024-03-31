import json

import jsonlines
from promptflow import tool


@tool
def process_output(
    user_question: str,
    query_entities: str,
    rweb_query: str,
    rweb_results: str,
    llm_summary_result: str,
    refs: str,
    llm_question_result: str,
    content_safety_result: str,
    deep_eval_score: float,
    deep_eval_score_reason: str,
) -> dict:
    """
    Process the output of the ReliefWeb chat flow.

    Args:
        user_question (str): The user's question.
        query_entities (str): The query entities.
        rweb_query (str): The ReliefWeb query.
        rweb_results (str): The ReliefWeb results.
        llm_summary_result (str): The LLM summary result.
        refs (str): The references.
        llm_question_result (str): The LLM question result.
        content_safety_result (str): The content safety result.
        deep_eval_score (float): The deep evaluation score.
        deep_eval_score_reason (str): The reason for the deep evaluation score.

    Returns:
        dict: The processed output.

    Raises:
        None
    """
    # TODO Hack for bug where running full output generates different output compared to just running this node.
    if "suggested_action" in content_safety_result:
        content_safety_result = content_safety_result["suggested_action"]

    if content_safety_result == "Accept":

        llm_summary_result = (
            llm_summary_result.replace("```json", "").replace("```", "").strip()
        )

        # Chain of Density prompt
        if "summaries_per_step" in llm_summary_result:
            result = json.loads(llm_summary_result)
            result = result["summaries_per_step"]
            # Extract last prompt
            llm_summary_result_processed = json.dumps(result[-1]["denser_summary"])
            llm_summary_result = json.loads(llm_summary_result)
        else:
            llm_summary_result_processed = llm_summary_result

        refs = json.loads(refs)
        rweb_results = json.loads(rweb_results)

        # If deep eval returned anything less than a perfect score, alert the user to the potential
        # concerns with the output
        if deep_eval_score < 1.0:
            llm_question_result += f"\n\nWarning! Fact checker evaluation returned a score of {deep_eval_score}/1.0"
            llm_question_result += f"Reason:\n\n{deep_eval_score_reason}"

        full_output = {
            "user_question": user_question,
            "query_entities": query_entities,
            "rweb_query": rweb_query,
            "rweb_results": rweb_results,
            "llm_summary_result": llm_summary_result,
            "llm_summary_result_processed": llm_summary_result_processed,
            "llm_question_result": llm_question_result,
            "refs": refs,
        }
        full_output["text_output"] = llm_question_result

        # Write data to jsonl to get content for data.jsonl
        with jsonlines.open("output.jsonl", mode="w") as writer:
            r = {}
            r["chat_history"] = []
            r["question"] = full_output["user_question"]
            r["context"] = str(full_output["rweb_results"])
            writer.write(r)
    else:
        full_output = {}
        full_output["text_output"] = (
            "Content safety check failed. Please try again with a different question."
        )

    full_output["content_safety_result"] = content_safety_result
    full_output["deep_eval_score"] = deep_eval_score
    full_output["deep_eval_score_reason"] = deep_eval_score_reason

    with open("output.json", "w") as f:
        json.dump(full_output, f, indent=4)

    return full_output
