"""Unit tests for the M4 tokenizer (``app.services.parser``).

The parser splits text into a *lossless*, strictly alternating sequence of
word / non-word runs. These tests pin down that contract:

* round-trip  -> ``"".join(tokenize(t)) == t`` for any input,
* alternation -> word and non-word tokens never repeat back-to-back,
* word_chars  -> which characters count as "word" is driven by config,
* tagging     -> ``tokenize_tagged`` flags each run as word / non-word.
"""
import pytest

from app.services.parser import (
    DEFAULT_WORD_CHARS,
    Token,
    tokenize,
    tokenize_tagged,
)


# --------------------------------------------------------------------------- #
# Round-trip: the parser must be lossless for arbitrary text.
# --------------------------------------------------------------------------- #
ROUND_TRIP_SAMPLES = [
    "",
    "hello",
    "Hello, world!",
    "  leading and trailing spaces  ",
    "line one\nline two\ttabbed",
    "punctuation!?... still: works;",
    "123 abc 456",
    "caf\u00e9 d\u00e9j\u00e0 vu",
    "don't can't won't",
    "---",
    "\n\n\n",
    "M\u00fcller stra\u00dfe \u00f1and\u00fa",
]


@pytest.mark.parametrize("text", ROUND_TRIP_SAMPLES)
def test_tokenize_round_trips(text):
    assert "".join(tokenize(text)) == text


@pytest.mark.parametrize("text", ROUND_TRIP_SAMPLES)
def test_tagged_round_trips(text):
    assert "".join(tok.text for tok in tokenize_tagged(text)) == text


# --------------------------------------------------------------------------- #
# Empty input.
# --------------------------------------------------------------------------- #
def test_empty_string_yields_no_tokens():
    assert tokenize("") == []
    assert tokenize_tagged("") == []


# --------------------------------------------------------------------------- #
# Basic word / non-word splitting on a normal sentence.
# --------------------------------------------------------------------------- #
def test_simple_sentence_splits_words_and_nonwords():
    assert tokenize("Hello, world!") == ["Hello", ", ", "world", "!"]


def test_simple_sentence_is_word_flags():
    tagged = tokenize_tagged("Hello, world!")
    assert tagged == [
        Token("Hello", True),
        Token(", ", False),
        Token("world", True),
        Token("!", False),
    ]


# --------------------------------------------------------------------------- #
# Structural invariants that must hold for every sample.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", [s for s in ROUND_TRIP_SAMPLES if s])
def test_tokens_are_never_empty(text):
    assert all(tok.text for tok in tokenize_tagged(text))


@pytest.mark.parametrize("text", [s for s in ROUND_TRIP_SAMPLES if s])
def test_word_and_nonword_runs_strictly_alternate(text):
    flags = [tok.is_word for tok in tokenize_tagged(text)]
    assert all(a != b for a, b in zip(flags, flags[1:])), flags


# --------------------------------------------------------------------------- #
# Leading / trailing / standalone non-word runs.
# --------------------------------------------------------------------------- #
def test_leading_and_trailing_nonwords():
    assert tokenize(" hi ") == [" ", "hi", " "]


def test_only_nonword_is_single_nonword_token():
    tagged = tokenize_tagged("...!!!")
    assert tagged == [Token("...!!!", False)]


def test_only_word_is_single_word_token():
    tagged = tokenize_tagged("hello")
    assert tagged == [Token("hello", True)]


def test_newlines_and_tabs_are_nonwords():
    assert tokenize("a\nb\tc") == ["a", "\n", "b", "\t", "c"]


# --------------------------------------------------------------------------- #
# Default word_chars: Latin letters + accented range are words;
# digits and apostrophes are NOT (they fall into non-word runs).
# --------------------------------------------------------------------------- #
def test_accented_letters_are_words_by_default():
    assert tokenize("caf\u00e9 d\u00e9j\u00e0") == ["caf\u00e9", " ", "d\u00e9j\u00e0"]


def test_digits_are_nonword_by_default():
    assert tokenize("abc123") == ["abc", "123"]
    assert tokenize_tagged("abc123") == [Token("abc", True), Token("123", False)]


def test_apostrophe_breaks_words_by_default():
    # An apostrophe is not in the default word_chars, so "don't" is 3 tokens.
    assert tokenize("don't") == ["don", "'", "t"]


# --------------------------------------------------------------------------- #
# Custom word_chars config (per-language, Lute-style).
# --------------------------------------------------------------------------- #
def test_custom_word_chars_can_include_digits():
    assert tokenize("abc123", word_chars="a-zA-Z0-9") == ["abc123"]


def test_custom_word_chars_can_include_apostrophe():
    assert tokenize("don't", word_chars="a-zA-Z'") == ["don't"]


def test_empty_word_chars_falls_back_to_default():
    # An empty config must behave exactly like the default alphabet.
    assert tokenize("Hello!", word_chars="") == tokenize("Hello!")
    assert tokenize("Hello!", word_chars="") == ["Hello", "!"]


def test_default_word_chars_constant_used_when_arg_omitted():
    # Calling with the exported default and omitting the arg agree.
    assert tokenize("Stra\u00dfe 42") == tokenize("Stra\u00dfe 42", word_chars=DEFAULT_WORD_CHARS)


# --------------------------------------------------------------------------- #
# tokenize() and tokenize_tagged() stay consistent.
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("text", ROUND_TRIP_SAMPLES)
def test_tokenize_matches_tagged_text(text):
    assert tokenize(text) == [tok.text for tok in tokenize_tagged(text)]
