import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = os.getenv("OPENAI_MODEL")

def generate_text(prompt: str) -> str:
    response = client.responses.create(
        model=MODEL_NAME,
        input=prompt
    )

    output = response.output_text

    if not output:
        raise ValueError("OpenAI returned an empty response")

    return output

def generate_structured(
        prompt: str,
        schema_name: str,
        schema: dict
    ):
    response  = client.responses.create(
        model=MODEL_NAME,
        input=prompt,
        text={
            "format":{
                "type": "json_schema",
                "name": schema_name,
                "schema": schema,
                "strict": True
            }
        }
    )

    usage = response.usage
    print("input:", usage.input_tokens,
          "cached:", usage.input_tokens_details.cached_tokens)

    return response.output_text

def test_llm():
    response = client.responses.create(
        model=MODEL_NAME,
        input="Suggest one travel destination in India for a beach lover"
    )

    return response.output_text