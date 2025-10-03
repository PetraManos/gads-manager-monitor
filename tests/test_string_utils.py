from core.string_utils import (
    norm,
    collapse_one_line,
    has_word,
    has_match_type_token,
    norm_collapse,
    make_key,
)

def test_norm_exact_replica():
    # NBSP, multiple spaces, trimming, casing
    assert norm("  A\u00A0B   C ") == "a b c"
    # None
    assert norm(None) == ""
    # Multiple internal whitespace
    assert norm("A   B C") == "a b c"
    # Already clean
    assert norm("Clean String") == "clean string"

def test_collapse_one_line():
    assert collapse_one_line("a\nb\r\nc") == "a b c"
    assert collapse_one_line("  a   \n  b  ") == "a b"
    assert collapse_one_line(None) == ""

def test_has_word():
    assert has_word("red blue green", "blue")
    assert not has_word("red-blue", "blue")     # separator is punctuation, but not a whole word
    assert has_word("blue.", "blue")            # punctuation boundary should match
    assert has_word("Big(Blue)+Sky", "Blue")    # escaped metachars in word

def test_has_match_type_token():
    assert has_match_type_token("Exact Match")
    assert has_match_type_token("phrase-match")
    assert has_match_type_token("BROAD_match")
    assert not has_match_type_token("random name")

def test_norm_collapse_and_make_key():
    assert norm_collapse("  A \n B  ") == "a b"
    assert make_key("  A \n B  ", "C") == "a b|c"
