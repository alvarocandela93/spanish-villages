from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from .ine_codes import (
    UnitType,
    classify_code,
    is_eligible_singular_entity,
    parse_ine_code,
)


@dataclass(frozen=True)
class ValidationIssue:
    """A single validation problem."""

    dataset: str
    identifier: str
    message: str

    def __str__(self) -> str:
        return f"[{self.dataset}] {self.identifier}: {self.message}"


def _require_string(
    value: Any,
    *,
    field: str,
    identifier: str,
    dataset: str,
) -> list[ValidationIssue]:
    if not isinstance(value, str) or not value.strip():
        return [
            ValidationIssue(
                dataset,
                identifier,
                f"{field} must be a non-empty string",
            )
        ]
    return []


def _require_non_negative_population(
    value: Any,
    *,
    identifier: str,
    dataset: str,
) -> list[ValidationIssue]:
    if not isinstance(value, int):
        return [
            ValidationIssue(
                dataset,
                identifier,
                "population must be an integer",
            )
        ]

    if value < 0:
        return [
            ValidationIssue(
                dataset,
                identifier,
                "population cannot be negative",
            )
        ]

    return []


def _validate_code(
    code: Any,
    *,
    identifier: str,
    dataset: str,
    expected_type: UnitType,
) -> list[ValidationIssue]:
    if not isinstance(code, str):
        return [
            ValidationIssue(
                dataset,
                identifier,
                "INE code must be a string",
            )
        ]

    try:
        parsed = parse_ine_code(code)
    except ValueError as exc:
        return [
            ValidationIssue(
                dataset,
                identifier,
                f"invalid INE code: {exc}",
            )
        ]

    actual_type = classify_code(parsed)

    if actual_type != expected_type:
        return [
            ValidationIssue(
                dataset,
                identifier,
                f"expected unit type {expected_type.value}, "
                f"got {actual_type.value}",
            )
        ]

    return []


def _duplicate_issues(
    records: Iterable[dict[str, Any]],
    *,
    id_field: str,
    dataset: str,
) -> list[ValidationIssue]:
    seen: set[str] = set()
    issues: list[ValidationIssue] = []

    for record in records:
        identifier = str(record.get(id_field, "<missing>"))

        if identifier in seen:
            issues.append(
                ValidationIssue(
                    dataset,
                    identifier,
                    f"duplicate {id_field}",
                )
            )

        seen.add(identifier)

    return issues


def validate_dataset(
    places: list[dict[str, Any]],
    municipalities: list[dict[str, Any]],
    nuclei: list[dict[str, Any]],
) -> list[ValidationIssue]:
    """
    Validate the complete canonical dataset.

    This function deliberately returns all discovered issues rather than
    raising on the first problem. That makes source-data failures easier
    to diagnose when processing the full national INE dataset.
    """

    issues: list[ValidationIssue] = []

    # ------------------------------------------------------------------
    # Municipality validation
    # ------------------------------------------------------------------

    issues.extend(
        _duplicate_issues(
            municipalities,
            id_field="ineCode",
            dataset="municipalities",
        )
    )

    municipality_ids: set[str] = set()

    for municipality in municipalities:
        code = municipality.get("ineCode")
        identifier = str(code) if code is not None else "<missing>"

        issues.extend(
            _require_string(
                municipality.get("name"),
                field="name",
                identifier=identifier,
                dataset="municipalities",
            )
        )

        issues.extend(
            _validate_code(
                code,
                identifier=identifier,
                dataset="municipalities",
                expected_type=UnitType.MUNICIPALITY_TOTAL,
            )
        )

        if isinstance(code, str):
            municipality_ids.add(code)

    # ------------------------------------------------------------------
    # Population-place validation
    # ------------------------------------------------------------------

    issues.extend(
        _duplicate_issues(
            places,
            id_field="ineCode",
            dataset="places",
        )
    )

    place_ids: set[str] = set()

    for place in places:
        code = place.get("ineCode")
        identifier = str(code) if code is not None else "<missing>"

        issues.extend(
            _require_string(
                place.get("name"),
                field="name",
                identifier=identifier,
                dataset="places",
            )
        )

        issues.extend(
            _require_non_negative_population(
                place.get("population"),
                identifier=identifier,
                dataset="places",
            )
        )

        issues.extend(
            _validate_code(
                code,
                identifier=identifier,
                dataset="places",
                expected_type=UnitType.SINGULAR_ENTITY,
            )
        )

        municipality_code = place.get("municipalityCode")

        if municipality_code not in municipality_ids:
            issues.append(
                ValidationIssue(
                    "places",
                    identifier,
                    f"municipalityCode {municipality_code!r} "
                    "does not reference an existing municipality",
                )
            )

        if isinstance(code, str):
            place_ids.add(code)

            population = place.get("population")

            if isinstance(population, int):
                expected_eligibility = is_eligible_singular_entity(
                    population,
                    UnitType.SINGULAR_ENTITY,
                )

                actual_eligibility = place.get("isEligible")

                if actual_eligibility != expected_eligibility:
                    issues.append(
                        ValidationIssue(
                            "places",
                            identifier,
                            "isEligible does not match the "
                            "population threshold",
                        )
                    )

    # ------------------------------------------------------------------
    # Nucleus validation
    # ------------------------------------------------------------------

    issues.extend(
        _duplicate_issues(
            nuclei,
            id_field="ineCode",
            dataset="nuclei",
        )
    )

    for nucleus in nuclei:
        code = nucleus.get("ineCode")
        identifier = str(code) if code is not None else "<missing>"

        issues.extend(
            _require_string(
                nucleus.get("name"),
                field="name",
                identifier=identifier,
                dataset="nuclei",
            )
        )

        issues.extend(
            _require_non_negative_population(
                nucleus.get("population"),
                identifier=identifier,
                dataset="nuclei",
            )
        )

        issues.extend(
            _validate_code(
                code,
                identifier=identifier,
                dataset="nuclei",
                expected_type=UnitType.NUCLEUS,
            )
        )

        parent_code = nucleus.get("entityCode")

        if parent_code not in place_ids:
            issues.append(
                ValidationIssue(
                    "nuclei",
                    identifier,
                    f"entityCode {parent_code!r} "
                    "does not reference an existing singular entity",
                )
            )

    return issues


def validate_or_raise(
    places: list[dict[str, Any]],
    municipalities: list[dict[str, Any]],
    nuclei: list[dict[str, Any]],
) -> None:
    """Validate the dataset and raise a readable error if invalid."""

    issues = validate_dataset(
        places=places,
        municipalities=municipalities,
        nuclei=nuclei,
    )

    if not issues:
        return

    formatted = "\n".join(str(issue) for issue in issues)

    raise ValueError(
        f"Dataset validation failed with {len(issues)} issue(s):\n"
        f"{formatted}"
    )