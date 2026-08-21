import enum
from collections import defaultdict
from typing import Annotated, Any, Literal, cast

from pydantic import AnyUrl, BaseModel, EmailStr, Field
from pydantic_extra_types.language_code import LanguageAlpha2
from pystow.utils import read_pydantic_tsv, safe_open_dict_reader, write_pydantic_json
from tqdm import tqdm

from nfdi_kg.constants import DATA

SECTIONS_PATH = DATA.joinpath("sections.tsv")
SECTIONS_ROLES_PATH = DATA.joinpath("section_roles.tsv")
WORKING_GROUPS_PATH = DATA.joinpath("working_groups.tsv")
WORKING_GROUP_ROLES_PATH = DATA.joinpath("working_group_roles.tsv")
INTERACTIONS_PATH = DATA.joinpath("interactions.tsv")
OUTPUT_JSON_PATH = DATA.joinpath("output.json")

type SectionAbbreviation = Literal[
    "meta", "elsa", "industry", "int", "edutrain", "infra"
]


type ExternalType = Literal[
    "project",
    "organization",
    "interest_group",
    "working_group",
    "consortium",
    "data_resource",
    "committee",
    "funding_body",
    "funding_call",
    "task_force",
    "standard",
]


class SourceType(enum.Enum):
    wg_charter = enum.auto()


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
    interactions: Annotated[list[Interaction], Field(default_factory=list)]
    roles: Annotated[list[Role], Field(default_factory=list)]


class Section(BaseModel):
    wikidata: str
    key: SectionAbbreviation
    label: str
    zenodo: Zenodo
    homepage: AnyUrl
    mailing_list: EmailStr
    interactions: Annotated[list[Interaction], Field(default_factory=list)]
    roles: Annotated[list[Role], Field(default_factory=list)]
    working_groups: Annotated[list[WorkingGroup], Field(default_factory=list)]


class Organization(BaseModel):
    type: ExternalType
    label: str
    abbreviation: str | None = None
    wikidata: str | None = None
    homepage: AnyUrl | None = None


type InteractionStatus = Literal["aspirational", "ramp-up", "active", "inactive"]


class Interaction(BaseModel):
    """Describes an interaction."""

    organization: Organization
    status: InteractionStatus | None = None
    comment: str | None = None


class KnowledgeBase(BaseModel):
    sections: list[Section]


def get_kb() -> KnowledgeBase:
    wikidata_to_interactions: defaultdict[str, list[Interaction]] = defaultdict(list)
    with safe_open_dict_reader(INTERACTIONS_PATH) as reader:
        for row in reader:
            org_type = row.pop("external_type") or None
            if not org_type:
                continue
            wikidata_to_interactions[row.pop("wikidata")].append(
                Interaction(
                    organization=Organization(
                        type=cast(ExternalType, org_type.replace(" ", "_")),
                        label=row.pop("external_name"),
                        wikidata=row.pop("external_wikidata", None) or None,
                        abbreviation=row.pop("external_short", None) or None,
                        homepage=row.pop("external_link", None) or None,
                    ),
                    comment=row.pop("comment", None) or None,
                )
            )

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
            label = row.pop("label")
            wikidata = row.pop("wikidata", None) or None
            if not wikidata:
                tqdm.write(f"skipping WG {label}")
                continue
            if z := row.pop("charter_zenodo", None):
                zenodo = Zenodo(record=z, language=row.pop("charter_language") or None)
            else:
                zenodo = None
            wg = WorkingGroup(
                label=label,
                key=row.pop("key"),
                wikidata=wikidata,
                zenodo=zenodo,
                mailing_list=row.pop("mailing_list", None) or None,
                start=row.pop("start", None) or None,
                end=row.pop("end", None) or None,
                roles=working_group_roles[wikidata],
                interactions=wikidata_to_interactions[wikidata],
            )
            working_groups[row["section_key"]].append(wg)

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
        if section_concept_zenodo_record := d.pop("concept_zenodo", None):
            d["zenodo"] = {
                "record": section_concept_zenodo_record,
                "language": d.pop("concept_language", None),
            }
        d["roles"] = section_roles[d["wikidata"]]
        d["working_groups"] = working_groups[d["key"]]
        d["interactions"] = wikidata_to_interactions[d["wikidata"]]
        return d

    sections = read_pydantic_tsv(SECTIONS_PATH, Section, process=_process_section)

    return KnowledgeBase(sections=sections)


def main() -> None:
    kb = get_kb()
    write_pydantic_json(kb, OUTPUT_JSON_PATH, indent=2)


if __name__ == "__main__":
    main()
