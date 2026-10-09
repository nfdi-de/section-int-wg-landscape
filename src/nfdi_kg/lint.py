import pandas as pd

from nfdi_kg.constants import DATA

SORT_COLUMNS: dict[str, str | list[str]] = {
    "consortium_member_institutions": ["consortium_label", "institution_label"],
    "eric_hierarchy": ["child name", "parent name"],
    "eric_relations": ["eric_name", "interaction_type", "name"],
    "erics": "name",
    "interactions": ["internal_name", "external_name"],
    "memberships": ["organization_name", "person_name"],
    "section_roles": ["section key", "person_name"],
    "sections": "key",
    "task_forces": ["type", "name"],
    "working_group_roles": ["section_key", "person_name"],
    "working_groups": "label",
}


def main():
    for path in DATA.glob("*.tsv"):
        df = pd.read_csv(path, sep="\t", dtype=str)
        for column in df.columns:
            df[column] = df[column].map(lambda s: s.strip(), na_action="ignore")
        if sort_column := SORT_COLUMNS.get(path.stem):
            df = df.sort_values(sort_column)
        df.to_csv(path, sep="\t", index=False)


if __name__ == "__main__":
    main()
