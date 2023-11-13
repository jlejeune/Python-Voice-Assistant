from datetime import datetime

from python_voice_assistant.actions.action import Action
from python_voice_assistant.models.message import Message


class StopAssistantAction(Action):
    def response(self, message: Message) -> Message:
        """This action says goodbye and shuts down the assistant."""
        return Message(content="Au revoir")


class EnableAssistantAction(Action):
    def response(self, message: Message) -> Message:
        """This collection says hello and is ready to hear command."""
        now = datetime.now()
        day_time = int(now.strftime("%H"))

        if day_time < 18:
            content = "Bonjour, en quoi puis-je vous aider"
        else:
            content = "Bonsoir, en quoi puis-je vous aider"
        return Message(content=content)
