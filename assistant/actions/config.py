from assistant.actions.collection.assistant import (
    EnableAssistantAction,
    StopAssistantAction,
)
from assistant.actions.collection.date import DateAction, TimeAction

ACTIONS: list[dict] = [
    {
        "enable": True,
        "class": EnableAssistantAction,
        "name": "enable_assistant",
        "tags": ["bonjour", "debout"],
        "description": "Enables the assistant (ready to hear command)",
    },
    {
        "enable": True,
        "class": StopAssistantAction,
        "name": "stop_assistant",
        "tags": ["au revoir", "à demain", "bonne nuit", "stoppe", "arrête toi"],
        "description": "Stops the assistant",
    },
    {
        "enable": True,
        "class": DateAction,
        "name": "date",
        "tags": ["quel jour", "date", "du jour"],
        "description": "Get the date",
    },
    {
        "enable": True,
        "class": TimeAction,
        "name": "time",
        "tags": ["quelle heure"],
        "description": "Get the time",
    },
]


ENABLED_ACTIONS: list[dict] = [
    action for action in ACTIONS if action.get("enable", False)
]
