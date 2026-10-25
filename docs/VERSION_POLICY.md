# Version and preservation policy

[Overview](../README.md) · [Change history](../CHANGELOG.md)

| Object | Identity | Intended use |
|---|---|---|
| Frozen research artifact | Tag `v2.2.0`, DOI [10.5281/zenodo.23642804](https://doi.org/10.5281/zenodo.23642804) | Reproduce and cite the article's numerical analysis |
| Earlier artifact | Tag `v2.1.0`, DOI [10.5281/zenodo.23641767](https://doi.org/10.5281/zenodo.23641767) | Historical traceability |
| Current documentation | `main`, identified by its Git commit | English guides, figure previews, repository checks and contribution instructions |

The `VERSION` and `CITATION.cff` fields identify the research artifact. Updating reader documentation does not create a new artifact version or redefine the object identified by its DOI. If documenting a change on `main`, cite its commit separately.

The analysis is protected by [a frozen baseline](verification/artifact_v2_2.json): all original data files, the five analysis scripts, pinned numerical dependencies and the artifact version are checked against their 2.2.0 hashes. Preview assets are copied from the already generated figures. Current documentation can change without rewriting the scientific sources or figures.

`INPUT_SHA256.json` on `main` covers its own included tracked files, including new documentation. The archived ZIP has a separate, unchanged manifest. A digest proves consistency with a snapshot; it does not independently authenticate a source paper or establish scientific validity.

Scientific corrections would require a separately identified change and, where appropriate, a new research release. Maintainers must never move an existing release tag, overwrite the attached ZIP, or substitute a file behind a published version DOI. This documentation update performs none of those actions.
