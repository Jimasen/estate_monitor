# app/core/event_bus.py

import logging
from typing import Callable, Dict, List


logger = logging.getLogger("event_bus")


class EventBus:

    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, handler: Callable):
        """
        Register event handler.
        """

        if event not in self.listeners:
            self.listeners[event] = []

        self.listeners[event].append(handler)

        logger.info(f"Handler subscribed to event: {event}")

    def publish(self, event: str, *args, **kwargs):
        """
        Trigger event.
        """

        handlers = self.listeners.get(event, [])

        logger.info(f"Publishing event: {event} to {len(handlers)} handlers")

        for handler in handlers:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Event handler failed: {e}")


event_bus = EventBus()
