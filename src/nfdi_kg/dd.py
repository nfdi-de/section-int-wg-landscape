from collections import defaultdict
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BaseModel, EmailStr, Field
from pydantic_extra_types.language_code import LanguageAlpha2
from pystow.utils import read_pydantic_tsv, safe_open_dict_reader, write_pydantic_json

from nfdi_kg.constants import DATA

SECTIONS_PATH = DATA.joinpath("sections.tsv")
SECTIONS_ROLES_PATH = DATA.joinpath("section_roles.tsv")
WORKING_GROUPS_PATH = DATA.joinpath("working_groups.tsv")
WORKING_GROUP_ROLES_PATH = DATA.joinpath("working_group_roles.tsv")
OUTPUT_JSON_PATH = DATA.joinpath("output.json")

type SectionAbbreviation = Literal[
    "meta", "elsa", "industry", "int", "edutrain", "infra"
]


class Zenodo(BaseModel):
    """A Zenodo link."""

    record: int
    language: LanguageAlpha2

    @property
    def url(self) -> str:
        return f"https://zenodo.org/record/{self.record}"


class Person(BaseModel):
    name: str
    orcid: str | None = None
    email: EmailStr | None = None


class Role(BaseModel):
    person: Person
    role: str | None = None
    start: str | None = None
    end: str | None = None


class WorkingGroup(BaseModel):
    wikidata: str | None = None
    label: str
    key: str
    zenodo: Zenodo | None = None
    mailing_list: EmailStr | None = None
    start: str | None = None
    end: str | None = None
    roles: Annotated[list[Role], Field(default_factory=list)]


class Section(BaseModel):
    wikidata: str
    key: SectionAbbreviation
    label: str
    zenodo: Zenodo
    homepage: AnyUrl
    mailing_list: EmailStr
    roles: Annotated[list[Role], Field(default_factory=list)]
    working_groups: Annotated[list[WorkingGroup], Field(default_factory=list)]


class KnowledgeBase(BaseModel):
    sections: list[Section]


def get_kb() -> KnowledgeBase:
    working_group_roles = defaultdict(list)
    with safe_open_dict_reader(WORKING_GROUP_ROLES_PATH) as reader:
        for row in reader:
            name = row.pop("person_name") or None
            if name is None:
                continue
            working_group_roles[row.pop("wikidata")].append(
                Role(
                    person=Person(
                        name=name,
                        orcid=row.pop("person_orcid") or None,
                        email=row.pop("person_email") or None,
                    ),
                    role=row.pop("role", None) or None,
                    start=row.pop("start", None) or None,
                    end=row.pop("end", None) or None,
                )
            )

    working_groups = defaultdict(list)
    with safe_open_dict_reader(WORKING_GROUPS_PATH) as reader:
        for row in reader:
            key = row.pop("section_key")
            if z := row.pop("charter_zenodo", None):
                zenodo = Zenodo(record=z, language=row.pop("charter_language") or None)
            else:
                zenodo = None
            wikidata = row.pop("wikidata", None) or None
            wg = WorkingGroup(
                label=row.pop("label"),
                key=row.pop("key"),
                wikidata=wikidata,
                zenodo=zenodo,
                mailing_list=row.pop("mailing_list", None) or None,
                start=row.pop("start", None) or None,
                end=row.pop("end", None) or None,
                roles=working_group_roles[wikidata],
            )
            working_groups[key].append(wg)

    section_roles = defaultdict(list)
    with safe_open_dict_reader(SECTIONS_ROLES_PATH) as reader:
        for row in reader:
            section_wikidata = row.pop("section")
            role = Role(
                person=Person(
                    name=row.pop("person_name"),
                    orcid=row.pop("person_orcid", None) or None,
                    email=row.pop("person_email", None) or None,
                ),
                role=row.pop("role"),
                start=row.pop("start", None) or None,
                end=row.pop("start", None) or None,
            )
            section_roles[section_wikidata].append(role)

    def _process_section(d: dict[str, Any]) -> dict[str, Any]:
        if zenodo := d.pop("concept_zenodo", None):
            d["zenodo"] = {
                "record": zenodo,
                "language": d.pop("concept_language", None),
            }
        d["roles"] = section_roles[d["wikidata"]]
        d["working_groups"] = working_groups[d["key"]]
        return d

    sections = read_pydantic_tsv(SECTIONS_PATH, Section, process=_process_section)
    return KnowledgeBase(sections=sections)


def main() -> None:
    kb = get_kb()
    write_pydantic_json(kb, OUTPUT_JSON_PATH, indent=2)


if __name__ == "__main__":
    main()
