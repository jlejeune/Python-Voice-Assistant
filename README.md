# Python Voice Assistant

A new voice assistant written in Python which can recognize human speech, talk to user and execute basic commands.

It uses third party APIs for speech recognition, OpenAI's GPT, etc...

I will add new agents to talk to more APIs later.

## Installation

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

## Configration

Rename the ```python_voice_assistant/.env.example``` file to ```.env``` and replace the values by your own.

### Assistant name

Define the name of your assistant, by using the ASSISTANT_NAME variable.

That name will be used to wake up your assistant before interacting with him.

### OpenAI

Define your OpenAi API key with the OPENAI_API_KEY variable.

## Create a custom action

To create a custom action:

1. Create a new python class in python_voice_assistant/actions/collection folder:

```python
# hello.py
from python_voice_assistant.actions.action import Action
from python_voice_assistant.models.message import Message


class HelloAction(Action):
    def response(self, message: Message) -> Message:
        """This action says hello."""
        return Message(content="Hello")
```

That class has to inherits from the Action class and has to implement a response method.

2. Create new configuration in assistant/actions/config.py:

```python
from python_voice_assistant.actions import HelloAction

{
    "enable": True,
    "class": HelloAction,
    "name": "hello",
    "tags": ["bonjour", "bonsoir"],
    "description": "Get the date",
}
```

The class key needs to match the name of the action class.

Add a name and a description.

Define the tags (voice words or sentences) which will trigger the action.

## Start

```bash
source venv/bin/activate
python main.py
```

## References

[SpeechRecognition library docs](https://pypi.org/project/SpeechRecognition/1.2.3)

[Google Translate Text-to-Speech API (gTTS)](https://gtts.readthedocs.io/en/latest/module.html#)

[OpenAI library](https://github.com/openai/openai-python)