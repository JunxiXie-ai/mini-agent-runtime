import json
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

    def chat(
        self,
        messages: list[dict[str, str]],
        tools: list[dict],
    ) -> dict:
        response = self.client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=tools,
            reasoning_effort="none",
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool_call = message.tool_calls[0]

            return {
                "type": "tool_call",
                "tool_call_id": tool_call.id,
                "tool_name": tool_call.function.name,
                "arguments": json.loads(tool_call.function.arguments),
            }

        return {
            "type": "final",
            "content": message.content or "",
        }