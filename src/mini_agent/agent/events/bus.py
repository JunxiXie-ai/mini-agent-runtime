from collections.abc import Callable

from mini_agent.agent.events.types import Event


EventHandler = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self.subscribers: list[EventHandler] = []

    def subscribe(self, handler: EventHandler) -> None:
        self.subscribers.append(handler)

    def publish(self, event: Event) -> None:
        for handler in self.subscribers:
            handler(event)