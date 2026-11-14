#!/usr/bin/env python3
"""
hf_daily.py — HF 热榜日更素材生成（A 方案：栏目化日更）

三件事：
  1. 拉 Hugging Face trending 榜（trendingScore 排序），过滤掉微调/量化变体
  2. 拉 14 个厂商组织最近 7 天的新建仓库（真·新模型，不是变体）
  3. 输出「今日候选」：每条都带一个可写的判断角度

设计原则：
  - 不做「今日 AI 汇总」这种加法，只做「3-5 条值得说的」
  - 每条必须能回答：这东西是什么、谁做的、有没有权重、能不能商用
  - 变体过滤：同一底座被社区反复微调/量化，会挤满榜单，必须剔掉

用法：
    python3 scripts/hf_daily.py            # 输出今日候选
    python3 scripts/hf_daily.py --json     # 机器可读
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "daily")
STD = {"mit", "apache-2.0", "bsd-3-clause"}

# 官方/一手组织：这些组织发布的才算「源头」，其余视为社区变体
OFFICIAL_ORGS = {
    "deepseek-ai", "Qwen", "zai-org", "moonshotai", "MiniMaxAI", "meituan-longcat",
    "stepfun-ai", "tencent", "baidu", "sensenova", "inclusionAI", "OpenBMB", "01-ai",
    "openai", "mistralai", "meta-llama", "google", "microsoft", "nvidia",
    "black-forest-labs", "Lightricks", "stabilityai", "allenai", "nousresearch",
    "anthropic", "ibm-granite", "tiiuae", "swiss-ai", "ByteDance", "bytedance-seed",
}

# 变体/量化的名字特征：命中即降权
VARIANT_PAT = re.compile(
    r"(?i)(gguf|awq|gptq|mlx|exl2|bnb|4bit|8bit|6bit|5bit|3bit|2bit|"
    r"uncensored|abliterat|quantiz|-int[48]-|w4a16|w8a8|fp8|fp4|"
    r"turbo|fusion|merge|dpo|orpo|kto|distill|lora|qlora)"
)

# 已知的大模型底座名（用于判断「是不是别人的微调」）
BASE_HINTS = [
    "qwen", "llama", "mistral", "deepseek", "glm", "kimi", "minimax", "ernie",
    "gemma", "phi", "nemotron", "gpt-oss", "longcat", "step-", "hy-", "ling-",
    "flux", "ltx", "sensenova", "hunyuan",
]


def curl_json(url, tries=3):
    """带重试的取 JSON。空响应或解析失败都算失败，不静默吞掉。"""
    err = None
    for _ in range(tries):
        r = subprocess.run(["curl", "-s", "--max-time", "25", url],
                           capture_output=True, text=True)
        txt = r.stdout.strip()
        if txt:
            try:
                return json.loads(txt), None
            except Exception as e:
                err = f"parse: {e}"
        else:
            err = "empty response (maybe 429)"
        time.sleep(1.5)
    return None, err


def license_of(m):
    tags = m.get("tags") or []
    lic = next((t.split(":", 1)[1] for t in tags if t.startswith("license:")), "-")
    if lic in STD:
        base = "std"
    elif lic == "-":
        base = "none"
    else:
        base = "custom"
    return lic, base


def is_variant(m, model_id, author):
    """判断是不是社区变体/非目标模态。

    三层判断，任一命中即剔：
      1. 模态不对（只要语言模型，不要 3D/图像生成/语音）
      2. 官方 tag 里自报 base_model（最可靠——作者自己承认是别人的微调）
      3. 名字特征（量化/合并/微调标记）+ 社区作者套用已知底座
    """
    name = model_id.split("/")[-1]

    # 1. 模态过滤
    task = (m.get("pipeline_tag") or "").lower()
    ALLOWED = {"text-generation", "text2text-generation", "image-text-to-text",
               "any-to-any", "feature-extraction", ""}
    if task and task not in ALLOWED:
        return True, f"模态不是语言模型({task})"

    # 2. 自报 base_model（finetune / quantized 都算变体）
    tags = m.get("tags") or []
    base_tags = [t for t in tags if t.startswith("base_model:")]
    if base_tags:
        return True, f"自报基于 {base_tags[0].split(':', 1)[1]}"

    # 3. 名字特征
    if VARIANT_PAT.search(name):
        return True, "名字含量化/微调标记"
    if author and author.lower() not in {o.lower() for o in OFFICIAL_ORGS}:
        low = name.lower()
        hits = [b for b in BASE_HINTS if b in low]
        if hits:
            return True, f"社区套用底座({hits[0]})"
    return False, ""


def fetch_trending(limit=60):
    url = (f"https://huggingface.co/api/models?sort=trendingScore"
           f"&direction=-1&limit={limit}")
    d, err = curl_json(url)
    if not isinstance(d, list):
        return [], err
    rows = []
    for m in d:
        mid = m.get("id") or ""
        if "/" not in mid:
            continue
        author = mid.split("/")[0]
        var, why = is_variant(m, mid, author)
        lic, base = license_of(m)
        rows.append({
            "id": mid, "author": author, "name": mid.split("/")[-1],
            "trending": m.get("trendingScore", 0), "likes": m.get("likes", 0),
            "downloads": m.get("downloads", 0), "license": lic, "license_base": base,
            "created": (m.get("createdAt") or "")[:10],
            "variant": var, "variant_reason": why,
            "task": m.get("pipeline_tag") or "-",
        })
    return rows, None


def fetch_new(days=7):
    """14 个厂商组织最近 N 天新建的仓库。"""
    orgs = ["deepseek-ai", "Qwen", "zai-org", "moonshotai", "MiniMaxAI",
            "meituan-longcat", "stepfun-ai", "tencent", "baidu", "sensenova",
            "inclusionAI", "openbmb", "01-ai", "openai", "mistralai", "meta-llama"]
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    out, fails = [], []
    for org in orgs:
        url = (f"https://huggingface.co/api/models?author={org}"
               f"&limit=30&sort=createdAt&direction=-1")
        d, err = curl_json(url)
        if not isinstance(d, list):
            fails.append((org, err))
            continue
        for m in d:
            c = (m.get("createdAt") or "")[:10]
            if c < since:
                continue
            lic, base = license_of(m)
            out.append({
                "id": m["id"], "org": org, "created": c,
                "license": lic, "license_base": base,
                "likes": m.get("likes", 0), "task": m.get("pipeline_tag") or "-",
            })
        time.sleep(0.3)
    return out, fails


def angle_for(r):
    """给每条一个可写的判断角度（不是描述，是观点）。"""
    base, lic = r["license_base"], r["license"]
    if base == "std":
        return f"许可证标签为 {lic}；核对 LICENSE、依赖许可与部署要求后再判断用途"
    if base == "custom":
        return f"标 other，需逐条读协议才能定商用"
    return "许可证未标，商用前必须自己查"


def main():
    as_json = "--json" in sys.argv
    trending, terr = fetch_trending()
    new, fails = fetch_new()

    # 只留「非变体 + 有趋势分」的
    clean = [r for r in trending if not r["variant"]]
    variants = [r for r in trending if r["variant"]]

    top = clean[:8]
    fresh = sorted(new, key=lambda x: x["created"], reverse=True)[:8]

    if as_json:
        print(json.dumps({"top": top, "new": fresh,
                          "variants_filtered": len(variants),
                          "errors": [terr] + fails}, ensure_ascii=False, indent=1))
        return

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n=== HF 日更候选 {today} ===")
    print(f"趋势榜抓 {len(trending)} 条，剔掉 {len(variants)} 条变体，剩 {len(clean)} 条\n")

    print("【A. 今日趋势 TOP 8】")
    for i, r in enumerate(top, 1):
        print(f"{i}. {r['id']}")
        print(f"   趋势 {r['trending']} · ♥{r['likes']} · 下载 {r['downloads']:,} · 建 {r['created']}")
        print(f"   角度：{angle_for(r)}")
    print()

    print("【B. 厂商新仓库（近 7 天）】")
    if not fresh:
        print("   无（这段时间没有厂商发布新仓库 → 今日不发 B 段）")
    for r in fresh:
        print(f"   {r['created']}  {r['id']}  [{r['license']}/{r['license_base']}]  ♥{r['likes']}")
    print()

    print("【C. 被剔掉的变体（说明为什么）】")
    for r in variants[:5]:
        print(f"   {r['id'][:55]:57s} {r['variant_reason']}")
    if fails:
        print(f"\n⚠️ 抓取失败：{fails}")

    # 存一份
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{today}.md")
    with open(path, "w") as f:
        f.write(f"# HF 日更候选 {today}\n\n## 趋势 TOP\n\n")
        for r in top:
            f.write(f"- **{r['id']}** · 趋势{r['trending']} · ♥{r['likes']} · "
                    f"{r['license']}/{r['license_base']}\n  - {angle_for(r)}\n")
        f.write("\n## 厂商新仓库（近 7 天）\n\n")
        f.write("无\n" if not fresh else "")
        for r in fresh:
            f.write(f"- {r['created']} `{r['id']}` [{r['license']}/{r['license_base']}]\n")
    print(f"已存：{path}")


if __name__ == "__main__":
    main()
