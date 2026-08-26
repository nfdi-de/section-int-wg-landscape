"""Constants for the NFDI KG package."""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.parent.resolve()
DATA = ROOT / "_data"

INTERACTIONS_PATH = DATA / "interactions.tsv"
SECTION_ROLES_PATH = DATA / "section_roles.tsv"
SECTIONS_PATH = DATA / "sections.tsv"
WORKING_GROUP_ROLES_PATH = DATA / "working_group_roles.tsv"
WORKING_GROUPS_PATH = DATA / "working_groups.tsv"


def get_working_groups_df() -> pd.DataFrame:
    """Get working groups dataframe."""
    return pd.read_csv(WORKING_GROUPS_PATH, sep="\t", dtype=str)


def get_interactions_df() -> pd.DataFrame:
    """Get interactions dataframe."""
    return pd.read_csv(INTERACTIONS_PATH, sep="\t", dtype=str)
