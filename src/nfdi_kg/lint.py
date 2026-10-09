import pandas as pd
from pydantic_extra_types.country import (
    _index_by_alpha2,
    _index_by_short_name,
)

from nfdi_kg.constants import DATA

SORT_COLUMNS: dict[str, str | list[str]] = {
    "consortium_member_institutions": ["consortium_label", "institution_label"],
    "eric_hierarchy": ["child name", "parent name"],
    "eric_relations": ["eric_name", "interaction_type", "name", "country"],
    "erics": "name",
    "interactions": ["internal_name", "external_name"],
    "memberships": ["organization_name", "person_name"],
    "section_roles": ["section key", "person_name"],
    "sections": "key",
    "task_forces": ["type", "name"],
    "working_group_roles": ["section_key", "person_name"],
    "working_groups": "label",
}

KOSOVO_CODE = "XK"


def _norm_locale(locale: str) -> str:
    if nc := _index_by_short_name().get(locale):
        return nc.alpha2
    if locale.lower() in {"international", "int", "intl", "int'l"}:
        return "International"
    if locale.lower() in {"europe", "european", "eu", "european union"}:
        return "Europe"
    if locale.lower() in {"nfdi"}:
        return "NFDI"
    if locale in _index_by_alpha2() or locale == KOSOVO_CODE:
        return locale
    raise ValueError(f"unknown country {locale}")


def main():
    for path in DATA.glob("*.tsv"):
        df = pd.read_csv(path, sep="\t", dtype=str)
        for column in df.columns:
            df[column] = df[column].map(
                lambda s: s.strip().rstrip("/"), na_action="ignore"
            )
        for column in ["country", "external_locale"]:
            if column in df.columns:
                df[column] = df[column].map(_norm_locale, na_action="ignore")
        if sort_column := SORT_COLUMNS.get(path.stem):
            df = df.sort_values(sort_column)
        df.to_csv(path, sep="\t", index=False)


if __name__ == "__main__":
    main()
