import logging
from typing import Set

class FillerWordFilter:
    def __init__(self, ignored_words, confidence_threshold=0.65, min_word_length=2):
        self.ignored_words_set = set(w.lower().strip() for w in ignored_words)
        self.confidence_threshold = confidence_threshold
        self.min_word_length = min_word_length
        self.is_agent_speaking = False
        self.logger = logging.getLogger("FillerWordFilter")
    def set_agent_speaking_state(self, is_speaking: bool):
        self.is_agent_speaking = is_speaking
    def should_block_interruption(self, text: str, confidence: float = 1.0) -> bool:
        if not self.is_agent_speaking:
            return False
        if confidence < self.confidence_threshold:
            self.logger.info(f"Ignoring due to low confidence: '{text}' with {confidence}")
            return True
        words = text.lower().strip().split()
        if not words or (len(words) == 1 and len(words[0]) < self.min_word_length):
            self.logger.info(f"Ignoring due to short or empty words: '{text}'")
            return True
        non_filler_words = [w for w in words if w not in self.ignored_words_set]
        if len(non_filler_words) == 0:
            self.logger.info(f"Ignoring as all words are fillers: '{text}'")
            return True
        self.logger.info(f"Valid interruption detected: '{text}'")
        return False
