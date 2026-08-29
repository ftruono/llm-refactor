"""
NICHE dataset

  1. Ratio di rimozione complessivo (occorrenze rimosse / introdotte)
  2. Suddivisione per tipologia di smell
  3. Suddivisione per tipologia di commit introducente (first_commit_goal)
  4. Incrocio smell x tipologia di commit (introdotti / rimossi / ratio)
  5. Tipo di operazione con cui avviene la rimozione (new_change_type)
  6. Arricchimento con i metadati di progetto in NICHE.csv (repo list):
     copertura dei progetti e ratio di rimozione per fascia
     "Engineered ML Project" (Y/N)
"""

import csv
import os
from dataclasses import dataclass, field

import pandas as pd

# ---------------------------------------------------------------------------
# COSTANTI
# ---------------------------------------------------------------------------

# Cartella dove risiedono i file del dataset NICHE (introducing / removing)
DATA_DIR = "resources/"


#REPO_DATA_DIR = "/mnt/user-data/uploads"
NICHE_REPO_FILE = os.path.join(DATA_DIR, "NICHE.csv")

# Colonna chiave usata per deduplicare le occorrenze di smell
KEY_COLUMNS = ["project_name", "filename", "smell_name", "occurrence_id", "line"]

# Ordine standard delle tipologie di commit introducente
GOAL_ORDER = ["new_feature", "bug_fixing", "enhancement", "refactoring", "other"]

# Limite dimensione campo per il parser CSV "robusto" (necessario per i file
# large, che hanno campi commit_message / modified_files molto grandi)
CSV_FIELD_SIZE_LIMIT = 10 ** 9

SUBSETS = {
    "small": {
        "introducing_files": [
            os.path.join(DATA_DIR, "NICHE_small_sampled_id_date_filtered_introducingv2.csv"),
        ],
        "merged_file": os.path.join(DATA_DIR, "small_intro_removing_output_results.csv"),
    },
    "medium": {
        "introducing_files": [
            os.path.join(DATA_DIR, "NICHE_medium_sampled_id_date_filtered_introducingv2.csv"),
        ],
        "merged_file": os.path.join(DATA_DIR, "medium_intro_removing_output_results.csv"),
    },
    "large": {
        "introducing_files": [
            os.path.join(DATA_DIR, "NICHE_large_sampled_id_date_filtered_introducingv2.csv"),
        ],
        "merged_file": os.path.join(DATA_DIR, "large_intro_removing_output_results.csv"),
    },
}


# ---------------------------------------------------------------------------
# LETTURA ROBUSTA DEI CSV
# ---------------------------------------------------------------------------

def robust_read_csv(path: str) -> pd.DataFrame:
    """Legge un CSV usando il modulo csv (non il parser C di pandas).

    Alcuni file del dataset (in particolare i file "large") contengono
    virgolette non correttamente escapate all'interno dei campi di testo
    libero (commit_message, modified_files). Il parser C di pandas si
    blocca con un errore fatale su tutto il file; il modulo csv, invece,
    permette di scartare solo le singole righe malformate.
    """
    csv.field_size_limit(CSV_FIELD_SIZE_LIMIT)
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        skipped = 0
        for row in reader:
            if len(row) != len(header):
                skipped += 1
                continue
            rows.append(row)
    if skipped:
        print(f"    [!] {os.path.basename(path)}: {skipped} righe malformate scartate")
    return pd.DataFrame(rows, columns=header)


def load_introducing(paths: list) -> pd.DataFrame:
    """Carica (ed eventualmente concatena) i file di introduzione, poi
    deduplica sia le righe identiche sia le occorrenze duplicate sulla
    chiave logica dello smell."""
    frames = [robust_read_csv(p) for p in paths]
    df = pd.concat(frames, ignore_index=True) if len(frames) > 1 else frames[0]

    n_raw = len(df)
    df = df.drop_duplicates()  # righe interamente identiche (overlap tra split)
    n_dedup_rows = len(df)
    df = df.drop_duplicates(subset=KEY_COLUMNS)  # occorrenze uniche
    n_unique = len(df)

    if n_raw != n_dedup_rows or n_dedup_rows != n_unique:
        print(
            f"    righe grezze: {n_raw} -> dopo rimozione duplicati esatti: "
            f"{n_dedup_rows} -> occorrenze uniche: {n_unique}"
        )
    return df


def load_merged(path: str) -> pd.DataFrame:
    """Carica il file introduzione<->rimozione e deduplica sulla chiave
    logica dell'occorrenza introdotta (una occorrenza puo' comparire piu'
    volte se e' stata "ri-matchata" su piu' release)."""
    df = robust_read_csv(path)
    return df.drop_duplicates(subset=KEY_COLUMNS)


# ---------------------------------------------------------------------------
# CALCOLI
# ---------------------------------------------------------------------------

@dataclass
class SubsetResult:
    name: str
    intro: pd.DataFrame
    removed: pd.DataFrame
    overall_ratio: dict = field(default_factory=dict)
    by_smell: pd.DataFrame = None
    by_goal: pd.DataFrame = None
    cross_intro: pd.DataFrame = None
    cross_removed: pd.DataFrame = None
    cross_ratio: pd.DataFrame = None
    removal_type_counts: pd.Series = None


def compute_overall_ratio(intro: pd.DataFrame, removed: pd.DataFrame) -> dict:
    n_intro = len(intro)
    n_removed = len(removed)
    return {
        "introdotti": n_intro,
        "rimossi": n_removed,
        "ratio": round(n_removed / n_intro, 4) if n_intro else float("nan"),
        "progetti_intro": intro["project_name"].nunique(),
        "progetti_rimossi": removed["project_name"].nunique(),
    }


def compute_breakdown(intro: pd.DataFrame, removed: pd.DataFrame, by: str) -> pd.DataFrame:
    intro_counts = intro[by].value_counts()
    removed_counts = removed[by].value_counts()
    tab = pd.DataFrame({"introdotti": intro_counts, "rimossi": removed_counts}).fillna(0)
    tab["rimossi"] = tab["rimossi"].astype(int)
    tab["ratio"] = (tab["rimossi"] / tab["introdotti"]).round(4)
    return tab.sort_values("introdotti", ascending=False)


def compute_cross(intro: pd.DataFrame, removed: pd.DataFrame):
    cross_intro = pd.crosstab(intro["smell_name"], intro["first_commit_goal"])
    cross_intro = cross_intro.reindex(columns=GOAL_ORDER, fill_value=0)

    cross_removed = pd.crosstab(removed["smell_name"], removed["first_commit_goal"])
    cross_removed = cross_removed.reindex(columns=GOAL_ORDER, fill_value=0)
    cross_removed = cross_removed.reindex(index=cross_intro.index, fill_value=0)

    cross_ratio = (cross_removed / cross_intro).round(4)
    return cross_intro, cross_removed, cross_ratio


def analyze_subset(name: str, config: dict) -> SubsetResult:
    print(f"\n[{name.upper()}] caricamento file introduzione...")
    intro = load_introducing(config["introducing_files"])

    print(f"[{name.upper()}] caricamento file introduzione<->rimozione...")
    removed = load_merged(config["merged_file"])

    result = SubsetResult(name=name, intro=intro, removed=removed)
    result.overall_ratio = compute_overall_ratio(intro, removed)
    result.by_smell = compute_breakdown(intro, removed, "smell_name")
    result.by_goal = compute_breakdown(intro, removed, "first_commit_goal")
    result.cross_intro, result.cross_removed, result.cross_ratio = compute_cross(intro, removed)
    result.removal_type_counts = removed["new_change_type"].value_counts()
    return result


def enrich_with_repo_metadata(result: SubsetResult, niche_repos: pd.DataFrame) -> pd.DataFrame:
    """Arricchisce l'analisi con i metadati di progetto (NICHE.csv):
    copertura dei progetti e ratio di rimozione per fascia
    'Engineered ML Project' (Y/N)."""
    projects = pd.DataFrame({"project_name": result.intro["project_name"].unique()})
    merged_meta = projects.merge(
        niche_repos, left_on="project_name", right_on="GitHub_Repo", how="left"
    )
    n_matched = merged_meta["GitHub_Repo"].notna().sum()
    n_total = len(merged_meta)

    intro_flag = result.intro.merge(
        niche_repos[["GitHub_Repo", "Engineered ML Project"]],
        left_on="project_name", right_on="GitHub_Repo", how="left",
    )
    removed_flag = result.removed.merge(
        niche_repos[["GitHub_Repo", "Engineered ML Project"]],
        left_on="project_name", right_on="GitHub_Repo", how="left",
    )
    breakdown = compute_breakdown(intro_flag, removed_flag, "Engineered ML Project")

    print(f"    progetti coperti da NICHE.csv: {n_matched}/{n_total}")
    return breakdown


# ---------------------------------------------------------------------------
# STAMPA REPORT
# ---------------------------------------------------------------------------

def print_subset_report(result: SubsetResult, engineered_breakdown: pd.DataFrame):
    print("\n" + "=" * 78)
    print(f"SUBSET: {result.name.upper()}")
    print("=" * 78)

    print("\n-- Ratio complessivo --")
    for k, v in result.overall_ratio.items():
        print(f"  {k}: {v}")

    print("\n-- Per tipologia di smell --")
    print(result.by_smell.to_string())

    print("\n-- Per tipologia di commit introducente (first_commit_goal) --")
    print(result.by_goal.to_string())

    print("\n-- Tipo di operazione di rimozione (new_change_type) --")
    print(result.removal_type_counts.to_string())

    print("\n-- Incrocio smell x tipologia commit: introdotti --")
    print(result.cross_intro.to_string())

    print("\n-- Incrocio smell x tipologia commit: rimossi --")
    print(result.cross_removed.to_string())

    print("\n-- Incrocio smell x tipologia commit: ratio --")
    print(result.cross_ratio.to_string())

    print("\n-- Ratio di rimozione per 'Engineered ML Project' (Y/N) [NICHE.csv] --")
    print(engineered_breakdown.to_string())


def print_cross_subset_comparison(results: dict):
    print("\n" + "=" * 78)
    print("CONFRONTO SMALL vs MEDIUM vs LARGE")
    print("=" * 78)
    comparison = pd.DataFrame({
        name: {
            "introdotti": r.overall_ratio["introdotti"],
            "rimossi": r.overall_ratio["rimossi"],
            "ratio": r.overall_ratio["ratio"],
            "progetti_intro": r.overall_ratio["progetti_intro"],
            "progetti_rimossi": r.overall_ratio["progetti_rimossi"],
        }
        for name, r in results.items()
    })
    print(comparison.to_string())


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    pd.set_option("display.width", 200)
    pd.set_option("display.max_columns", 20)

    print("Caricamento metadati repository da NICHE.csv...")
    niche_repos = pd.read_csv(NICHE_REPO_FILE)

    results = {}
    for name, config in SUBSETS.items():
        result = analyze_subset(name, config)
        engineered_breakdown = enrich_with_repo_metadata(result, niche_repos)
        print_subset_report(result, engineered_breakdown)
        results[name] = result

    print_cross_subset_comparison(results)


if __name__ == "__main__":
    main()