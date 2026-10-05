from pathlib import Path
from uuid import uuid4

from mini_agent.agent.loop import AgentLoop
from mini_agent.agent.events.bus import EventBus
from mini_agent.agent.events.trace_writer import TraceWriter
from mini_agent.agent.events.types import Event
from mini_agent.agent.run_state import RunState
from mini_agent.agent.session import Session

def print_event(event: Event) -> None:
    print(f"[Event] {event.type}: {event.data}")


def run_agent(goal: str, session: Session | None = None) -> str:
    run_id = uuid4().hex
    event_bus = EventBus(run_id=run_id)

    trace_path = Path("traces") / f"{run_id}.jsonl"
    trace_writer = TraceWriter(trace_path)
    state = RunState()

    event_bus.subscribe(print_event)
    event_bus.subscribe(trace_writer.write)
    event_bus.subscribe(state.on_event)

    print(f"[Trace] {trace_path}")

    agent = AgentLoop(event_bus=event_bus)
    result = agent.run(goal, session=session)

    print(f"[State] {state}")
    return result