# Chinese LLM License Tracker / 大模型选型核查表

A maintained list of 23 model entries across 12 vendors: public weights, license tags, and evidence for model selection. It is a curated list, not an exhaustive catalog or a guarantee of production readiness.

**从这里开始：[大模型选型核查清单](docs/model-selection-checklist.md)** · [完整 CSV](data/models.csv) · [X 核查记录](https://x.com/zqh930514)

## 本次更新 / Current status — 2026-11-14

- Refreshed the HF metadata for all mapped repositories. Exact fetch times are in `checked_at`.
- Fixed the scanner and selected table: **LongCat-2.5 has public weights and a MIT license**. It is no longer classified as `NO_WEIGHTS` on the next refresh.
- Preserved the earlier manually maintained `license_base` field while the HF license tag is unchanged. **Preservation does not mean the LICENSE text was reviewed again today.** A license text may change without its tag changing.
- Read the fixed-version official LICENSE for Kimi K3.1-Pro and LongCat-2.5; evidence and conditions are in the [checklist](docs/model-selection-checklist.md).

### Classification / 分类口径

| Field | Meaning |
|---|---|
| `license` | The tag returned by Hugging Face; a discovery hint, not the complete agreement |
| `license_tier=STD` | Tag is MIT / Apache-2.0 / BSD-3-Clause; verify the actual text and other obligations |
| `license_tier=CUSTOM` | Nonstandard tag; **does not mean non-commercial** |
| `license_base` | Prior manual assessment: `std`, `mit-based`, `custom`; `unreviewed` if not established |
| `NO_WEIGHTS` | Curated entry without a mapped public weight repository; this is not an exhaustive search result |

Current tag counts: **12 STD, 10 CUSTOM, 1 NO_WEIGHTS**. Carried-forward `license_base` labels: 12 `std`, 6 `mit-based`, 4 `custom`, 1 unmapped. These are separate classification fields, not two conflicting counts.

### Model table

| Vendor | Model | Official repository | HF tag | Tag tier | License base |
|---|---|---|---|---|---|
| Alibaba | Qwen3.8-Flash-Next | [Qwen/Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | `other` | `CUSTOM` | `mit-based` |
| Baidu | ERNIE-5.5-Flash-Base | [baidu/ERNIE-5.5-Flash-Base](https://huggingface.co/baidu/ERNIE-5.5-Flash-Base) | `other` | `CUSTOM` | `custom` |
| Baidu | ERNIE-5.5-Flash-Base-BF16 | [baidu/ERNIE-5.5-Flash-Base-BF16](https://huggingface.co/baidu/ERNIE-5.5-Flash-Base-BF16) | `other` | `CUSTOM` | `custom` |
| Meta | Llama-3.3-70B | [meta-llama/Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) | `llama3.3` | `CUSTOM` | `custom` |
| MiniMax | M2.5 | [MiniMaxAI/MiniMax-M2.5](https://huggingface.co/MiniMaxAI/MiniMax-M2.5) | `other` | `CUSTOM` | `custom` |
| MiniMax | M3 | [MiniMaxAI/MiniMax-M3](https://huggingface.co/MiniMaxAI/MiniMax-M3) | `other` | `CUSTOM` | `mit-based` |
| Mistral | Large-4-1T-A52B | [mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) | `other` | `CUSTOM` | `mit-based` |
| Moonshot | Kimi-K3 | [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3) | `other` | `CUSTOM` | `mit-based` |
| Moonshot | Kimi-K3.1-Pro | [moonshotai/Kimi-K3.1-Pro](https://huggingface.co/moonshotai/Kimi-K3.1-Pro) | `other` | `CUSTOM` | `mit-based` |
| Zhipu | GLM-5.3 | [zai-org/GLM-5.3](https://huggingface.co/zai-org/GLM-5.3) | `other` | `CUSTOM` | `mit-based` |
| Alibaba | Qwen3.8-Max | Not mapped | `-` | `NO_WEIGHTS` | `-` |
| Alibaba | Qwen3.8-27B | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | `apache-2.0` | `STD` | `std` |
| DeepSeek | V4-Pro | [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) | `mit` | `STD` | `std` |
| DeepSeek | V4.1-Flash | [deepseek-ai/DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) | `mit` | `STD` | `std` |
| DeepSeek | V4.1-Flash-1017 | [deepseek-ai/DeepSeek-V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017) | `mit` | `STD` | `std` |
| Meituan | LongCat-2.0 | [meituan-longcat/LongCat-2.0](https://huggingface.co/meituan-longcat/LongCat-2.0) | `mit` | `STD` | `std` |
| Meituan | LongCat-2.5 | [meituan-longcat/LongCat-2.5](https://huggingface.co/meituan-longcat/LongCat-2.5) | `mit` | `STD` | `std` |
| Meituan | LongCat-Flash-Chat | [meituan-longcat/LongCat-Flash-Chat](https://huggingface.co/meituan-longcat/LongCat-Flash-Chat) | `mit` | `STD` | `std` |
| OpenAI | gpt-oss-120b | [openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b) | `apache-2.0` | `STD` | `std` |
| StepFun | Step-3.7-Flash | [stepfun-ai/Step-3.7-Flash](https://huggingface.co/stepfun-ai/Step-3.7-Flash) | `apache-2.0` | `STD` | `std` |
| Tencent | Hy-Nomas | [tencent/Hy-Nomas](https://huggingface.co/tencent/Hy-Nomas) | `apache-2.0` | `STD` | `std` |
| Zhipu | GLM-5.2 | [zai-org/GLM-5.2](https://huggingface.co/zai-org/GLM-5.2) | `mit` | `STD` | `std` |
| Zhipu | GLM-5.3-Flash | [zai-org/GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) | `mit` | `STD` | `std` |

`Qwen3.8-Max` remains an unmapped entry in this maintained list. Recheck official release channels before concluding that a model has no public weights. Repository creation, release announcements, and completion of weight uploads are different events.

## How to use this data

1. Confirm the official repository, actual weight files, access conditions, and exact revision.
2. Distinguish Base, Instruct/Chat, and supported modalities. Base models can generate continuations; they should not be assumed to provide chat or tool-use behavior out of the box.
3. Read the full LICENSE, including thresholds, attribution, territory, derivative-model conditions, and exceptions. Check filenames such as `LICENSE-MODEL` as well as `LICENSE`.
4. Verify runtime compatibility and resources. Active MoE parameters and download size are not direct measurements of inference VRAM.
5. Record dates, sources, estimates versus measurements, and corrections.

See the [checklist with fixed-version evidence](docs/model-selection-checklist.md) for the complete workflow and examples.

## Refresh / 刷新

```bash
python3 scripts/check_hf.py
python3 scripts/check_hf.py --diff
```

Requires Python 3 and curl; no API key required. The script refreshes mapped model metadata and discovers recent repositories under watched organizations. The flagship selection and unmapped entries are maintained manually.

```text
scripts/check_hf.py             metadata refresh and new-repository discovery
data/models.csv                current metadata and carried-forward manual labels
data/new_repos.json             recently created repositories for review
docs/model-selection-checklist.md  checklist and source-backed examples
snapshots/                     dated historical records
```

## Scope and limitations / 边界

- The scanner reads **tags and metadata**, not complete license text. A tag refresh does not constitute a fresh commercial-use review.
- Prior manual `license_base` labels are retained only if the tag matches. A changed tag resets the label to a tag-based `std` hint or `unreviewed`; even an unchanged tag can hide text changes, so always re-read the target revision.
- HF `downloads` and `likes` are recorded as returned by the API; do not treat them as weekly increments or unique users.
- No automatic benchmark, parameter, VRAM, or deployment validation is implied.
- Historical files under `daily/` and `snapshots/` preserve earlier observations; consult the current table and later corrections before relying on them.
- Failed fetches are marked `UNKNOWN` / `FETCH_FAILED`, not evidence of missing weights.

## 中文说明

这个仓库帮助开发者区分三个问题：**能否取得权重、是否适合目标用途、具体许可允许什么**。它不把「开源」或一个许可证标签直接等同于「可上线」。

`other` 只是线索，不等于禁止商用；MIT/Apache 也有应履行的条款。模型卡、LICENSE、部署要求和真实使用场景要一起看。

2026-11-14 修正了 LongCat-2.5 在旧 README 和刷新脚本中的过时分类，并补充核查清单。Kimi 的 2000 万美元门槛须连同 MaaS 定义、营收口径和第 4 条豁免阅读，不能省略条件。

## Contributing

Corrections are welcome. Include the official repository, revision or fixed-version source, relevant clause, and observation date. Separate what the author states from what you measured.

## License

Data: CC0. Scripts: MIT.
