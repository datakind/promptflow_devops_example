
from promptflow import tool
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv
load_dotenv('../../.env')

# Deep eval, see https://github.com/confident-ai/deepeval

@tool
def test_case(processed_output: dict):
    rweb_results = processed_output['rweb_results']

    input = ""
    for r in rweb_results:
        input += r['title'] + " " + str(r['body']) 

    actual_output = processed_output['llm_summary_result_processed']

    # What if we ta

    #answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.5)
    #test_case = LLMTestCase(
    #    input="What if these shoes don't fit?",
    #    # Replace this with the actual output from your LLM application
    #    actual_output=llm_model_summary,
    #    retrieval_context=[raw_text]
    #)
    #assert_test(test_case, [answer_relevancy_metric])

    print(input)
    print("=======")
    print(actual_output)

    test_case = LLMTestCase(input=input, actual_output=actual_output)
    metric = SummarizationMetric(
        threshold=0.5,
        model="gpt-4",
        #assessment_questions=[
        #    "Is the coverage score based on a percentage of 'yes' answers?",
        #    "Does the score ensure the summary's accuracy with the source?",
        #    "Does a higher score mean a more comprehensive summary?"
        #]
    )

    metric.measure(test_case)
    print(metric.score)
    print(metric.reason)

if __name__ == "__main__":
    # This is the original text to be summarized
    input = """
    The 'coverage score' is calculated as the percentage of assessment questions
    for which both the summary and the original document provide a 'yes' answer. This
    method ensures that the summary not only includes key information from the original
    text but also accurately represents it. A higher coverage score indicates a
    more comprehensive and faithful summary, signifying that the summary effectively
    encapsulates the crucial points and details from the original content.
    """

    # This is the summary, replace this with the actual output from your LLM application
    actual_output="""
    The coverage score quantifies how well a summary captures and
    accurately represents key information from the original text,
    with a higher score indicating greater comprehensiveness.
    """

    input = "714 cows walked from top to bottom fields last friday"
    actual_output = input

    test_case = LLMTestCase(input=input, actual_output=actual_output)
    metric = SummarizationMetric(
        threshold=0.5,
        model="gpt-4",
        assessment_questions=[
            "Is the coverage score based on a percentage of 'yes' answers?",
            "Does the score ensure the summary's accuracy with the source?",
            "Does a higher score mean a more comprehensive summary?"
        ]
    )

    metric.measure(test_case)
    print(metric.score)
    print(metric.reason)