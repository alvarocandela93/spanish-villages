import pytest

from spanish_villages_pipeline.ine_codes import (
    UnitType,
    is_eligible_singular_entity,
    parse_ine_code,
)


def test_parse_entity_singular():
    parsed = parse_ine_code("01001000100")
    assert parsed.unit_type == UnitType.SINGULAR_ENTITY


def test_parse_nucleus():
    parsed = parse_ine_code("01001000101")
    assert parsed.unit_type == UnitType.NUCLEUS


def test_parse_disseminated():
    parsed = parse_ine_code("01001000199")
    assert parsed.unit_type == UnitType.DISEMINATED


def test_eligibility_threshold():
    assert is_eligible_singular_entity(9_999, UnitType.SINGULAR_ENTITY)
    assert not is_eligible_singular_entity(10_000, UnitType.SINGULAR_ENTITY)
    assert not is_eligible_singular_entity(100, UnitType.NUCLEUS)


def test_invalid_code():
    with pytest.raises(ValueError):
        parse_ine_code("123")
