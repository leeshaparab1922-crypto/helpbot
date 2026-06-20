from dataclasses import dataclass, field
from typing import Any


@dataclass
class Conversation:
    _messages: list[dict[str, Any]] = field(default_factory=list)

    @property
    def messages(self) -> list[dict[str, Any]]:
        return self._messages

    def add_user(self, text: str) -> None:
        self._messages.append(
            {"role": "user", "content": text}
        )

    def add_assistant(self, text: str) -> None:
        self._messages.append(
            {"role": "assistant", "content": text}
        )

    def __len__(self) -> int:
        return len(self._messages)