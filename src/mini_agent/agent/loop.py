from mini_agent.llm.fake_provider import FakeLLMProvider
from mini_agent.tools.registry import create_default_registry


class AgentLoop:
    def __init__(self, max_steps: int = 10) -> None:
        self.max_steps = max_steps
        self.llm = FakeLLMProvider()
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

            response = self.llm.chat(messages)

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

                messages.append(
                    {
                        "role": "assistant",
                        "content": f"tool_call: {tool_name}",
                    }
                )

                messages.append(
                    {
                        "role": "user",
                        "content": f"tool_result: {tool_result}",
                    }
                )

        return "Agent stopped because the maximum number of steps was reached."