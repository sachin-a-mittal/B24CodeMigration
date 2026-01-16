import os
from openai import AzureOpenAI

def call_azure_openai(prompt: str) -> str:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    response = client.responses.create(
        model=deployment,
        input=prompt,
    )

    return response.output_text