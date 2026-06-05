---
layout: home
title: Curation
permalink: /curation/
---

## Sections

<table>
<thead>
<tr>
<th>Section</th>
<th>Section Concept</th>
<th>Wikidata</th>
<th>Unofficial Docs.</th>
</tr>
</thead>
<tbody>
{% for section in site.data.sections %}
<tr>
<td><a href="{{ section.website }}">{{ section.label }}</a></td>
<td><a href="https://zenodo.org/records/{{ section.concept_zenodo }}">📩</a> ({{ section.concept_language }})</td>
<td><a href="https://wikidata.org/wiki/{{ section.wikidata }}">{{ section.wikidata }}</a></td>
<td><a href="https://nfdi-de.github.io/nfdi-sections/docs/{{ section.key }}/intro">Unofficial Docs.</a></td>
</tr>
{% endfor %}
</tbody>
</table>

## Working Groups

<table>
<thead>
<tr>
<th>Working Group</th>
<th>Charter</th>
<th>Wikidata</th>
</tr>
</thead>
<tbody>
{% for working_group in site.data.section_working_groups %}
<tr>
<td>
<a href="https://nfdi-de.github.io/nfdi-sections/docs/{{ working_group.section_key }}/{{ working_group.key }}">{{ working_group.label }}</a>
({{ working_group.section_key }})
</td>
<td>
{% if working_group.charter_zenodo and working_group.charter_zenodo != "duplicate" %}
<a href="https://zenodo.org/records/{{ working_group.charter_zenodo }}">📩</a> ({{ working_group.charter_language }})
{% endif %}
</td>
<td>
{% if working_group.wikidata %}
<a href="https://wikidata.org/wiki/{{ working_group.wikidata }}">{{ working_group.wikidata }}</a>
{% endif %}
</td>
</tr>
{% endfor %}
</tbody>
</table>

## Working Group External Connections (Curated)

<table>
<thead>
<tr>
<th>Working Group</th>
<th>External</th>
<th>External Wikidata</th>
<th>External Type</th>
</tr>
</thead>
<tbody>
{% for record in site.data.section_working_group_external %}
<tr>
<td>
    {% if record.wikidata %}
    {{ record.wikidata }}
    ({{ record.wg | replace: "wg_", "" | replace: "_", " " }})
    {% else %}
    {{ record.wg | replace: "wg_", "" | replace: "_", " " }}
    {% endif %}
</td>
<td><a href="{{ record.external_link }}">{{ record.external }}{% if record.external_short %} ({{ record.external_short}}){% endif %}</a></td>
<td>{% if record.external_wikidata %}<a href="https://wikidata.org/wiki/{{ record.external_wikidata }}">{{ record.external_wikidata }}</a>{% endif %}</td>
<td>{{ record.external_type }}</td>
</tr>
{% endfor %}
</tbody>
</table>
