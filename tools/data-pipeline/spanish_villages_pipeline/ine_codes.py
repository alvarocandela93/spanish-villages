"""INE 11-digit population unit codes (PPMMMCCSSNN)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class UnitType(str, Enum):
    MUNICIPALITY_TOTAL = "municipality_total"
    COLLECTIVE_ENTITY = "collective_entity"
    SINGULAR_ENTITY = "singular_entity"
    NUCLEUS = "nucleus"
    DISEMINATED = "disseminated"
    OTHER = "other"


@dataclass(frozen=True)
class ParsedIneCode:
    raw: str
    province_code: str
    municipality_code: str
    collective_code: str
    singular_code: str
    nucleus_code: str

    @property
    def municipality_ine_code(self) -> str:
        return f"{self.province_code}{self.municipality_code}"

    @property
    def unit_type(self) -> UnitType:
        cc = self.collective_code
        ss = self.singular_code
        nn = self.nucleus_code
        if cc == "00" and ss == "00" and nn == "00":
            return UnitType.MUNICIPALITY_TOTAL
        if nn == "99":
            return UnitType.DISEMINATED
        if cc != "00" and ss == "00" and nn == "00":
            return UnitType.COLLECTIVE_ENTITY
        if ss != "00" and nn == "00":
            return UnitType.SINGULAR_ENTITY
        if ss != "00" and nn != "00":
            return UnitType.NUCLEUS
        return UnitType.OTHER


def parse_ine_code(code: str) -> ParsedIneCode:
    normalized = code.strip()
    if len(normalized) != 11 or not normalized.isdigit():
        raise ValueError(f"Invalid INE code: {code!r}")
    return ParsedIneCode(
        raw=normalized,
        province_code=normalized[0:2],
        municipality_code=normalized[2:5],
        collective_code=normalized[5:7],
        singular_code=normalized[7:9],
        nucleus_code=normalized[9:11],
    )


def build_ine_code(
    province: str,
    municipality: str,
    collective: str,
    singular: str,
    nucleus: str,
) -> str:
    return f"{province}{municipality}{collective}{singular}{nucleus}"


def entity_code_for(parsed: ParsedIneCode) -> str | None:
    """INE code of the parent entidad singular, if this row is a nucleus or diseminado."""
    if parsed.unit_type not in (UnitType.NUCLEUS, UnitType.DISEMINATED):
        return None
    return build_ine_code(
        parsed.province_code,
        parsed.municipality_code,
        parsed.collective_code,
        parsed.singular_code,
        "00",
    )


POPULATION_THRESHOLD = 10_000


def is_eligible_singular_entity(population: int, unit_type: UnitType) -> bool:
    return unit_type == UnitType.SINGULAR_ENTITY and population < POPULATION_THRESHOLD
