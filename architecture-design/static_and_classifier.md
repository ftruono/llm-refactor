# Analisi smell-introducing / removing commit — NICHE

Analisi del rapporto tra commit che introducono uno smell e commit che lo rimuovono, suddivisa per tipologia di smell e per tipologia di commit introducente (`first_commit_goal`: new_feature, bug_fixing, enhancement, refactoring, other).

> **Nota metodologica**: nei file sorgente non esiste una classificazione dedicata al commit di *rimozione*; l'unica dimensione di "tipologia" disponibile è quella del commit che ha **introdotto** lo smell. È questa la dimensione usata di seguito per la suddivisione per "tipologia di refactoring/commit".

---

## Capitolo 1 — NICHE Small

File usati: `NICHE_small_sampled_id_date_filtered_introducingv2.csv` (introduzioni), `small_intro_removing_output_results.csv` (match introduzione↔rimozione).

### 1.1 Ratio complessivo

| Metrica | Valore |
|---|---|
| Introdotti | 1226 |
| Rimossi (occorrenze uniche con match) | 297 |
| **Ratio di rimozione** | **24,2%** |
| Progetti con introduzioni | 79 |
| Progetti con almeno una rimozione | 52 |

### 1.2 Per tipologia di smell

| Smell | Introdotti | Rimossi | Ratio |
|---|---:|---:|---:|
| columns_and_datatype_not_explicitly_set | 657 | 165 | 25,1% |
| pytorch_call_method_misused | 192 | 52 | 27,1% |
| in_place_apis_misused | 141 | 50 | 35,5% |
| gradients_not_cleared_before_backward_propagation | 126 | 16 | 12,7% |
| dataframe_conversion_api_misused | 50 | 0 | 0% |
| tensor_array_not_used | 38 | 13 | 34,2% |
| Chain_Indexing | 13 | 1 | 7,7% |
| unnecessary_iteration | 8 | 0 | 0% |
| merge_api_parameter_not_explicitly_set | 1 | 0 | 0% |

**Evidenze**: `in_place_apis_misused` e `tensor_array_not_used` hanno il tasso di rimozione più alto; `dataframe_conversion_api_misused` (50 casi) non viene mai rimosso nel campione small (attenzione: N basso, smentito su medium — vedi Cap. 2).

### 1.3 Per tipologia di commit introducente

| Tipologia | Introdotti | Rimossi | Ratio |
|---|---:|---:|---:|
| new_feature | 315 | 86 | 27,3% |
| bug_fixing | 120 | 30 | 25,0% |
| other | 274 | 67 | 24,5% |
| enhancement | 390 | 90 | 23,1% |
| refactoring | 127 | 24 | 18,9% |

**Evidenza**: gli smell introdotti da commit di **refactoring** hanno il ratio di rimozione più basso — segnale da verificare su campione più ampio (N=127 non enorme).

### 1.4 Tipo di operazione di rimozione (`new_change_type`)

| Operazione | Occorrenze |
|---|---:|
| MODIFY | 194 |
| RENAME | 100 |
| DELETE | 2 |
| UNKNOWN | 1 |

### 1.5 Incrocio smell × tipologia commit — Introdotti

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| columns_and_datatype_not_explicitly_set | 196 | 82 | 196 | 61 | 122 |
| in_place_apis_misused | 42 | 13 | 44 | 19 | 23 |
| pytorch_call_method_misused | 47 | 15 | 60 | 22 | 48 |
| gradients_not_cleared_before_backward_propagation | 21 | 8 | 60 | 3 | 34 |
| tensor_array_not_used | 8 | 2 | 21 | 3 | 4 |
| dataframe_conversion_api_misused | 0 | 0 | 5 | 19 | 26 |
| Chain_Indexing | 1 | 0 | 3 | 0 | 9 |
| unnecessary_iteration | 0 | 0 | 1 | 0 | 7 |
| merge_api_parameter_not_explicitly_set | 0 | 0 | 0 | 0 | 1 |

### 1.6 Incrocio smell × tipologia commit — Rimossi

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| columns_and_datatype_not_explicitly_set | 53 | 20 | 43 | 17 | 32 |
| in_place_apis_misused | 12 | 8 | 12 | 3 | 15 |
| pytorch_call_method_misused | 14 | 2 | 12 | 4 | 20 |
| gradients_not_cleared_before_backward_propagation | 4 | 0 | 6 | 3 | 3 |
| tensor_array_not_used | 3 | 0 | 6 | 1 | 3 |
| dataframe_conversion_api_misused | 0 | 0 | 0 | 0 | 0 |
| Chain_Indexing | 0 | 0 | 0 | 0 | 1 |
| unnecessary_iteration | 0 | 0 | 0 | 0 | 0 |
| merge_api_parameter_not_explicitly_set | 0 | 0 | 0 | 0 | 0 |

*(Nota: `gradients_not_cleared...` introdotto da refactoring ha ratio 100% ma su soli 3 casi → non affidabile.)*

---

## Capitolo 2 — NICHE Medium

File usati: `NICHE_medium_sampled_id_date_filtered_introducingv2.csv` (introduzioni), `medium_intro_removing_output_results.csv` (match introduzione↔rimozione).

### 2.1 Ratio complessivo

| Metrica | Valore |
|---|---|
| Introdotti | 4882 |
| Rimossi (occorrenze uniche con match) | 1327 |
| **Ratio di rimozione** | **27,2%** |
| Progetti con introduzioni | 105 |
| Progetti con almeno una rimozione | 74 |

### 2.2 Per tipologia di smell

| Smell | Introdotti | Rimossi | Ratio |
|---|---:|---:|---:|
| in_place_apis_misused | 591 | 245 | 41,5% |
| gradients_not_cleared_before_backward_propagation | 179 | 51 | 28,5% |
| tensor_array_not_used | 169 | 43 | 25,4% |
| columns_and_datatype_not_explicitly_set | 3447 | 899 | 26,1% |
| merge_api_parameter_not_explicitly_set | 17 | 4 | 23,5% |
| pytorch_call_method_misused | 339 | 66 | 19,5% |
| dataframe_conversion_api_misused | 73 | 14 | 19,2% |
| Chain_Indexing | 64 | 3 | 4,7% |
| memory_not_freed | 3 | 2 | 66,7% (N troppo piccolo) |

**Evidenze**: `Chain_Indexing` si conferma lo smell meno rimosso in assoluto (coerente con small). `dataframe_conversion_api_misused` qui viene rimosso in 19,2% dei casi — smentisce il "mai rimosso" osservato su small, che era quindi un artefatto di campione piccolo.

### 2.3 Per tipologia di commit introducente

| Tipologia | Introdotti | Rimossi | Ratio |
|---|---:|---:|---:|
| other | 1169 | 404 | 34,6% |
| new_feature | 1473 | 394 | 26,7% |
| refactoring | 696 | 183 | 26,3% |
| enhancement | 1038 | 233 | 22,4% |
| bug_fixing | 506 | 113 | 22,3% |

**Evidenza chiave**: il pattern "refactoring = ratio di rimozione più basso" osservato su small **non si conferma** su medium — qui il refactoring (26,3%) è in linea con new_feature, mentre sono enhancement e bug_fixing ad avere il ratio più basso. Il segnale di small era probabilmente rumore statistico (N=127).

### 2.4 Tipo di operazione di rimozione (`new_change_type`)

| Operazione | Occorrenze |
|---|---:|
| MODIFY | 866 |
| RENAME | 440 |
| DELETE | 11 |
| UNKNOWN | 10 |

Stesso pattern di small: la rimozione avviene per lo più via modifica diretta (~2/3), il resto via rinomina.

### 2.5 Incrocio smell × tipologia commit — Introdotti

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| columns_and_datatype_not_explicitly_set | 992 | 346 | 746 | 547 | 816 |
| in_place_apis_misused | 177 | 72 | 90 | 53 | 199 |
| pytorch_call_method_misused | 134 | 47 | 85 | 22 | 51 |
| gradients_not_cleared_before_backward_propagation | 70 | 14 | 44 | 22 | 29 |
| tensor_array_not_used | 40 | 6 | 50 | 36 | 37 |
| dataframe_conversion_api_misused | 29 | 3 | 12 | 9 | 20 |
| Chain_Indexing | 23 | 18 | 8 | 6 | 9 |
| merge_api_parameter_not_explicitly_set | 7 | 0 | 1 | 1 | 8 |
| memory_not_freed | 1 | 0 | 2 | 0 | 0 |

### 2.6 Incrocio smell × tipologia commit — Rimossi

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| columns_and_datatype_not_explicitly_set | 273 | 73 | 150 | 129 | 274 |
| in_place_apis_misused | 49 | 30 | 34 | 25 | 107 |
| pytorch_call_method_misused | 30 | 3 | 16 | 8 | 9 |
| gradients_not_cleared_before_backward_propagation | 22 | 5 | 13 | 6 | 5 |
| tensor_array_not_used | 12 | 0 | 15 | 10 | 6 |
| dataframe_conversion_api_misused | 2 | 1 | 3 | 5 | 3 |
| Chain_Indexing | 2 | 1 | 0 | 0 | 0 |
| merge_api_parameter_not_explicitly_set | 3 | 0 | 1 | 0 | 0 |
| memory_not_freed | 1 | 0 | 1 | 0 | 0 |

### 2.7 Incrocio smell × tipologia commit — Ratio

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| columns_and_datatype_not_explicitly_set | 27,5% | 21,1% | 20,1% | 23,6% | 33,6% |
| in_place_apis_misused | 27,7% | 41,7% | 37,8% | 47,2% | 53,8% |
| pytorch_call_method_misused | 22,4% | 6,4% | 18,8% | 36,4% | 17,6% |
| gradients_not_cleared_before_backward_propagation | 31,4% | 35,7% | 29,5% | 27,3% | 17,2% |
| tensor_array_not_used | 30,0% | 0% | 30,0% | 27,8% | 16,2% |
| dataframe_conversion_api_misused | 6,9% | 33,3% | 25,0% | 55,6% | 15,0% |
| Chain_Indexing | 8,7% | 5,6% | 0% | 0% | 0% |
| merge_api_parameter_not_explicitly_set | 42,9% | — | 100% | 0% | 0% |
| memory_not_freed | 100% | — | 50% | — | — |

**Evidenza notevole**: `in_place_apis_misused` introdotto da commit di **refactoring** o "other" viene rimosso molto più spesso (47,2% e 53,8%) — qui il refactoring aiuta a ripulire lo smell, contrariamente all'impressione data dal dato aggregato su small.

---

## Capitolo 3 — NICHE Large

File usati: `NICHE_large_sampled_id_date_filtered_introducingv-p1/p2/p3.csv` (introduzioni, uniti in un unico dataset), `large_intro_removing_output_results.csv` (match introduzione↔rimozione).

> **Nota tecnica**: i tre file di introduzione contengono alcuni campi testuali (commit message / lista file modificati) con virgolette non correttamente escapate, che mandano in errore il parser CSV standard. Sono stati letti con un parser tollerante che scarta solo le righe realmente malformate (1 riga su 5355 nel file p1); dopo l'unione dei tre file sono state rimosse 293 righe duplicate esatte (probabile overlap ai bordi dello split in 3 parti). Il totale netto di introduzioni uniche usato per l'analisi è **11.518** (su 11.666 righe grezze).

### 3.1 Ratio complessivo

| Metrica | Valore |
|---|---|
| Introdotti (unici) | 11.518 |
| Rimossi (occorrenze uniche con match) | 2.793 |
| **Ratio di rimozione** | **24,3%** |
| Progetti con introduzioni | 125 |
| Progetti con almeno una rimozione | 105 |

### 3.2 Per tipologia di smell

| Smell | Introdotti | Rimossi | Ratio |
|---|---:|---:|---:|
| tensor_array_not_used | 5648 | 1116 | 19,8% |
| columns_and_datatype_not_explicitly_set | 3302 | 970 | 29,4% |
| in_place_apis_misused | 841 | 259 | 30,8% |
| gradients_not_cleared_before_backward_propagation | 732 | 153 | 20,9% |
| pytorch_call_method_misused | 698 | 263 | **37,7%** |
| dataframe_conversion_api_misused | 134 | 8 | 6,0% |
| merge_api_parameter_not_explicitly_set | 68 | 3 | 4,4% |
| Chain_Indexing | 63 | 14 | 22,2% |
| memory_not_freed | 20 | 5 | 25,0% |
| unnecessary_iteration | 8 | 1 | 12,5% |
| nan_equivalence_comparison_misused | 2 | 1 | 50% (N troppo piccolo) |
| matrix_multiplication_api_misused | 2 | 0 | 0% (N troppo piccolo) |

**Evidenze**: la composizione degli smell è molto diversa da small/medium — qui `tensor_array_not_used` è di gran lunga il più numeroso (in small/medium era minoritario), segno che il campione large include progetti/pattern di codice differenti. `Chain_Indexing` **non si conferma** più come lo smell meno rimosso (qui è a metà classifica, 22,2%); i ratio più bassi passano a `merge_api_parameter_not_explicitly_set` (4,4%) e `dataframe_conversion_api_misused` (6,0%) — quest'ultimo conferma comunque la tendenza a persistere già vista su small/medium, seppur con ratio diverso da zero.

### 3.3 Per tipologia di commit introducente

| Tipologia | Introdotti | Rimossi | Ratio |
|---|---:|---:|---:|
| enhancement | 2487 | 689 | **27,7%** |
| refactoring | 1586 | 415 | 26,2% |
| new_feature | 4594 | 1088 | 23,7% |
| other | 1804 | 397 | 22,0% |
| bug_fixing | 1047 | 204 | 19,5% |

**Evidenza**: su large il refactoring (26,2%) è la seconda tipologia per ratio di rimozione, non più l'ultima come su small né a metà come su medium. È **bug_fixing** ad avere il ratio più basso qui. Questo conferma ulteriormente che il pattern "refactoring = ratio più basso" di small era un artefatto statistico: su campioni più ampi (medium e large) il refactoring si comporta in modo simile o meglio delle altre tipologie.

### 3.4 Tipo di operazione di rimozione (`new_change_type`)

| Operazione | Occorrenze |
|---|---:|
| MODIFY | 1647 |
| RENAME | 1127 |
| DELETE | 15 |
| UNKNOWN | 4 |

Pattern coerente con small e medium: prevale la modifica diretta, ma qui la quota di RENAME (~40%) è leggermente più alta rispetto a small/medium (~30-34%).

### 3.5 Incrocio smell × tipologia commit — Introdotti

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| tensor_array_not_used | 2423 | 510 | 1535 | 789 | 391 |
| columns_and_datatype_not_explicitly_set | 1213 | 285 | 537 | 447 | 820 |
| in_place_apis_misused | 363 | 100 | 135 | 120 | 123 |
| gradients_not_cleared_before_backward_propagation | 279 | 64 | 130 | 115 | 144 |
| pytorch_call_method_misused | 224 | 79 | 105 | 77 | 213 |
| dataframe_conversion_api_misused | 39 | 2 | 27 | 16 | 50 |
| merge_api_parameter_not_explicitly_set | 19 | 2 | 3 | 6 | 38 |
| Chain_Indexing | 16 | 3 | 8 | 15 | 21 |
| memory_not_freed | 15 | 0 | 2 | 1 | 2 |
| unnecessary_iteration | 0 | 2 | 4 | 0 | 2 |
| nan_equivalence_comparison_misused | 1 | 0 | 1 | 0 | 0 |
| matrix_multiplication_api_misused | 2 | 0 | 0 | 0 | 0 |

### 3.6 Incrocio smell × tipologia commit — Rimossi

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| tensor_array_not_used | 419 | 51 | 389 | 180 | 77 |
| columns_and_datatype_not_explicitly_set | 367 | 83 | 179 | 142 | 199 |
| in_place_apis_misused | 104 | 36 | 44 | 37 | 38 |
| gradients_not_cleared_before_backward_propagation | 71 | 15 | 26 | 19 | 22 |
| pytorch_call_method_misused | 119 | 18 | 44 | 32 | 50 |
| dataframe_conversion_api_misused | 1 | 0 | 3 | 1 | 3 |
| merge_api_parameter_not_explicitly_set | 1 | 0 | 0 | 1 | 1 |
| Chain_Indexing | 5 | 1 | 2 | 2 | 4 |
| memory_not_freed | 0 | 0 | 2 | 1 | 2 |
| unnecessary_iteration | 0 | 0 | 0 | 0 | 1 |
| nan_equivalence_comparison_misused | 1 | 0 | 0 | 0 | 0 |
| matrix_multiplication_api_misused | 0 | 0 | 0 | 0 | 0 |

### 3.7 Incrocio smell × tipologia commit — Ratio

| Smell | new_feature | bug_fixing | enhancement | refactoring | other |
|---|---:|---:|---:|---:|---:|
| tensor_array_not_used | 17,3% | 10,0% | 25,3% | 22,8% | 19,7% |
| columns_and_datatype_not_explicitly_set | 30,3% | 29,1% | 33,3% | 31,8% | 24,3% |
| in_place_apis_misused | 28,7% | 36,0% | 32,6% | 30,8% | 30,9% |
| gradients_not_cleared_before_backward_propagation | 25,4% | 23,4% | 20,0% | 16,5% | 15,3% |
| pytorch_call_method_misused | **53,1%** | 22,8% | 41,9% | 41,6% | 23,5% |
| dataframe_conversion_api_misused | 2,6% | 0% | 11,1% | 6,2% | 6,0% |
| merge_api_parameter_not_explicitly_set | 5,3% | 0% | 0% | 16,7% | 2,6% |
| Chain_Indexing | 31,2% | 33,3% | 25,0% | 13,3% | 19,0% |
| memory_not_freed | 0% | — | 100% | 100% | 100% |
| unnecessary_iteration | — | 0% | 0% | — | 50% |
| nan_equivalence_comparison_misused | 100% | — | 0% | — | — |

**Evidenza notevole**: `pytorch_call_method_misused` introdotto da commit **new_feature** viene rimosso oltre la metà delle volte (53,1%) — nettamente sopra la media generale dello smell (37,7%); introdotto da bug_fixing o "other" invece resta più a lungo (~23%). `tensor_array_not_used`, lo smell più numeroso qui, ha ratio più basso proprio quando introdotto da bug_fixing (10%) — coerente con l'idea che le correzioni "veloci" tendano a introdurre smell più duraturi.

---

## Confronto rapido Small vs Medium vs Large

| Metrica | Small | Medium | Large |
|---|---|---|---|
| Introdotti (unici) | 1226 | 4882 | 11.518 |
| Rimossi (unici) | 297 | 1327 | 2793 |
| Ratio complessivo | 24,2% | 27,2% | 24,3% |
| Smell più numeroso | columns_and_datatype (53,6%) | columns_and_datatype (70,6%) | tensor_array_not_used (49,0%) |
| Smell meno rimosso (N robusto) | Chain_Indexing (7,7%) | Chain_Indexing (4,7%) | merge_api_parameter (4,4%) / dataframe_conversion (6,0%) |
| Smell più rimosso (N robusto) | in_place_apis_misused (35,5%) | in_place_apis_misused (41,5%) | pytorch_call_method_misused (37,7%) |
| Tipologia commit con ratio più basso | refactoring (18,9%) | bug_fixing/enhancement (~22-23%) | bug_fixing (19,5%) |
| Tipologia commit con ratio più alto | new_feature (27,3%) | other (34,6%) | enhancement (27,7%) |

**Considerazioni finali**:
- Il **ratio di rimozione complessivo è sorprendentemente stabile** (~24-27%) attraverso i tre campioni, nonostante dimensioni molto diverse — è probabilmente il pattern più affidabile trovato finora.
- La **composizione degli smell cambia radicalmente** tra i campioni (in small/medium domina `columns_and_datatype_not_explicitly_set`, in large domina `tensor_array_not_used`): questo indica che i tre sottoinsiemi (small/medium/large) non sono semplicemente "più progetti dello stesso tipo" ma hanno probabilmente caratteristiche di codebase diverse (dimensione dei progetti, dominio applicativo, ecc.) — varrebbe la pena capire se il campionamento a monte segue una logica di stratificazione per dimensione progetto.
- L'ipotesi iniziale "il refactoring rimuove meno smell" (emersa solo su small) **non è mai confermata su medium o large**: su bug_fixing e enhancement si osservano invece i ratio più bassi in modo più consistente. Direi che questa pista va abbandonata a favore di un focus su bug_fixing come possibile "tipologia a rischio persistenza smell".
- Bordo interessante da approfondire: `pytorch_call_method_misused` su large ha un salto di ratio molto marcato tra new_feature (53%) e bug_fixing/other (~23%) — se questo pattern si ripete anche isolando gli altri smell principali, potrebbe essere il segnale più solido di tutta l'analisi.