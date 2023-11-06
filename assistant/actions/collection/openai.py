import logging

from assistant.actions.action import Action
from assistant.clients.config import openai_model, openai_max_tokens, openai_temperature
from assistant.clients.openai import OpenAiClient
from assistant.exceptions.openai import OpenAiGenerationError
from assistant.models.message import Message, MessageRole


class OpenAiAction(Action):
    """This action talks to OpenAI's GPT."""

    def response(self, message: "Message") -> "Message":
        try:
            return OpenAiClient.get_chat_completion(
                messages=[{"content": message.content, "role": MessageRole.USER}],
                model=openai_model,
                max_tokens=openai_max_tokens,
                temperature=openai_temperature,
            )
        except OpenAiGenerationError as err:
            logging.error(err)
            return Message(content="")
