# Pipeline PyRef: refactoring su commit di introduzione/rimozione smell

Questo pacchetto esegue [PyRef](https://github.com/PyRef/PyRef) sui commit di
introduzione e rimozione degli smell nel dataset NICHE, per costruire un csv
con cui correlare refactoring e introduzione/rimozione di smell.

## File

- `setup_pyref.sh` — clona PyRef, installa le dipendenze (pandas compatibile
  con Python 3.9+) e applica una patch necessaria (PyRef usa `DataFrame.append`,
  rimosso in pandas >= 2.0).
- `pyref_pipeline.py` — pipeline principale, **resumable** (salva una cache su
  disco dopo ogni commit processato, quindi puoi interromperla e ripartire).
  Si configura modificando alcune variabili globali in cima al file, non ci
  sono parametri da riga di comando.

## 1. Setup (una tantum)

Requisiti: Python 3.9+, `git` in PATH, connessione internet.

```bash
chmod +x setup_pyref.sh
./setup_pyref.sh
```

Questo crea una cartella `PyRef/` con il tool pronto all'uso. Alla fine dello
script viene eseguito un test su un repo giocattolo (DummyRef): se vedi dei
refactoring stampati (es. `Rename Class`, `Extract Method`, ...) è tutto ok.

## 2. Configurazione

Apri `pyref_pipeline.py` e modifica le variabili in cima al file:

```python
SUBSET = "small"                                   # "small" | "medium" | "large"
INPUT_CSV = "small_intro_removing_output_results.csv"
OUTPUT_CSV = "small_pyref_results.csv"

PYREF_DIR = "PyRef"                # cartella dove si trova PyRef (creata da setup_pyref.sh)
REPOS_DIR = None                   # None = <PYREF_DIR>/Repos
CACHE_DIR = "pyref_cache"          # cartella per i file di cache/resume

FETCH_TIMEOUT = 120                # secondi max per il fetch mirato di un commit
COMMIT_TIMEOUT = 300               # secondi max per l'estrazione refactoring su un commit

RETRY_ERRORS = False               # True = ritenta i commit finiti in error/timeout/fetch_error
```

Colonne richieste nel csv indicato in `INPUT_CSV`: `project_name` (formato
`owner/repo`), `Commit_ID` (commit di introduzione dello smell), `new_commit`
(commit di rimozione dello smell).

## 3. Esecuzione

```bash
python3 pyref_pipeline.py
```

Lo script:
1. per ogni repo unico nel dataset crea un repo git locale "vuoto" in `<PYREF_DIR>/Repos/<repo>` (solo `git init` + remote, senza scaricare nulla)
2. per ogni commit unico (sia di introduzione sia di rimozione) **scarica solo quel commit specifico e il suo genitore** (`git fetch --depth 2 origin <commit>`) — non l'intera storia del repo — poi esegue `PyRef getrefs -c <commit>` e registra i tipi di refactoring rilevati
3. alla fine scrive il csv indicato in `OUTPUT_CSV` con le colonne:
   `repo, smell_name, commitid_introdotto, pyref_refactor_intro, pyref_refactor_intro_count, pyref_refactor_intro_status, commitid_rimosso, pyref_ref_removed, pyref_ref_removed_count, pyref_ref_removed_status`

Questo approccio evita di scaricare l'intera storia dei repo (che per progetti
con migliaia di commit può pesare centinaia di MB): si scaricano solo gli
oggetti git necessari per i due commit richiesti da ogni riga del csv. GitHub
supporta il fetch mirato per SHA anche per repo pubblici, quindi funziona per
la stragrande maggioranza dei progetti del dataset.

`pyref_refactor_intro` / `pyref_ref_removed` contengono i tipi di refactoring
rilevati su quel commit, separati da `;` (stringa vuota se nessuno). Le colonne
`_count` danno direttamente un numero utile per l'analisi di correlazione
(es. correlare `pyref_refactor_intro_count > 0` con l'introduzione dello smell).

Lo `status` può essere:
- `ok` — PyRef ha girato correttamente (0 o più refactoring trovati)
- `nodiff` — nessun file `.py` **modificato** in quel commit (es. il commit
  aggiunge solo file nuovi, è un merge o un commit di root): PyRef non ha nulla
  da confrontare, quindi 0 refactoring per costruzione, non per assenza di dati
- `fetch_error` — non è stato possibile scaricare quel commit specifico da
  GitHub (repo rinominato/privato/cancellato, commit non raggiungibile, problemi di rete)
- `error` / `timeout` — PyRef ha fallito o impiegato troppo tempo su quel commit

## 4. Interrompere e riprendere

La cache è salvata in `pyref_cache/<SUBSET>_cache.json` dopo ogni commit. Se
interrompi lo script con Ctrl+C (o va in errore), rilancialo con lo **stesso
comando** (`python3 pyref_pipeline.py`, stessa configurazione): riprende
esattamente da dove si era fermato, senza rifare il lavoro già svolto. Alla
fine di ogni esecuzione viene comunque (ri)scritto il csv `OUTPUT_CSV` con lo
stato corrente della cache, quindi puoi anche interromperlo e controllare i
risultati parziali (i commit non ancora processati avranno `status = missing`).

## 5. Ripetere per medium e large

Cambia in cima al file `SUBSET`, `INPUT_CSV` e `OUTPUT_CSV`, poi rilancia:

```python
SUBSET = "medium"
INPUT_CSV = "medium_intro_removing_output_results.csv"
OUTPUT_CSV = "medium_pyref_results.csv"
```

```bash
python3 pyref_pipeline.py
```

Ogni subset ha la sua cache separata (`small_cache.json`, `medium_cache.json`,
`large_cache.json`), quindi non si sovrascrivono a vicenda.

## 6. Riprovare i commit falliti

Se alcuni commit sono finiti in `error`, `timeout` o `fetch_error` (es. per
problemi di rete transitori), imposta `RETRY_ERRORS = True` in cima al file e
rilancia: verranno rimossi dalla cache solo quei commit (gli `ok`/`nodiff`
restano intatti) e ricalcolati. Ricordati di rimettere `RETRY_ERRORS = False`
dopo, altrimenti ad ogni esecuzione futura ritenterà sempre gli stessi eventuali
fallimenti persistenti.

## Note sui tempi

- Ogni commit richiede solo un piccolo fetch mirato (in genere pochi KB-MB,
  non l'intero repo), quindi anche progetti con storie molto lunghe restano
  veloci da processare.
- Con centinaia di repo e migliaia di commit unici nei subset medium/large,
  l'esecuzione completa richiede comunque tempo per via del numero di
  richieste di rete e chiamate a PyRef: per questo la pipeline è pensata per
  essere interrotta/ripresa liberamente.
