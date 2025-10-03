from core.string_utils import norm, collapse_one_line, has_word
from core.names import CampaignName

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
    assert collapse_one_line(" a \n b \t  c ") == "a b c"

def test_has_word():
    assert has_word("red blue green", "blue")
    # hyphen is a non-word char -> should count as a boundary (GS parity)
    assert has_word("red-blue", "blue")


def test_has_match_type_token_via_object():
    # GS parity requires "...match"
    assert CampaignName("Exact Match").has_match_type_token
    assert CampaignName("phrase-match").has_match_type_token
    assert CampaignName("BROAD_match").has_match_type_token
    assert not CampaignName("random name").has_match_type_token
