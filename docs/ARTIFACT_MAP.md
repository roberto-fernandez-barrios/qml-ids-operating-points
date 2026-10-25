# Article-to-artifact map

[Overview](../README.md) · [Reproduce](REPRODUCIBILITY.md) · [Machine-readable map](artifact_map.json)

This map identifies the evidence and generated outputs behind each article object. Editorial headings/captions can differ from the frozen artifact, and the compact main tables are typeset in the manuscript. It does not claim byte-identical manuscript source generation.

Run `python -B scripts/reproduce.py` to create the relative paths below. Generated outputs are deliberately excluded from the immutable input manifest and Git tracking; the two figure previews in `docs/assets/` are separately preserved copies.

| Article object | Generated paths | Selection/interpretation |
|---|---|---|
| Main figure: all 24 descriptive points | `figures/figure1_operating_points.pdf`<br>`figures/figure1_operating_points.svg`<br>`results/FIGURE_MANIFEST_V2_2.json` | principal; intervals only where main_interval_display is true |
| K17 comparison figure | `figures/figure2_k17_tradeoff.pdf`<br>`figures/figure2_k17_tradeoff.svg` | Figure 7 Test only; no Train or cross-validation substitution |
| Selection and access denominators | `results/SUMMARY_V2.json`<br>`tables/selection.tex` | Article-level inclusion and documentary families; 25/21/20/15 are different denominators |
| Source-object interpretation table | `tables/source_dossiers.tex` | Source registry and study notes support the manually typeset compact table |
| Six-point conditional analysis | `tables/conditional_points.tex`<br>`tables/intervals.tex` | main_interval_display; unverified independence |
| Hypothetical provenance illustrations | `tables/k03_hypothetical.tex`<br>`tables/k11_hypothetical.tex`<br>`tables/hypothetical_intervals.tex` | Test-adjusted or training-described source evidence |
| Supplementary mapping/code sensitivities | `tables/supplementary_counts.tex`<br>`tables/legacy_conditional_points.tex` | Read labels and reconstruction assumptions; legacy table retains original release caption |
| Verification and browseable extraction | `results/TECHNICAL_VERIFICATION_V2.json`<br>`results/ANALYSIS_V2.json`<br>`results/extraction_browser.html` | 180 technical checks; 466 derived records, not independent studies |

## Trace a particular number

1. Find its `Kxx-Pyyy` record in `results/ANALYSIS_V2.json` or the generated HTML browser.
2. Read `dataset`, `detector`, `operating_point` and `fuente_localizacion` together.
3. Join `study` to `data/BASE_ESTUDIOS.json` and `data/SOURCE_REGISTRY.json` for claim, threshold, evaluation design, source version and access.
4. Check counts/denominators and `provenance_en` before interpreting an interval. Missing or rounded cells cannot be replaced by convenient totals.

The schema names `ANALYSIS_V2.json` and `SUMMARY_V2.json` are retained for compatibility. They do not mean that artifact 2.2.0 is a different corpus or an older computation.
