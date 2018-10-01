from collections import defaultdict
import trio


class Dispatcher:

    def __init__(self, event_generator, q_size=0):
        self._event_generator = event_generator
        self._events = trio.Queue(q_size)
        self._handlers = defaultdict(list)
        self._nursery = None

    async def __call__(self):
        async with trio.open_nursery() as nursery:
            self._nursery = nursery
            nursery.start_soon(self._producer)
            nursery.start_soon(self._consumer)

    def on(self, event_type):
        """Decorator version of `self.add_handler`."""
        def decorator(func):
            self.add_handler(event_type, func)
            return func
        return decorator

    def add_handler(self, event_type, event_handler):
        self._handlers[event_type].append(event_handler)

    async def _producer(self):
        async for event in self._event_generator():
            await self._events.put(event)

    async def _consumer(self):
        async for event in self._events:
            self._dispatch(event)

    def _dispatch(self, event):
        for handler in self._handlers[event['type']]:
            self._nursery.start_soon(handler, event['object'])
