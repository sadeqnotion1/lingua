"""Text tokenization (Lute-style parsing).

M4 milestone. Splits a text into an ordered, **lossless** sequence of tokens
that alternate between:

* **words**     - maximal runs of the language's word-characters, and
* **non-words** - everything in between (spaces, punctuation, newlines).

Joining the tokens back together reproduces the original text exactly
(``"".join(tokenize(t)) == t``), so the reader can render each token in order
while colouring only the word tokens by learning status.

The set of word characters comes from the language's ``word_chars`` config: a
regex character-class *body* such as ``"a-zA-Z\u00c0-\u017f"`` (see
``app/models/language.py``), matching Lute v3's configuration model.
"""
from __future__ import annotations

import re
from typing import List, NamedTuple

# Mirrors Language.word_chars default in app/models/language.py so the parser
# behaves the same way whether or not a caller passes an explicit config.
DEFAULT_WORD_CHARS = "a-zA-Z\u00c0-\u017f"


class Token(NamedTuple):
    """A single piece of a tokenized text.

    ``text``    - the exact substring (never empty).
    ``is_word`` - True for a word run, False for a non-word run.
    """

    text: str
    is_word: bool


def _word_regex(word_chars: str) -> "re.Pattern[str]":
    """Build the 'one or more word characters' matcher for a language.

    ``word_chars`` is inserted verbatim into a character class, exactly like
    Lute, so ranges (``a-z``) and escapes (``\\u00c0``) keep working. An empty
    config falls back to the default Latin alphabet.
    """
    return re.compile(f"[{word_chars or DEFAULT_WORD_CHARS}]+")


def tokenize_tagged(
    text: str, word_chars: str = DEFAULT_WORD_CHARS
) -> List[Token]:
    """Tokenize ``text`` into ordered :class:`Token` objects.

    Word and non-word runs strictly alternate and concatenate back to the
    original input. Returns ``[]`` for an empty string.
    """
    if not text:
        return []

    pattern = _word_regex(word_chars)
    tokens: List[Token] = []
    pos = 0
    for match in pattern.finditer(text):
        start, end = match.start(), match.end()
        if start > pos:  # non-word run before this word
            tokens.append(Token(text[pos:start], False))
        tokens.append(Token(text[start:end], True))
        pos = end
    if pos < len(text):  # trailing non-word run
        tokens.append(Token(text[pos:], False))
    return tokens


def tokenize(text: str, word_chars: str = DEFAULT_WORD_CHARS) -> List[str]:
    """Return ordered, alternating word / non-word substrings.

    This is the M4 contract: ``"".join(tokenize(t)) == t`` for any input.
    Use :func:`tokenize_tagged` when you also need to know which tokens are
    words (the reader in M5 will).
    """
    return [tok.text for tok in tokenize_tagged(text, word_chars)]
