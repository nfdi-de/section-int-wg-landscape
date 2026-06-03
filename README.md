# Section International Engagement Working Group on Landscaping and Outreach

Links:

- [Rolling Agenda](https://docs.google.com/document/d/1kvNkhYTdnMuBjMOZS5RcwXZa1xCi57heHeRf9VbQIbw/edit?usp=sharing)
- [RocketChat](https://go.rocket.chat/invite?host=all-chat.nfdi.de&path=invite%2FsJ8Gdy)
- [Working Group Mailing List](https://lists.nfdi.de/postorius/lists/section-int-wg-landscape.lists.nfdi.de)

## Diagram

```mermaid
---
config:
      theme: redux
---
graph LR
    
    internalPerson[Person] -.-> external
    internalInstitution[Institution] -.->  external
    internalConsortium[NFDI Consortium] -.-> external
    internalSection[NFDI Section] -.-> external
    internalWG[Section Working Group] -.-> external

    subgraph external [External]
        funder[Funder]
        project[Project]
        workingGroup[Working Group]
        organization[Organization]
        externalPerson[Person]
        externalOther[Other Stakeholder]
    end

    subgraph internal [NFDI]
        internalPerson -- member of --> internalInstitution -- member of --> internalConsortium
        internalPerson -- member of --> internalWG -- member of --> internalSection
    end
```

## License

Code in this repository is licensed under MIT.
Data in this repository are licensed under CC0.
