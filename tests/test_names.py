from core.names import CampaignName, has_match_type_token, declared_type, expected_label, is_dynamic_search_name, is_branded_search_name


def test_declared_type_phrase_only():
    assert declared_type("Brand - Phrase") == "PHRASE_ONLY"
    assert expected_label("PHRASE_ONLY") == "PHRASE"

def test_dynamic_and_brand():
    assert is_dynamic_search_name("Retail Dynamic") is True
    assert is_branded_search_name("Brand - Search") is True

def test_has_match_type_token_requires_match_word():
    assert CampaignName("Exact Match").has_match_type_token
    assert CampaignName("phrase-match").has_match_type_token
    assert CampaignName("BROAD_match").has_match_type_token
    # No "match" word → False (GS parity)
    assert not CampaignName("Brand - Exact").has_match_type_token
    # punctuation should not count as word boundary without "match"
    assert not CampaignName("red-blue").has_match_type_token

def test_declared_type_variants():
    assert CampaignName("Brand - Phrase").declared_type == "PHRASE_ONLY"
    assert CampaignName("Brand - Exact").declared_type  == "EXACT_ONLY"
    assert CampaignName("Brand - Broad").declared_type  == "BROAD_ONLY"
    # P/E shorthand or tokens together ⇒ PHRASE_AND_EXACT
    assert CampaignName("P/E").declared_type == "PHRASE_AND_EXACT"
    assert CampaignName("Exact & Phrase").declared_type == "PHRASE_AND_EXACT"
    assert CampaignName("Phrase + Exact").declared_type == "PHRASE_AND_EXACT"
    # Ambiguous/mixed with broad shouldn’t force a type
    assert CampaignName("Brand - Phrase - Broad").declared_type is None

def test_expected_label_mapping():
    assert CampaignName("Brand - Phrase").expected_label == "PHRASE"
    assert expected_label("EXACT_ONLY") == "EXACT"
    assert expected_label("BROAD_ONLY") == "BROAD"
    assert expected_label("PHRASE_AND_EXACT") == "PHRASE or EXACT"
    assert expected_label(None) == ""

def test_dynamic_and_branded_detection():
    assert CampaignName("Dynamic Search Ads AU").is_dynamic_search
    assert is_dynamic_search_name("DSA Campaign")  # wrapper
    assert CampaignName("Brand - Phrase").is_branded_search
    assert is_branded_search_name("Branded - Exact")  # wrapper
    assert not CampaignName("Generic - Exact").is_branded_search

def test_function_wrappers_delegate_to_object():
    assert has_match_type_token("Exact Match")
    assert declared_type("Brand - Exact") == "EXACT_ONLY"