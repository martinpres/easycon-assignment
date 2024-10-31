from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Message:
    payload: Any
    topic: str

    def to_dict(self):
        return {
            'payload': self.payload,
            'topic': self.topic
        }
