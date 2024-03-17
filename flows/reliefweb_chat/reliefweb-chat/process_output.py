
from promptflow import tool
import json

@tool
def process_output(result: str, refs: str) -> str:
    result = json.loads(result)
    if "summaries_per_step" in result:
        result = result["summaries_per_step"]
    print(result)
    result = result[-1]["denser_summary"]
    result += f"\n\nRefrences:\n\n{refs}"
    print(result)
    print("uuuuuuuu")
    return result
