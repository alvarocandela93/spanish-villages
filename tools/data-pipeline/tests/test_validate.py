import pytest

from spanish_villages_pipeline.ine_codes import UnitType
from spanish_villages_pipeline.validate import (
    validate_dataset,
    validate_or_raise,
)


def municipality(code="01001000"):
    return {
        "ineCode": code,
        "name": "Example Municipality",
    }


def place(
    code="01001000100",
    name="Example Village",
    population=5000,
    municipality_code="01001000",
    is_eligible=True,
):
    return {
        "ineCode": code,
        "name": name,
        "population": population,
        "municipalityCode": municipality_code,
        "isEligible": is_eligible,
    }


def nucleus(
    code="01001000101",
    name="Example Nucleus",
    population=1000,
    entity_code="01001000100",
):
    return {
        "ineCode": code,
        "name": name,
        "population": population,
        "entityCode": entity_code,
    }


def test_valid_dataset_has_no_issues():
    issues = validate_dataset(
        places=[place()],
        municipalities=[municipality()],
        nuclei=[nucleus()],
    )

    assert issues == []


def test_population_of_9999_is_eligible():
    issues = validate_dataset(
        places=[place(population=9999, is_eligible=True)],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert issues == []


def test_population_of_10000_is_not_eligible():
    issues = validate_dataset(
        places=[place(population=10000, is_eligible=False)],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert issues == []


def test_wrong_eligibility_flag_is_rejected():
    issues = validate_dataset(
        places=[place(population=10000, is_eligible=True)],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert any(
        "isEligible does not match" in issue.message
        for issue in issues
    )


def test_negative_population_is_rejected():
    issues = validate_dataset(
        places=[place(population=-1)],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert any(
        "population cannot be negative" in issue.message
        for issue in issues
    )


def test_empty_place_name_is_rejected():
    issues = validate_dataset(
        places=[place(name="")],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert any(
        "name must be a non-empty string" in issue.message
        for issue in issues
    )


def test_duplicate_place_ids_are_rejected():
    issues = validate_dataset(
        places=[
            place(),
            place(),
        ],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert any(
        "duplicate ineCode" in issue.message
        for issue in issues
    )


def test_place_with_unknown_municipality_is_rejected():
    issues = validate_dataset(
        places=[
            place(municipality_code="99999999"),
        ],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert any(
        "does not reference an existing municipality" in issue.message
        for issue in issues
    )


def test_place_must_be_singular_entity():
    # Municipality-total code, not an entity code.
    issues = validate_dataset(
        places=[
            place(code="01001000000"),
        ],
        municipalities=[municipality()],
        nuclei=[],
    )

    assert any(
        "expected unit type singular_entity" in issue.message
        for issue in issues
    )


def test_nucleus_with_unknown_parent_is_rejected():
    issues = validate_dataset(
        places=[place()],
        municipalities=[municipality()],
        nuclei=[
            nucleus(entity_code="99999999999"),
        ],
    )

    assert any(
        "does not reference an existing singular entity" in issue.message
        for issue in issues
    )


def test_nucleus_must_have_nucleus_code():
    issues = validate_dataset(
        places=[place()],
        municipalities=[municipality()],
        nuclei=[
            nucleus(code="01001000100"),
        ],
    )

    assert any(
        "expected unit type nucleus" in issue.message
        for issue in issues
    )


def test_duplicate_municipality_ids_are_rejected():
    issues = validate_dataset(
        places=[],
        municipalities=[
            municipality(),
            municipality(),
        ],
        nuclei=[],
    )

    assert any(
        "duplicate ineCode" in issue.message
        for issue in issues
    )


def test_validate_or_raise_accepts_valid_dataset():
    validate_or_raise(
        places=[place()],
        municipalities=[municipality()],
        nuclei=[nucleus()],
    )


def test_validate_or_raise_raises_for_invalid_dataset():
    with pytest.raises(ValueError, match="Dataset validation failed"):
        validate_or_raise(
            places=[place(population=-1)],
            municipalities=[municipality()],
            nuclei=[],
        )