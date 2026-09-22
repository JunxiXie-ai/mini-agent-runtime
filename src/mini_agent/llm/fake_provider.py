class FakeLLMProvider:
    def chat(self, messages: list[dict[str, str]]) -> dict:
        tool_results = [
            message["content"]
            for message in messages
            if "tool_result" in message["content"]
        ]

        if len(tool_results) == 0:
            return {
                "type": "tool_call",
                "tool_name": "write_file",
                "arguments": {
                    "path": "hello.py",
                    "content": 'print("Hello World")\n',
                },
            }

        if len(tool_results) == 1:
            return {
                "type": "tool_call",
                "tool_name": "read_file",
                "arguments": {
                    "path": "hello.py",
                },
            }

        return {
            "type": "final",
            "content": "Task completed and verified successfully.",
        }