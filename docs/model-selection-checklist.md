# 大模型选型核查清单 / Model selection checklist

核查方法更新：2026-11-14。每次选型都应重新读取目标版本；示例不代表所有模型。

## 1. 确认权重与版本

- 从厂商官方主页确认发布账号，再查看仓库和实际权重文件。
- 记录完整模型 ID、revision/commit SHA、核查日期和访问条件。
- 区分只有 API、公开权重、需申请访问；没有找到仓库不能直接推断从未发布。
- 仓库创建、模型发布和权重上传完成是不同事件。不要用建仓日期代替发布时间。

## 2. 确认用途与接口

- 读取模型卡，区分 Base、Instruct/Chat，以及文本/图像/音频等模态。
- Base 通常支持续写，不应默认具备对话、指令遵循或工具调用能力；是否需要后训练取决于用途。
- 检查 config、tokenizer/processor、chat template 和模型卡示例；区分作者宣称与独立实测。

## 3. 读取完整许可证

- 读取目标 revision 的 LICENSE；也检查 LICENSE-MODEL、LICENSE.txt 等文件和模型卡链接。
- HF 标签是检索线索，不能替代授权正文。`other` 不等于禁止商用。
- 分别记录授权对象、商业用途、营收口径、月活、署名、地域、再分发和衍生模型条款。
- MIT/Apache 标签不代表免除保留声明等义务，也不能单独证明整套产品可直接上线。

## 4. 估算并验证部署资源

- 记录权重精度与文件体积、运行框架版本、硬件与并行要求。
- 区分总参数、激活参数、权重显存、KV cache 和运行额外开销。
- 不把下载体积或 MoE 激活参数直接等同于推理显存。
- 量化版本要重新检查来源、兼容性、许可、质量与速度；估算和实测分开标注。

## 5. 留下可复核记录

建议每条记录采用：

| 字段 | 填写内容 |
|---|---|
| 模型 | 官方模型 ID + commit SHA |
| 核查时间 | 日期、时区 |
| 权重 | 文件证据、访问条件 |
| 用途 | Base / Instruct / 模态；依据 |
| 许可 | 正文链接、条款编号、触发条件、例外 |
| 部署 | 官方要求 / 理论估算 / 本机实测，分别注明 |
| 更新 | 前次结论、变化、原因、更正链接 |

不要用旧版本的许可结论覆盖新版本，也不要把自动标签刷新称为逐条重审。

## 两个有原文的例子（2026-11-14）

### Kimi K3.1-Pro：两个不同的营收口径

原文：[官方 LICENSE，固定版本 d9e99b0](https://huggingface.co/moonshotai/Kimi-K3.1-Pro/blob/d9e99b0792a5e93b78ea9bea62a68167e36ddd9e/LICENSE)。

- 第 2 条：经营协议定义的 Model as a Service 的主体及关联方，任意连续 12 个月合计营收超过 2000 万美元，商用前须另签协议。MaaS 定义排除部分特定功能内嵌产品和单纯请求转发。
- 第 3 条：使用该模型/衍生模型的商业产品或服务，月活超过 1 亿或月营收超过 2000 万美元，界面须显著展示模型名称。
- 第 4 条：上述第 2、3 条不适用于协议定义的内部使用，以及通过官方产品或认证推理合作伙伴访问的使用。

这些条件必须一起读，不能只写「2000 万门槛」。

### LongCat-2.5：有公开权重，标准 MIT 仍有声明义务

原文：[官方 LICENSE，固定版本 60032d9](https://huggingface.co/meituan-longcat/LongCat-2.5/blob/60032d966e6369b822f0e61d2eff01368d38b111/LICENSE)。

该版本公开仓库包含 safetensors 权重文件，LICENSE 使用标准 MIT 文本。MIT 授予使用、修改、分发和销售等权限，同时要求副本或重要部分保留版权及许可声明；包含按现状提供和免责条款。

## English summary

Check the official weights and exact revision; distinguish Base and instruction-tuned models; read the full license and its exceptions; separate deployment estimates from measurements; preserve dated evidence and corrections. A Hugging Face license tag alone is not a production-readiness or commercial-use assessment.
