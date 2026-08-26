"""Summarize the current curation burden."""

from typing import Any

import click
import pandas as pd

from nfdi_kg.constants import get_interactions_df, get_working_groups_df

CHARTER_EMPTY = {
    "Q141133902": "Data Protection",
    "Q141133933": "Data Integration ",
    "Q141133943": "Electronic Lab Notebook",
}


@click.command()
def main() -> None:
    interactions_df = get_interactions_df()
    curated = interactions_df["wikidata"].unique()

    working_groups_df = get_working_groups_df()

    def _get_status(row: dict[str, Any]) -> str:
        if "wikidata" not in row:
            return "Wikidata not available"
        elif row["wikidata"] in CHARTER_EMPTY:
            return "Charter Contains No Information"
        elif row["wikidata"] in curated:
            return "Charter Curated"
        elif pd.isna(row["charter_zenodo"]):
            return "No Charter Available"
        else:
            return "Charter Uncurated"

    working_groups_df["status"] = [
        _get_status(row) for _, row in working_groups_df.iterrows()
    ]
    working_groups_df = working_groups_df[
        working_groups_df["status"] != "Charter Curated"
    ]

    click.echo("Curation of Working Groups' interactions\n")
    click.echo(
        working_groups_df[["wikidata", "label", "status"]].to_markdown(index=False)
    )


if __name__ == "__main__":
    main()
