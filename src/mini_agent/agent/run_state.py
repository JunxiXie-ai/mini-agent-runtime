from dataclasses import dataclass

from mini_agent.agent.events.types import Event


@dataclass
class RunState:
    status: str = "pending"
    current_step: int = 0
    tool_calls: int = 0
    tool_failures: int = 0
    reason: str | None = None

    def on_event(self, event: Event) -> None:
        if event.type == "run_started":
            self.status = "running"
            self.reason = None
        elif event.type == "step_started":
            self.current_step = event.data["step"]
        elif event.type == "tool_call_started":
            self.tool_calls += 1
        elif event.type == "tool_call_failed":
            self.tool_failures += 1
        elif event.type == "run_finished":
            self.status = event.data["status"]
            self.reason = event.data.get("reason")