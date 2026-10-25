# English data dictionary

[Overview](../README.md) · [Artifact map](ARTIFACT_MAP.md) · [Machine-readable field definitions](data_dictionary.json)

The immutable extraction retains Spanish field names. This guide explains the actual schema without rewriting the data. Join records by `study` → article `id`; use source version and `fuente_localizacion` to identify the underlying object. `null` means unidentified/unavailable under the recorded interpretation, **not zero**. An absent optional field is not equivalent to a measured zero.

`fpr`, `tpr` and their derived intervals are proportions; multiply by 100 for percent. A difference in percentage points is `100 * (rate_A - rate_B)`. The nested `original_metrics` field deliberately retains source representations and can contain percentages or proportions. Never apply a global rescaling or reconstruct counts from its rounded metrics.

For example, K10-P001 has `fp=12`, `n0=6000` and an identified FPR of 0.002. Its `tp` remains null; the conditional TPR relies on the separately documented attack-total/false-negative assumptions. `principal=true` means a point is descriptive in the main figure, not that an interval is justified. Use generated `main_interval_display` for the six-point conditional block.

The 25 article rows and 466 point/summary/configuration rows are different units. Repeated settings within an article do not increase the number of independent studies. See [Interpretation](INTERPRETATION.md) before pooling or comparing records.

## Study records: BASE_ESTUDIOS.json

| Field | Meaning |
|---|---|
| `id` | Stable Kaissar-frame identifier K01–K25. |
| `orden_kaissar` | Position in the selected review frame. |
| `autores` | Author string as recorded during extraction, not the authoritative full citation. |
| `year` | Year as recorded for that source version. |
| `title` | Article title. |
| `doi` | Source DOI. |
| `url` | Source locator URL. |
| `inclusion` | incluir = included; excluir = excluded; pendiente = unresolved eligibility. |
| `razon` | Reason for eligibility disposition, independent of result sign and matrix availability. |
| `acceso` | Access state as recorded; consult the English registry for normalized labels. |
| `fuentes` | Local filenames of consulted source versions, retained as provenance only; not portable dependencies. |
| `localizacion` | Exact source location notes. |
| `afirmacion_autores` | Original authors’ claim as extracted; separate from our reference levels. |
| `objetivo_fpr_numerico_autores` | Whether an explicit numerical FPR target was found in the consulted source portions. |
| `referencias_nuestras` | Analyst-defined FPR references as proportions (0.01, 0.001, 0.0001). |
| `umbral` | Decision-rule/threshold selection information. |
| `diseno` | Evaluation design and provenance notes. |
| `comparacion_qc` | Recoverable quantum–classical comparison and its limits. |
| `notas` | Additional article-level notes. |
| `familia_informe` | Documentary-family key linking related reports; not proof of experimental independence. |
| `calibracion_fpr_sustentada` | Whether supported FPR calibration was established from the consulted evidence. |
| `estado_calibracion` | Textual calibration-evidence status. |
| `registro_piloto` | Link to an original pilot record where applicable; no separate study added. |
| `puntos` | Record IDs assigned to this article, including summary and administrative/configuration rows. |
| `hashes_fuentes` | SHA-256 fingerprints of privately consulted source versions. |
| `fuentes_no_locales` | Additional nonlocal source locators/status records. |

## Point records: PUNTOS_OPERACION.json

| Field | Meaning |
|---|---|
| `id` | Stable record identifier, e.g. K17-P009; not an independent-study count. |
| `study` | Article/frame identifier joining BASE_ESTUDIOS and SOURCE_REGISTRY. |
| `dataset` | Dataset name as recorded from the source; identity/version is not independently authenticated. |
| `detector` | Source detector/configuration label. |
| `operating_point` | Source-specific setting or source-object identity, not necessarily a disclosed numerical threshold. |
| `fuente_localizacion` | Figure, table, section or page identifying the source object. |
| `tipo` | Evidence representation category; see category definitions below. |
| `unidad` | Unit described by the source (e.g. traffic records or nodes), not automatically alerts/incidents. |
| `umbral_remision` | Pointer to article-level threshold/selection notes. |
| `principal` | Membership in the 24-point descriptive figure; does not imply valid sampling inference. |
| `n0` | Benign denominator when identified or explicitly reconstruction-conditioned. |
| `n1` | Attack denominator when identified or explicitly reconstruction-conditioned. |
| `tn` | Benign cases predicted benign. |
| `fp` | Benign cases predicted attack (any attack class). |
| `fn` | Attack cases predicted benign. |
| `tp` | Attack cases predicted attack; absent when not fully allocated. Do not fill from a nominal total. |
| `fpr` | FP/n0, or the identified normalized benign-row error rate; stored as a proportion. |
| `tpr` | Identified or explicitly conditioned aggregate attack detection, stored as a proportion. |
| `conteos_originales` | Whether the source supplies count-based evidence; not an independence flag. |
| `denominador_verificado` | Extraction-level denominator flag; does not certify independent observations or selection. |
| `calibracion_sustentada` | Whether calibration support was established in the consulted material; false is not proof no such method exists elsewhere. |
| `inferencia` | Original extraction note on inferential interpretation; current display tier is added during analysis. |
| `accuracy` | Reported accuracy, stored as a proportion when represented in this field; cannot identify all confusion cells. |
| `f1` | Reported F1, stored as a proportion; class/scope follows source notes. |
| `n_test_total` | Reported total evaluation size or nominal source total; not automatically a benign denominator. |
| `n0_upper` | Upper bound on possible benign sample size from a total; not an observed benign count. |
| `alternate_fpr` | Alternative conditional FPR under a different class mapping/orientation; not a second observation. |
| `alternate_tpr` | Alternative conditional TPR under a different class mapping/orientation. |
| `attack_names` | Attack-class labels corresponding to tpr_by_attack. |
| `tpr_by_attack` | Detection proportions for individual attack classes; unknown weights prevent automatic pooling. |
| `tpr_range` | Identified TPR range over unspecified attack-class weights, prior to extra rounding allowance. |
| `rounding_step` | Displayed normalized-matrix increment in proportion units; no sampling uncertainty implied. |
| `tpr_identificacion` | Conditions required to reconstruct the attack-detection rate. |
| `nominal_size` | Source nominal sample size; not necessarily the evaluated matrix total. |
| `raw_matrix` | Source matrix retaining its recorded class ordering. |
| `raw_matrix_order` | Actual/predicted axes and class-order description for raw_matrix. |
| `label_mapping` | Class-to-benign/attack mapping assumption or source statement. |
| `positive_class` | Source convention for the positive class; do not assume it means attack. |
| `original_metrics` | Metrics preserved in their original source representation. Units may differ (percent/proportion); consult the source before conversion. |
| `f1_by_class` | Source class-specific F1 scores stored as proportions; not a confusion matrix. |
| `pos_val_error` | Positive-class validation error as extracted; interpretation depends on class semantics. |
| `neg_val_error` | Negative-class validation error as extracted; interpretation depends on class semantics. |
| `convergence_epochs` | Reported convergence-epoch summaries by optimizer; not evaluated-case counts. |
| `source_caveat` | Source-specific ambiguity or limitation. |
| `notas` | Additional extraction notes. |

## Derived fields: results/ANALYSIS_V2.json

| Field | Meaning |
|---|---|
| `resolution_fpr` | Empirical count increment 1/n0; not a confidence limit. |
| `fpr_U95_cond` | One-sided 95% Clopper–Pearson upper FPR limit under the specified fixed-detector binomial model. |
| `fpr_ci95_cond` | Two-sided marginal 95% Clopper–Pearson FPR interval; not simultaneous coverage. |
| `tpr_ci95_cond` | Two-sided marginal 95% TPR interval under the same sampling assumptions and any reconstruction conditions. |
| `reference_support_cond` | Comparison of the conditional upper limit with analytical reference levels; not demonstrated population control. |
| `source_training_results` | Source describes the result as training, including K11 and K17 Train objects. |
| `source_test_adjustments` | Source reports adjustments after observing the test, as for K03. |
| `main_interval_display` | Selects exactly six K10/K17 conditional illustrations; independence remains unverified. |
| `provenance_class` | Analysis-level provenance category, kept separate from source representation tipo. |
| `provenance_en` | English explanation of source provenance and interpretation. |
| `interval_status_en` | Whether limits are hypothetical, conditional or unavailable; explicit interpretive status. |
| `fpr_rounding_range` | FPR range assuming rounding to nearest at the displayed precision; not a confidence interval. |
| `tpr_identification_rounding_range` | TPR range incorporating unknown attack weights and the stated rounding assumption. |

## Source registry: SOURCE_REGISTRY.json

| Field | Meaning |
|---|---|
| `id` | Frame/article identifier. |
| `doi` | Source DOI. |
| `url` | Public source URL. |
| `title` | Source article title. |
| `authors_as_recorded` | Historical author string; complete citation is in REFERENCES.tex. |
| `year_as_recorded` | Year associated with the consulted record. |
| `eligibility` | English inclusion/exclusion/unresolved label. |
| `access` | English access classification. |
| `location_and_version` | Exact methodological location and source version. |
| `consulted_source_fingerprints` | Filenames and SHA-256 of consulted copies; not file requirements. |
| `source_copies_in_reproduction_package` | False: original report copies are intentionally excluded. |
| `source_access_note` | How to locate the original source and interpret its fingerprint. |

## Evidence-representation categories

| `tipo` | Meaning |
|---|---|
| `metricas_resumen` | Summary metrics; integer cells need not be identifiable. |
| `conteos` | Count matrix. Completeness does not establish independent evaluation. |
| `conteos_parciales` | Partially allocated matrix; analyze identified rows separately. |
| `conteos_training` | Training-labelled count object. |
| `suplemento_codigo` | Saved code output; correspondence with a published figure may remain unresolved. |
| `matriz_normalizada` | Normalized matrix; counts and class weights may be unavailable. |
| `conteos_mapeo_condicionado` | Count interpretation depends on the class-to-benign/attack mapping. |
| `normalizada_orientacion_ambigua` | Normalized matrix with unresolved axis orientation. |

These categories describe representation, not a universal evidence ranking. The current provenance rule is added by the analysis code. The frozen extraction's original notes are preserved alongside that rule.
