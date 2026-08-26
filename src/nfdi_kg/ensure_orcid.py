"""Collate all ORCiD identifiers and make sure they're in wikidata."""

import itertools as itt

import click
import pandas as pd
import wikidata_client
from quickstatements_client import EntityLine
from quickstatements_client.model import lines_to_new_tab
from quickstatements_client.sources.orcid import iter_orcid_lines
from tqdm import tqdm

from nfdi_kg.constants import DATA


@click.command()
def main() -> None:
    df1 = pd.read_csv(DATA.joinpath("section_roles.tsv"), sep="\t")
    df1 = df1[df1["person_orcid"].notna()]

    df2 = pd.read_csv(DATA.joinpath("working_group_roles.tsv"), sep="\t")
    df2 = df2[df2["person_orcid"].notna()]

    orcids = sorted(
        set(df1["person_orcid"].unique()).union(df2["person_orcid"].unique())
    )

    tqdm.write(f"querying wikidata for {len(orcids)} ORCiDs")
    orcid_to_entities = wikidata_client.get_entities_by_orcid(orcids)

    orcid_without_entities = set(orcids).difference(orcid_to_entities)
    if not orcid_without_entities:
        tqdm.write("everyone is in!")
        lines = []
        for wg_wikidata, orcid in df2[["wikidata", "person_orcid"]].values:
            if pd.isna(wg_wikidata) or pd.isna(orcid):
                continue
            line = EntityLine(
                subject=wg_wikidata, predicate="P488", target=orcid_to_entities[orcid]
            )
            lines.append(line)
        lines_to_new_tab(lines)
    elif False:
        tqdm.write(f"need to create {len(orcid_without_entities)} new records")
        lines_to_new_tab(
            itt.chain.from_iterable(
                iter_orcid_lines(orcid)
                for orcid in tqdm(orcid_without_entities, desc="Querying ORCiD API")
            )
        )


if __name__ == "__main__":
    main()
