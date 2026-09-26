from spanish_villages_pipeline.normalize import normalize_for_search


def test_accent_insensitive():
    assert normalize_for_search("Ávila") == normalize_for_search("avila")


def test_case_insensitive():
    assert normalize_for_search("Teruel") == normalize_for_search("TERUEL")
