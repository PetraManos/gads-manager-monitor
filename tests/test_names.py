from core.names import declared_type, expected_label, is_dynamic_search_name, is_branded_search_name

def test_declared_type_phrase_only():
    assert declared_type("Brand - Phrase") == "PHRASE_ONLY"
    assert expected_label("PHRASE_ONLY") == "PHRASE"

def test_dynamic_and_brand():
    assert is_dynamic_search_name("Retail Dynamic") is True
    assert is_branded_search_name("Brand - Search") is True
