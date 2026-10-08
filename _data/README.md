# Data

This folder contains curated information about organizations and their
relationships

## NFDI Parts

- `task_forces.tsv` puts information from
  https://www.nfdi.de/community-meetings/?lang=en on task forces and jours fixes

## Consortium Membership

The `consortium_member_institutions.tsv` connects NFDI consortia to the
institutions that are members, along with a small amount of context. This was
originally seeded from Wikidata with the following query, then extended with
additional curation:

```sparql
SELECT ?consortia ?consortiaLabel ?consortiaROR ?institution ?institutionLabel ?institutionROR ?role ?roleLabel ?start ?end
WHERE
{
  ?consortia wdt:P31 wd:Q98270496 ;
             p:P1416 ?statement .
  ?statement ps:P1416 ?institution .
  OPTIONAL {?statement pq:P580 ?start }
  OPTIONAL {?statement pq:P582 ?end }
  OPTIONAL { ?statement pq:P3831 ?role }
  OPTIONAL { ?institution wdt:P6782 ?institutionROR }
  OPTIONAL { ?consortia wdt:P6782 ?consortiaROR }
  SERVICE wikibase:label {
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en".
  }
}
ORDER BY ?consortiaLabel ?institutionLabel
```

## European Research Infrastructure Consortium (ERIC)

For each ERIC, capture the following:

1. The page listing all the members. For example,
   [DARIAH](https://www.dariah.eu) lists them
   [here](https://www.dariah.eu/network/members-and-partners/).
2. The status of Germany (member, observer, partner, N/A)
3. The mediating institutions and people. For example, DARIAH is a rather large
   ERIC that has a national entity ([DARIAH-DE](https://de.dariah.eu/en/)), a
   representing entity
   ([BMFTR](https://www.bmftr.bund.de/EN/Home/home_node.html)), a national
   coordinating institution
   ([University of Göttingen](https://www.sub.uni-goettingen.de/en/)), and a
   handful of partner institutions

- `erics.tsv` the few dozen ERICs
- `eric_relations` connects the ERICs (or their subdivisions) to organizations
- `eric_hierarchy` connects European-level ERICs to subdivisions, such as DARIAH
  connected to DARIAH-DE
