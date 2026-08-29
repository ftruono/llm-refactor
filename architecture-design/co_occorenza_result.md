# Analisi di co-occorrenza degli smell — NICHE (livello commit)

Per ogni commit che introduce smell, si considera l'insieme degli smell distinti introdotti in quel commit. La co-occorrenza tra due smell A e B è misurata come:

- **Co-commit**: numero di commit in cui A e B compaiono entrambi (introdotti insieme)
- **Jaccard**: `co_commits / (commit_con_A + commit_con_B − co_commits)` — quanto le due "popolazioni" di commit si sovrappongono (0 = mai insieme, 1 = sempre insieme)
- **Lift**: `P(A e B insieme) / (P(A) × P(B))` — quanto la co-occorrenza osservata è più/meno frequente di quella attesa per puro caso. **Lift > 1** = i due smell si "attraggono" (compaiono insieme più del previsto); **Lift < 1** = tendono a evitarsi; **Lift ≈ 1** = indipendenti.

> Nota: coppie con conteggio molto basso (1-2 commit) possono avere Jaccard/Lift molto alti o bassi per puro rumore statistico — vanno lette con cautela.

## Diffusione della co-occorrenza

| Subset | Commit introducenti totali | Commit con ≥2 smell diversi introdotti insieme | % |
|---|---:|---:|---:|
| Small | 527 | 63 | 12,0% |
| Medium | 1717 | 218 | 12,7% |
| Large | 2658 | 335 | 12,6% |

Percentuale molto stabile tra i tre subset: circa **1 commit su 8** introduce più di un tipo di smell contemporaneamente.

---

## Capitolo 1 — Small

| Smell A | Smell B | Co-commit | Jaccard | Lift |
|:--------------------------------------------------|:--------------------------------------------------|------------:|----------:|-------:|
| columns_and_datatype_not_explicitly_set | in_place_apis_misused | 31 | 0.088 | 0.87 |
| columns_and_datatype_not_explicitly_set | dataframe_conversion_api_misused | 15 | 0.046 | 1.43 |
| gradients_not_cleared_before_backward_propagation | pytorch_call_method_misused | 9 | 0.057 | 0.75 |
| columns_and_datatype_not_explicitly_set | pytorch_call_method_misused | 6 | 0.014 | 0.09 |
| columns_and_datatype_not_explicitly_set | unnecessary_iteration | 4 | 0.012 | 1.62 |
| columns_and_datatype_not_explicitly_set | gradients_not_cleared_before_backward_propagation | 4 | 0.011 | 0.11 |
| dataframe_conversion_api_misused | gradients_not_cleared_before_backward_propagation | 3 | 0.041 | 1.58 |
| gradients_not_cleared_before_backward_propagation | tensor_array_not_used | 2 | 0.025 | 0.74 |
| dataframe_conversion_api_misused | pytorch_call_method_misused | 2 | 0.016 | 0.58 |
| columns_and_datatype_not_explicitly_set | tensor_array_not_used | 2 | 0.006 | 0.14 |
| dataframe_conversion_api_misused | tensor_array_not_used | 2 | 0.051 | 2.58 |
| Chain_Indexing | merge_api_parameter_not_explicitly_set | 1 | 0.333 | 175.67 |
| gradients_not_cleared_before_backward_propagation | in_place_apis_misused | 1 | 0.009 | 0.15 |
| Chain_Indexing | columns_and_datatype_not_explicitly_set | 1 | 0.003 | 0.54 |
| pytorch_call_method_misused | tensor_array_not_used | 1 | 0.008 | 0.21 |

---

## Capitolo 2 — Medium

| Smell A | Smell B | Co-commit | Jaccard | Lift |
|:--------------------------------------------------|:--------------------------------------------------|------------:|----------:|-------:|
| columns_and_datatype_not_explicitly_set | in_place_apis_misused | 150 | 0.106 | 0.71 |
| columns_and_datatype_not_explicitly_set | dataframe_conversion_api_misused | 28 | 0.022 | 0.79 |
| Chain_Indexing | columns_and_datatype_not_explicitly_set | 15 | 0.012 | 1.19 |
| columns_and_datatype_not_explicitly_set | merge_api_parameter_not_explicitly_set | 15 | 0.012 | 1.26 |
| columns_and_datatype_not_explicitly_set | gradients_not_cleared_before_backward_propagation | 9 | 0.007 | 0.12 |
| columns_and_datatype_not_explicitly_set | tensor_array_not_used | 4 | 0.003 | 0.07 |
| columns_and_datatype_not_explicitly_set | pytorch_call_method_misused | 4 | 0.003 | 0.04 |
| gradients_not_cleared_before_backward_propagation | pytorch_call_method_misused | 4 | 0.018 | 0.54 |
| Chain_Indexing | dataframe_conversion_api_misused | 3 | 0.048 | 6.31 |
| Chain_Indexing | in_place_apis_misused | 2 | 0.007 | 0.71 |
| dataframe_conversion_api_misused | gradients_not_cleared_before_backward_propagation | 2 | 0.014 | 0.71 |
| dataframe_conversion_api_misused | in_place_apis_misused | 2 | 0.006 | 0.25 |
| dataframe_conversion_api_misused | pytorch_call_method_misused | 2 | 0.012 | 0.56 |
| gradients_not_cleared_before_backward_propagation | in_place_apis_misused | 1 | 0.003 | 0.06 |
| in_place_apis_misused | pytorch_call_method_misused | 1 | 0.002 | 0.05 |
| Chain_Indexing | tensor_array_not_used | 1 | 0.011 | 1.36 |
| in_place_apis_misused | tensor_array_not_used | 1 | 0.003 | 0.08 |
| in_place_apis_misused | merge_api_parameter_not_explicitly_set | 1 | 0.003 | 0.38 |

---

## Capitolo 3 — Large

| Smell A | Smell B | Co-commit | Jaccard | Lift |
|:--------------------------------------------------|:--------------------------------------------------|------------:|----------:|-------:|
| columns_and_datatype_not_explicitly_set | in_place_apis_misused | 199 | 0.125 | 0.98 |
| columns_and_datatype_not_explicitly_set | dataframe_conversion_api_misused | 55 | 0.039 | 1.65 |
| Chain_Indexing | columns_and_datatype_not_explicitly_set | 31 | 0.022 | 1.78 |
| columns_and_datatype_not_explicitly_set | tensor_array_not_used | 24 | 0.013 | 0.08 |
| columns_and_datatype_not_explicitly_set | merge_api_parameter_not_explicitly_set | 24 | 0.017 | 1.75 |
| columns_and_datatype_not_explicitly_set | gradients_not_cleared_before_backward_propagation | 21 | 0.013 | 0.14 |
| dataframe_conversion_api_misused | in_place_apis_misused | 18 | 0.042 | 1.97 |
| columns_and_datatype_not_explicitly_set | pytorch_call_method_misused | 16 | 0.009 | 0.10 |
| gradients_not_cleared_before_backward_propagation | pytorch_call_method_misused | 13 | 0.023 | 0.40 |
| in_place_apis_misused | pytorch_call_method_misused | 9 | 0.013 | 0.21 |
| gradients_not_cleared_before_backward_propagation | tensor_array_not_used | 6 | 0.007 | 0.10 |
| dataframe_conversion_api_misused | gradients_not_cleared_before_backward_propagation | 6 | 0.017 | 0.88 |
| Chain_Indexing | dataframe_conversion_api_misused | 5 | 0.055 | 6.39 |
| in_place_apis_misused | tensor_array_not_used | 5 | 0.005 | 0.06 |
| in_place_apis_misused | merge_api_parameter_not_explicitly_set | 4 | 0.010 | 1.06 |
| Chain_Indexing | in_place_apis_misused | 3 | 0.007 | 0.63 |
| dataframe_conversion_api_misused | tensor_array_not_used | 3 | 0.005 | 0.24 |
| gradients_not_cleared_before_backward_propagation | in_place_apis_misused | 3 | 0.004 | 0.07 |
| columns_and_datatype_not_explicitly_set | unnecessary_iteration | 3 | 0.002 | 1.14 |
| pytorch_call_method_misused | tensor_array_not_used | 3 | 0.004 | 0.05 |
| columns_and_datatype_not_explicitly_set | nan_equivalence_comparison_misused | 2 | 0.001 | 1.89 |
| in_place_apis_misused | unnecessary_iteration | 2 | 0.005 | 2.75 |
| dataframe_conversion_api_misused | merge_api_parameter_not_explicitly_set | 1 | 0.011 | 1.62 |
| dataframe_conversion_api_misused | pytorch_call_method_misused | 1 | 0.003 | 0.14 |
| columns_and_datatype_not_explicitly_set | matrix_multiplication_api_misused | 1 | 0.001 | 1.89 |
| gradients_not_cleared_before_backward_propagation | merge_api_parameter_not_explicitly_set | 1 | 0.003 | 0.35 |
| in_place_apis_misused | matrix_multiplication_api_misused | 1 | 0.003 | 6.89 |
| matrix_multiplication_api_misused | tensor_array_not_used | 1 | 0.002 | 4.96 |
| merge_api_parameter_not_explicitly_set | tensor_array_not_used | 1 | 0.002 | 0.19 |
| merge_api_parameter_not_explicitly_set | pytorch_call_method_misused | 1 | 0.003 | 0.34 |
| Chain_Indexing | tensor_array_not_used | 1 | 0.002 | 0.15 |
| Chain_Indexing | nan_equivalence_comparison_misused | 1 | 0.029 | 40.27 |
| dataframe_conversion_api_misused | nan_equivalence_comparison_misused | 1 | 0.016 | 21.10 |
| in_place_apis_misused | nan_equivalence_comparison_misused | 1 | 0.003 | 3.44 |

---

## Sintesi

- La coppia più frequente in **valore assoluto** in tutti e tre i subset è sempre `columns_and_datatype_not_explicitly_set` ↔ `in_place_apis_misused`, ma il Lift resta ≤1 in ognuno (0.87 / 0.71 / 0.98): compaiono spesso insieme solo perché il primo smell è di gran lunga il più comune, non per una vera associazione.
- La coppia con l'associazione statistica più forte e **replicata su più subset** è `Chain_Indexing` ↔ `dataframe_conversion_api_misused`: Lift 6,31 su medium e 6,39 su large (assente/non calcolabile su small per mancanza di co-occorrenze dirette) — smell rari che tendono a comparire in cluster.
- Le coppie con Lift molto estremo ma singolo co-commit (es. Chain_Indexing ↔ nan_equivalence_comparison_misused, Lift 40) sono statisticamente poco robuste (N=1) e vanno considerate solo come spunto, non come pattern consolidato.