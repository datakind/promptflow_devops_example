import ast
import json
import sys

from promptflow import tool


@tool
def extract_references(results: str) -> str:
    results = json.loads(results)
    refs = []
    for r in results:
        ref = {}
        ref["title"] = r["title"]
        ref["url"] = r["url"]
        sources = []
        for s in r["source"]:
            sources.append(s["name"])
        ref["source"] = sources
        refs.append(ref)
    refs = json.dumps(refs, indent=4)
    return str(refs)
