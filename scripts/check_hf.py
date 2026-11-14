#!/usr/bin/env python3
"""
check_hf.py — Open Weights License Tracker

Two jobs:
  1. Track a curated list of flagship LLM repos -> data/models.csv
  2. Discover brand-new repos (created within N days) -> data/new_repos.json

Design note: auto-picking "newest repo per vendor" fails badly (it surfaces
OCR / audio / guard models instead of the flagship LLM). So the flagship list is
curated by hand, and discovery is a separate, clearly-labelled output.

Usage:
    python3 scripts/check_hf.py           # refresh data
    python3 scripts/check_hf.py --diff    # + report license changes since last run

No API key needed.
"""

import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_CSV = os.path.join(ROOT, "data", "models.csv")
NEW_JSON = os.path.join(ROOT, "data", "new_repos.json")

# ---- Curated flagship list -------------------------------------------------
# (vendor, display_name, hf_repo)
FLAGSHIPS = [
    # DeepSeek — all MIT
    ("DeepSeek", "V4.1-Flash-1017", "deepseek-ai/DeepSeek-V4.1-Flash-1017"),
    ("DeepSeek", "V4-Pro",          "deepseek-ai/DeepSeek-V4-Pro"),
    ("DeepSeek", "V4.1-Flash",      "deepseek-ai/DeepSeek-V4.1-Flash"),
    # Alibaba / Qwen
    ("Alibaba",  "Qwen3.8-27B",        "Qwen/Qwen3.8-27B"),
    ("Alibaba",  "Qwen3.8-Flash-Next", "Qwen/Qwen3.8-Flash-Next"),
    # Zhipu
    ("Zhipu",    "GLM-5.2",       "zai-org/GLM-5.2"),
    ("Zhipu",    "GLM-5.3",       "zai-org/GLM-5.3"),
    ("Zhipu",    "GLM-5.3-Flash", "zai-org/GLM-5.3-Flash"),
    # Moonshot — all CUSTOM
    ("Moonshot", "Kimi-K3",       "moonshotai/Kimi-K3"),
    ("Moonshot", "Kimi-K3.1-Pro", "moonshotai/Kimi-K3.1-Pro"),
    # MiniMax — all CUSTOM
    ("MiniMax",  "M3",   "MiniMaxAI/MiniMax-M3"),
    ("MiniMax",  "M2.5", "MiniMaxAI/MiniMax-M2.5"),
    # Meituan
    ("Meituan",  "LongCat-2.5",       "meituan-longcat/LongCat-2.5"),
    ("Meituan",  "LongCat-2.0",       "meituan-longcat/LongCat-2.0"),
    ("Meituan",  "LongCat-Flash-Chat", "meituan-longcat/LongCat-Flash-Chat"),
    # StepFun
    ("StepFun",  "Step-3.7-Flash", "stepfun-ai/Step-3.7-Flash"),
    # Tencent
    ("Tencent",  "Hy-Nomas", "tencent/Hy-Nomas"),
    # Baidu
    ("Baidu",    "ERNIE-5.5-Flash-Base",      "baidu/ERNIE-5.5-Flash-Base"),
    ("Baidu",    "ERNIE-5.5-Flash-Base-BF16", "baidu/ERNIE-5.5-Flash-Base-BF16"),
    # Overseas reference points
    ("Mistral",  "Large-4-1T-A52B", "mistralai/Mistral-Large-4-1T-A52B"),
    ("OpenAI",   "gpt-oss-120b",    "openai/gpt-oss-120b"),
    ("Meta",     "Llama-3.3-70B",   "meta-llama/Llama-3.3-70B-Instruct"),
]

# Manually curated entries without a mapped public weights repository.
# Absence from this list of mapped repos is not proof that no weights exist elsewhere.
API_ONLY = [
    ("Alibaba", "Qwen3.8-Max", "no HF repo; API only"),
]

# Orgs to scan for new uploads.
WATCH_ORGS = [
    "deepseek-ai", "Qwen", "zai-org", "moonshotai", "MiniMaxAI",
    "meituan-longcat", "stepfun-ai", "tencent", "baidu", "sensenova",
    "openai", "mistralai", "meta-llama",
]

STD_LICENSES = {"mit", "apache-2.0", "bsd-3-clause"}
DISCOVER_DAYS = 14

HEADER = ("vendor,model,hf_repo,license,license_tier,license_base,downloads,likes,"
          "created,last_modified,checked_at\n")


def curl_json(url, retries=2):
    for i in range(retries):
        try:
            out = subprocess.run(["curl", "-s", "--max-time", "25", url],
                                 capture_output=True, text=True, check=False).stdout
            return json.loads(out)
        except Exception:
            if i == retries - 1:
                return None
            time.sleep(1)
    return None


def tier(lid):
    if not lid or lid == "-":
        return "UNKNOWN"
    return "STD" if lid.lower() in STD_LICENSES else "CUSTOM"


def main():
    do_diff = "--diff" in sys.argv
    now = datetime.now(timezone.utc)
    checked = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    prev = {}
    if os.path.exists(DATA_CSV):
        with open(DATA_CSV, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                prev[r["hf_repo"]] = r

    rows = []
    for vendor, name, repo in FLAGSHIPS:
        d = curl_json(f"https://huggingface.co/api/models/{repo}")
        if not isinstance(d, dict) or "id" not in d:
            print(f"  [warn] {repo}: fetch failed", file=sys.stderr)
            rows.append(dict(vendor=vendor, model=name, hf_repo=repo,
                             license="FETCH_FAILED", license_tier="UNKNOWN",
                             license_base="unreviewed",
                             downloads=0, likes=0, created="", last_modified="",
                             checked_at=checked))
            continue
        tags = d.get("tags") or []
        lic = next((t.split(":", 1)[1] for t in tags if t.startswith("license:")), "-")
        rows.append(dict(
            vendor=vendor, model=name, hf_repo=repo,
            license=lic, license_tier=tier(lic),
            # Preserve the earlier manual assessment only while the HF tag is unchanged.
            # A preserved label is not a fresh review of the LICENSE text.
            license_base=(prev.get(repo, {}).get("license_base", "unreviewed")
                          if prev.get(repo, {}).get("license") == lic
                          else "std" if tier(lic) == "STD" else "unreviewed"),
            downloads=d.get("downloads", 0), likes=d.get("likes", 0),
            created=(d.get("createdAt") or "")[:10],
            last_modified=(d.get("lastModified") or "")[:10],
            checked_at=checked,
        ))
        time.sleep(0.3)

    for vendor, model, note in API_ONLY:
        rows.append(dict(vendor=vendor, model=model, hf_repo="(none)",
                         license="-", license_tier="NO_WEIGHTS", license_base="-",
                         downloads=0, likes=0, created="", last_modified="",
                         checked_at=checked))

    os.makedirs(os.path.dirname(DATA_CSV), exist_ok=True)
    with open(DATA_CSV, "w", newline="", encoding="utf-8") as f:
        f.write(HEADER)
        for r in sorted(rows, key=lambda x: (x["license_tier"], x["vendor"], x["model"])):
            f.write(f'{r["vendor"]},{r["model"]},{r["hf_repo"]},{r["license"]},'
                    f'{r["license_tier"]},{r["license_base"]},{r["downloads"]},{r["likes"]},'
                    f'{r["created"]},{r["last_modified"]},{r["checked_at"]}\n')

    std = sum(1 for r in rows if r["license_tier"] == "STD")
    cust = sum(1 for r in rows if r["license_tier"] == "CUSTOM")
    none = sum(1 for r in rows if r["license_tier"] == "NO_WEIGHTS")
    print(f"Flagship table: {len(rows)} rows -> {DATA_CSV}")
    print(f"  STD: {std}   CUSTOM: {cust}   NO_WEIGHTS: {none}")

    # ---- discovery: brand-new repos ----
    cutoff = (now - timedelta(days=DISCOVER_DAYS)).strftime("%Y-%m-%d")
    known = {r["hf_repo"] for r in rows}
    new = []
    for org in WATCH_ORGS:
        d = curl_json(f"https://huggingface.co/api/models?author={org}"
                      f"&limit=100&sort=createdAt&direction=-1")
        if not isinstance(d, list):
            continue
        for m in d:
            created = (m.get("createdAt") or "")[:10]
            if created < cutoff:
                continue
            if m["id"] in known:
                continue
            tags = m.get("tags") or []
            lic = next((t.split(":", 1)[1] for t in tags if t.startswith("license:")), "-")
            new.append(dict(org=org, repo=m["id"], license=lic,
                            tier=tier(lic), created=created,
                            likes=m.get("likes", 0)))
        time.sleep(0.35)

    new.sort(key=lambda x: (x["created"], x["likes"]), reverse=True)
    with open(NEW_JSON, "w", encoding="utf-8") as f:
        json.dump(new, f, indent=2, ensure_ascii=False)
    print(f"New repos in last {DISCOVER_DAYS}d: {len(new)} -> {NEW_JSON}")

    if do_diff and prev:
        print("\nChanges vs previous run:")
        n = 0
        cur = {r["hf_repo"]: r for r in rows}
        for k, r in cur.items():
            if k in prev and prev[k]["license"] != r["license"]:
                print(f"  LICENSE CHANGED  {k}: {prev[k]['license']} -> {r['license']}")
                n += 1
        for k in prev:
            if k not in cur:
                print(f"  REMOVED FROM LIST {k}")
                n += 1
        if not n:
            print("  (no changes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
