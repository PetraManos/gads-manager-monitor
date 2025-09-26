from core.names import declared_type, expected_label

def test_declared_type_matrix():
    cases = {
        "Brand - Phrase": ("PHRASE_ONLY", "PHRASE"),
        "Brand - Exact": ("EXACT_ONLY", "EXACT"),
        "Brand - Broad": ("BROAD_ONLY", "BROAD"),
        "P/E": ("PHRASE_AND_EXACT", "PHRASE or EXACT"),
        "": (None, ""),
    }
    for k, (decl, label) in cases.items():
        assert declared_type(k) == decl
        assert expected_label(decl) == label
