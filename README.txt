QML-IDS / KAISSAR CORPUS — DERIVED-DATA REPRODUCTION PACKAGE, v2.1.0
Prepared 25 October 2026. Authors and declarations confirmed; no journal submission or acceptance is claimed.

PURPOSE
Reconstruct the published operating points recovered from a closed 25-entry frame.
21 articles are included, representing 20 identified documentary families; substantive
methodological material was consulted for 15. Five articles supply 24 main descriptive
points. Ten points from three articles enter the primary conditional binomial analysis.
This package contains no new training data, predictions or quantum executions.

REQUIREMENTS AND COMMANDS
Python 3.12 or later for the pinned dependencies (tested: Python 3.13.12), numpy,
scipy and matplotlib. Exact tested versions are recorded
in requirements-tested.txt and docs/VERSIONS.json. A TeX installation is NOT needed.
If dependencies are absent, use a separate virtual environment and install them with:
  python -m pip install -r requirements-tested.txt
Installation is a separate, optional network operation. Reconstruction is offline.
From the extracted package root, run:
  python -B scripts/verify_package.py
  python -B scripts/reproduce.py
The second command also performs the first check, regenerates all analysis outputs,
figures and tables, verifies numerical agreement with v1, and builds an HTML browser.
Open results/extraction_browser.html in a browser for the derived records and DOI links.
Outputs: results/ANALYSIS_V2.json, SUMMARY_V2.json, TECHNICAL_VERIFICATION_V2.json,
PACKAGE_INTEGRITY.json, ENVIRONMENT.json, figures/*.pdf and *.png, tables/*.tex.
Generated files are deliberately not the immutable inputs checked by INPUT_SHA256.json.

INTEGRITY AND PORTABILITY
INPUT_SHA256.json covers every included immutable file using relative paths. A missing
or changed included file fails the package check. The original Windows workspace is
not consulted. Primary document copies are intentionally excluded, not missing inputs.
Filenames and source hashes in the registry are provenance records, not dependencies.
The optional audit of original workspace files belongs to the private editorial bundle,
uses a configurable root, and reports NOT_REQUESTED or UNAVAILABLE when appropriate.
It must not label an unavailable path as an altered file.

INTERPRETATION
Counts and rates remain linked to their original detector, subset and operating point.
K10 has an exact benign row; its TPR additionally assumes Table 2/3 correspondence
and exhaustive false negatives. K11 is training-described and receives no main-figure
intervals. K07 has identification/rounding ranges, not invented counts or binomial
intervals. The saved K03 H-QNN output is supplementary because identity with the
published figure is unverified. K17 equal denominators do not establish paired data.
Intervals condition on the specified fixed-detector binomial model. No verified
population guarantee, operational alert reduction, or field-wide frequency is inferred.
1%, 0.1% and 0.01% are analyst-defined scales, not targets imposed on source authors.

FILES AND RIGHTS
data/: derived records, source/version locators, frozen transcription and v1 reference.
scripts/: deterministic reconstruction, checks and browser generation.
docs/: frozen extraction protocol, references, versions and rights/status notes.
No publisher PDF, extracted full text, source figure, journal template or author-review
worksheet is included. New figures are redrawn from the derived numbers and carry
source attribution; they do not reproduce source artwork.
The data schema retains Spanish field names. English interpretation is supplied in
the notes, registry, browser and accompanying article/supplement.
Software is licensed under MIT; derived data and documentation under CC BY 4.0.
See LICENSE, LICENSE-DATA and LICENSING.txt for scope.
Repository: https://github.com/roberto-fernandez-barrios/qml-ids-operating-points
Release tag: v2.1.0
Version archive: https://doi.org/10.5281/zenodo.23641767
CITATION.cff and .zenodo.json contain the author/version metadata. The archive DOI
identifies this software/data artifact, not a published or accepted journal article.

REVIEW STATUS
Technical checks are assistant-assisted arithmetic and consistency checks. The second
transcription is frozen prior work, not a fresh independent human source review.
All authors approved the manuscript. Separate focal source-by-source verification
remains unsigned and is managed in the private author bundle.
No source-access or sampling assumption is established by a successful software run.
