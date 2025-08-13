import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from pydantic import BaseModel, Field

load_dotenv()

class LLMOutput(BaseModel):
    name: str
    address: str
    phone:int
    education:list[str]
    experience: list[str]
    skills: list[str]
    projects:list[str]

def extract_data_from_llm(data: str) -> dict:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    if not all([endpoint, deployment, subscription_key, api_version]):
        raise ValueError("Missing required environment variables in .env file")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    response = client.chat.completions.parse(
        model=deployment,  # ✅ This fixes your error
        messages=[
            {
                "role": "system",
                "content": "You are a data extraction assistant. Extract the required fields from the provided data and return only valid JSON."
            },
            {
                "role": "user",
                "content": f"Extract the necessary fields from this data: {data}"
            },
        ],
        response_format=LLMOutput,
        max_completion_tokens=1000,
        temperature=0.0,
    )

    if hasattr(response.choices[0].message, "parsed") and response.choices[0].message.parsed:
        return response.choices[0].message.parsed.model_dump()
    else:
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return {}

