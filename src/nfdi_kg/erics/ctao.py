"""Scrape the CTAO consortium page."""

URL = "https://www.ctao.org/partners/ctao-consortium/"

import pyobo
import pystow
from pydantic_extra_types.country import _index_by_short_name
from tabulate import tabulate

from nfdi_kg.constants import DATA

ERIC_RELATIONS = DATA.joinpath("eric_relations.tsv")


def main() -> None:
    """Scrape the CTAO consortium page."""
    grounder = pyobo.get_grounder("ror", progress=True)
    rows = []
    soup = pystow.ensure_soup("tmp", url=URL, name="csao.html")
    for path in soup.find_all(class_="dhsv-akkordeon--item"):
        title = path.find("h3")
        if not title:
            raise ValueError

        if title.text in _index_by_short_name():
            code = _index_by_short_name()[title.text].alpha2
        elif title.text == "United States of America":
            code = "US"
        elif title.text in "Czech Republic":
            code = "CZ"
        else:
            print("FAILED TO LOOKUP", title.text)
            continue

        for anchor in path.find_all("a"):
            name = anchor.text
            if name is None:
                raise ValueError

            match = grounder.get_best_match(name)
            if match is None and "," in name:
                for part in name.split(","):
                    match = grounder.get_best_match(part)
                    if match is not None:
                        break

            rows.append(
                (
                    "Q1070229",
                    "CTAO",
                    "member",
                    code,
                    "",  # wikidata
                    match.identifier if match is not None else "",  # ROR
                    anchor.text,
                    "",  # abbr
                    anchor.get("href").rstrip(),
                    "",  # people
                    "",  # comment
                )
            )

    with ERIC_RELATIONS.open("a") as file:
        for row in rows:
            print(*row, sep="\t", file=file)

    print(tabulate(rows))


if __name__ == "__main__":
    main()
