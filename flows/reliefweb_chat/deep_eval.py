import os

from deepeval.metrics import FaithfulnessMetric, SummarizationMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from promptflow import tool
from promptflow.connections import AzureOpenAIConnection

load_dotenv("../../.env")


class AzureOpenAI(DeepEvalBaseLLM):
    """
    A class representing a custom Azure OpenAI model.

    Attributes:
        model: The underlying model used for generating responses.

    Methods:
        load_model: Loads the model.
        generate: Generates a response given a prompt.
        a_generate: Asynchronously generates a response given a prompt.
        get_model_name: Returns the name of the model.
    """

    def __init__(self, model):
        """
        Initializes an instance of the DeepEval class.

        Parameters:
        model (object): The model object to be used for evaluation.
        """
        self.model = model

    def load_model(self):
        """
        Loads and returns the model.

        Returns:
            The loaded model.
        """
        return self.model

    def generate(self, prompt: str) -> str:
        """
        Generates a response based on the given prompt using the chat model.

        Args:
            prompt (str): The prompt to generate a response for.

        Returns:
            str: The generated response.
        """
        chat_model = self.load_model()
        return chat_model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        """
        Generates a response using the chat model.

        Args:
            prompt (str): The prompt for generating the response.

        Returns:
            str: The generated response.
        """
        chat_model = self.load_model()
        res = await chat_model.ainvoke(prompt)
        return res.content

    def get_model_name(self):
        """
        Returns the name of the custom Azure OpenAI model.
        """
        return "Custom Azure OpenAI Model"


# Deep eval, see https://github.com/confident-ai/deepeval
@tool
def test_case(
    processed_output: dict, conn: AzureOpenAIConnection, deployment_name: str
):
    """
    An example function for evaluating a question using the deepeval library.

    Args:
        processed_output (dict): The processed output containing the necessary data for evaluation.
        conn (AzureOpenAIConnection): The AzureOpenAIConnection object for connecting to Azure services.
        deployment_name (str): The name of the deployment.

    Returns:
        dict: A dictionary containing the evaluation score and reason.
    """
    conn_dict = dict(conn)

    rweb_results = processed_output["rweb_results"]
    input = ""
    for r in rweb_results:
        input += r["title"] + " " + str(r["body"])

    actual_output = processed_output["llm_summary_result_processed"]

    # Set up LLM connection
    custom_model = AzureChatOpenAI(
        openai_api_version=conn_dict["api_version"],
        azure_deployment=deployment_name,
        azure_endpoint=conn_dict["api_base"],
        openai_api_key=conn_dict["api_key"],
    )
    model = AzureOpenAI(model=custom_model)

    user_question = processed_output["user_question"]
    actual_output = (processed_output["llm_question_result"],)
    rweb_results = str(processed_output["rweb_results"])

    print("user_question: ", user_question)
    print("actual_output: ", actual_output)
    print("rweb_results: ", rweb_results)

    test_case = LLMTestCase(
        input=user_question,
        actual_output=actual_output,
        retrieval_context=[rweb_results],
    )
    metric = FaithfulnessMetric(threshold=0.5, model=model, include_reason=True)

    metric.measure(test_case)

    return {"deepeval_score": metric.score, "deepevalscore_reason": metric.reason}
