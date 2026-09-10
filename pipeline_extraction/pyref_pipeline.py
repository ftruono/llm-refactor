#!/usr/bin/env python3

import csv
import json
import os
import re
import subprocess
import sys
import time

# =============================================================================
# Parameters
# =============================================================================

SUBSET = "small"  # "small" | "medium" | "large" - usato solo per nominare i file di cache
INPUT_CSV = "../resources/small_intro_removing_output_results.csv"
OUTPUT_CSV = "small_pyref_results.csv"

PYREF_DIR = "pyRef"                # cartella dove si trova PyRef (creata da setup_pyref.sh)
REPOS_DIR = None                   # None = <PYREF_DIR>/Repos
CACHE_DIR = "pyref_cache"          # cartella per i file di cache/resume

CLONE_TIMEOUT = 3600                 # secondi max per il clone completo di un repo
COMMIT_TIMEOUT = 3600                # secondi max per l'estrazione refactoring su un commit

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


def run_pyref_commit(repo, repopath, commit, cache, pyref_dir):

    ck = f"{repo}::{commit}"
    if ck in cache["commits"]:
        return cache["commits"][ck]
   # errore del json filename
    sname = extract_json_name(repo)
    json_path = os.path.join(repopath.split('/')[0], f"{sname}_data.json")
    if os.path.exists(json_path):
        try:
            os.remove(json_path)
        except OSError:
            pass

    try:
        res = subprocess.run(
            [sys.executable, "main.py", "getrefs", "-r", os.path.abspath(repopath), "-c", commit],
            cwd=pyref_dir, timeout=COMMIT_TIMEOUT, capture_output=True, text=True
        )
    except subprocess.TimeoutExpired:
        result = {"status": "timeout", "count": None, "types": []}
        cache["commits"][ck] = result
        return result
    except Exception as e:
        result = {"status": "error", "count": None, "types": [], "msg": str(e)}
        cache["commits"][ck] = result
        return result

    if "FileNotFoundError" in res.stderr or ("No such file or directory" in res.stderr):
        # nessun file .py modificato in questo commit -> nessun refactoring possibile
        # (es. commit che aggiunge solo file nuovi, merge commit, root commit, ecc.)
        result = {"status": "nodiff", "count": 0, "types": []}
        cache["commits"][ck] = result
        return result

    if res.returncode != 0:
        result = {"status": "error", "count": None, "types": [], "msg": res.stderr[-500:]}
        cache["commits"][ck] = result
        return result

    types = []
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for entry in data:
                if entry.get("Commit") == commit:
                    rt = entry.get("Refactoring Type")
                    if isinstance(rt, list):
                        types.extend(rt)
                    elif rt:
                        types.append(rt)
        except Exception as e:
            result = {"status": "error", "count": None, "types": [], "msg": f"json parse: {e}"}
            cache["commits"][ck] = result
            return result

    result = {"status": "ok", "count": len(types), "types": types}
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
    print(f"Total repo: {len(repo_commits)} | Total unique commit : {total_commits_all} | already in cache: {already_done}", flush=True)

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
                continue
            print(f"[{ridx+1}/{len(repos)}] {repo}  commit {cidx+1}/{len(commits)}: {commit}", flush=True)
            run_pyref_commit(repo, repopath, commit, cache, pyref_dir)
            save_cache(cache_dir, subset, cache)
    print(f"Done subset {subset}. Elapsed: {time.time() - t_start:.1f}s", flush=True)


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
        })
    fieldnames = list(out_rows[0].keys()) if out_rows else []
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