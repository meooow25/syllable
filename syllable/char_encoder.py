import numpy as np

class CharacterEncoder:
    """Encodes strings to one-hot representation."""

    def __init__(self, chars):
        chars = sorted(set(chars))
        self.num_chars = len(chars)
        self.char_indices = {c: i for i, c in enumerate(chars)}
        self.indices_char = {i: c for i, c in enumerate(chars)}

    def encode(self, text, num_rows):
        x = np.zeros((num_rows, self.num_chars))
        for i, c in enumerate(text):
            x[i, self.char_indices[c]] = 1
        return x

    def decode(self, mat):
        return ''.join(self.indices_char[i]
                       for row in mat
                       if (i := next(iter(row.nonzero()[0]), None)) is not None)
