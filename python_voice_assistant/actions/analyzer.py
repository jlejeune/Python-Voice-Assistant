from functools import lru_cache
from typing import TYPE_CHECKING, Any, Optional

from python_voice_assistant.actions.config import ENABLED_ACTIONS
from python_voice_assistant.core.config import math_symbols_mapping

if TYPE_CHECKING:  # no pragma cover
    from scipy.sparse._csr import csr_matrix
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity


class Analyzer:
    def __init__(
        self,
        weight_measure: "TfidfVectorizer",
        similarity_measure: "cosine_similarity",
        args: dict[str, Any],
        sensitivity: float,
    ) -> None:
        self.weight_measure = weight_measure
        self.similarity_measure = similarity_measure
        self.vectorizer = self._create_vectorizer(args)
        self.sensitivity = sensitivity

    @property
    @lru_cache
    def action_configs(self) -> list[dict]:
        return ENABLED_ACTIONS

    @property
    @lru_cache()
    def tags(self) -> list[str]:
        tags_list: list[str] = []
        for action in ENABLED_ACTIONS:
            tags_list.append(action["tags"])
        return [",".join(tag) for tag in tags_list]

    def extract_action_config_from_text(self, text: str) -> Optional[dict]:
        """Extract action config from text."""
        train_tdm = self._train_model()
        text_with_replaced_math_symbols = self._replace_math_symbols_with_words(text)

        test_tdm = self.vectorizer.transform([text_with_replaced_math_symbols])

        similarities = self.similarity_measure(
            train_tdm, test_tdm
        )  # Calculate similarities

        action_index = similarities.argsort(axis=None)[
            -1
        ]  # Extract the most similar action

        if similarities[action_index] > self.sensitivity:
            return [action_config for action_config in enumerate(self.action_configs) if action_config[0] == action_index][0][1]  # type: ignore
        return None

    def _replace_math_symbols_with_words(self, text: str) -> str:
        replaced_text = ""
        for word in text.split():
            if word in math_symbols_mapping.values():
                for key, value in math_symbols_mapping.items():
                    if value == word:
                        replaced_text += " " + key
            else:
                replaced_text += " " + word
        return replaced_text

    def _create_vectorizer(self, args: dict[str, Any]) -> "TfidfVectorizer":
        """Create vectorizer."""
        return self.weight_measure(**args)

    def _train_model(self) -> "csr_matrix":
        """Create/train the model."""
        return self.vectorizer.fit_transform(self.tags)
