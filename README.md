# syllable
A Python library to count syllables in English

This is a small fun project to count syllables and detect syllable patterns, inspired by [u/haikusbot](https://www.reddit.com/r/haikusbot/).

The library uses a model trained on the [CMUdict](https://github.com/cmusphinx/cmudict/) dictionary of pronunciations, and has an accuracy of ~95%.  
The model is intentionally small in size, so that it can run fast.

The model is probably terrible for non-English words.

```py
>>> from syllable import CmudictSyllableCounter, ModelSyllableCounter
>>> csc, msc = CmudictSyllableCounter(), ModelSyllableCounter()
>>> csc.count_syllables('family')
(2, 3)
>>> msc.count_syllables('family')
(3,)
>>>
>>> from syllable import CompositeSyllableCounter, SyllablePatternMatcher
>>> comp = CompositeSyllableCounter([csc, msc])
>>> matcher = SyllablePatternMatcher(comp, (5, 7, 5)) # or SyllablePatternMatcher.haiku(comp)
>>> matcher.match("family can be two or three syllables, but thisweirdword's just three")
[['family', 'can', 'be'], ['two', 'or', 'three', 'syllables,', 'but'], ["thisweirdword's", 'just', 'three']]
