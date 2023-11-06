from enum import Enum
from typing import NamedTuple, Optional, TypedDict


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class Message(NamedTuple):
    content: str
    was_cut_short: Optional[bool] = None


class ChatCompletionMessage(TypedDict):
    role: str
    content: str
