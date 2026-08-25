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
<th>Mailing List</th>
<th>Unofficial Docs.</th>
<th>Wikidata</th>
</tr>
</thead>
<tbody>
{% for section in site.data.sections %}
<tr>
<td>
    <a href="{{ section.website }}">{{ section.label }}</a>
</td>
<td align="center">
    <a href="https://zenodo.org/records/{{ section.concept_zenodo }}">📖
    {% if section.concept_language == "en" %}(🇺🇸){% elsif section.concept_language == "de" %}(🇩🇪){% endif %}
    </a>
</td>
<td align="center">
    {% if section.mailing_list %}<a href="mailto:{{ section.mailing_list }}">📧</a>{% endif %}
</td>
<td>
    <a href="https://nfdi-de.github.io/nfdi-sections/docs/{{ section.key }}/intro">Unofficial Docs.</a>
</td>
<td align="center">
    <a href="https://wikidata.org/wiki/{{ section.wikidata }}">{{ section.wikidata }}</a>
</td>
</tr>
{% endfor %}
</tbody>
</table>

## Working Groups

<table>
<thead>
<tr>
<th>Section</th>
<th>Working Group</th>
<th>Charter</th>
<th>Mailing List</th>
<th>Wikidata</th>
</tr>
</thead>
<tbody>
{% for working_group in site.data.working_groups %}
<tr>
<td>{{ working_group.section_key }}</td>
<td>
    <a href="https://nfdi-de.github.io/nfdi-sections/docs/{{ working_group.section_key }}/{{ working_group.key }}">{{ working_group.label }}</a>
</td>
<td align="center">
    {% if working_group.charter_zenodo and working_group.charter_zenodo != "duplicate" %}
    <a href="https://zenodo.org/records/{{ working_group.charter_zenodo }}">📩
    {% if working_group.charter_language == "en" %}(🇺🇸){% elsif working_group.charter_language == "de" %}(🇩🇪){% endif %}
    </a>
    {% endif %}
</td>
<td align="center">
    {% if working_group.mailing_list %}
    <a href="mailto:{{ working_group.mailing_list }}">📧</a>
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
<th>External Locale</th>
</tr>
</thead>
<tbody>
{% for record in site.data.interactions %}
<tr>
<td>
    {% if record.wikidata %}
        <a href="https://wikidata.org/wiki/{{ record.wikidata }}">{{ record.wg }}</a>
    {% else %}
        {{ record.wg }}
    {% endif %}
</td>
<td>
    {% if record.external_link %}
    <a href="{{ record.external_link }}">
        {% if record.external_short %}
        {{ record.external_short}}
        {% else %}{{ record.external_name }}
        {% endif %}
    </a>
    {% else %}
    {% if record.external_short %}
        {{ record.external_short}}
        {% else %}{{ record.external_name }}
        {% endif %}
    {% endif %}
</td>
<td>
    {% if record.external_wikidata %}
        <a href="https://wikidata.org/wiki/{{ record.external_wikidata }}">{{ record.external_wikidata }}</a>
    {% endif %}
</td>
<td>{{ record.external_type }}</td>
<td>{% if record.external_locale %}{{ record.external_locale }}{% endif %}</td>
</tr>
{% endfor %}
</tbody>
</table>
