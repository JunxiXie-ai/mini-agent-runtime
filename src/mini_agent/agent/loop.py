from mini_agent.llm.deepseek_provider import DeepSeekProvider, SYSTEM_PROMPT
from mini_agent.tools.registry import create_default_registry
from mini_agent.agent.events.bus import EventBus
from mini_agent.agent.events.types import Event
from mini_agent.agent.session import Session

import json

class AgentLoop:
    def __init__(self, event_bus: EventBus, max_steps: int = 10) -> None:
        self.max_steps = max_steps
        self.llm = DeepSeekProvider()
        self.tools = create_default_registry()
        self.event_bus = event_bus

    def run(self, goal: str, session: Session | None = None) -> str:
        if session is None:
            session = Session()

        messages = session.messages

        if not messages:
            messages.append({
                "role": "system",
                "content": SYSTEM_PROMPT,
            })

        messages.append({
            "role": "user",
            "content": goal,
        })

        self.event_bus.publish(
            Event(
                type="run_started",
                data={
                    "goal": goal,
                },
            )
        )

        for step in range(1, self.max_steps + 1):
            self.event_bus.publish(
                Event(
                    type="step_started",
                    data={
                        "step": step,
                    },
                )
            )

            try:
                response = self.llm.chat(
                    messages,
                    self.tools.get_openai_schemas(),
                )
            except Exception as exc:
                self.event_bus.publish(
                    Event(type="step_finished", data={"step": step})
                )
                self.event_bus.publish(
                    Event(
                        type="run_finished",
                        data={
                            "status": "failed",
                            "reason": "llm_error",
                            "steps": step,
                            "error": str(exc),
                        },
                    )
                )
                return f"Agent stopped because the LLM failed: {exc}"

            if response["type"] == "final":
                messages.append(
                    {
                        "role": "assistant",
                        "content": response["content"],
                    }
                )

                self.event_bus.publish(
                    Event(
                        type="step_finished",
                        data={
                            "step": step,
                        },
                    )
                )

                self.event_bus.publish(
                    Event(
                        type="run_finished",
                        data={
                            "status": "success",
                            "steps": step,
                        },
                    )
                )

                return response["content"]

            if response["type"] == "tool_call":
                tool_name = response["tool_name"]
                arguments = response["arguments"]

                self.event_bus.publish(
                    Event(
                        type="tool_call_started",
                        data={
                            "tool_name": tool_name,
                            "arguments": arguments,
                        },
                    )
                )

                tool_result = self.tools.execute(
                    name=tool_name,
                    arguments=arguments,
                )

                if tool_result.success:
                    self.event_bus.publish(
                        Event(
                            type="tool_call_finished",
                            data={
                                "tool_name": tool_name,
                                "output": tool_result.output,
                            },
                        )
                    )
                else:
                    self.event_bus.publish(
                        Event(
                            type="tool_call_failed",
                            data={
                                "tool_name": tool_name,
                                "error": tool_result.output,
                            },
                        )
                    )

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
                        "content": tool_result.output,
                    }
                )

            self.event_bus.publish(
                Event(
                    type="step_finished",
                    data={
                        "step": step,
                    },
                )
            )

        self.event_bus.publish(
            Event(
                type="run_finished",
                data={
                    "status": "failed",
                    "reason": "max_steps",
                    "steps": self.max_steps,
                },
            )
        )

        return "Agent stopped because the maximum number of steps was reached."