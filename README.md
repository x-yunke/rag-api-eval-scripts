# 🛠️ RAG API Evaluation Scripts

## 1. 业务背景 (Background)
用于 Ascend C / CANN 智能助手 API 覆盖率评测的轻量级工具链。
核心目标：通过自动化脚本处理 L1 真实开发者语料，快速计算召回指标，辅助 PM 进行架构诊断与策略迭代。

## 2. 核心链路 (Core Pipelines)

* **`jsonl_cleaner.py` (语料降噪)**
  * **业务逻辑**：清洗 JSONL 格式的原始 Query，剔除纯符号、单字等低质量语料。
  * **防御目标**：防止“影子文档”和劣质语料污染评测基线。

* **`evaluate_top_k.py` (归因诊断)**
  * **业务逻辑**：基于打流结果，计算 Top-1 (精确命中) 与 Top-5 (召回兜底) 准确率。
  * **诊断能力**：自动归因系统缺陷。若 Top-1 与 Top-5 持平且分值偏低，系统判定为 **Indexing 物理断供**，而非 Ranking 排序问题。

## 3. 设计理念 (Design Philosophy)
* **Vibe Coding**: 探索基于 LLM 的自然语言编程范式。
* **Zero Dependency**: 纯原生 Python 实现，开箱即用，降低 PM 跨域评测的上手门槛。
