import os

from dotenv import load_dotenv
from openai import OpenAI


class DeepSeekProvider:
    def __init__(self) -> None:
        load_dotenv()

        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com",
        )

    def chat(self, messages: list[dict[str, str]]) -> dict:
        response = self.client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            reasoning_effort="none",
        )

        content = response.choices[0].message.content

        return {
            "type": "final",
            "content": content or "",
        }