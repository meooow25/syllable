from ..pattern import SyllablePatternMatcher

def do_test_try_match(pattern, counts, expected_breaks=None):
    counts = [c if isinstance(c, tuple) else (c,) for c in counts]
    matched, breaks = SyllablePatternMatcher._try_match(pattern, counts)
    expected_matched = bool(expected_breaks)
    assert matched == expected_matched
    if matched:
        assert breaks == expected_breaks

def test_try_match_matches():
    do_test_try_match(
        [10],
        [(6, 8, 10, 12, 14)]
        [0],
    )
    do_test_try_match(
        [2, 3],
        [1, 1, 1, 1, 1],
        [4, 1],
    )
    do_test_try_match(
        [2, 3],
        [1, 1, (1, 2), 1],
        [3, 1],
    )
    do_test_try_match(
        [2, 3],
        [(2, 3), (2, 3)],
        [1, 0],
    )
    do_test_try_match(
        [2, 3],
        [1, (1, 2, 3), 1, (1, 2, 3), 1],
        [4, 1],
    )
    do_test_try_match(
        [1, 2, 3, 4],
        [(1, 10), 2, 1, (2, 20), 1, 2, (1, 10)],
        [6, 3, 1, 0],
    )
    do_test_try_match(
        [1, 3, 5, 2, 10, 12, 3],
        [1, 3, 5, 2, 10, 12, 3],
        [6, 5, 4, 3, 2, 1, 0],
    )
    do_test_try_match(
        [1, 3, 5, 2, 10, 12, 3],
        [1, 1, 2, 3, 2, 1, 1, 4, 6, 12, 1, 1, 1],
        [12, 9, 8, 6, 4, 2, 0],
    )

def test_try_match_does_not_match():
    do_test_try_match(
        [10],
        [(6, 8, 9, 11, 12, 14)]
    )
    do_test_try_match(
        [2, 3],
        [1, 1, 1, 1],
    )
    do_test_try_match(
        [2, 3],
        [1, 1, 1, 1, 1, 1],
    )
    do_test_try_match(
        [2, 3],
        [3, 2],
    )
    do_test_try_match(
        [2, 3],
        [5],
    )
    do_test_try_match(
        [1, 2, 3, 4],
        [1, 2, 1, 2, 1, 2],
    )
    do_test_try_match(
        [1, 2, 3, 4],
        [1, 2, 1, 2, 1, 2, 1, 2],
    )


class FakeSyllableCounter:
    d = {
        'some': (1,),
        'random': (2,),
        'words': (3,),
        'here': (4,),
        'for': (1, 2),
        'testing': (3, 4),
        'purposes': (),
    }
    def count_syllables(self, word):
        return self.d[word]

fsc = FakeSyllableCounter()

def test_match_matches():
    spm = SyllablePatternMatcher(fsc, [1, 2, 3])
    assert spm.match('some random words') == [['some'], ['random'], ['words']]
    assert spm.match('some random some random') == [['some'], ['random'], ['some', 'random']]
    assert spm.match('for for for for') == [['for'], ['for'], ['for', 'for']]
    assert spm.match('for random testing') == [['for'], ['random'], ['testing']]

def test_match_does_not_match():
    spm = SyllablePatternMatcher(fsc, [1, 2, 3])
    assert spm.match('words random some') is None
    assert spm.match('some random here') is None
    assert spm.match('some purposes') is None
    assert spm.match('testing testing') is None
