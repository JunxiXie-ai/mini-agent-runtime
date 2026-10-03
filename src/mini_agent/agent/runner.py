from mini_agent.agent.loop import AgentLoop
from mini_agent.agent.events.bus import EventBus
from mini_agent.agent.events.types import Event


def print_event(event: Event) -> None:
    print(f"[Event] {event.type}: {event.data}")


def run_agent(goal: str) -> str:
    event_bus = EventBus()

    event_bus.subscribe(print_event)

    agent = AgentLoop(event_bus=event_bus)

    return agent.run(goal)