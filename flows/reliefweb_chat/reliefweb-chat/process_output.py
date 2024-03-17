
from promptflow import tool
import json

@tool
def process_output(user_question: str, query_entities: str, rweb_query: str, rweb_results: str, llm_summary_result: str, \
                   refs: str, llm_question_result: str, content_safety_result: bool) -> dict:

    if content_safety_result == 'Accept':
        result = json.loads(llm_summary_result)
        if "summaries_per_step" in result:
            result = result["summaries_per_step"]
        llm_summary_result_processed = json.dumps(result[-1]['denser_summary'])

        refs = json.loads(refs)
        llm_summary_result = json.loads(llm_summary_result)
        rweb_results = json.loads(rweb_results)

        full_output = {
            "user_question": user_question,
            "query_entities": query_entities,
            "rweb_query": rweb_query,
            "rweb_results": rweb_results,
            "llm_summary_result": llm_summary_result,
            "llm_summary_result_processed": llm_summary_result_processed,
            "llm_question_result": llm_question_result,
            "refs": refs
        }
        full_output['text_output'] = f"SUMMARY:\n\n {llm_summary_result_processed}\n\nANSWER:\n\n{llm_question_result}\n\nREFERENCES:\n\n{refs}"
    else:
        full_output = {}
        full_output['text_output'] = "Content safety check failed. Please try again with a different question."

    full_output['content_safety_result'] = content_safety_result
    with open('output.json', 'w') as f:
        json.dump(full_output, f, indent=4)

    return full_output
