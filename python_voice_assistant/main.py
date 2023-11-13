from python_voice_assistant.core.conversation import Conversation
from python_voice_assistant.core.listener import Listener
from python_voice_assistant.core.responder import Responder
from python_voice_assistant.settings import Settings


def main() -> None:
    # Get settings
    _settings = Settings()

    # Define listener
    listener: Listener = Listener()

    # Define responder
    responder: Responder = Responder()

    # Define conversation object and start it
    conversation = Conversation(
        listener=listener,
        responder=responder,
        assistant_name=_settings.assistant_name,
    )
    conversation.start_conversation()


if __name__ == "__main__":
    main()
