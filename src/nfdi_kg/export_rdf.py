from collections import Counter
from typing import Annotated, Literal

import bioregistry
import rdflib
import typer
from curies import Reference
from pydantic import AnyHttpUrl, BaseModel, BeforeValidator
from pystow.utils import read_pydantic_tsv
from rdflib import FOAF, ORG, RDF, RDFS, SKOS, XSD, URIRef
from pydantic_extra_types.country import CountryAlpha2
from pystow.utils import tabulate_counter
from nfdi_kg.constants import ERICS_PATH, RDF_PATH, ERICS_RELATIONS_PATH


def with_prefix(prefix: str) -> BeforeValidator:
    def _ll(s: str | Reference | None) -> Reference | None:
        if s is None:
            return None
        elif isinstance(s, str):
            return Reference(prefix=prefix, identifier=s)
        else:
            return s

    return BeforeValidator(_ll)


class ERIC(BaseModel):
    wikidata: Annotated[Reference, with_prefix("wikidata")]
    ror: Annotated[Reference | None, with_prefix("ror")] = None
    abbreviation: str | None = None
    name: str
    website: AnyHttpUrl
    status_reference: AnyHttpUrl | None = None


class ERICRelation(BaseModel):
    eric_wikidata: Annotated[Reference, with_prefix("wikidata")]
    interaction_type: str
    country: CountryAlpha2 | Literal["XK", "International", "EU"]
    wikidata: Annotated[Reference, with_prefix("wikidata")]
    ror: Annotated[Reference, with_prefix("ror")]
    name: str
    subdivision: str | None = None
    abbr: str | None = None
    website: AnyHttpUrl | None = None
    people: str | None = None
    comment: str | None = None


def get_graph() -> rdflib.Graph:
    graph = rdflib.Graph()
    converter = bioregistry.get_default_converter()
    converter.bind_rdflib(graph)

    def add(s, p, o) -> None:
        graph.add((s, p, o))

    def _uri(reference: Reference) -> URIRef:
        return rdflib.URIRef(converter.expand_reference(reference, strict=True))

    models = read_pydantic_tsv(ERICS_PATH, ERIC)
    for model in models:
        node = _uri(model.wikidata)
        add(node, RDF.type, ORG.organization)
        add(node, RDFS.label, rdflib.Literal(model.name))
        add(
            node,
            FOAF.homepage,
            rdflib.Literal(model.website.encoded_string(), datatype=XSD.anyURI),
        )
        if model.ror:
            add(node, SKOS.exactMatch, _uri(model.ror))

    relation_counter = Counter()
    for model2 in read_pydantic_tsv(ERICS_RELATIONS_PATH, ERICRelation, failure_action="skip"):
        match model2.interaction_type:
            case "member":
                p = ORG.hasMember
            case _:
                p = ORG.linkedTo

        s, o = _uri(model2.eric_wikidata), _uri(model2.wikidata)
        add(s, p, o)

        relation_counter[model2.interaction_type] += 1

        if model2.people:
            node = rdflib.BNode()  # a reified node
            add(node, RDF.type, RDF.Statement)
            add(node, RDF.subject, s)
            add(node, RDF.predicate, p)
            add(node, RDF.object, o)

    typer.echo(tabulate_counter(relation_counter))

    return graph


def main() -> None:
    graph = get_graph()
    graph.serialize(RDF_PATH, format="turtle")


if __name__ == "__main__":
    typer.run(main)
