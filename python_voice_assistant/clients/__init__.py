from python_voice_assistant.clients.openai import OpenAiClient
from python_voice_assistant.settings import OpenAiSettings

_openai_settings = OpenAiSettings()

__all__ = ["OPENAI_CLIENT"]

OPENAI_CLIENT = OpenAiClient(
    api_key=_openai_settings.api_key,
    model=_openai_settings.model,
    max_tokens=_openai_settings.max_tokens,
    temperature=_openai_settings.temperature,
)
