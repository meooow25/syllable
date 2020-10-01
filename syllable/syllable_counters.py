import json
import string
from pathlib import Path

import numpy as np
from keras import models

from .char_encoder import CharacterEncoder

# TODO: Not great, improve this. Use importlib.resources.
def get_path(path, cur_dir = Path(__file__).parent):
    return cur_dir / path

CMUDICT_FILE = get_path('cmudict/cmudict.dict')
MODEL_DIR = get_path('model_data/model')
CHARS_FILE = get_path('model_data/chars.json')


class CmudictSyllableCounter:
    def __init__(self, file=CMUDICT_FILE):
        self.d = self._read_from(file)

    @staticmethod
    def _read_from(file):
        d = {}
        with open(file) as f:
            for line in f:
                word, *pieces = line.split()
                if '(' in word:  # Alternate pronunciation
                    word = word[:word.index('(')]
                syllables = sum(p[-1].isdigit() for p in pieces)
                d.setdefault(word, []).append(syllables)
        for w, cnts in d.items():
            d[w] = tuple(sorted(set(cnts)))
        return d

    def count_syllables(self, word):
        word = word.lower().lstrip(string.punctuation)
        counts = self.d.get(word)
        if counts:
            return counts
        word = word.rstrip(string.punctuation)
        return self.d.get(word) or ()


class ModelSyllableCounter:
    def __init__(self, model_dir=MODEL_DIR, chars_file=CHARS_FILE):
        with open(chars_file) as f:
            j = json.load(f)
        self.chars = j['chars']
        self.maxlen = j['maxlen']
        self.char_enc = CharacterEncoder(self.chars)
        self.model = models.load_model(model_dir)
        self.trimchars = ''.join(set(string.punctuation) - set(self.chars))

    def count_syllables(self, word):
        word = word.lower().strip(self.trimchars)
        if count := self._count(word):
            return (int(round(count)),)
        return ()

    def _count(self, word):
        if len(word) > self.maxlen:
            return None
        if not all(c in self.chars for c in word):
            return None
        x = np.array([self.char_enc.encode(word, self.maxlen)])
        return self.model(x, training=False)[0][0].numpy()


class CompositeSyllableCounter:
    def __init__(self, delegates):
        self.delegates = delegates

    def count_syllables(self, word):
        for delegate in self.delegates:
            if counts := delegate.count_syllables(word):
                return counts
        return ()
