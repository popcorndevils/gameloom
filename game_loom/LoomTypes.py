from tkinter import ttk as tw
from typing import NamedTuple, Any, Callable, Dict, Tuple


class LoomEvent(NamedTuple):
    '''
    name: name of the event\n
    args: names of required keyword arguments.
    '''
    name: str
    args: Tuple[str, ...]


class LoomFrame(tw.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._events: Dict[str, Dict[str, Any]] = {}

    @property
    def event_names(self) -> str:
        return ", ".join([f"'{k}'" for k in self._events.keys()])

    def register_event(self, event_type: LoomEvent):
        if event_type.name in self._events:
            raise KeyError(f"Event '{event_type.name}' already registered.")

        self._events[event_type.name] = {
            "callbacks": [],
            "signature": event_type.args,
        }

    def observe_event(self, event_name: str, func: Callable):
        event = self._events.get(event_name)
        if event is None:
            raise ValueError(
                f"Event '{event_name}' is unknown. Known events: [{self.event_names}]"
            )

        event["callbacks"].append(func)

    def fire_event(self, event_name: str, **kwargs: Any):
        event = self._events.get(event_name)

        if event is None:
            raise ValueError(
                f"Event '{event_name}' is unknown. Known events: [{self.event_names}]"
            )

        signature = event["signature"]

        if signature:
            for required_arg in signature:
                if required_arg not in kwargs:
                    raise TypeError(
                        f"Missing required argument '{required_arg}' for event '{event_name}'."
                    )

        callback_args = {arg: kwargs[arg] for arg in signature} if signature is not None else None

        for func in event["callbacks"]:
            # Pass only the arguments defined in the signature to the callback
            # This prevents passing extra, unknown keyword arguments.
            # You can also use `func(**kwargs)` if you trust the consumer.
            if callback_args:
                func(**callback_args)
            else:
                func()
