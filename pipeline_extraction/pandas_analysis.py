
import pandas as pd

INPUT_CSV = "large_pyref_results.csv"
OUTPUT_MD = "analisi_removing_large_pandas.md"

df = pd.read_csv(INPUT_CSV, dtype=str)

n_raw = len(df)

# --- unique
dedup = df.drop_duplicates(
    subset=["repo", "commitid_introduced", "commitid_removed", "smell_name"]
).copy()
n_dedup = len(dedup)

# to num
dedup["removed_count_num"] = pd.to_numeric(dedup["pyref_ref_removed_count"], errors="coerce")
dedup["has_refactor"] = dedup["removed_count_num"] > 0


status_counts = dedup["pyref_ref_removed_status"].value_counts()


ok = dedup[dedup["pyref_ref_removed_status"] == "ok"]
n_ok = len(ok)
n_with_refactor = int(ok["has_refactor"].sum())
n_without_refactor = n_ok - n_with_refactor
ratio_on_ok = n_with_refactor / n_ok if n_ok else float("nan")
ratio_on_all = n_with_refactor / n_dedup if n_dedup else float("nan")

# --- Ratio per tipologia di smell ---
per_smell = (
    ok.groupby("smell_name")["has_refactor"]
    .agg(analizzabili="count", con_refactoring="sum")
    .assign(ratio=lambda d: d["con_refactoring"] / d["analizzabili"])
)
totali_per_smell = dedup.groupby("smell_name").size().rename("istanze_totali")
per_smell = per_smell.join(totali_per_smell).sort_values("ratio", ascending=False)


with_refactor_rows = ok[ok["has_refactor"]]

refactor_types = (
    with_refactor_rows["pyref_ref_removed"]
    .str.split(";")
    .explode()
    .str.strip()
)
refactor_types = refactor_types[refactor_types != ""]
refactor_counts = refactor_types.value_counts()
total_refactor_ops = int(refactor_counts.sum())


exploded = with_refactor_rows[["smell_name", "pyref_ref_removed"]].copy()
exploded["pyref_ref_removed"] = exploded["pyref_ref_removed"].str.split(";")
exploded = exploded.explode("pyref_ref_removed")
exploded["pyref_ref_removed"] = exploded["pyref_ref_removed"].str.strip()
exploded = exploded[exploded["pyref_ref_removed"] != ""]
refactor_by_smell = (
    exploded.groupby(["smell_name", "pyref_ref_removed"]).size().rename("occorrenze")
)


def pct(n, d):
    return f"{100 * n / d:.1f}%" if d else "n/d"


# --- Report markdown ---
lines = []
lines.append("# Analisi dei commit di rimozione smell — subset `large` (versione pandas)\n")
lines.append(f"- Righe totali (una per occorrenza di smell): **{n_raw}**")
lines.append(f"- Combinazioni uniche dopo deduplica: **{n_dedup}**\n")

lines.append("## Copertura (status PyRef sul commit di rimozione)\n")
lines.append("| Status | # combinazioni | % sul totale |")
lines.append("|---|---:|---:|")
for status, count in status_counts.items():
    lines.append(f"| `{status}` | {count} | {pct(count, n_dedup)} |")
lines.append("")

lines.append("## Ratio complessivo\n")
lines.append(f"- Su **{n_ok}** commit analizzabili (`status=ok`): **{n_with_refactor}** ({pct(n_with_refactor, n_ok)}) mostrano refactoring")
lines.append(f"- Sul totale delle {n_dedup} combinazioni: {pct(n_with_refactor, n_dedup)} mostrano refactoring\n")

lines.append("## Ratio per tipologia di smell\n")
lines.append("| Smell | Istanze totali | Analizzabili | Con refactoring | Ratio |")
lines.append("|---|---:|---:|---:|---:|")
for smell, row in per_smell.iterrows():
    lines.append(
        f"| `{smell}` | {int(row['istanze_totali'])} | {int(row['analizzabili'])} | "
        f"{int(row['con_refactoring'])} | {pct(row['con_refactoring'], row['analizzabili'])} |"
    )
lines.append("")

lines.append("## Tipologie di refactoring rilevate\n")
lines.append(f"Totale operazioni: **{total_refactor_ops}**, su **{n_with_refactor}** commit.\n")
lines.append("| Tipo di refactoring | Occorrenze | % |")
lines.append("|---|---:|---:|")
for rtype, count in refactor_counts.items():
    lines.append(f"| {rtype} | {count} | {pct(count, total_refactor_ops)} |")
lines.append("")

lines.append("## Tipologie di refactoring per smell\n")
for smell in per_smell.index:
    if smell not in refactor_by_smell.index.get_level_values(0):
        continue
    sub = refactor_by_smell.loc[smell].sort_values(ascending=False)
    lines.append(f"**`{smell}`** (totale: {int(sub.sum())})\n")
    lines.append("| Tipo di refactoring | Occorrenze |")
    lines.append("|---|---:|")
    for rtype, count in sub.items():
        lines.append(f"| {rtype} | {count} |")
    lines.append("")

report = "\n".join(lines)
with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(report)

print(report)