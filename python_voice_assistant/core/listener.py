import logging
from typing import TYPE_CHECKING

import speech_recognition as sr

from python_voice_assistant.exceptions.listener import ListenerTimeout

if TYPE_CHECKING:  # pragma no cover
    from speech_recognition.audio import AudioData


class Listener:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 1
        self.microphone = sr.Microphone()

    def _get_text_from_audio(self, audio: "AudioData", language: str = "fr-FR") -> str:
        try:
            text = self.recognizer.recognize_google(audio, language=language)

            if text is None or len(text) == 0:
                logging.warning("No speech detected in audio")
                text = ""
            else:
                logging.info(f"Text: {text}")
        except sr.UnknownValueError:
            logging.error("Google Speech Recognition could not understand audio")
            text = ""
        except sr.RequestError:
            logging.error(
                "Error requesting results from Google Speech Recognition service"
            )
            text = ""
        return text.lower()

    def listen(self) -> str:
        """Listen audio and returns the heard text."""
        with self.microphone as source:
            logging.info("Listening for input...")
            self.recognizer.adjust_for_ambient_noise(source)  # may be customizable
            try:
                audio = self.recognizer.listen(source, timeout=3)
            except sr.WaitTimeoutError:
                raise ListenerTimeout("Timeout waiting for audio")
        return self._get_text_from_audio(audio)
