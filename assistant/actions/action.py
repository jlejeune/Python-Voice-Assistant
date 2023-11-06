import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Unpack

from dacite import from_dict

if TYPE_CHECKING:  # pragma no cover
    from assistant.models.message import Message


@dataclass
class Action(ABC):
    name: str
    description: str
    tags: list[str]
    enable: bool

    @classmethod
    def from_config(cls, **kwargs: Unpack[Any]) -> "Action":
        return from_dict(data_class=cls, data=kwargs)

    @abstractmethod
    def response(self, message: "Message") -> "Message":
        pass

    @staticmethod
    def extract_tags(voice_transcript: str, tags: list[str]) -> set[str]:
        """This method identifies the tags from the user transcript for a specific action."""
        try:
            transcript_words = voice_transcript.split()
            return set(transcript_words).intersection(tags)
        except Exception as e:
            logging.error(f"Failed to extract tags with message: {e}")
            return set()
