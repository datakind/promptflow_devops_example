
from promptflow import tool
import json

@tool
def process_output(result: str, refs: str) -> str:
    result = json.loads(result)
    result = result["denser_summary"]
    result += f"\n\nRefrences:\n\n{refs}"
    return result
