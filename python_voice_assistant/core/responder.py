import logging
import os

import playsound
from gtts import gTTS


class Responder:
    audio_filename: str = os.path.join(os.getcwd(), "speech.mp3")

    def __init__(self, language: str = "fr") -> None:
        self.language = language

    def speech(self, text: str) -> None:
        """ "Speak the given text."""
        tts = gTTS(text=text, lang=self.language)
        tts.save(self.audio_filename)
        logging.debug(f"Play {self.audio_filename} file with playsound")
        playsound.playsound(self.audio_filename)
        self._cleanup_audio_file()

    def _cleanup_audio_file(self) -> None:
        """Remove audio file if exists."""
        if os.path.exists(self.audio_filename):
            logging.debug(f"Delete {self.audio_filename} file")
            os.remove(self.audio_filename)
