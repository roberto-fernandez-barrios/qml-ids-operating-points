# Reproduction guide

[Repository overview](../README.md) · [Output map](ARTIFACT_MAP.md) · [Version policy](VERSION_POLICY.md)

## Choose the object to reproduce

- **Published artifact:** extract `qml_ids_reproduction_v2_2.zip` from [Zenodo](https://doi.org/10.5281/zenodo.23642804) or the [GitHub release](https://github.com/roberto-fernandez-barrios/qml-ids-operating-points/releases/tag/v2.2.0). This is the exact version cited by the manuscript.
- **Current repository:** clone `main` for the same analysis, plus the English guides, previews and CI. Record the commit if citing this evolving documentation.

For a tagged Git checkout:

```bash
git clone https://github.com/roberto-fernandez-barrios/qml-ids-operating-points.git
cd qml-ids-operating-points
git switch --detach v2.2.0
```

The portable release ZIP has SHA-256:

```text
78b2f4f3acc81e3735cc9b02bb47207c7e22e00f153c92f3c105a5adc5142656
```

## Environment and execution

Use Python 3.12 or 3.13 and the versions in [requirements-tested.txt](../requirements-tested.txt). The original local environment is recorded in [VERSIONS.json](VERSIONS.json). The [CI run history](https://github.com/roberto-fernandez-barrios/qml-ids-operating-points/actions/workflows/reproduce.yml) records actual Windows/Linux outcomes, not merely a claim of portability.

```bash
python -m venv .venv
```

Activate in Linux/macOS: `source .venv/bin/activate`. In Windows PowerShell: `.venv\Scripts\Activate.ps1`. If local policy prevents activation, invoke `.venv\Scripts\python.exe` directly; changing the machine's execution policy is unnecessary.

```bash
python -m pip install -r requirements-tested.txt
python -B scripts/verify_package.py
python -B scripts/reproduce.py
```

Run from the extracted/clone root. Paths with spaces are supported. Installation needs network access; the four-stage reconstruction does not. A standard CPU environment is sufficient. The process uses no quantum service, external dataset, API key, detector training or TeX installation. No runtime or memory requirement is inferred from classifier training described in the source articles.

## What each stage does

| Stage | Purpose | Success evidence |
|---|---|---|
| `verify_package.py` | Check included files against relative SHA-256 paths | `results/PACKAGE_INTEGRITY.json`: `PASS` |
| `prepare_analysis.py` | Reconstruct rates, conditional limits, figures and tables | `results/ANALYSIS_V2.json`, `SUMMARY_V2.json`, figures/tables |
| `verify_analysis.py` | Cross-check counts and invert binomial tails independently of the beta-quantile implementation | `results/TECHNICAL_VERIFICATION_V2.json`: `PASS`, `n_checks: 180` |
| `make_browser.py` | Build a local view of derived records and source links | `results/extraction_browser.html` |

`reproduce.py` runs these stages in order and writes `results/ENVIRONMENT.json`. It exits nonzero on failure. No original workspace path is required. Source filenames/hashes identify consulted documents; their intentionally absent copies are not dependencies.

The numerical verifier checks tolerance-based agreement with frozen values, all 24 displayed points, the six conditional points, the K07 ranges and the K11 rounding. It is not independent human extraction or verification of sampling assumptions. PDF metadata and rendering can vary by platform even when reconstructed numerical values agree.

## Current-branch documentation checks

After reproduction on `main`, run:

```bash
python -B tools/verify_repository.py
```

This checks preservation of the archived data/analysis code, relative documentation links, dictionary coverage, citation identifiers and the article-to-artifact map. The CI workflow runs this command after the 180 analysis checks. Its downloadable reports record the environment and outputs; it does not publish a new research release.

## Troubleshooting

| Symptom | Action |
|---|---|
| Import or package-version error | Confirm the intended virtual environment is active; install the pinned requirements there. |
| Integrity failure | Re-extract the untouched archive or inspect deliberate local changes. Do not refresh hashes to hide an unexplained failure. |
| Empty/missing figure folders | Inspect the first failing reconstruction stage. Figures are generated, not bundled in the frozen input ZIP. |
| No window appears | Expected: figures are saved to disk. Open the PNG/PDF or local HTML browser. |
| Source PDF unavailable | Follow the DOI/version locators. This affects source reinspection, not offline numerical reconstruction. |

For an unresolved issue, include the artifact version/commit, operating system, Python/dependency versions, failing command and traceback in the [issue tracker](https://github.com/roberto-fernandez-barrios/qml-ids-operating-points/issues). Do not include credentials or copyrighted source copies.
