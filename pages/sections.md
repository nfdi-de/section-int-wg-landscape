---
layout: home
title: Sections
permalink: /sections/
---

## Sections

<table>
<thead>
<tr>
<th>Section</th>
<th>Section Concept</th>
<th>Wikidata</th>
</tr>
</thead>
<tbody>
{% for section in site.data.sections %}
<tr>
<td><a href="https://nfdi-de.github.io/nfdi-sections/docs/{{ section.key }}/intro">{{ section.label }}</a></td>
<td><a href="https://zenodo.org/records/{{ section.concept }}">Download</a> ({{ section.concept_language }})</td>
<td><a href="https://wikidata.org/wiki/{{ section.wikidata }}">{{ section.wikidata }}</a></td>
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
</td>
<td>
{% if working_group.charter %}
<a href="{{ working_group.charter }}">Download</a> ({{ working_group.charter_language }})
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