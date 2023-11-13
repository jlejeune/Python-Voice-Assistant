import json
import logging
from typing import Any, List

import openai

from python_voice_assistant.exceptions.openai import OpenAiGenerationError
from python_voice_assistant.models.message import Message, ChatCompletionMessage


class OpenAiClient:
    """Client to interact with the OpenAI API."""

    def __init__(
        self, api_key: str, model: str, max_tokens: int, temperature: float
    ) -> None:
        openai.api_key = api_key
        self.model: str = model
        self.max_tokens: int = max_tokens
        self.temperature: float = temperature

    def get_chat_completion(
        self,
        messages: List[ChatCompletionMessage],
    ) -> Message:
        """
        Returns a completion (response) from the specified OpenAI GPT model.
        Reference: https://platform.openai.com/docs/api-reference/chat
        """
        if len(messages) == 0:
            raise ValueError(
                "The messages argument must be a list with at least one object."
            )

        logging.debug(
            f"Sending prompt to chat completion endpoint: {json.dumps(messages)}"
        )

        completion: Any = openai.ChatCompletion.create(
            messages=messages,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )

        choices = completion["choices"]
        tokens_used = completion["usage"]["total_tokens"]
        was_cut_short = False

        if len(choices) == 0:
            raise OpenAiGenerationError(
                "No choices returned from Open AI for provided context"
            )

        first_choice = choices[0]

        if first_choice["finish_reason"] == "length":
            logging.warning(
                "OpenAI stopped generating due to a limit on the max tokens. "
                f"Max tokens is set to: {self.max_tokens}. "
                f"Total tokens consumed with prompt were: {tokens_used}"
            )
            was_cut_short = True

        first_choice_text: str = (
            first_choice["message"]["content"].replace("\n", " ").strip()
        )

        return Message(first_choice_text, was_cut_short)
