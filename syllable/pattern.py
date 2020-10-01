HAIKU_PATTERN = (5, 7, 5)


class SyllablePatternMatcher:
    def __init__(self, syllable_counter, pattern):
        self.syllable_counter = syllable_counter
        self.pattern = pattern
        self.pattern_sum = sum(pattern)

    @staticmethod
    def haiku(syllable_counter):
        return SyllablePatternMatcher(syllable_counter, HAIKU_PATTERN)

    def get_counts(self, words, strict=False):
        res = []
        for w in words:
            cur = self.syllable_counter.count_syllables(w)
            if not cur and strict:
                return None
            res.append(cur)
        return res

    def match(self, text):
        # Some short circuit checks
        if len(text) < self.pattern_sum:
            return None
        words = text.split()
        if len(words) > self.pattern_sum:
            return None

        # If word is not countable, return
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
