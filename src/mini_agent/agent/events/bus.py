from collections.abc import Callable
from dataclasses import replace

from mini_agent.agent.events.types import Event


EventHandler = Callable[[Event], None]


class EventBus:
    def __init__(self, run_id: str | None = None) -> None:
        self.run_id = run_id
        self.subscribers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self.subscribers.append(handler)

    def publish(self, event: Event) -> None:
        if self.run_id is not None:
            event = replace(event, run_id=self.run_id)

        for handler in self.subscribers:
            handler(event)