import os
from openai import AzureOpenAI
    
def call_azure_openai(prompt: str, temperature: float = 0.2) -> str:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )

    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a banking-grade modernization expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )

    return response.choices[0].message.content