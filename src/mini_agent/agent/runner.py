from pathlib import Path
from uuid import uuid4

from mini_agent.agent.loop import AgentLoop
from mini_agent.agent.events.bus import EventBus
from mini_agent.agent.events.trace_writer import TraceWriter
from mini_agent.agent.events.types import Event


def print_event(event: Event) -> None:
    print(f"[Event] {event.type}: {event.data}")


def run_agent(goal: str) -> str:
    event_bus = EventBus()

    trace_path = Path("traces") / f"{uuid4().hex}.jsonl"
    trace_writer = TraceWriter(trace_path)

    event_bus.subscribe(print_event)
    event_bus.subscribe(trace_writer.write)

    print(f"[Trace] {trace_path}")

    agent = AgentLoop(event_bus=event_bus)
    return agent.run(goal)