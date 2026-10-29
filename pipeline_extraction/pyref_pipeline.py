#!/usr/bin/env python3

import csv
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

# =============================================================================
# Parameters
# =============================================================================

SUBSET = "large"  # "small" | "medium" | "large" - usato solo per nominare i file di cache
INPUT_CSV = "../resources/large_intro_removing_output_results.csv"
OUTPUT_CSV = "large_pyref_results_x2_full.csv"
COPY_BACKUP_PYREF = "backup/large"
# cartelle dove cercare i JSON di PyRef gia' prodotti (nome file: <repo>-<commit>_copy_<timestamp>.json)
BACKUP_READ_DIRS = ["backup/large", "backup/medium", "backup/small"]

PYREF_DIR = "pyRef"                # cartella dove si trova PyRef (creata da setup_pyref.sh)
REPOS_DIR = None                   # None = <PYREF_DIR>/Repos
CACHE_DIR = "pyref_cache"          # cartella per i file di cache/resume

CLONE_TIMEOUT = 3600                 # secondi max per il clone completo di un repo
COMMIT_TIMEOUT = 90                # secondi max per l'estrazione refactoring su un commit

RETRY_ERRORS = False                # True = ritenta i commit finiti in error/timeout

# =============================================================================

csv.field_size_limit(10**7)


def extract_json_name(repo):
    return re.split('/', repo)[-1]


def cache_path(cache_dir, subset):
    return os.path.join(cache_dir, f"{subset}_cache.json")


def load_cache(cache_dir, subset):
    p = cache_path(cache_dir, subset)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"repos": {}, "commits": {}}


def save_cache(cache_dir, subset, cache):
    p = cache_path(cache_dir, subset)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f)
    os.replace(tmp, p)


def read_rows(path):
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        r = csv.DictReader(f)
        return list(r)


def clone_repo(repo, cache, repos_dir):
    """Cloning repo and return a path or None."""
    key = repo
    st = cache["repos"].get(key)
    path = os.path.join(repos_dir, repo)
    if st == "ok" and os.path.isdir(path):
        return path
    if st == "failed":
        return None
    if os.path.isdir(path):
        cache["repos"][key] = "ok"
        return path
    url = f"https://github.com/{repo}.git"
    print(f"  Cloning {repo} ...", flush=True)
    try:
        res = subprocess.run(
            ["git", "clone", "--quiet", url, path],
            timeout=CLONE_TIMEOUT, capture_output=True, text=True
        )
        if res.returncode != 0 or not os.path.isdir(path):
            print(f"    clone FAILED: {res.stderr[:300]}", flush=True)
            cache["repos"][key] = "failed"
            return None
        cache["repos"][key] = "ok"
        return path
    except subprocess.TimeoutExpired:
        print("    clone TIMEOUT", flush=True)
        cache["repos"][key] = "failed"
        return None
    except Exception as e:
        print(f"    clone ERROR: {e}", flush=True)
        cache["repos"][key] = "failed"
        return None


def find_backup_json(sname, commit):
    """JSON di PyRef gia' salvato per questo repo+commit nelle cartelle BACKUP_READ_DIRS (il piu' recente), o None."""
    found = []
    for d in BACKUP_READ_DIRS:
        found.extend(glob.glob(os.path.join(d, f"{glob.escape(sname)}-{commit}_copy_*.json")))
    return max(found, key=os.path.getmtime) if found else None


def read_backup_json(path, commit):
    """Ritorna (types, pyref_result): pyref_result = le entry INTERE di PyRef per questo commit."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    types, pyref_result = [], []
    for entry in data:
        if entry.get("Commit") == commit:
            rt = entry.get("Refactoring Type")
            if isinstance(rt, list):
                types.extend(rt)
            elif rt:
                types.append(rt)
            pyref_result.append(entry)
    return types, pyref_result


def run_pyref_commit(repo, repopath, commit, cache, pyref_dir):
    ck = f"{repo}::{commit}"
    if ck in cache["commits"]:
        return cache["commits"][ck]
    # errore del json filename
    sname = extract_json_name(repo)

    # backup gia' presente -> aggiorno la cache senza lanciare PyRef
    backup_json = find_backup_json(sname, commit)
    if backup_json:
        try:
            types, pyref_result = read_backup_json(backup_json, commit)
            print(f"from backup {backup_json}", flush=True)
            result = {"status": "ok", "count": len(types), "types": types, "pyref_result": pyref_result}
            cache["commits"][ck] = result
            return result
        except Exception as e:
            print(f"backup not readable ({e}), running PyRef", flush=True)

    json_path = os.path.join(repopath.split('/')[0], f"{sname}_data.json")
    if os.path.exists(json_path):
        try:
            os.remove(json_path)
        except OSError:
            pass
    print(f"run for {repo} with {commit}", flush=True)
    try:
        res = subprocess.run(
            [sys.executable, "main.py", "getrefs", "-r", os.path.abspath(repopath), "-c", commit],
            cwd=pyref_dir, timeout=COMMIT_TIMEOUT, capture_output=True, text=True
        )
    except subprocess.TimeoutExpired:
        print(f"failed timeout for {repo} with {commit}", flush=True)
        result = {"status": "timeout", "count": None, "types": [], "pyref_result": []}
        cache["commits"][ck] = result
        return result
    except Exception as e:
        print(f"failed exception for {repo} with {commit}", flush=True)
        result = {"status": "error", "count": None, "types": [], "pyref_result": [], "msg": str(e)}
        cache["commits"][ck] = result
        return result

    if "FileNotFoundError" in res.stderr or ("No such file or directory" in res.stderr):
        # nessun file .py modificato in questo commit -> nessun refactoring possibile
        # (es. commit che aggiunge solo file nuovi, merge commit, root commit, ecc.)
        print(f"NotFound for {repo} with {commit}", flush=True)
        result = {"status": "nodiff", "count": 0, "types": [], "pyref_result": []}
        cache["commits"][ck] = result
        return result

    if res.returncode != 0:
        print(f"failed for {repo} with {commit}", flush=True)
        result = {"status": "error", "count": None, "types": [], "pyref_result": [], "msg": res.stderr[-500:]}
        cache["commits"][ck] = result
        return result

    types = []
    pyref_result = []
    if os.path.exists(json_path):
        print(f"saving in backup for execution {repo}::{commit}", flush=True)
        timestamp = int(time.time())
        copy_path = f"{sname}-{commit}_copy_{timestamp}.json"
        shutil.copy2(json_path, os.path.join(COPY_BACKUP_PYREF, copy_path))
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data:
                if entry.get("Commit") == commit:
                    pyref_result.append(entry)
                    rt = entry.get("Refactoring Type")
                    if isinstance(rt, list):
                        types.extend(rt)
                    elif rt:
                        types.append(rt)
        except Exception as e:
            result = {"status": "error", "count": None, "types": [], "pyref_result": [], "msg": f"json parse: {e}"}
            cache["commits"][ck] = result
            return result

    result = {"status": "ok", "count": len(types), "types": types, "pyref_result": pyref_result}
    cache["commits"][ck] = result
    return result


def process_subset(subset, input_csv, pyref_dir, repos_dir, cache_dir):
    print(f"=== Processing subset: {subset} ===", flush=True)
    rows = read_rows(input_csv)
    print(f"rows: {len(rows)}", flush=True)

    repo_commits = {}
    for row in rows:
        repo = row["project_name"]
        repo_commits.setdefault(repo, set())
        if row.get("Commit_ID"):
            repo_commits[repo].add(row["Commit_ID"])
        if row.get("new_commit"):
            repo_commits[repo].add(row["new_commit"])

    cache = load_cache(cache_dir, subset)
    repos = sorted(repo_commits.keys())

    total_commits_all = sum(len(v) for v in repo_commits.values())
    already_done = sum(1 for repo in repos for c in repo_commits[repo] if f"{repo}::{c}" in cache["commits"])
    print(
        f"Total repo: {len(repo_commits)} | Total unique commit : {total_commits_all} | already in cache: {already_done}",
        flush=True)

    t_start = time.time()
    for ridx, repo in enumerate(repos):
        repopath = clone_repo(repo, cache, repos_dir)
        save_cache(cache_dir, subset, cache)
        if repopath is None:
            continue
        commits = sorted(repo_commits[repo])
        for cidx, commit in enumerate(commits):
            ck = f"{repo}::{commit}"
            if ck in cache["commits"]:
                print(f"skipped for: {repo}::{commit}")
                continue
            print(f"[{ridx + 1}/{len(repos)}] {repo}  commit {cidx + 1}/{len(commits)}: {commit}", flush=True)
            run_pyref_commit(repo, repopath, commit, cache, pyref_dir)
            save_cache(cache_dir, subset, cache)
    print(f"Done subset {subset}. Elapsed: {time.time() - t_start:.1f}s", flush=True)


def location_file(location):

    location = location or ""
    if not location.endswith(".py") and ".py/" in location:
        return location[:location.index(".py/") + 3]
    return location


def same_file_result(relative_path, r):

    same = [e for e in r.get("pyref_result", [])
            if location_file(e.get("Location")) == relative_path
            or location_file(e.get("New Location")) == relative_path]
    if same:
        return 1, json.dumps(same, ensure_ascii=False)
    return 0, ""


def same_function_result(function_name, same_file_json):
    """
    Solo se same_file = 1 (same_file_json valorizzato): tra le entry nello stesso file tiene quelle
    con function_name == Original oppure == Updated.
    Ritorna (1, JSON delle entry) se ce n'e' almeno una, altrimenti (0, "").
    """
    if not same_file_json:
        return 0, ""
    same = [e for e in json.loads(same_file_json)
            if function_name == e.get("Original") or function_name == e.get("Updated")]
    if same:
        return 1, json.dumps(same, ensure_ascii=False)
    return 0, ""


def build_output_csv(subset, input_csv, output_csv, cache_dir):
    rows = read_rows(input_csv)
    cache = load_cache(cache_dir, subset)
    out_rows = []
    for row in rows:
        repo = row["project_name"]
        c_intro = row.get("Commit_ID", "")
        c_rem = row.get("new_commit", "")
        r_intro = cache["commits"].get(f"{repo}::{c_intro}", {})
        r_rem = cache["commits"].get(f"{repo}::{c_rem}", {})
        same_i, out_i = same_file_result(row.get("relative_path", ""), r_intro)
        same_r, out_r = same_file_result(row.get("relative_path", ""), r_rem)
        func_i, func_out_i = same_function_result(row.get("function_name", ""), out_i)
        func_r, func_out_r = same_function_result(row.get("function_name", ""), out_r)
        out_rows.append({
            "repo": repo,
            "smell_name": row.get("smell_name", ""),
            "commitid_introduced": c_intro,
            "pyref_refactor_intro": ";".join(r_intro.get("types", [])),
            "pyref_refactor_intro_count": r_intro.get("count", ""),
            "pyref_refactor_intro_status": r_intro.get("status", "missing"),
            "commitid_removed": c_rem,
            "pyref_ref_removed": ";".join(r_rem.get("types", [])),
            "pyref_ref_removed_count": r_rem.get("count", ""),
            "pyref_ref_removed_status": r_rem.get("status", "missing"),
            "same_file_intro": same_i,
            "py_ref_out_same_file_intro": out_i,
            "same_file_removed": same_r,
            "py_ref_out_same_file_removed": out_r,
            "same_function_intro": func_i,
            "pyref_out_same_function_intro": func_out_i,
            "same_function_removed": func_r,
            "pyref_out_same_function_removed": func_out_r,
        })
        fieldnames = [
            "repo", "smell_name",
            # introduzione
            "commitid_introduced", "pyref_refactor_intro", "pyref_refactor_intro_count", "pyref_refactor_intro_status",
            "same_file_intro", "py_ref_out_same_file_intro",
            "same_function_intro", "pyref_out_same_function_intro",
            # rimozione
            "commitid_removed", "pyref_ref_removed", "pyref_ref_removed_count", "pyref_ref_removed_status",
            "same_file_removed", "py_ref_out_same_file_removed",
            "same_function_removed", "pyref_out_same_function_removed",
        ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Wrote {len(out_rows)} rows to {output_csv}", flush=True)


if __name__ == "__main__":
    pyref_dir = os.path.abspath(PYREF_DIR)
    repos_dir = os.path.abspath(REPOS_DIR) if REPOS_DIR else os.path.join(pyref_dir, "Repos")
    cache_dir = os.path.abspath(CACHE_DIR)
    os.makedirs(cache_dir, exist_ok=True)
    os.makedirs(repos_dir, exist_ok=True)

    if not os.path.isdir(pyref_dir):
        print(f"ERROR: PyRef directory non found in {pyref_dir}. execute setup_pyref.sh first", file=sys.stderr)
        sys.exit(1)

    if RETRY_ERRORS:
        cache = load_cache(cache_dir, SUBSET)
        before = len(cache["commits"])
        cache["commits"] = {k: v for k, v in cache["commits"].items() if v.get("status") not in ("error", "timeout")}
        removed = before - len(cache["commits"])
        save_cache(cache_dir, SUBSET, cache)
        print(f"Removed {removed} entry with error/timeout from cache", flush=True)

    process_subset(SUBSET, INPUT_CSV, pyref_dir, repos_dir, cache_dir)
    build_output_csv(SUBSET, INPUT_CSV, OUTPUT_CSV, cache_dir)