"""M4 tokenizer tests.

These exercise the public parser interface only (tokenize / tokenize_tagged),
so they describe *what* the tokenizer does, not *how* - they survive any
internal refactor of the regex/looping. Pure functions: no DB or app fixtures.
"""
import pytest

from app.services.parser import (
    DEFAULT_WORD_CHARS,
    Token,
    tokenize,
    tokenize_tagged,
)


def test_splits_words_and_spaces():
    assert tokenize("hello world") == ["hello", " ", "world"]


def test_punctuation_is_a_nonword_token():
    assert tokenize("Hi, there!") == ["Hi", ", ", "there", "!"]


def test_empty_string_yields_no_tokens():
    assert tokenize("") == []


def test_leading_and_trailing_nonwords_are_preserved():
    assert tokenize("  hi  ") == ["  ", "hi", "  "]


def test_newlines_are_preserved_as_nonwords():
    assert tokenize("a\nb") == ["a", "\n", "b"]


@pytest.mark.parametrize(
    "text",
    [
        "The quick brown fox.",
        "  spaced  out \n lines \t too!",
        "caf\u00e9 cr\u00e8me",
        "",
        "!!!",
    ],
)
def test_roundtrip_is_lossless(text):
    assert "".join(tokenize(text)) == text


def test_accented_latin_chars_are_words_by_default():
    # e-acute (U+00E9) and e-grave (U+00E8) fall in the default range.
    assert tokenize("caf\u00e9 cr\u00e8me") == ["caf\u00e9", " ", "cr\u00e8me"]


def test_digits_are_nonwords_under_default_config():
    # Default word_chars is letters only, so digits split off.
    assert tokenize("ab12") == ["ab", "12"]


def test_custom_word_chars_can_include_digits():
    assert tokenize("ab12 cd", word_chars="a-zA-Z0-9") == ["ab12", " ", "cd"]


def test_tagged_marks_words_and_nonwords():
    assert tokenize_tagged("hi!") == [Token("hi", True), Token("!", False)]


def test_tagged_alternates_strictly():
    kinds = [t.is_word for t in tokenize_tagged("one, two three.")]
    # No two adjacent tokens share the same kind.
    assert all(a != b for a, b in zip(kinds, kinds[1:]))


def test_default_word_chars_matches_language_model():
    # Guards against drift from app/models/language.py's default.
    assert DEFAULT_WORD_CHARS == "a-zA-Z\u00c0-\u017f"
