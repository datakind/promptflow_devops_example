from promptflow import tool


@tool
def my_python_tool(
    hate_category: str,
    self_harm_category: str,
    sexual_category: str,
    violence_category: str,
    text: str,
) -> dict:
    """
    This function takes in various categories and a text input, and returns a dictionary
    representing the output of Azure content safety. It is a placeholder to simulate a content
    safety node. You can add content safety tests here using Libraries like gaurdrails AI or deep eval.

    Args:
        hate_category (str): The category for hate content.
        self_harm_category (str): The category for self-harm content.
        sexual_category (str): The category for sexual content.
        violence_category (str): The category for violence content.
        text (str): The input text to be analyzed.

    Returns:
        dict: A dictionary representing the output of Azure content safety, with the following structure:
            {
                "suggested_action": "Accept",
                "action_by_category": {
                    "Hate": "Accept",
                    "SelfHarm": "Accept",
                    "Sexual": "Accept",
                    "Violence": "Accept",
                },
            }
    """
    output = {
        "suggested_action": "Accept",
        "action_by_category": {
            "Hate": "Accept",
            "SelfHarm": "Accept",
            "Sexual": "Accept",
            "Violence": "Accept",
        },
    }

    return output
