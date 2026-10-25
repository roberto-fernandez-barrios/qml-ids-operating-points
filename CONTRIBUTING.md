# Reporting a reproducibility or evidence issue

Thank you for helping make the reconstruction inspectable. Use the [issue tracker](https://github.com/roberto-fernandez-barrios/qml-ids-operating-points/issues) for questions or corrections.

For an evidence correction, give the study/point ID, exact source version and figure/table/page, the recorded value and the proposed correction. Explain whether it changes counts, interpretation or only wording. Link to a lawful public source; do not upload copyrighted full texts or credentials.

For a reproduction issue, give the tag/commit, OS, Python and package versions, command and traceback. Distinguish an unavailable original source from a failure to reproduce the included derived records.

Documentation pull requests are welcome. Keep the frozen corpus and source objects unchanged. The historical protocol and published releases are retained; a scientific correction requires an explicitly scoped analysis change rather than a silent documentation edit.

Maintainers: run the commands in [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md), stage intentional files, then run `python -B tools/update_manifest.py` and stage the resulting manifest. Inspect the diff before committing. A regenerated hash is not a substitute for investigating an unexplained mismatch. CI must retain the archive-preservation checks.

Contributed code follows MIT; contributed documentation follows CC BY 4.0, as described in [LICENSING.txt](LICENSING.txt). No new author attribution or scientific contribution is inferred merely from opening an issue.
