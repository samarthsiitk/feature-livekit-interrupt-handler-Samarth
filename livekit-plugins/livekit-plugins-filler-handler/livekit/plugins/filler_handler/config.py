import os
class FillerConfig:
    DEFAULT_FILLER_WORDS = [
        'uh','um','umm','hmm','haan','ah','er','eh','mm','mhm','aha','huh','like','you know','okay','acha','yup','ch','woah','shh','yeah','gotcha','yes'
    ]

    @staticmethod
    def get_filler_words():
        env_words = os.getenv('FILLER_WORDS', '').strip()
        if env_words:
            return [w.strip() for w in env_words.split(',') if w.strip()]
        return FillerConfig.DEFAULT_FILLER_WORDS

    @staticmethod
    def get_confidence_threshold():
        return float(os.getenv('FILLER_CONFIDENCE_THRESHOLD', '0.65'))

    @staticmethod
    def get_min_word_length():
        return int(os.getenv('FILLER_MIN_WORD_LENGTH', '2'))
