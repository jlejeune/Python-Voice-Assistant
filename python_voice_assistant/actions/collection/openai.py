import logging

from python_voice_assistant.actions.action import Action
from python_voice_assistant.exceptions.openai import OpenAiGenerationError
from python_voice_assistant.models.message import Message, MessageRole
from python_voice_assistant.clients import OPENAI_CLIENT


class OpenAiAction(Action):
    """This action talks to OpenAI's GPT."""

    def response(self, message: "Message") -> "Message":
        try:
            return OPENAI_CLIENT.get_chat_completion(
                messages=[{"content": message.content, "role": MessageRole.USER}]
            )
        except OpenAiGenerationError as err:
            logging.error(err)
            return Message(content="")
