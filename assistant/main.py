from assistant.clients.config import openai_api_key
from assistant.clients.openai import OpenAiClient
from assistant.core.config import assistant_name
from assistant.core.conversation import Conversation
from assistant.core.listener import Listener
from assistant.core.responder import Responder


def main() -> None:
    # Define listener
    listener: Listener = Listener()

    # Define responder
    responder: Responder = Responder()

    # Define OpenAi client
    OpenAiClient(api_key=openai_api_key)

    # Define conversation object and start it
    conversation = Conversation(
        listener=listener,
        responder=responder,
        assistant_name=assistant_name,
    )
    conversation.start_conversation()


if __name__ == "__main__":
    main()
