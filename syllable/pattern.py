from typing import Iterable, List, Optional, Tuple

from .syllable_counters import SyllableCounter

HAIKU_PATTERN = (5, 7, 5)

class SyllablePatternMatcher:
    """Tries to match a syllable pattern to some input text."""

    def __init__(self, syllable_counter: SyllableCounter,
                 pattern: Iterable[int]):
        self.syllable_counter = syllable_counter
        self.pattern = tuple(pattern)
        self.pattern_sum = sum(pattern)

    @staticmethod
    def haiku(syllable_counter: SyllableCounter):
        """Returns a matcher for the pattern (5, 7, 5)."""
        return SyllablePatternMatcher(syllable_counter, HAIKU_PATTERN)

    def get_counts(self, words: Iterable[str],
                   strict=False) -> Optional[List[Tuple[int, ...]]]:
        """Returns syllable counts for each word. If strict is True, returns
        early with None if counting fails for any word.
        """
        res = []
        for w in words:
            cur = self.syllable_counter.count_syllables(w)
            if not cur and strict:
                return None
            res.append(cur)
        return res

    def match(self, text: str) -> Optional[List[List[str]]]:
        """Attempts to match the text with self.pattern.

        Splits the text into words and tries to find an arrangement that
        satisfies the syllable pattern.

        For the pattern (3, 2) and a decent syllable counter, with input text
        "This is some input", the match will return
        [["This", "is", "some"], ["input"]].

        If multiple matches are possible, any one of them is returned.
        If a match is not found, None is returned.
        """
        # Short circuit check
        words = text.split()
        if len(words) > self.pattern_sum:
            return None

        # If any word is not countable, return
        counts = self.get_counts(words, strict=True)
        if counts is None:
            return None

        matched, breaks = self._try_match(self.pattern, counts)
        if not matched:
            return None

        lines = []
        cur_line = []
        for i, w in enumerate(words):
            cur_line.append(w)
            if i == breaks[-1]:
                lines.append(cur_line)
                cur_line = []
                breaks.pop()
        return lines

    @staticmethod
    def _try_match(pattern, counts):
        # Dynamic programming code to match the pattern. Returns the first found
        # solution so only requires storing the bad states.
        # Time complexity is
        # O(len(flatten(counts)) * len(pattern) * sum(pattern))
        # O(len(flatten(counts)) * sum(pattern)) is possible, but meh this is
        # good enough.

        pattern = tuple(pattern)
        breaks = []
        bad_states = set()

        def f(idx, pattern):
            if idx == len(counts):
                return not pattern
            if not pattern:
                return False
            key = (idx, *pattern)
            if key in bad_states:
                return False

            cur_counts = counts[idx]
            for cur_count in cur_counts:
                remaining = pattern[0] - cur_count
                if remaining < 0:
                    continue
                new_pattern = ((remaining,) if remaining else ()) + pattern[1:]
                cur_ok = f(idx + 1, new_pattern)
                if cur_ok:
                    if not remaining:
                        breaks.append(idx)
                    return True
            bad_states.add(key)
            return False

        return f(0, pattern), breaks
