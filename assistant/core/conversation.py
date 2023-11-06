import logging
import sys
from typing import TYPE_CHECKING, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from assistant.actions.analyzer import Analyzer
from assistant.actions.collection.openai import OpenAiAction
from assistant.core.config import analyzer_config
from assistant.exceptions.listener import ListenerTimeout
from assistant.models.message import Message

if TYPE_CHECKING:  # pragma no cover
    from assistant.core.listener import Listener
    from assistant.core.responder import Responder


class Conversation:
    def __init__(
        self,
        listener: "Listener",
        responder: "Responder",
        assistant_name: Optional[str] = None,
    ) -> None:
        self.listener = listener
        self.responder = responder
        self.assistant_name: Optional[str] = (
            assistant_name.lower() if assistant_name else None
        )
        self.analyzer = Analyzer(
            weight_measure=TfidfVectorizer,
            similarity_measure=cosine_similarity,
            args=analyzer_config.get("args", {}),
            sensitivity=analyzer_config.get("sensitivity", 0.2),
        )

    def start_conversation(self) -> None:
        """Start a continuous conversation until the wake word is detected."""
        already_activated: bool = False
        while True:
            try:
                voice_transcript: Optional[str] = self.listener.listen()
            except ListenerTimeout:
                logging.debug("Timeout, waiting for new wake word")
                already_activated = False
                continue

            if not voice_transcript:
                logging.error(
                    "Listener returned an empty text, waiting for new wake word"
                )
                already_activated = False
                continue

            if already_activated:
                pass
            elif self.assistant_name is not None:
                if not voice_transcript.lower().startswith(self.assistant_name):
                    logging.info(
                        f"Speech recognized, but wake word '{self.assistant_name}' not heard."
                    )
                    logging.debug("Starting to listen again...")
                    continue
                already_activated = True
                voice_transcript = voice_transcript[len(self.assistant_name) :].strip()

            # if only wake word has been detected return
            if len(voice_transcript) == 0:
                self.responder.speech("Oui ?")
                already_activated = True
                continue

            # Determine action to run
            action_config: Optional[
                dict
            ] = self.analyzer.extract_action_config_from_text(voice_transcript)

            # If action can't be determined ask ChatGPT
            if not action_config:
                action_config = {
                    "enable": True,
                    "class": OpenAiAction,
                    "name": "openai",
                    "tags": [],
                    "description": "Get response from OpenAI API",
                }

            response = self._get_action_response(
                action_config=action_config, voice_transcript=voice_transcript
            )
            logging.info(f"Text response: {response.content}")
            self.responder.speech(response.content)

            # Exit if stop_assistant action is called
            if action_config.get("name") == "stop_assistant":
                self._exit()

    @staticmethod
    def _exit(exit_code: int = 0) -> None:
        """Stop the conversation with given exit_code."""
        sys.exit(exit_code)

    @staticmethod
    def _get_action_response(action_config: dict, voice_transcript: str) -> Message:
        try:
            _class = action_config.get("class")
            return _class.from_config(**action_config).response(
                Message(content=voice_transcript)
            )
        except Exception as err:
            response_text = f"Failed to execute action {action_config.get('name')} with message: {err}"
            logging.error(response_text)
            return Message(content=response_text)
