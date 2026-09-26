from mini_agent.llm.deepseek_provider import DeepSeekProvider
from mini_agent.tools.registry import create_default_registry

import json

class AgentLoop:
    def __init__(self, max_steps: int = 10) -> None:
        self.max_steps = max_steps
        self.llm = DeepSeekProvider()
        self.tools = create_default_registry()

    def run(self, goal: str) -> str:
        messages = [
            {
                "role": "user",
                "content": goal,
            }
        ]

        for step in range(1, self.max_steps + 1):
            print(f"[Agent] Step {step}")

            response = self.llm.chat(
                messages, 
                self.tools.get_openai_schemas()
                )

            if response["type"] == "final":
                return response["content"]

            if response["type"] == "tool_call":
                tool_name = response["tool_name"]
                arguments = response["arguments"]

                print(f"[Agent] Tool call: {tool_name}")

                tool_result = self.tools.execute(
                    name=tool_name,
                    arguments=arguments,
                )

                print(f"[Tool] Result: {tool_result}")

                tool_call_id = response["tool_call_id"]

                messages.append(
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": tool_call_id,
                                "type": "function",
                                "function": {
                                    "name": tool_name,
                                    "arguments": json.dumps(arguments),
                                },
                            }
                        ],
                    }
                )

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "content": tool_result,
                    }
                )

        return "Agent stopped because the maximum number of steps was reached."