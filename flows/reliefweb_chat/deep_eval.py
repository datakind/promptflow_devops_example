
from promptflow import tool
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import SummarizationMetric
from deepeval.test_case import LLMTestCase
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
import os
from langchain_openai import AzureChatOpenAI
from deepeval.models.base_model import DeepEvalBaseLLM
from promptflow.connections import AzureOpenAIConnection

from dotenv import load_dotenv
load_dotenv('../../.env')

class AzureOpenAI(DeepEvalBaseLLM):
    def __init__(
        self,
        model
    ):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        return "Custom Azure OpenAI Model"

# Deep eval, see https://github.com/confident-ai/deepeval

@tool
def test_case(processed_output: dict, conn: AzureOpenAIConnection, deployment_name: str):

    conn_dict = dict(conn)

    rweb_results = processed_output['rweb_results']
    input = ""
    for r in rweb_results:
        input += r['title'] + " " + str(r['body']) 

    actual_output = processed_output['llm_summary_result_processed']

    # OpenAI
    #model = ChatOpenAI(
    #    # model_name="gpt-3.5-turbo",
    #    model_name="gpt-3.5-turbo-16k",
    #    api_key=os.getenv("OPENAI_API_KEY"),
    #    temperature=1,
    #    max_tokens=1000,
    #)

    custom_model = AzureChatOpenAI(
        openai_api_version=conn_dict["api_version"],
        azure_deployment=deployment_name,
        azure_endpoint=conn_dict["api_base"],
        openai_api_key=conn_dict["api_key"],
    )

    model = AzureOpenAI(model=custom_model)

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
        model=model,
        #assessment_questions=[
        #    "Which organizations are mentioned?",
        #    "How many people, organizations or countries are involved?",
        #    "What types of situations are mentioned?"
        #    #processed_output['user_question']
        #]
    )

    metric.measure(test_case)
    print(metric.score)
    print(metric.reason)

    return {
        "summarization_score": metric.score,
        "summarization_score_reason": metric.reason
    }

# Just for testing
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

    # Replace these with real values
    custom_model = AzureChatOpenAI(
        openai_api_version=os.getenv("OPENAI_API_VERSION"),
        azure_deployment=os.getenv("DEPLOYMENT_NAME"),
        azure_endpoint=os.getenv("BASE_URL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
    )
    model = AzureOpenAI(model=custom_model)

    test_case = LLMTestCase(input=input, actual_output=actual_output)
    metric = SummarizationMetric(
        threshold=0.5,
        model=model,
        # Score can be determined with set questions
        #assessment_questions=[
        #    "Is the coverage score based on a percentage of 'yes' answers?",
        #    "Does the score ensure the summary's accuracy with the source?",
        #    "Does a higher score mean a more comprehensive summary?"
        #]
    )

    metric.measure(test_case)
    print(metric.score)
    print(metric.reason)