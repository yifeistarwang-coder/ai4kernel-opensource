# 开源仓库索引

本索引收录 [AI4Kernel Landscape](https://github.com/yifeistarwang-coder/ai4kernel_landscape) 研究目录中**已公开开源**的全部产物。landscape 快照日期 `2026-10-30`。

> **口径说明**：本索引只收录**有可核查公开仓库地址**的条目。收录不代表代码质量、许可兼容性或可复现性已经过审阅；许可一列是 GitHub API 对仓库默认许可证的识别结果，`NOASSERTION` 表示仓库内有许可证文件但 API 未能归一化，空白表示仓库未声明许可证——使用前必须自行核对上游 `LICENSE`。

## 统计

| 维度 | 数量 |
| --- | ---: |
| GitHub 仓库（去重后） | 61 |
| HuggingFace 模型 / 数据集 | 10 |
| 其他平台仓库 | 1 |
| 合计开源产物 | 72 |

## 许可证分布

| 许可证 | 仓库数 |
| --- | ---: |
| `Apache-2.0` | 23 |
| `MIT` | 15 |
| `未声明` | 14 |
| `NOASSERTION` | 6 |
| `BSD-3-Clause` | 3 |

## 组织分布

| 组织 | 仓库数 |
| --- | ---: |
| [AMD-AGI](https://github.com/AMD-AGI) | 4 |
| [meta-pytorch](https://github.com/meta-pytorch) | 3 |
| [zhang677](https://github.com/zhang677) | 3 |
| [flagos-ai](https://github.com/flagos-ai) | 3 |
| [NVIDIA](https://github.com/NVIDIA) | 3 |
| [ScalingIntelligence](https://github.com/ScalingIntelligence) | 2 |
| [tile-ai](https://github.com/tile-ai) | 2 |
| [ornith-ai](https://github.com/ornith-ai) | 2 |
| [QiMeng-IPRC](https://github.com/QiMeng-IPRC) | 2 |
| [0satan0](https://github.com/0satan0) | 1 |
| [Anjiang-Wei](https://github.com/Anjiang-Wei) | 1 |
| [mindspore-ai](https://github.com/mindspore-ai) | 1 |
| [OptimAI-Lab](https://github.com/OptimAI-Lab) | 1 |
| [RightNow-AI](https://github.com/RightNow-AI) | 1 |
| [taratt](https://github.com/taratt) | 1 |
| [aisa-group](https://github.com/aisa-group) | 1 |
| [alibaba](https://github.com/alibaba) | 1 |
| [AMDResearch](https://github.com/AMDResearch) | 1 |
| [BonnieW05](https://github.com/BonnieW05) | 1 |
| [CUDA-Bench](https://github.com/CUDA-Bench) | 1 |
| [facebookresearch](https://github.com/facebookresearch) | 1 |
| [flashinfer-ai](https://github.com/flashinfer-ai) | 1 |
| [ISO-Bench](https://github.com/ISO-Bench) | 1 |
| [parallelcodefoundry](https://github.com/parallelcodefoundry) | 1 |
| [SakanaAI](https://github.com/SakanaAI) | 1 |
| [Snowflake-AI-Research](https://github.com/Snowflake-AI-Research) | 1 |
| [thunlp](https://github.com/thunlp) | 1 |
| [wzzll123](https://github.com/wzzll123) | 1 |
| [HazyResearch](https://github.com/HazyResearch) | 1 |
| [ROCm](https://github.com/ROCm) | 1 |
| [tensormux](https://github.com/tensormux) | 1 |
| [triton-lang](https://github.com/triton-lang) | 1 |
| [caoshiyi](https://github.com/caoshiyi) | 1 |
| [Dogacel](https://github.com/Dogacel) | 1 |
| [StigLidu](https://github.com/StigLidu) | 1 |
| [ucb-bar](https://github.com/ucb-bar) | 1 |
| [AI9Stars](https://github.com/AI9Stars) | 1 |
| [ByteDance-Seed](https://github.com/ByteDance-Seed) | 1 |
| [BytedTsinghua-SIA](https://github.com/BytedTsinghua-SIA) | 1 |
| [CSJianYang](https://github.com/CSJianYang) | 1 |
| [hgl71964](https://github.com/hgl71964) | 1 |
| [hkust-nlp](https://github.com/hkust-nlp) | 1 |
| [RLsys-Foundation](https://github.com/RLsys-Foundation) | 1 |
| [Wangyaoyuu](https://github.com/Wangyaoyuu) | 1 |
| [weich97](https://github.com/weich97) | 1 |
| [qhy991](https://github.com/qhy991) | 1 |

## 按分类

### 执行与知识底座（9）

| 仓库 | 许可 | 主语言 | 硬件 | 任务 | 星标 | 说明 |
| --- | --- | --- | --- | --- | ---: | --- |
| [flagos-ai/FlagGems](https://github.com/flagos-ai/FlagGems) | `Apache-2.0` | Python | NVIDIA、AMD、Other | PyTorch operator → Triton 实现 | 1164 | FlagGems is an operator library for large language models implemented in the Triton Language. |
| [HazyResearch/ThunderKittens](https://github.com/HazyResearch/ThunderKittens) | `MIT` | Cuda | NVIDIA | Tile 级程序 → CUDA kernel | 3786 | Tile primitives for speedy kernels |
| [meta-pytorch/tritonbench](https://github.com/meta-pytorch/tritonbench) | `BSD-3-Clause` | Python | NVIDIA、AMD | 现有算子实现 → 正确性与性能回归测试 | 374 | Tritonbench is a collection of PyTorch custom operators with example inputs to measure their performance. |
| [NVIDIA/cutlass](https://github.com/NVIDIA/cutlass) | `NOASSERTION` | C++ | NVIDIA | 布局 / tile → CUDA 线性代数 | 10679 | CUDA Templates and Python DSLs for High-Performance Linear Algebra |
| [ROCm/aiter](https://github.com/ROCm/aiter) | `MIT` | Python | AMD | AMD 推理算子 → 高性能执行 | 599 | AI Tensor Engine for ROCm |
| [tensormux/kernel-skills](https://github.com/tensormux/kernel-skills) | `MIT` | TypeScript | — | 专家规则 → Agent context | 87 | Open source skill library for AI coding agents to write, optimize, and debug high performance compute kernels … |
| [tile-ai/BitBLAS](https://github.com/tile-ai/BitBLAS) | `MIT` | Python | NVIDIA | 量化 GEMM / GEMV | 10 | ReDesign of https://github.com/microsoft/BitBLAS |
| [tile-ai/tilelang](https://github.com/tile-ai/tilelang) | `NOASSERTION` | Python | NVIDIA、AMD、Ascend、CPU、Other | Tile-level DSL → kernel | 8850 |  Domain-specific language designed to streamline the development of high-performance GPU/CPU/Accelerators kern… |
| [triton-lang/triton](https://github.com/triton-lang/triton) | `MIT` | MLIR | NVIDIA、AMD | Triton DSL → GPU kernel | 20485 | Development repository for the Triton language and compiler |

### 评测与验证（19）

| 仓库 | 许可 | 主语言 | 硬件 | 任务 | 星标 | 说明 |
| --- | --- | --- | --- | --- | ---: | --- |
| [aisa-group/InferenceBench](https://github.com/aisa-group/InferenceBench) | `Apache-2.0` | Python | NVIDIA | 目标模型与服务场景 → 优化推理服务器 | 50 | Benchmarking Open-Ended Inference Optimization by AI Agents |
| [alibaba/atrex-bench](https://github.com/alibaba/atrex-bench) | `Apache-2.0` | Python | AMD | 生产 trace → 加权 kernel 正确性与性能评测 | 38 | End-to-end benchmark for AI-generated GPU kernels, drawn from real production traces — turn a PyTorch referenc… |
| [AMDResearch/NPUEval](https://github.com/AMDResearch/NPUEval) | `—` | C++ | AMD、Other | 算子任务 → AIE C++ kernel | 34 | NPUEval is an LLM evaluation dataset written specifically to target AIE kernel code generation on RyzenAI hard… |
| [BonnieW05/KernelBenchX](https://github.com/BonnieW05/KernelBenchX) | `Apache-2.0` | Python | NVIDIA | Triton 候选 → 分类别正确性与效率评测 | 54 | KernelBenchX: A Comprehensive Benchmark for Evaluating LLM-Generated GPU Kernels |
| [CUDA-Bench/CUDABench](https://github.com/CUDA-Bench/CUDABench) | `—` | Python | NVIDIA | 自然语言 → CUDA | 20 | 以自然语言任务而非仅以高层框架代码为输入评测 CUDA 生成。 |
| [facebookresearch/kernel_bench_verified](https://github.com/facebookresearch/kernel_bench_verified) | `MIT` | Python | NVIDIA | 生成 CUDA kernel → 可靠性复核 | 16 | Welcome to KernelBench-Verified. This repository provides a robust, realistic evaluation framework for assessi… |
| [flagos-ai/KernelGenBench](https://github.com/flagos-ai/KernelGenBench) | `Apache-2.0` | Python | NVIDIA、Ascend、Other | 多来源算子 → 多硬件 Triton kernel | 25 | 以共同 Triton 目标研究算子来源和硬件平台变化时的生成能力与成本。 |
| [flashinfer-ai/flashinfer-bench](https://github.com/flashinfer-ai/flashinfer-bench) | `Apache-2.0` | Python | NVIDIA | Serving workload → kernel 评测 | 301 | Building the Virtuous Cycle for AI-driven LLM Systems |
| [ISO-Bench/ISO-Bench](https://github.com/ISO-Bench/ISO-Bench) | `Apache-2.0` | Python | NVIDIA | 代码库 + 瓶颈描述 → 推理系统优化 patch | 0 | A benchmark framework for evaluating AI agents on software performance optimization tasks |
| [meta-pytorch/BackendBench](https://github.com/meta-pytorch/BackendBench) | `BSD-3-Clause` | Python | NVIDIA | PyTorch backend → 实现与验证 | 156 | Ship correct and fast LLM kernels to PyTorch |
| [NVIDIA/compute-eval](https://github.com/NVIDIA/compute-eval) | `NOASSERTION` | Python | NVIDIA | 自然语言 → CUDA | 149 | Evaluating Large Language Models for CUDA Code Generation ComputeEval is a framework designed to generate and … |
| [NVIDIA/SOL-ExecBench](https://github.com/NVIDIA/SOL-ExecBench) | `Apache-2.0` | Python | NVIDIA | 真实模型算子 → 正确性与硬件效率评测 | 328 | A benchmark of real-world DL kernel problems  |
| [parallelcodefoundry/ParEval](https://github.com/parallelcodefoundry/ParEval) | `MIT` | C++ | CPU、NVIDIA | 任务描述 → 并行程序 | 47 | Parallel Code Evaluation Benchmark |
| [SakanaAI/robust-kbench](https://github.com/SakanaAI/robust-kbench) | `Apache-2.0` | Python | NVIDIA | PyTorch → CUDA + 稳健验证 | 107 | 围绕 Agent 生成 kernel 的稳健性、验证和优化进行评测。 |
| [ScalingIntelligence/KernelBench](https://github.com/ScalingIntelligence/KernelBench) | `NOASSERTION` | Jupyter Notebook | NVIDIA | PyTorch → GPU kernel | 1302 | KernelBench: Can LLMs Write GPU Kernels? - Benchmark + Toolkit with Torch -&gt; CUDA (+ more DSLs) |
| [Snowflake-AI-Research/fastkernels](https://github.com/Snowflake-AI-Research/fastkernels) | `Apache-2.0` | Python | NVIDIA | 生产模型模块 → kernel 生成与模型内评测 | 10 | 在生产模型接口和真实调用路径中复核生成 kernel 的有效收益。 |
| [thunlp/TritonBench](https://github.com/thunlp/TritonBench) | `Apache-2.0` | Python | NVIDIA | 自然语言 / PyTorch → Triton | 143 | TritonBench: Benchmarking Large Language Model Capabilities for Generating Triton Operators |
| [wzzll123/MultiKernelBench](https://github.com/wzzll123/MultiKernelBench) | `NOASSERTION` | Python | NVIDIA、Ascend、TPU、Intel、Other | PyTorch → 多后端 kernel | 75 | MultiArchKernelBench: A Multi-Platform Benchmark for Kernel Generation |
| [zhang677/PTXBench](https://github.com/zhang677/PTXBench) | `Apache-2.0` | Python | NVIDIA | 架构指令约束 → CUDA/PTX kernel | 37 | PTXBench: an open-source environment for kernel agents with architecture-specifc CUDA/PTX |

### 搜索与优化（4）

| 仓库 | 许可 | 主语言 | 硬件 | 任务 | 星标 | 说明 |
| --- | --- | --- | --- | --- | ---: | --- |
| [caoshiyi/K-Search](https://github.com/caoshiyi/K-Search) | `Apache-2.0` | Python | NVIDIA、Other | Serving kernel → 规划驱动搜索 | 144 | Automated High-Performance GPU Kernel Generation |
| [Dogacel/auto-gpu-kernel](https://github.com/Dogacel/auto-gpu-kernel) | `Apache-2.0` | Python | NVIDIA | 参考 kernel → 自动优化 | 317 | Winner 🏆 (Agent-only) MLSys 2026 - FlashInfer AI Kernel Generation Contest for the DeepSeek Sparse Attention (… |
| [StigLidu/AdaExplore](https://github.com/StigLidu/AdaExplore) | `MIT` | Python | NVIDIA | PyTorch → 失败记忆辅助 Triton 搜索 | 24 | [COLM-LLA 2026] The official implementation for paper "AdaExplore: Failure-Driven Adaptation and Diversity-Pre… |
| [ucb-bar/autocomp](https://github.com/ucb-bar/autocomp) | `BSD-3-Clause` | Python | NVIDIA、TPU、Trainium、CPU、Other | Kernel → 硬件特定优化 | 152 | Autocomp: Optimize any AI kernel, anywhere. |

### Agent 与环境（12）

| 仓库 | 许可 | 主语言 | 硬件 | 任务 | 星标 | 说明 |
| --- | --- | --- | --- | --- | ---: | --- |
| [0satan0/KernelMem](https://github.com/0satan0/KernelMem) | `—` | Python | NVIDIA | PyTorch → 记忆辅助 CUDA 优化 | 31 | 以长期专家知识和短期任务轨迹两层记忆协调多 Agent 生成、修复及优化 CUDA kernel。 |
| [AMD-AGI/AgentKernelArena](https://github.com/AMD-AGI/AgentKernelArena) | `Apache-2.0` | Python | AMD | Agent → GPU kernel 任务 | 123 | AgentKernelArena is a platform for evaluating and training AI agents for GPU kernel optimization, combining re… |
| [AMD-AGI/Apex](https://github.com/AMD-AGI/Apex) | `MIT` | Python | AMD | Serving bottleneck → ROCm kernel | 78 | Agents, and RL environment, for optimizing GPU kernels on AMD ROCm using LLM agents. Benchmarks LLM serving wo… |
| [AMD-AGI/GEAK](https://github.com/AMD-AGI/GEAK) | `Apache-2.0` | Python | AMD | 算子任务 → Triton | 197 | Generating Efficient AI-Centric Kernels |
| [Anjiang-Wei/Astra](https://github.com/Anjiang-Wei/Astra) | `—` | Python | NVIDIA | SGLang CUDA → 优化 CUDA | 19 | 从 SGLang 的现成 CUDA 实现出发，让专门 Agent 协作进行生成、测试、profile 和规划。 |
| [meta-pytorch/KernelAgent](https://github.com/meta-pytorch/KernelAgent) | `Apache-2.0` | Python | NVIDIA、Intel | PyTorch → 优化 GPU kernel | 610 | Autonomous GPU Kernel Generation &amp; Optimization via Deep Agents |
| [mindspore-ai/akg](https://github.com/mindspore-ai/akg) | `Apache-2.0` | Python | NVIDIA、Ascend、CPU、Other | 算子任务 → 多后端 kernel | 264 | AKG (Auto Kernel Generator) is an optimizer for operators in Deep Learning Networks, which provides the abilit… |
| [OptimAI-Lab/CudaForge](https://github.com/OptimAI-Lab/CudaForge) | `MIT` | Python | NVIDIA | PyTorch → CUDA 生成与优化 | 94 | Official Repo of CudaForge |
| [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel) | `MIT` | Python | NVIDIA | PyTorch模型 → 瓶颈提取与kernel替换 | 1614 | Autoresearch for GPU kernels. Give it any PyTorch model, go to sleep, wake up to optimized Triton kernels. |
| [taratt/cutegen](https://github.com/taratt/cutegen) | `NOASSERTION` | Python | NVIDIA | PyTorch → CuTe kernel | 7 | An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe |
| [zhang677/AccelOpt](https://github.com/zhang677/AccelOpt) | `Apache-2.0` | Python | Trainium、NVIDIA | 已有 kernel → 记忆辅助优化 | 79 | [MLSys 2026] AccelOpt: Self-improving Agents for AI Accelerator Kernel Optimization |
| [zhang677/PCL-lite](https://github.com/zhang677/PCL-lite) | `MIT` | Python | Other | ML 库任务 → STeP ASPL | 17 | [ICML 2025] Adaptive Self-improvement LLM Agentic System for ML Library Development |

### 训练、模型与数据（15）

| 仓库 | 许可 | 主语言 | 硬件 | 任务 | 星标 | 说明 |
| --- | --- | --- | --- | --- | ---: | --- |
| [AI9Stars/AutoTriton](https://github.com/AI9Stars/AutoTriton) | `—` | — | NVIDIA | PyTorch → Triton | 68 | 以监督与强化学习提高 Triton 代码生成能力。 |
| [AMD-AGI/AMDKernelVault](https://github.com/AMD-AGI/AMDKernelVault) | `Apache-2.0` | Python | AMD | PyTorch/CUDA → HIP 或 Triton | 10 | AMDKernelVault A research and engineering playground for HIP and Triton kernel generation, optimization, and L… |
| [ByteDance-Seed/cudaLLM](https://github.com/ByteDance-Seed/cudaLLM) | `Apache-2.0` | Python | NVIDIA | 自然语言/PyTorch → CUDA | 156 | 基于 Qwen3-8B 的 CUDA 专用模型，模型卡记录两阶段 SFT 与性能反馈 RL。 |
| [BytedTsinghua-SIA/CUDA-Agent](https://github.com/BytedTsinghua-SIA/CUDA-Agent) | `—` | Python | NVIDIA | PyTorch → CUDA | 1346 | CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation |
| [CSJianYang/Industrial-Coder](https://github.com/CSJianYang/Industrial-Coder) | `—` | Python | NVIDIA、Other | 工业代码 / GPU kernel 优化 | 118 | 32B 工业代码基础模型，统一芯片设计、GPU kernel、嵌入式和编译器优化等场景。 |
| [hgl71964/cuasmrl](https://github.com/hgl71964/cuasmrl) | `MIT` | C++ | NVIDIA | CUDA cubin/SASS → 调度优化 | 19 | 在 NVIDIA SASS 指令层把调度改写建模为 assembly game，以 PPO 和实机吞吐奖励优化既有 CUDA kernel。 |
| [hkust-nlp/KernelGYM](https://github.com/hkust-nlp/KernelGYM) | `—` | Python | NVIDIA | PyTorch → Triton | 216 | [KernelGYM &amp; Dr. Kernel] A distributed GPU environment and a collection of RL training methods to support … |
| [ornith-ai/CUDA-L1](https://github.com/ornith-ai/CUDA-L1) | `MIT` | Python | NVIDIA | CUDA kernel → 优化实现 | 327 | CUDA-L1: Improving CUDA Optimization via Contrastive Reinforcement Learning |
| [ornith-ai/CUDA-L2](https://github.com/ornith-ai/CUDA-L2) | `MIT` | Cuda | NVIDIA | HGEMM 配置 → 优化 CUDA kernel | 486 | CUDA-L2: Surpassing cuBLAS Performance for Matrix Multiplication through Reinforcement Learning |
| [QiMeng-IPRC/QiMeng-Kernel](https://github.com/QiMeng-IPRC/QiMeng-Kernel) | `Apache-2.0` | — | NVIDIA | PyTorch → Triton/CUDA kernel | 10 | [AAAI 2026] QiMeng-Kernel: Macro-Thinking Micro-Coding Paradigm for LLM-Based High-Performance GPU Kernel Gene… |
| [QiMeng-IPRC/QiMeng-MuPa](https://github.com/QiMeng-IPRC/QiMeng-MuPa) | `—` | Python | CPU、NVIDIA | 顺序代码 → 并行代码 | 12 | [NeurIPS 2025] QiMeng-MuPa: Mutual-Supervised Learning for Sequential-to-Parallel Code Translation |
| [RLsys-Foundation/TritonForge](https://github.com/RLsys-Foundation/TritonForge) | `—` | Python | NVIDIA、AMD | PyTorch → Triton | 153 | 🔥 LLM-powered GPU kernel synthesis: Train models to convert PyTorch ops into optimized Triton kernels via SFT+… |
| [ScalingIntelligence/kernelbench-tinker](https://github.com/ScalingIntelligence/kernelbench-tinker) | `—` | Python | NVIDIA | 模型 rollout → kernel reward | 31 | Tinker ↔ KernelBench Integration enabling RL for GPU Kernel Generation |
| [Wangyaoyuu/SparseRL](https://github.com/Wangyaoyuu/SparseRL) | `—` | Python | NVIDIA | 稀疏矩阵 → CUDA kernel | 9 | [ICLR'26 Oral] The open-source code release for the SparseRL paper ("Mastering Sparse CUDA Generation Through … |
| [weich97/NPUKernelBench](https://github.com/weich97/NPUKernelBench) | `—` | C++ | Ascend | 算子描述 → AscendC kernel | 14 | 面向昇腾 NPU 的 AscendC 生成、领域模型与评测一体化框架。 |

### 未归类（2）

| 仓库 | 许可 | 说明 |
| --- | --- | --- |
| [flagos-ai/awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) | `Apache-2.0` | Review automated kernel generation in the era of LLMs |
| [qhy991/Awesome-LLM-Kernel-Agent](https://github.com/qhy991/Awesome-LLM-Kernel-Agent) | `—` | A repository with academic works about Kernel generation with LLM Agent |

## HuggingFace 模型与数据集

模型权重与数据集同样属于开源交付物，但它们不是代码仓库，单列于此。

| 产物 | 类型 | 对应工作 | 硬件 | 说明 |
| --- | --- | --- | --- | --- |
| [amd/AIG-Datasets](https://huggingface.co/amd/AIG-Datasets) | dataset | AMDKernelVault / HIPKernelGen | AMD | 面向 AMD CDNA/ROCm 的执行验证 HIP、Triton kernel 语料与 agentic 训练框架。 |
| [ByteDance-Seed/cudaLLM-8B](https://huggingface.co/ByteDance-Seed/cudaLLM-8B) | model | cudaLLM | NVIDIA | 基于 Qwen3-8B 的 CUDA 专用模型，模型卡记录两阶段 SFT 与性能反馈 RL。 |
| [cognition-ai/Kevin-32B](https://huggingface.co/cognition-ai/Kevin-32B) | model | Kevin | NVIDIA | 用多轮强化学习训练 CUDA kernel 生成模型。 |
| [facebook/KernelLLM](https://huggingface.co/facebook/KernelLLM) | model | KernelLLM | — | 面向 PyTorch 到 Triton 转换的专用模型。 |
| [GPUMODE/KernelBook](https://huggingface.co/GPUMODE/KernelBook) | dataset | KernelBook | — | 配对 PyTorch 与 Triton 实现的代码翻译数据集。 |
| [hpcgroup/hpc-instruct](https://huggingface.co/hpcgroup/hpc-instruct) | dataset | HPC-Instruct | CPU、NVIDIA | 用于 HPC-Coder-V2 的 121,551 条合成指令数据，含代码综合、并行化、优化和执行模型翻译。 |
| [lkongam/KernelCoder](https://huggingface.co/lkongam/KernelCoder) | model | ConCuR / KernelCoder | NVIDIA | 以简洁且信息充分的推理轨迹构造 PyTorch-推理-CUDA 配对数据并训练 KernelCoder。 |
| [MooreThreads/MusaCoder-27B](https://huggingface.co/MooreThreads/MusaCoder-27B) | model | MusaCoder | NVIDIA、Other | 面向 Moore Threads GPU 的 CUDA/MUSA 原生 kernel 全栈训练框架与 27B 模型。 |
| [SakanaAI/AI-CUDA-Engineer-Archive](https://huggingface.co/SakanaAI/AI-CUDA-Engineer-Archive) | dataset | AI CUDA Engineer Archive | NVIDIA | 约三万条 Agent 生成 CUDA kernel 及 torch/NCU/Clang-tidy 轨迹，含错误、正确性和 speedup 字段。 |
| [ScalingIntelligence/kernelbench-samples](https://huggingface.co/ScalingIntelligence/kernelbench-samples) | dataset | KernelBench Samples | NVIDIA | KernelBench 实验生成样本及评测结果数据，按 baseline、重复采样和迭代 refinement 组织。 |

## 其他平台仓库

| 仓库 | 对应工作 | 说明 |
| --- | --- | --- |
| [https://gitcode.com/cann/cannbot-skills](https://gitcode.com/cann/cannbot-skills) | CANNBot-CAKE | 面向昇腾 NPU 的 CANN 原生 Agent 工作流，从自然语言或已有 AscendC 基线生成、演化并交付可部署算子。 |

## 重定向与改名

landscape 数据层里记录的仓库地址有 3 个与 GitHub 当前规范名不一致（组织改名或仓库迁移）。
GitHub 会自动重定向旧地址，但直接用规范名更可靠。

| landscape 中记录的地址 | GitHub 规范名 |
| --- | --- |
| `AMD-AGI/hip_kernel_llm_lab` | [AMD-AGI/AMDKernelVault](https://github.com/AMD-AGI/AMDKernelVault) |
| `deepreinforce-ai/CUDA-L1` | [ornith-ai/CUDA-L1](https://github.com/ornith-ai/CUDA-L1) |
| `deepreinforce-ai/CUDA-L2` | [ornith-ai/CUDA-L2](https://github.com/ornith-ai/CUDA-L2) |
