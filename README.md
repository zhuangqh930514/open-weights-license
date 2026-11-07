# Chinese LLM License Tracker

**Which Chinese LLM can you actually deploy?** A license audit of 23 flagship models — DeepSeek, Qwen, Kimi, GLM, MiniMax, ERNIE, LongCat, StepFun, Tencent. For each one it answers three questions: does it ship downloadable open weights, is it a base checkpoint or a trained model, and does the license permit commercial use. Refreshed weekly from the Hugging Face API.

Most "open source model" announcements are ambiguous. Some release full weights. Some release a pre-training checkpoint that can't be used without further training. Some release nothing and only sell API access. This repo tracks the difference, weekly, from the source: the Hugging Face API.

> **English** below · [中文说明见文末](#中文说明)

---

## Why this exists

If you're evaluating a model for commercial use, three questions matter more than benchmark scores:

1. **Are the weights actually downloadable?** Many flagship models exist only behind an API.
2. **Is it a base checkpoint or a trained model?** A base checkpoint needs your own post-training before it can be used. That is a very different commitment from downloading an instruct model.
3. **What does the license permit?** `MIT` / `Apache-2.0` are standard and commercially safe. `other` means a custom agreement you must read line by line.

Vendor marketing doesn't answer these. Model cards often bury them. This repo puts them in one table, refreshed weekly.

## Current snapshot — 2026-11-06

23 flagship models tracked across 12 vendors.

| License tier | Count | Meaning |
|---|---:|---|
| `STD` — MIT / Apache-2.0 | **11** | Standard OSI licenses. Commercially safe, modification and redistribution allowed. |
| `CUSTOM` — `other` | **10** | Weights are downloadable, but the license is vendor-specific. **Read before commercial use.** |
| `NO_WEIGHTS` | **2** | No public weights at all. API access only. |

### The table

See [`data/models.csv`](data/models.csv) for the full dataset. Selected rows:

| Vendor | Model | License | Tier |
|---|---|---|---|
| DeepSeek | V4.1-Flash-1017 | `mit` | STD |
| DeepSeek | V4-Pro | `mit` | STD |
| Alibaba | Qwen3.8-27B | `apache-2.0` | STD |
| Zhipu | GLM-5.2 | `mit` | STD |
| Zhipu | GLM-5.3-Flash | `mit` | STD |
| Meituan | LongCat-2.0 | `mit` | STD |
| StepFun | Step-3.7-Flash | `apache-2.0` | STD |
| Tencent | Hy-Nomas | `apache-2.0` | STD |
| OpenAI | gpt-oss-120b | `apache-2.0` | STD |
| — | — | — | — |
| Moonshot | Kimi-K3 | `other` | CUSTOM |
| Moonshot | Kimi-K3.1-Pro | `other` | CUSTOM |
| MiniMax | M3 | `other` | CUSTOM |
| Zhipu | GLM-5.3 | `other` | CUSTOM |
| Alibaba | Qwen3.8-Flash-Next | `other` | CUSTOM |
| Mistral | Large-4-1T-A52B | `other` | CUSTOM |
| Baidu | ERNIE-5.5-Flash-Base | `other` | CUSTOM |
| Meta | Llama-3.3-70B | `llama3.3` | CUSTOM |
| — | — | — | — |
| Alibaba | Qwen3.8-Max | — | **NO_WEIGHTS** |
| Meituan | LongCat-2.5 | — | **NO_WEIGHTS** |

## Findings that surprised us

These were verified against the HF API, not taken from announcements:

1. **A vendor's license can tighten between generations.** Zhipu's `GLM-5.2` is `MIT`. The newer flagship `GLM-5.3` is `other`. Upgrading the model can mean downgrading your legal position.
2. **"Open source" sometimes means a base checkpoint.** Baidu's `ERNIE-5.5-Flash-Base` is a pre-training endpoint — 280B total / 14B active, 304 GB across 139 files. It ships without mid- or post-training. You cannot chat with it out of the box.
3. **Some headline models have no weights at all.** `Qwen3.8-Max` and `LongCat-2.5` are widely discussed as "open source flagships" in the press. Neither has a Hugging Face repo. Qwen's newest public weights are `Qwen3.8-27B` and `Qwen3.8-Flash-Next`; Meituan's are still `LongCat-2.0`.
4. **Mistral's flagship is not Apache.** `Mistral-Large-4-1T-A52B` is `other`, despite the common assumption that Mistral ships permissively.

## How it works

```
scripts/check_hf.py   # scans the HF API and regenerates data/
data/models.csv       # the table (curated flagship list, refreshed weekly)
data/new_repos.json   # any repo created in the last 14 days across tracked orgs
snapshots/            # dated markdown snapshots, for diffing over time
```

Run it yourself:

```bash
python3 scripts/check_hf.py          # refresh data
python3 scripts/check_hf.py --diff   # also report license changes since last run
```

No API key required. Requires only `python3` and `curl`.

### Why a curated list

An earlier version auto-selected "the newest repo per vendor". It surfaced OCR models, audio models and prompt-guard classifiers instead of the flagship LLMs. Automatic selection does not work for this dataset, so the flagship list is curated by hand in `scripts/check_hf.py`, while `new_repos.json` handles discovery separately. If a flagship is missing, open an issue.

## Scope and limitations

- Covers **flagship LLMs** plus a few pairs for reference (one overseas model per major lab). It is not an exhaustive index of every HF repo.
- `downloads` and `likes` are lifetime counters from HF, not weekly.
- License classification is mechanical: `mit` / `apache-2.0` / `bsd-3-clause` → `STD`, everything else → `CUSTOM`. It does not read the actual license text. **`CUSTOM` does not mean non-commercial** — it means you must read the terms.
- Parameter counts are not scraped, because HF exposes them inconsistently across architectures. Where a figure appears in the notes, it was verified manually.
- Data reflects public state at the timestamps in `checked_at`.

## Contributing

Corrections are welcome, especially:
- a flagship model that should be in the list
- a license that changed and wasn't caught
- a `CUSTOM` license you've actually read, with a one-line summary of commercial terms

Open an issue with the HF repo URL and the evidence.

## License

Data: CC0. Scripts: MIT.

---

## 中文说明

**这个仓库回答一个问题：哪些国产大模型的权重，是你真能下载来用的？**

市面上的"开源"公告口径混乱：有的放了完整权重，有的放的是个没做完后训练的 Base checkpoint，有的压根没放权重、只卖 API。这个仓库每周从 Hugging Face API 直接抓，把差别摊开。

### 三档分类

| 档位 | 含义 |
|---|---|
| `STD` | MIT / Apache-2.0 等标准开源协议，商用安全，可改可再分发 |
| `CUSTOM` | 权重能下，但许可是厂商自定义协议，**商用前必须逐条读** |
| `NO_WEIGHTS` | 没有任何公开权重，只有 API |

### 四条核实出来的结论

1. **同一家厂的许可证会收紧**：智谱 `GLM-5.2` 是 MIT，更新的旗舰 `GLM-5.3` 变成 `other`。换代可能是法律风险的降级。
2. **"开源"有时只是 Base**：百度 `ERNIE-5.5-Flash-Base` 是预训练终点，280B 总参 / 14B 激活 / 304 GB / 139 个文件，没做中训练和后训练，下载下来不能直接对话。
3. **有些头条模型根本没有权重**：`Qwen3.8-Max`、`LongCat-2.5` 被广泛当作"开源旗舰"讨论，但 HF 上没有仓库。
4. **Mistral 的旗舰不是 Apache**：`Mistral-Large-4-1T-A52B` 是 `other`，不是普遍以为的宽松协议。

### 用法

```bash
python3 scripts/check_hf.py          # 刷新数据
python3 scripts/check_hf.py --diff   # 额外报告许可证变更
```

无需 API key，只要 `python3` 和 `curl`。

### 边界

- 只覆盖**旗舰大模型**，不是全量 HF 索引
- 许可证分类是机械判定，不读协议正文；`CUSTOM` 不等于不能商用，只是要求你自己读条款
- 参数不自动抓取（HF 各架构暴露方式不一致），文中出现的数字均为人工核实

发现错漏请开 issue，附 HF 仓库链接和证据。
