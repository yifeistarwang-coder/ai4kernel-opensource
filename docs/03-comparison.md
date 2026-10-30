# 项目对比

四个对比轴：**架构**（项目怎么搭）、**基础**（构建在什么之上）、**硬件厂商**（跑在谁的芯片上）、**硬件架构**（具体到哪一代芯片）。

表中每一格都来自可核查的公开材料：架构列来自仓库 README 与顶层目录结构，基础列来自仓库声明的依赖关系，硬件两列来自仓库文档与任务说明。空白表示公开材料未标注，不等于不支持。

## 架构对比

### 架构模式分布

| 架构模式 | 项目数 |
| --- | ---: |
| 单脚本编排 + 长短期记忆库 + NCU/NSYS 剖析驱动的多轮自进化 | 1 |
| 受控实验平台: 统一任务契约 + 多 agent 适配层 + 独立评测打分 + A/B 对照 | 1 |
| 端到端优化流水线: benchmark-identify-optimize-grade-integrate + 知识库回注 | 1 |
| 确定性 JS 编排 + 分层多 agent（Director→TechLead→专家工程师） | 1 |
| 单脚本多 agent 循环 + 基线对比（compare-kind 参数化分支） | 1 |
| 分层多 Agent 流水线: 静态路由-子图融合-并行生成-端到端组合 + 硬件引导优化环 | 1 |
| 编译器主线 + 大模型 Agent 副线的双子项目仓库 (AKG-MLIR / AKG-AGENT) | 1 |
| 单入口 Python 多智能体循环: 生成 kernel - 测正确性 - 分析硬件反馈 - 迭代改进 | 1 |
| 固定评测 + 编辑-评测-保留/回滚 循环，单文件作用域 + Amdahl 定律调度 | 1 |
| 生成-测试-修正循环 + 节点持久化 (generate-test-refine, 延迟 profiling) | 1 |
| 自改进 Agent 循环 + 优化记忆库 + 结构化 kernel 数据库 + profiling 服务 | 1 |
| 自适应自改进 Agent + 结构化 IR（benchcard）+ 脚本化实验矩阵 | 1 |
| 容器隔离 + 批调度作业: agent 写 launcher → 容器内评测速度与质量 → LLM 裁判审查 | 1 |
| 三段式评测: compile → correctness → performance(SOL)，生成与评测分会话隔离 | 1 |
| 评测三段式: 提示生成脚本 + 功能测试脚本（生成与评测解耦） | 1 |
| 评测三段式: call→exe→perf 分阶段流水线 + 机器级 golden 基线 | 1 |
| 评测三段式: dataset-generate-evaluate（编译 + ncu 剖析） | 1 |
| 扩展评测框架: 复用 KernelBench + TF32 基线 + 隐藏测试门控 + 交互式排行榜 | 1 |
| 多来源算子集 + 双赛道（LLM Pass@K / Agent 迭代）+ 多芯片后端 | 1 |
| 数据集 + 固定 Schema 驱动的 pypi 基准套件 | 1 |
| 评测三段式: 提交挖掘造题(commit→LLM 测试) - agent 运行 CLI(plan/prepare/report) - 三方性能对比 | 1 |
| PyTorch 后端目录约定 + 三套测试套件 (smoke/opinfo/torchbench) 动态替换算子 | 1 |
| datapack 版本化题库 + Podman 沙箱评测 + 单发与 agent 两种生成器 | 1 |
| 问题目录格式 (definition+workload) + 容器内 CLI 评测 + roofline 式 SOL-Score 排名 | 1 |
| 离线三段式流水线: prompts → generate → drivers → analysis | 1 |
| 任务目录 + 六重过滤校验 + 组件化并行评测 API | 1 |
| 评测三段式: 数据集-prompt-生成器 与 评测脚本 分离 + 离线结果分析 | 1 |
| 四级抽象 L1-L4 + baseline/candidate 槽位替换 + benchmark-serve 一体 | 1 |
| 双通道评测 (生成式 G / 任务式 T) + 三段式打分: 调用准确-执行准确-性能效率 | 1 |
| 基准四件套: 任务数据集 + prompt 策略插件 + 参考实现 + 后端评测插件 | 1 |
| Profiling 服务 + 双通道 agent（多轮模型循环 / 编码代理网关）+ Fixit 与 KernelGen 两条 SFT 数据线 | 1 |
| 后端中立的 Triton 算子库 + ATen 注册层 + 多后端分发 | 1 |
| header-only CUDA DSL: tile 原语 + Load-Store-Compute-Finish 生产者/消费者模板 | 1 |
| 算子级基准套件 + git submodule 复用第三方 kernel 实现 | 1 |
| header-only C++ 模板库 + 同构 Python DSL (CuTe DSL) 的双语言栈 | 1 |
| 多后端算子库: Triton/CK/ASM/Opus/FlyDSL 并存 + 统一 C++ 与 Python API | 1 |
| Markdown 技能库为真源 + JSON Schema 元数据 + 构建期索引生成 + npm 分发 (CLI 与 TS API) | 1 |
| 算子库 + MatmulConfig 描述层 + DSL 定制 + 多框架集成 + benchmark 目录 | 1 |
| DSL 前端 + TVM 多级 IR 编译管线 + 可插拔后端注册表 + 示例/调试工具库 | 1 |
| Python 前端 + MLIR/LLVM 后端 + 解释器旁路 + 环境变量驱动调试 | 1 |
| 世界模型引导的迭代优化: 生成器 + 共演化世界模型 + 任务后端适配层 | 1 |
| 双 CLI 分层: 优化 agent(kopt) + 验证基准(kbench)，共用统一 BenchmarkAdapter | 1 |
| 两阶段: Adapt(合成任务-失败蒸馏-技能记忆) + Explore(MCTS 树搜索) | 1 |
| Agent 工具循环 + 束搜索 + 可插拔硬件目标（agent/backend/hw_config 三件套） | 1 |
| 两段式训练: SFT 打底 + GRPO 强化学习（规则奖励 + 执行奖励顺序叠加） | 1 |
| 全栈训练框架: CPT-SFT-RL 三段流水线 + 数据生成器 + 独立验证服务 | 1 |
| 两段式训练: SFT → RL（编译+测试结果作奖励） | 1 |
| 标准化 agent 工作区模板: 实现-编译-校验-剖析 四步自愈循环 | 1 |
| 通用工业代码基础模型: Code-Flow 三段训练 + 多领域工业仿真环境 | 1 |
| Triton 编译器主仓 + 附加 cuasmrl 包的 fork 结构 | 1 |
| 评测服务三段式: API-任务队列-GPU worker，外加可插拔 backend/toolkit/workflow 三层抽象 | 1 |
| 对比式 RL 训练 + 产物仓库 (逐行 JSON 记录 ref/custom/cuda_graph 代码与四组 score) | 1 |
| RL 产出的 kernel 资产库 + 离线/服务器双模式评测脚本（对标 cuBLAS 系列） | 1 |
| 训练-推理-评测三段脚本化流水线 (train / inference / eval_generations) | 1 |
| 互监督双阶段: co-verify (翻译与单测互相验证造数据) - co-evolve (用该数据微调) | 1 |
| 全栈训练框架: 同一 SLIME 框架承载 SFT-RL 两段 + 独立 KBenchEval 评测目录 | 1 |
| RL 闭环: Tinker Env 单轮交互 + Modal 远程评测 + 奖励整形 | 1 |
| 预训练-SFT-PPO 三段式 + 编译器/执行器反馈的层次奖励 | 1 |
| 评测三段式: prompt 生成 → CANN 编译 → 数值比对（可选性能） | 1 |
| 纯文档分类清单: 按 taxonomy 分层索引条目 | 1 |
| YAML 数据源 + Makefile 渲染 Mermaid 分类图/时间线 + 标记区块自动回写 README | 1 |

### 项目角色分布

| 角色 | 项目数 |
| --- | ---: |
| 评测基准 | 21 |
| Agent 搜索循环 | 15 |
| 训练流水线 | 9 |
| 数据集 / 模型 | 5 |
| DSL / kernel 表达层 | 4 |
| 执行运行时底座 | 3 |
| 编译器底座 | 2 |
| 综述清单 | 2 |

### 全量对照

| 项目 | 角色 | 架构模式 | 评测 | Agent 循环 | 验证机制 |
| --- | --- | --- | --- | --- | --- |
| [flagos-ai/FlagGems](https://github.com/flagos-ai/FlagGems) | 执行运行时底座 | 后端中立的 Triton 算子库 + ATen 注册层 + 多后端分发 | 无 | 无 | — |
| [HazyResearch/ThunderKittens](https://github.com/HazyResearch/ThunderKittens) | DSL / kernel 表达层 | header-only CUDA DSL: tile 原语 + Load-Store-Compute-Finish 生产者/消费者模板 | 有 | 无 | compile、correctness、runtime |
| [meta-pytorch/tritonbench](https://github.com/meta-pytorch/tritonbench) | 评测基准 | 算子级基准套件 + git submodule 复用第三方 kernel 实现 | 有 | 无 | runtime |
| [NVIDIA/cutlass](https://github.com/NVIDIA/cutlass) | DSL / kernel 表达层 | header-only C++ 模板库 + 同构 Python DSL (CuTe DSL) 的双语言栈 | 有 | 无 | compile、correctness、runtime、profile |
| [ROCm/aiter](https://github.com/ROCm/aiter) | 执行运行时底座 | 多后端算子库: Triton/CK/ASM/Opus/FlyDSL 并存 + 统一 C++ 与 Python API | 有 | 无 | compile、correctness、runtime |
| [tensormux/kernel-skills](https://github.com/tensormux/kernel-skills) | 数据集 / 模型 | Markdown 技能库为真源 + JSON Schema 元数据 + 构建期索引生成 + npm 分发 (CLI 与 TS API) | 无 | 无 | static-check |
| [tile-ai/BitBLAS](https://github.com/tile-ai/BitBLAS) | 执行运行时底座 | 算子库 + MatmulConfig 描述层 + DSL 定制 + 多框架集成 + benchmark 目录 | 有 | 无 | compile、correctness |
| [tile-ai/tilelang](https://github.com/tile-ai/tilelang) | DSL / kernel 表达层 | DSL 前端 + TVM 多级 IR 编译管线 + 可插拔后端注册表 + 示例/调试工具库 | 有 | 无 | compile、correctness |
| [triton-lang/triton](https://github.com/triton-lang/triton) | DSL / kernel 表达层 | Python 前端 + MLIR/LLVM 后端 + 解释器旁路 + 环境变量驱动调试 | 有 | 无 | compile、correctness |
| [aisa-group/InferenceBench](https://github.com/aisa-group/InferenceBench) | 评测基准 | 容器隔离 + 批调度作业: agent 写 launcher → 容器内评测速度与质量 → LLM 裁判审查 | 有 | 有 | correctness、runtime、contract |
| [alibaba/atrex-bench](https://github.com/alibaba/atrex-bench) | 评测基准 | 三段式评测: compile → correctness → performance(SOL)，生成与评测分会话隔离 | 有 | 无 | compile、correctness、runtime、static-check |
| [AMDResearch/NPUEval](https://github.com/AMDResearch/NPUEval) | 评测基准 | 评测三段式: 提示生成脚本 + 功能测试脚本（生成与评测解耦） | 有 | 有 | compile、correctness |
| [BonnieW05/KernelBenchX](https://github.com/BonnieW05/KernelBenchX) | 评测基准 | 评测三段式: call→exe→perf 分阶段流水线 + 机器级 golden 基线 | 有 | 无 | compile、correctness、runtime |
| [CUDA-Bench/CUDABench](https://github.com/CUDA-Bench/CUDABench) | 评测基准 | 评测三段式: dataset-generate-evaluate（编译 + ncu 剖析） | 有 | 无 | compile、correctness、runtime、profile |
| [facebookresearch/kernel_bench_verified](https://github.com/facebookresearch/kernel_bench_verified) | 评测基准 | 扩展评测框架: 复用 KernelBench + TF32 基线 + 隐藏测试门控 + 交互式排行榜 | 有 | 无 | correctness、runtime |
| [flagos-ai/KernelGenBench](https://github.com/flagos-ai/KernelGenBench) | 评测基准 | 多来源算子集 + 双赛道（LLM Pass@K / Agent 迭代）+ 多芯片后端 | 有 | 无 | correctness |
| [flashinfer-ai/flashinfer-bench](https://github.com/flashinfer-ai/flashinfer-bench) | 评测基准 | 数据集 + 固定 Schema 驱动的 pypi 基准套件 | 有 | 无 | — |
| [ISO-Bench/ISO-Bench](https://github.com/ISO-Bench/ISO-Bench) | 评测基准 | 评测三段式: 提交挖掘造题(commit→LLM 测试) - agent 运行 CLI(plan/prepare/report) - 三方性能对比 | 有 | 无 | correctness、runtime |
| [meta-pytorch/BackendBench](https://github.com/meta-pytorch/BackendBench) | 评测基准 | PyTorch 后端目录约定 + 三套测试套件 (smoke/opinfo/torchbench) 动态替换算子 | 有 | 无 | compile、correctness、runtime |
| [NVIDIA/compute-eval](https://github.com/NVIDIA/compute-eval) | 评测基准 | datapack 版本化题库 + Podman 沙箱评测 + 单发与 agent 两种生成器 | 有 | 有 | compile、correctness、runtime、static-check、profile |
| [NVIDIA/SOL-ExecBench](https://github.com/NVIDIA/SOL-ExecBench) | 评测基准 | 问题目录格式 (definition+workload) + 容器内 CLI 评测 + roofline 式 SOL-Score 排名 | 有 | 无 | compile、correctness、runtime |
| [parallelcodefoundry/ParEval](https://github.com/parallelcodefoundry/ParEval) | 评测基准 | 离线三段式流水线: prompts → generate → drivers → analysis | 有 | 无 | compile、runtime |
| [SakanaAI/robust-kbench](https://github.com/SakanaAI/robust-kbench) | 评测基准 | 任务目录 + 六重过滤校验 + 组件化并行评测 API | 有 | 无 | compile、correctness、runtime、static-check、profile |
| [ScalingIntelligence/KernelBench](https://github.com/ScalingIntelligence/KernelBench) | 评测基准 | 评测三段式: 数据集-prompt-生成器 与 评测脚本 分离 + 离线结果分析 | 有 | 无 | compile、correctness、runtime |
| [Snowflake-AI-Research/fastkernels](https://github.com/Snowflake-AI-Research/fastkernels) | 评测基准 | 四级抽象 L1-L4 + baseline/candidate 槽位替换 + benchmark-serve 一体 | 有 | 无 | correctness、runtime |
| [thunlp/TritonBench](https://github.com/thunlp/TritonBench) | 评测基准 | 双通道评测 (生成式 G / 任务式 T) + 三段式打分: 调用准确-执行准确-性能效率 | 有 | 无 | compile、correctness、runtime |
| [wzzll123/MultiKernelBench](https://github.com/wzzll123/MultiKernelBench) | 评测基准 | 基准四件套: 任务数据集 + prompt 策略插件 + 参考实现 + 后端评测插件 | 有 | 无 | compile、correctness、runtime、static-check |
| [zhang677/PTXBench](https://github.com/zhang677/PTXBench) | Agent 搜索循环 | Profiling 服务 + 双通道 agent（多轮模型循环 / 编码代理网关）+ Fixit 与 KernelGen 两条 SFT 数据线 | 有 | 有 | compile、correctness、runtime、profile |
| [caoshiyi/K-Search](https://github.com/caoshiyi/K-Search) | Agent 搜索循环 | 世界模型引导的迭代优化: 生成器 + 共演化世界模型 + 任务后端适配层 | 有 | 有 | correctness、runtime |
| [Dogacel/auto-gpu-kernel](https://github.com/Dogacel/auto-gpu-kernel) | Agent 搜索循环 | 双 CLI 分层: 优化 agent(kopt) + 验证基准(kbench)，共用统一 BenchmarkAdapter | 有 | 有 | compile、correctness、runtime |
| [StigLidu/AdaExplore](https://github.com/StigLidu/AdaExplore) | Agent 搜索循环 | 两阶段: Adapt(合成任务-失败蒸馏-技能记忆) + Explore(MCTS 树搜索) | 有 | 有 | compile、correctness、runtime |
| [ucb-bar/autocomp](https://github.com/ucb-bar/autocomp) | Agent 搜索循环 | Agent 工具循环 + 束搜索 + 可插拔硬件目标（agent/backend/hw_config 三件套） | 有 | 有 | compile、runtime |
| [0satan0/KernelMem](https://github.com/0satan0/KernelMem) | Agent 搜索循环 | 单脚本编排 + 长短期记忆库 + NCU/NSYS 剖析驱动的多轮自进化 | 有 | 有 | compile、correctness、runtime、profile |
| [AMD-AGI/AgentKernelArena](https://github.com/AMD-AGI/AgentKernelArena) | 评测基准 | 受控实验平台: 统一任务契约 + 多 agent 适配层 + 独立评测打分 + A/B 对照 | 有 | 有 | compile、correctness、runtime |
| [AMD-AGI/Apex](https://github.com/AMD-AGI/Apex) | Agent 搜索循环 | 端到端优化流水线: benchmark-identify-optimize-grade-integrate + 知识库回注 | 有 | 有 | compile、correctness、runtime、static-check |
| [AMD-AGI/GEAK](https://github.com/AMD-AGI/GEAK) | Agent 搜索循环 | 确定性 JS 编排 + 分层多 agent（Director→TechLead→专家工程师） | 有 | 有 | compile、correctness、runtime |
| [Anjiang-Wei/Astra](https://github.com/Anjiang-Wei/Astra) | Agent 搜索循环 | 单脚本多 agent 循环 + 基线对比（compare-kind 参数化分支） | 有 | 有 | correctness、runtime |
| [meta-pytorch/KernelAgent](https://github.com/meta-pytorch/KernelAgent) | Agent 搜索循环 | 分层多 Agent 流水线: 静态路由-子图融合-并行生成-端到端组合 + 硬件引导优化环 | 有 | 有 | compile、correctness、runtime、profile |
| [mindspore-ai/akg](https://github.com/mindspore-ai/akg) | 编译器底座 | 编译器主线 + 大模型 Agent 副线的双子项目仓库 (AKG-MLIR / AKG-AGENT) | 有 | 有 | compile |
| [OptimAI-Lab/CudaForge](https://github.com/OptimAI-Lab/CudaForge) | Agent 搜索循环 | 单入口 Python 多智能体循环: 生成 kernel - 测正确性 - 分析硬件反馈 - 迭代改进 | 有 | 有 | compile、correctness、runtime、profile |
| [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel) | Agent 搜索循环 | 固定评测 + 编辑-评测-保留/回滚 循环，单文件作用域 + Amdahl 定律调度 | 有 | 有 | compile、correctness、runtime、profile |
| [taratt/cutegen](https://github.com/taratt/cutegen) | Agent 搜索循环 | 生成-测试-修正循环 + 节点持久化 (generate-test-refine, 延迟 profiling) | 有 | 有 | compile、correctness、runtime、profile |
| [zhang677/AccelOpt](https://github.com/zhang677/AccelOpt) | Agent 搜索循环 | 自改进 Agent 循环 + 优化记忆库 + 结构化 kernel 数据库 + profiling 服务 | 有 | 有 | runtime、profile |
| [zhang677/PCL-lite](https://github.com/zhang677/PCL-lite) | Agent 搜索循环 | 自适应自改进 Agent + 结构化 IR（benchcard）+ 脚本化实验矩阵 | 有 | 有 | static-check、correctness |
| [AI9Stars/AutoTriton](https://github.com/AI9Stars/AutoTriton) | 数据集 / 模型 | 两段式训练: SFT 打底 + GRPO 强化学习（规则奖励 + 执行奖励顺序叠加） | 无 | 无 | none |
| [AMD-AGI/AMDKernelVault](https://github.com/AMD-AGI/AMDKernelVault) | 训练流水线 | 全栈训练框架: CPT-SFT-RL 三段流水线 + 数据生成器 + 独立验证服务 | 有 | 有 | compile、correctness、runtime |
| [ByteDance-Seed/cudaLLM](https://github.com/ByteDance-Seed/cudaLLM) | 训练流水线 | 两段式训练: SFT → RL（编译+测试结果作奖励） | 有 | 无 | compile、correctness |
| [BytedTsinghua-SIA/CUDA-Agent](https://github.com/BytedTsinghua-SIA/CUDA-Agent) | 数据集 / 模型 | 标准化 agent 工作区模板: 实现-编译-校验-剖析 四步自愈循环 | 有 | 有 | compile、correctness、runtime、profile |
| [CSJianYang/Industrial-Coder](https://github.com/CSJianYang/Industrial-Coder) | 数据集 / 模型 | 通用工业代码基础模型: Code-Flow 三段训练 + 多领域工业仿真环境 | 无 | 有 | compile、correctness、runtime |
| [hgl71964/cuasmrl](https://github.com/hgl71964/cuasmrl) | 编译器底座 | Triton 编译器主仓 + 附加 cuasmrl 包的 fork 结构 | 无 | 无 | none |
| [hkust-nlp/KernelGYM](https://github.com/hkust-nlp/KernelGYM) | 训练流水线 | 评测服务三段式: API-任务队列-GPU worker，外加可插拔 backend/toolkit/workflow 三层抽象 | 有 | 有 | compile、correctness、runtime |
| [ornith-ai/CUDA-L1](https://github.com/ornith-ai/CUDA-L1) | 训练流水线 | 对比式 RL 训练 + 产物仓库 (逐行 JSON 记录 ref/custom/cuda_graph 代码与四组 score) | 有 | 无 | runtime |
| [ornith-ai/CUDA-L2](https://github.com/ornith-ai/CUDA-L2) | 数据集 / 模型 | RL 产出的 kernel 资产库 + 离线/服务器双模式评测脚本（对标 cuBLAS 系列） | 有 | 无 | compile、runtime |
| [QiMeng-IPRC/QiMeng-Kernel](https://github.com/QiMeng-IPRC/QiMeng-Kernel) | 训练流水线 | 训练-推理-评测三段脚本化流水线 (train / inference / eval_generations) | 有 | 无 | none |
| [QiMeng-IPRC/QiMeng-MuPa](https://github.com/QiMeng-IPRC/QiMeng-MuPa) | 训练流水线 | 互监督双阶段: co-verify (翻译与单测互相验证造数据) - co-evolve (用该数据微调) | 有 | 无 | correctness、runtime |
| [RLsys-Foundation/TritonForge](https://github.com/RLsys-Foundation/TritonForge) | 训练流水线 | 全栈训练框架: 同一 SLIME 框架承载 SFT-RL 两段 + 独立 KBenchEval 评测目录 | 有 | 有 | compile、correctness、runtime |
| [ScalingIntelligence/kernelbench-tinker](https://github.com/ScalingIntelligence/kernelbench-tinker) | 训练流水线 | RL 闭环: Tinker Env 单轮交互 + Modal 远程评测 + 奖励整形 | 有 | 无 | compile、correctness、runtime、static-check |
| [Wangyaoyuu/SparseRL](https://github.com/Wangyaoyuu/SparseRL) | 训练流水线 | 预训练-SFT-PPO 三段式 + 编译器/执行器反馈的层次奖励 | 有 | 无 | compile、correctness、runtime |
| [weich97/NPUKernelBench](https://github.com/weich97/NPUKernelBench) | 评测基准 | 评测三段式: prompt 生成 → CANN 编译 → 数值比对（可选性能） | 有 | 无 | compile、correctness、runtime |
| [flagos-ai/awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation) | 综述清单 | 纯文档分类清单: 按 taxonomy 分层索引条目 | 无 | 无 | — |
| [qhy991/Awesome-LLM-Kernel-Agent](https://github.com/qhy991/Awesome-LLM-Kernel-Agent) | 综述清单 | YAML 数据源 + Makefile 渲染 Mermaid 分类图/时间线 + 标记区块自动回写 README | 无 | 无 | none |

## 基础层对比

「基础」指项目直接构建其上的 kernel 表达层或运行时。同一个项目可能同时依赖多个（例如以 Triton 为主、同时支持 CUDA C++ 兜底）。

| 基础层 | 项目数 | 使用该基础的项目 |
| --- | ---: | --- |
| torch | 35 | `0satan0/KernelMem`、`AMD-AGI/AMDKernelVault`、`AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`ByteDance-Seed/cudaLLM`、`BytedTsinghua-SIA/CUDA-Agent`、`CSJianYang/Industrial-Coder`、`NVIDIA/SOL-ExecBench`、`NVIDIA/compute-eval`、`OptimAI-Lab/CudaForge`、`RLsys-Foundation/TritonForge`、`ROCm/aiter`、`RightNow-AI/autokernel`、`SakanaAI/robust-kbench`、`ScalingIntelligence/KernelBench`、`ScalingIntelligence/kernelbench-tinker`、`Snowflake-AI-Research/fastkernels`、`StigLidu/AdaExplore`、`aisa-group/InferenceBench`、`alibaba/atrex-bench`、`caoshiyi/K-Search`、`facebookresearch/kernel_bench_verified`、`flagos-ai/FlagGems`、`flagos-ai/KernelGenBench`、`hkust-nlp/KernelGYM`、`meta-pytorch/BackendBench`、`meta-pytorch/KernelAgent`、`meta-pytorch/tritonbench`、`ornith-ai/CUDA-L1`、`ornith-ai/CUDA-L2`、`thunlp/TritonBench`、`tile-ai/BitBLAS`、`weich97/NPUKernelBench`、`wzzll123/MultiKernelBench` |
| Triton | 28 | `AI9Stars/AutoTriton`、`AMD-AGI/AMDKernelVault`、`AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`BonnieW05/KernelBenchX`、`CSJianYang/Industrial-Coder`、`NVIDIA/SOL-ExecBench`、`RLsys-Foundation/TritonForge`、`ROCm/aiter`、`RightNow-AI/autokernel`、`ScalingIntelligence/KernelBench`、`Snowflake-AI-Research/fastkernels`、`StigLidu/AdaExplore`、`alibaba/atrex-bench`、`caoshiyi/K-Search`、`flagos-ai/FlagGems`、`flagos-ai/KernelGenBench`、`hgl71964/cuasmrl`、`hkust-nlp/KernelGYM`、`meta-pytorch/KernelAgent`、`meta-pytorch/tritonbench`、`mindspore-ai/akg`、`taratt/cutegen`、`tensormux/kernel-skills`、`thunlp/TritonBench`、`zhang677/AccelOpt`、`zhang677/PTXBench` |
| CUDA-C++ | 27 | `0satan0/KernelMem`、`Anjiang-Wei/Astra`、`ByteDance-Seed/cudaLLM`、`BytedTsinghua-SIA/CUDA-Agent`、`CSJianYang/Industrial-Coder`、`CUDA-Bench/CUDABench`、`HazyResearch/ThunderKittens`、`NVIDIA/SOL-ExecBench`、`NVIDIA/compute-eval`、`NVIDIA/cutlass`、`OptimAI-Lab/CudaForge`、`RightNow-AI/autokernel`、`SakanaAI/robust-kbench`、`ScalingIntelligence/KernelBench`、`ScalingIntelligence/kernelbench-tinker`、`Snowflake-AI-Research/fastkernels`、`Wangyaoyuu/SparseRL`、`caoshiyi/K-Search`、`facebookresearch/kernel_bench_verified`、`hgl71964/cuasmrl`、`hkust-nlp/KernelGYM`、`ornith-ai/CUDA-L1`、`ornith-ai/CUDA-L2`、`parallelcodefoundry/ParEval`、`taratt/cutegen`、`tensormux/kernel-skills`、`zhang677/PTXBench` |
| HIP | 8 | `AMD-AGI/AMDKernelVault`、`AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`ROCm/aiter`、`ScalingIntelligence/KernelBench`、`parallelcodefoundry/ParEval`、`tensormux/kernel-skills` |
| vLLM | 8 | `AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`ISO-Bench/ISO-Bench`、`QiMeng-IPRC/QiMeng-MuPa`、`aisa-group/InferenceBench`、`tensormux/kernel-skills`、`ucb-bar/autocomp` |
| SGLang | 7 | `AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`Anjiang-Wei/Astra`、`ISO-Bench/ISO-Bench`、`RLsys-Foundation/TritonForge`、`aisa-group/InferenceBench` |
| CUTLASS | 7 | `NVIDIA/SOL-ExecBench`、`NVIDIA/compute-eval`、`ScalingIntelligence/KernelBench`、`alibaba/atrex-bench`、`meta-pytorch/tritonbench`、`ornith-ai/CUDA-L2`、`taratt/cutegen` |
| torch.compile | 4 | `BytedTsinghua-SIA/CUDA-Agent`、`SakanaAI/robust-kbench`、`alibaba/atrex-bench`、`hkust-nlp/KernelGYM` |
| FlashInfer | 3 | `Dogacel/auto-gpu-kernel`、`flashinfer-ai/flashinfer-bench`、`zhang677/AccelOpt` |
| AITer | 2 | `AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex` |
| MLIR | 2 | `mindspore-ai/akg`、`triton-lang/triton` |
| PyTorch-ATen | 2 | `flagos-ai/FlagGems`、`meta-pytorch/BackendBench` |
| TileLang | 2 | `ScalingIntelligence/KernelBench`、`tile-ai/BitBLAS` |
| AKG | 1 | `mindspore-ai/akg` |
| ThunderKittens | 1 | `ScalingIntelligence/KernelBench` |
| TVM | 1 | `tile-ai/tilelang` |
| LLVM | 1 | `triton-lang/triton` |
| AscendC | 1 | `weich97/NPUKernelBench` |

### 项目之间的依赖

上表讲的是「构建在哪个底座上」，这里讲的是「直接依赖哪个项目」。依赖方向几乎全是单向的：生成类项目依赖评测类项目，评测类项目不依赖生成类项目。

| 依赖方仓库 | 关系 | 被依赖的工作 |
| --- | --- | --- |
| [0satan0/KernelMem](https://github.com/0satan0/KernelMem) | `evaluated_on` | `kernelbench` |
| [ByteDance-Seed/cudaLLM](https://github.com/ByteDance-Seed/cudaLLM) | `evaluated_on` | `kernelbench` |
| [OptimAI-Lab/CudaForge](https://github.com/OptimAI-Lab/CudaForge) | `evaluated_on` | `kernelbench` |
| [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel) | `uses` | `kernelbench` |
| [StigLidu/AdaExplore](https://github.com/StigLidu/AdaExplore) | `evaluated_on` | `kernelbench` |
| [caoshiyi/K-Search](https://github.com/caoshiyi/K-Search) | `evaluated_on` | `kernelbench` |
| [mindspore-ai/akg](https://github.com/mindspore-ai/akg) | `evaluated_on` | `kernelbench` |
| [taratt/cutegen](https://github.com/taratt/cutegen) | `evaluated_on` | `kernelbench` |
| [zhang677/AccelOpt](https://github.com/zhang677/AccelOpt) | `evaluated_on` | `flashinfer-bench` |

被依赖最多的是 `kernelbench`（8 次）、`flashinfer-bench`（1 次）。这说明大部分生成系统的能力度量，最终都落在同一个公共任务集上。

## 硬件厂商对比

厂商维度回答的是「这条路在哪个生态里被验证过」。非 NVIDIA 生态的项目数量明显更少，且多数集中在评测而非生成闭环。

| 厂商 | 项目数 | 项目 |
| --- | ---: | --- |
| NVIDIA | 49 | `0satan0/KernelMem`、`AI9Stars/AutoTriton`、`Anjiang-Wei/Astra`、`BonnieW05/KernelBenchX`、`ByteDance-Seed/cudaLLM`、`BytedTsinghua-SIA/CUDA-Agent`、`CSJianYang/Industrial-Coder`、`CUDA-Bench/CUDABench`、`Dogacel/auto-gpu-kernel`、`HazyResearch/ThunderKittens`、`ISO-Bench/ISO-Bench`、`NVIDIA/SOL-ExecBench`、`NVIDIA/compute-eval`、`NVIDIA/cutlass`、`OptimAI-Lab/CudaForge`、`QiMeng-IPRC/QiMeng-Kernel`、`QiMeng-IPRC/QiMeng-MuPa`、`RLsys-Foundation/TritonForge`、`RightNow-AI/autokernel`、`SakanaAI/robust-kbench`、`ScalingIntelligence/KernelBench`、`ScalingIntelligence/kernelbench-tinker`、`Snowflake-AI-Research/fastkernels`、`StigLidu/AdaExplore`、`Wangyaoyuu/SparseRL`、`aisa-group/InferenceBench`、`caoshiyi/K-Search`、`facebookresearch/kernel_bench_verified`、`flagos-ai/FlagGems`、`flagos-ai/KernelGenBench`、`flashinfer-ai/flashinfer-bench`、`hgl71964/cuasmrl`、`hkust-nlp/KernelGYM`、`meta-pytorch/BackendBench`、`meta-pytorch/KernelAgent`、`meta-pytorch/tritonbench`、`mindspore-ai/akg`、`ornith-ai/CUDA-L1`、`ornith-ai/CUDA-L2`、`parallelcodefoundry/ParEval`、`taratt/cutegen`、`thunlp/TritonBench`、`tile-ai/BitBLAS`、`tile-ai/tilelang`、`triton-lang/triton`、`ucb-bar/autocomp`、`wzzll123/MultiKernelBench`、`zhang677/AccelOpt`、`zhang677/PTXBench` |
| AMD | 12 | `AMD-AGI/AMDKernelVault`、`AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`AMDResearch/NPUEval`、`RLsys-Foundation/TritonForge`、`ROCm/aiter`、`alibaba/atrex-bench`、`flagos-ai/FlagGems`、`meta-pytorch/tritonbench`、`tile-ai/tilelang`、`triton-lang/triton` |
| 其他 | 10 | `AMDResearch/NPUEval`、`CSJianYang/Industrial-Coder`、`caoshiyi/K-Search`、`flagos-ai/FlagGems`、`flagos-ai/KernelGenBench`、`mindspore-ai/akg`、`tile-ai/tilelang`、`ucb-bar/autocomp`、`wzzll123/MultiKernelBench`、`zhang677/PCL-lite` |
| 华为昇腾 | 5 | `flagos-ai/KernelGenBench`、`mindspore-ai/akg`、`tile-ai/tilelang`、`weich97/NPUKernelBench`、`wzzll123/MultiKernelBench` |
| CPU | 5 | `QiMeng-IPRC/QiMeng-MuPa`、`mindspore-ai/akg`、`parallelcodefoundry/ParEval`、`tile-ai/tilelang`、`ucb-bar/autocomp` |
| Intel | 2 | `meta-pytorch/KernelAgent`、`wzzll123/MultiKernelBench` |
| Trainium | 2 | `ucb-bar/autocomp`、`zhang677/AccelOpt` |
| Google TPU | 2 | `ucb-bar/autocomp`、`wzzll123/MultiKernelBench` |

## 硬件架构对比

具体到芯片代际的分布。绝大多数项目只写「一张 NVIDIA GPU」，能定位到具体代际的是少数，这也解释了为什么跨项目对比加速比并不可靠。

| 硬件架构 | 项目数 | 项目 |
| --- | ---: | --- |
| NVIDIA Hopper (H100/H200) | 16 | `Dogacel/auto-gpu-kernel`、`HazyResearch/ThunderKittens`、`ISO-Bench/ISO-Bench`、`NVIDIA/cutlass`、`RLsys-Foundation/TritonForge`、`RightNow-AI/autokernel`、`Snowflake-AI-Research/fastkernels`、`aisa-group/InferenceBench`、`caoshiyi/K-Search`、`facebookresearch/kernel_bench_verified`、`ornith-ai/CUDA-L1`、`ornith-ai/CUDA-L2`、`tensormux/kernel-skills`、`tile-ai/tilelang`、`zhang677/AccelOpt`、`zhang677/PTXBench` |
| NVIDIA Ampere (A100) | 11 | `0satan0/KernelMem`、`BonnieW05/KernelBenchX`、`NVIDIA/cutlass`、`RightNow-AI/autokernel`、`Snowflake-AI-Research/fastkernels`、`StigLidu/AdaExplore`、`aisa-group/InferenceBench`、`ornith-ai/CUDA-L1`、`ornith-ai/CUDA-L2`、`tile-ai/BitBLAS`、`tile-ai/tilelang` |
| AMD CDNA 3 (MI300X) | 10 | `AMD-AGI/AMDKernelVault`、`AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`RLsys-Foundation/TritonForge`、`ROCm/aiter`、`RightNow-AI/autokernel`、`ScalingIntelligence/KernelBench`、`tensormux/kernel-skills`、`tile-ai/tilelang` |
| NVIDIA Blackwell (B200) | 9 | `BonnieW05/KernelBenchX`、`Dogacel/auto-gpu-kernel`、`HazyResearch/ThunderKittens`、`NVIDIA/SOL-ExecBench`、`NVIDIA/compute-eval`、`NVIDIA/cutlass`、`Snowflake-AI-Research/fastkernels`、`caoshiyi/K-Search`、`tile-ai/tilelang` |
| NVIDIA Ada (L40S/4090) | 8 | `BonnieW05/KernelBenchX`、`NVIDIA/cutlass`、`RightNow-AI/autokernel`、`ornith-ai/CUDA-L1`、`tensormux/kernel-skills`、`tile-ai/BitBLAS`、`tile-ai/tilelang`、`ucb-bar/autocomp` |
| AMD CDNA (MI100/MI200) | 5 | `AMD-AGI/AgentKernelArena`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`ROCm/aiter`、`ScalingIntelligence/KernelBench` |
| AMD RDNA (Radeon) | 4 | `AMD-AGI/AgentKernelArena`、`AMD-AGI/GEAK`、`ROCm/aiter`、`tile-ai/tilelang` |
| NVIDIA Volta (V100) | 3 | `NVIDIA/cutlass`、`tile-ai/BitBLAS`、`tile-ai/tilelang` |
| x86 CPU | 2 | `CSJianYang/Industrial-Coder`、`tile-ai/tilelang` |
| ARM CPU | 2 | `CSJianYang/Industrial-Coder`、`tile-ai/tilelang` |
| 昇腾 950PR | 1 | `tile-ai/tilelang` |
| TPU v6e | 1 | `ucb-bar/autocomp` |
| TPU v5 | 1 | `ucb-bar/autocomp` |

## 厂商 × 角色交叉

把「硬件厂商」和「架构角色」交叉，能看出每个生态里开源的是哪一层。

| 厂商 | Agent 搜索循环 | 评测基准 | 数据集 / 模型 | 编译器底座 | DSL / kernel 表达层 | 执行运行时底座 | 综述清单 | 训练流水线 | 合计 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AMD | 2 | 4 | 0 | 0 | 2 | 2 | 0 | 2 | 12 |
| 华为昇腾 | 0 | 3 | 0 | 1 | 1 | 0 | 0 | 0 | 5 |
| CPU | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 5 |
| Intel | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| NVIDIA | 12 | 17 | 4 | 2 | 4 | 2 | 0 | 8 | 49 |
| 其他 | 3 | 3 | 1 | 1 | 1 | 1 | 0 | 0 | 10 |
| Google TPU | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| Trainium | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |

## 单项目档案

### [flagos-ai/FlagGems](https://github.com/flagos-ai/FlagGems)

FlagGems is an operator library for large language models implemented in the Triton Language.

| 项 | 内容 |
| --- | --- |
| 角色 | 执行运行时底座 |
| 架构模式 | 后端中立的 Triton 算子库 + ATen 注册层 + 多后端分发 |
| 入口 | `torch.* / torch.nn.functional.* API（经 ATen 注册后自动路由到 Triton 实现）`、`官方文档 Getting Started 安装与调用流程`、`官方文档 usage 使用说明` |
| 基础层 | Triton、PyTorch-ATen、torch |
| 硬件厂商 | NVIDIA、AMD、Other |
| 硬件架构 | — |
| 评测 | 无 |
| 验证机制 | — |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 1164 |
| 最近推送 | 2026-10-30 |

> FlagGems 是 FlagOS 全栈中的算子层：用 Triton 写后端中立的算子集合，并通过注册 PyTorch 的 ATen backend，让用户不改动底层 API 即可把算子切到 Triton 实现，实现 develop once, run anywhere。README 列出的工程要点包括 eager 模式即可用（不依赖 torch.compile）、pointwise 算子的自动代码生成（支持任意输入类型与布局）、按函数的快速运行时分发、多后端接口（10+ 后端），以及仍在推进的 C++ Triton 函数分发器。

### [HazyResearch/ThunderKittens](https://github.com/HazyResearch/ThunderKittens)

Tile primitives for speedy kernels

| 项 | 内容 |
| --- | --- |
| 角色 | DSL / kernel 表达层 |
| 架构模式 | header-only CUDA DSL: tile 原语 + Load-Store-Compute-Finish 生产者/消费者模板 |
| 入口 | `#include "kittens.cuh" (header-only，无需安装)`、`cd kernels/gemm/bf16_h100 && make && make run`、`cd tests && make -j (编译上千个 kernel)`、`./unit_tests printout (执行单测并输出失败详情)`、`cd llama_demo && bash demo_8b.sh / cd lolcats_demo && bash demo_8b.sh` |
| 基础层 | CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200)、NVIDIA Blackwell (B200) |
| 评测 | 每 kernel 自带 Makefile、正确性测试与 benchmark |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 3786 |
| 最近推送 | 2026-09-12 |

> 整个库是 header-only，clone 后 include kittens.cuh 即可用，库本身不提供安装步骤。2.0 起不再作为 Python 包发布，kernels 目录下每个 kernel 必须单独编译，Makefile、测试与 benchmark 都与对应 kernel 源码同目录。每个 kernel 刻意自包含而不共用统一 harness，目的是让任何人轻松新增 kernel；库本身只提供数据类型（register/shared × tile/vector）与操作，kernel 通过 layout 与模板参数描述算法。

### [meta-pytorch/tritonbench](https://github.com/meta-pytorch/tritonbench)

Tritonbench is a collection of PyTorch custom operators with example inputs to measure their performance.

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 算子级基准套件 + git submodule 复用第三方 kernel 实现 |
| 入口 | `python install.py`、`python run.py --op gemm`、`pip install -e . 后用 tritonbench.load_opbench_by_name("addmm")(op_args).run()` |
| 基础层 | Triton、CUTLASS、torch |
| 硬件厂商 | NVIDIA、AMD |
| 硬件架构 | — |
| 评测 | 按 op 名运行算子基准，度量 Triton 实现与 PyTorch 的性能差异 |
| 验证机制 | runtime |
| Agent 循环 | 无 |
| 许可 | BSD-3-Clause |
| 星标 | 374 |
| 最近推送 | 2026-10-30 |

> 它本质上是一组带样例输入的 PyTorch 自定义算子，用来看 Triton 实现本身以及它与 PyTorch 集成后的性能，而不是一个通用 harness。结构上最大的特点是 kernel 来源不自研，而是把 generative-recommenders、Liger-Kernel、tilelang、flash-attention、FBGEMM、ThunderKittens、AITer 等项目以 git submodule 形式引入，其中 CUDA 与 HIP 实现各取所需。同时支持两种用法：命令行按算子名跑，或 pip install -e . 后作为库按名字加载算子基准并注入自定义参数。

### [NVIDIA/cutlass](https://github.com/NVIDIA/cutlass)

CUDA Templates and Python DSLs for High-Performance Linear Algebra

| 项 | 内容 |
| --- | --- |
| 角色 | DSL / kernel 表达层 |
| 架构模式 | header-only C++ 模板库 + 同构 Python DSL (CuTe DSL) 的双语言栈 |
| 入口 | `cmake .. -DCUTLASS_NVCC_ARCHS=90a (header-only，无需构建)`、`make test_unit -j (GoogleTest 单元测试)`、`make cutlass_profiler -j16`、`./tools/profiler/cutlass_profiler --kernels=cutlass_tensorop_s*gemm_f16_*_nt_align8 --m=3456 --n=4096 --k=4096`、`Python: import cutlass / @cute.jit / cutlass.jax.cutlass_call`、`examples/python/CuTeDSL/cute/notebooks (notebook 入门)` |
| 基础层 | CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Volta (V100)、NVIDIA Ampere (A100)、NVIDIA Ada (L40S/4090)、NVIDIA Hopper (H100/H200)、NVIDIA Blackwell (B200) |
| 评测 | profiler 跑 GEMM/Conv 并与 reference 比对 |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 无 |
| 许可 | NOASSERTION |
| 星标 | 10679 |
| 最近推送 | 2026-10-28 |

> 以 CuTe 的多维 layout/tensor 抽象为核心，把 GEMM 层级拆成 collective、mainloop、epilogue 等可复用组件，并按 tile 大小、数据类型、数学指令策略参数化。C++ 侧是 header-only 模板库，客户端只需把 include/ 加进头文件搜索路径；Python 侧是 CuTe DSL，编译期做布局一致性检查，比 C++ 编译快几个数量级并可直接被框架调用。tools/library 预实例化全部受支持模板，tools/profiler 负责批量跑分并同时与 reference_device、cuBLAS 比对，test/unit 用 GoogleTest 覆盖 API 与 GEMM 计算。

### [ROCm/aiter](https://github.com/ROCm/aiter)

AI Tensor Engine for ROCm

| 项 | 内容 |
| --- | --- |
| 角色 | 执行运行时底座 |
| 架构模式 | 多后端算子库: Triton/CK/ASM/Opus/FlyDSL 并存 + 统一 C++ 与 Python API |
| 入口 | `git clone --recursive https://github.com/ROCm/aiter.git && ./.github/scripts/install_triton.sh`、`AITER_USE_SYSTEM_TRITON=1 python3 -m pip install -e .`、`python3 op_tests/test_mha.py (也可用 test_mla/test_moe/test_gemm_a8w8 等)`、`AITER_MAX_JOBS=8 python3 -m aiter.aot.pa (AOT 预编译)`、`pip install -r requirements-triton-comms.txt (启用 Iris 通信算子)` |
| 基础层 | Triton、HIP、torch |
| 硬件厂商 | AMD |
| 硬件架构 | AMD CDNA (MI100/MI200)、AMD CDNA 3 (MI300X)、AMD RDNA (Radeon) |
| 评测 | op_tests/ 下每个算子一个独立测试脚本，可单独运行 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 599 |
| 最近推送 | 2026-10-30 |

> 同一算子可以有 Triton、Composable Kernel、手写 ASM、Opus、FlyDSL 多种后端实现，贡献规则强制一个 PR 只改一个后端，跨后端改动必须拆成 stacked PR 依次合入。构建期策略集中在 aiter_worker_limits.py 一个共享入口：按 cgroup 的 CPU 与内存配额自动推算编译 worker 数并允许 AITER_MAX_JOBS 覆盖，GPU 执行池另按可见 GPU 数乘 AITER_GPU_WORKERS_PER_DEVICE 限流，嵌套 fan-out 时子进程强制 -j1 防超订。发布侧每两周一个 release 分支与 tag，自动化校验 tag 指向分支 HEAD、并确认各 ROCm/Python 组合的 wheel 数量完整才上传。

### [tensormux/kernel-skills](https://github.com/tensormux/kernel-skills)

Open source skill library for AI coding agents to write, optimize, and debug high performance compute kernels across CUDA, Triton, and quantized workloads.

| 项 | 内容 |
| --- | --- |
| 角色 | 数据集 / 模型 |
| 架构模式 | Markdown 技能库为真源 + JSON Schema 元数据 + 构建期索引生成 + npm 分发 (CLI 与 TS API) |
| 入口 | `npm install @krxgu/kernel-skills`、`npx @krxgu/kernel-skills list`、`kernel-skills list\|search\|show\|path\|bundle\|categories\|tags`、`TypeScript API: searchSkills / getSkill / bundleSkills`、`npm run validate:skills 与 npm run generate:index` |
| 基础层 | CUDA-C++、HIP、Triton、vLLM |
| 硬件厂商 | — |
| 硬件架构 | NVIDIA Hopper (H100/H200)、NVIDIA Ada (L40S/4090)、AMD CDNA 3 (MI300X) |
| 评测 | 无 |
| 验证机制 | static-check |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 87 |
| 最近推送 | 2026-06-21 |

> 内容真源是 skills/ 下每个技能目录中的 SKILL.md（遵循 11 段模板）加一份 skill.json 元数据，两者配对存放。构建期把全部 skill.json 聚合成 generated/skills.index.json，CLI 与 TypeScript API 只读这份索引，因此运行期不需要解析 Markdown。schema/skill.schema.json 限定允许的 category (cuda/triton/patterns/quantization/portability/inference) 与 difficulty 取值，validate-skills 脚本在提交前拦截缺字段、重复 id、目录名与 category 不符、空 tags、SKILL.md 小于 400 字节等问题。npm 包只是分发层，README 明确声明自己不是编译器、不是 benchmark harness、不是服务运行时、也不是自主 agent，且不执行生成的代码。质量要求靠 proof/ 目录里的实测前后证据来支撑，例如 softmax 技能用 8 组形状的通过/失败矩阵证明指导前后的差异。

### [tile-ai/BitBLAS](https://github.com/tile-ai/BitBLAS)

ReDesign of https://github.com/microsoft/BitBLAS

| 项 | 内容 |
| --- | --- |
| 角色 | 执行运行时底座 |
| 架构模式 | 算子库 + MatmulConfig 描述层 + DSL 定制 + 多框架集成 + benchmark 目录 |
| 入口 | `pip install bitblas`、`python -c "import bitblas; print(bitblas.__version__)"`、`bitblas.Matmul(config=bitblas.MatmulConfig(...))`、`bitblas.Linear (PyTorch nn.Linear 类模块)`、`python -c "import bitblas; print(bitblas.__version__)" 校验安装` |
| 基础层 | torch、TileLang |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Ampere (A100)、NVIDIA Volta (V100)、NVIDIA Ada (L40S/4090) |
| 评测 | benchmark/ 收录各 dtype 组合与设备的算子性能，端到端对比 vLLM |
| 验证机制 | compile、correctness |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 10 |
| 最近推送 | 2026-01-28 |

> 主体是一个 bitblas Python 包，只暴露 Matmul 与 Linear 两个 API，算子形态由 MatmulConfig（M/N/K、dtype 组合、layout、group_size、scaling/zeros）描述后自动生成内核。功能边界按目录切分：integration/ 接入 PyTorch、GPTQModel、AutoGPTQ、vLLM 与 BitNet，benchmark/ 单独收集各格式与设备基准。扩展方式有两条：一是基于 TIR Script 的 DSL 自定义混合精度算子，FlashAttention 算子新增时直接用 TileLang 实现。

### [tile-ai/tilelang](https://github.com/tile-ai/tilelang)

 Domain-specific language designed to streamline the development of high-performance GPU/CPU/Accelerators kernels

| 项 | 内容 |
| --- | --- |
| 角色 | DSL / kernel 表达层 |
| 架构模式 | DSL 前端 + TVM 多级 IR 编译管线 + 可插拔后端注册表 + 示例/调试工具库 |
| 入口 | `pip install tilelang`、`python -c "import tilelang; print(tilelang.__version__)"`、`@tilelang.jit 装饰的 kernel 函数`、`examples/quickstart.py`、`.agents/skills/tilelang-backend/SKILL.md (后端移植编码助手技能)` |
| 基础层 | TVM |
| 硬件厂商 | NVIDIA、AMD、Ascend、CPU、Other |
| 硬件架构 | NVIDIA Volta (V100)、NVIDIA Ampere (A100)、NVIDIA Ada (L40S/4090)、NVIDIA Hopper (H100/H200)、NVIDIA Blackwell (B200)、AMD CDNA 3 (MI300X)、AMD RDNA (Radeon)、昇腾 950PR、x86 CPU、ARM CPU |
| 评测 | 示例内置 assert_close 校验；性能脚本在独立 tilelang-benchmark 仓库 |
| 验证机制 | compile、correctness |
| Agent 循环 | 无 |
| 许可 | NOASSERTION |
| 星标 | 8850 |
| 最近推送 | 2026-10-30 |

> tilelang 是建在 TVM 之上的 DSL，@tilelang.jit 会按输入 shape 与编译期参数特化 kernel，用户用 T.Kernel/T.gemm/T.copy 描述 tile 级计算。它正从单后端演进为 TileLang-X 多后端架构：device 与 host CodeGen 都收拢到 backend registry，CUDA/ROCm/Metal 有静态方言，Ascend A2/A3、MUSA、MetaX、HYGON、TANG 等生态适配器则拆到独立仓库。README 把大量篇幅给了编译期可观测性：IR dump、pass 可视化、pass diff、编译器 pass 计时，说明其架构把「可调试」当作一等公民。

### [triton-lang/triton](https://github.com/triton-lang/triton)

Development repository for the Triton language and compiler

| 项 | 内容 |
| --- | --- |
| 角色 | DSL / kernel 表达层 |
| 架构模式 | Python 前端 + MLIR/LLVM 后端 + 解释器旁路 + 环境变量驱动调试 |
| 入口 | `pip install triton`、`@triton.jit 装饰的 kernel 函数`、`make dev-install / make dev-install-llvm`、`make test`、`make test-nogpu`、`TRITON_INTERPRET=1 解释器模式` |
| 基础层 | MLIR、LLVM |
| 硬件厂商 | NVIDIA、AMD |
| 硬件架构 | — |
| 评测 | make test 跑全量测试（需 GPU），make test-nogpu 用解释器免 GPU |
| 验证机制 | compile、correctness |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 20485 |
| 最近推送 | 2026-10-30 |

> Triton 分成 Python DSL 前端与 C++/MLIR/LLVM 编译后端，2.0 把后端重写为 MLIR，并支持背靠背 matmul（flash attention 类）。构建上不绑定系统 LLVM：用 cmake/llvm-info.json 里的 llvm_hash 锁定版本，README 明确说 LLVM 无稳定 API、不能用任意版本。可观测性是核心设计：所有编译与调试开关集中在 python/triton/knobs.py，可用环境变量覆盖，并提供 IR dump、MLIR reproducer、kernel override、interpreter 等机制。测试分 make test（需 GPU）与 make test-nogpu（解释器）两条路径。

### [aisa-group/InferenceBench](https://github.com/aisa-group/InferenceBench)

Benchmarking Open-Ended Inference Optimization by AI Agents

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 容器隔离 + 批调度作业: agent 写 launcher → 容器内评测速度与质量 → LLM 裁判审查 |
| 入口 | `bash src/commit_utils/commit.sh --agents codex:gpt-5.3-codex-high --scenarios all --num-hours 2 --seed-pairs 21:1337 --bid 40 [--dry-run]`、`bash containers/build_container.sh inference`、`bash containers/build_backend_containers.sh torch vllm sglang`、`bash containers/download_hf_cache/download_hf_cache.sh --resources-file containers/download_hf_cache/resources.json --workers 4`、`bash src/commit_utils/baselines/submit_precompute_all_baselines.sh "mistralai/Mistral-7B-Instruct-v0.3" 40 torch 248 248 500 4`、`bash src/commit_utils/baselines/submit_hpo_search_baselines.sh "mistralai/Mistral-7B-Instruct-v0.3" 40 random vllm a 7200`、`source src/commit_utils/set_env_vars.sh`、`apptainer exec ... bash src/commit_utils/precache_seeds.sh` |
| 基础层 | torch、vLLM、SGLang |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200)、NVIDIA Ampere (A100) |
| 评测 | 四场景吞吐延迟 + PyTorch 质量参考 + Claude 裁判审查 |
| 验证机制 | correctness、runtime、contract |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 50 |
| 最近推送 | 2026-10-26 |

> 每个 agent 在固定时间预算内为一个基座模型编写 server launcher，随后在全新容器中运行它，在四种负载场景下测服务速度，并与 PyTorch 参考实现比对回答质量。生成与评测用 Apptainer 容器加 HTCondor 批作业隔离，容器内预置 torch/vllm/sglang/tgi 后端镜像与锁定的 Python 依赖。另设 Claude 裁判审阅 launcher 与服务日志以识别被禁的取巧手段，并提供同等时间预算的 vLLM/SGLang 随机搜索基线做公平对照。

### [alibaba/atrex-bench](https://github.com/alibaba/atrex-bench)

End-to-end benchmark for AI-generated GPU kernels, drawn from real production traces — turn a PyTorch reference into a DSL kernel (Triton, Gluon, FlyDSL, CuteDSL) and grade it on compilation, numerical correctness, and speed-of-light efficiency, on both AMD and NVIDIA GPUs.

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 三段式评测: compile → correctness → performance(SOL)，生成与评测分会话隔离 |
| 入口 | `python scripts/run_generate.py --operator attention_forward --backend flydsl --cli claude --output-dir outputs/attention_forward_flydsl --mirror-trace`、`python scripts/run_eval.py --input path/to/generated_kernel.py --reference-dir data/attention_forward --output results/attention_forward_flydsl --num-correctness-cases 5 --bench-iters 3`、`python scripts/run_eval.py --torch-compile --reference-dir data/attention_forward --output results/torch_compile`、`python scripts/run_eval.py --baseline-input A --input B --reference-dir ... (A-B-B-A 对照)`、`python scripts/run_eval.py --distribution ray_data --ray-max-workers 4 --ray-shapes-per-shard 1 ...`、`python scripts/cleanup_for_generation.py`、`python scripts/roofline.py`、`python scripts/static_roofline_check.py`、`docker run -it --rm --gpus all treinfra/atrex-bench:2.10.0-cuda12.8-cudnn9-devel` |
| 基础层 | torch、torch.compile、Triton、CUTLASS |
| 硬件厂商 | AMD |
| 硬件架构 | — |
| 评测 | trace 派生算子集 + 三段评测 + roofline SOL 效率 + ABBA 对照 |
| 验证机制 | compile、correctness、runtime、static-check |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 38 |
| 最近推送 | 2026-10-29 |

> 每个算子是一个自描述目录（reference.py、input.py、shapes.json、metadata.json、roofline.json），评测器分编译、数值正确性、性能三段，性能按缓存的 roofline SOL 效率打分。生成与评测强制分两次独立 clone：生成前用 cleanup_for_generation.py 就地删掉 metadata/roofline/评测器与 .git 历史，避免 agent 读到答案，评测用完整的新 clone。评测支持 torch.compile 基线、A-B-B-A 反向平衡对照、按 shape 分片并用 Ray Data 分发到多 GPU worker，worker 失败只重试受影响分片且已成功分片被提交保留。

### [AMDResearch/NPUEval](https://github.com/AMDResearch/NPUEval)

NPUEval is an LLM evaluation dataset written specifically to target AIE kernel code generation on RyzenAI hardware.

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 评测三段式: 提示生成脚本 + 功能测试脚本（生成与评测解耦） |
| 入口 | `./install.sh`、`./scripts/launch_jupyter.sh`、`docker_run_script.sh scripts/run_completions.py`、`docker_run_script.sh scripts/run_functional_tests.py` |
| 基础层 | — |
| 硬件厂商 | AMD、Other |
| 硬件架构 | — |
| 评测 | 数据集 prompt 喂给 AIECoder 生成解，功能测试脚本独立判定通过 |
| 验证机制 | compile、correctness |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 34 |
| 最近推送 | 2025-11-08 |

> 整体是围绕一个 NPU 评测数据集搭建的最小可复现流水线。install.sh 会拉起 XRT docker 镜像，构建 XRT 与 XDNA debian 包并安装到宿主机，同时准备带齐 NPU 应用编译工具链的 NPUEval 容器。评测被刻意拆成两个可独立运行的脚本：run_completions.py 负责把数据集里的所有 prompt 喂给 AIECoder agent 生成解法（需要 OPENAI_API_KEY，会请求 gpt-4.1 与 gpt-4o-mini），run_functional_tests.py 只负责评估已生成的解法，因此评测端只需要 NPU、不需要 LLM 访问权限，这对无外网或无 key 的环境很友好。所有脚本都可以通过 docker_run_script.sh 作为独立容器会话执行，同时提供 JupyterLab（8888 端口）供交互式探索数据集。底层依赖是 MLIR-AIE / LLVM-AIE 与 AI Engine API，NPU 侧通过实验性未签名内核模块工作。

### [BonnieW05/KernelBenchX](https://github.com/BonnieW05/KernelBenchX)

KernelBenchX: A Comprehensive Benchmark for Evaluating LLM-Generated GPU Kernels

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 评测三段式: call→exe→perf 分阶段流水线 + 机器级 golden 基线 |
| 入口 | `bash scripts/run_eval.sh [--bench-timeout SEC] <source> <output_dir> <gpus>`、`bash scripts/run_eval_from_files.sh [--bench-timeout SEC] <source> <output_dir> <gpus>`、`python metrics/run_missing_benchmarks.py --machine 4090 --all`、`examples/Examples.ipynb` |
| 基础层 | Triton |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Blackwell (B200)、NVIDIA Ampere (A100)、NVIDIA Ada (L40S/4090) |
| 评测 | call/exe/perf 三段：确定性测试校验 + 与 GPU 匹配 golden 比加速比 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 54 |
| 最近推送 | 2026-06-01 |

> 评测被切成 call（能否编译运行）→ exe（数值正确性）→ perf（性能）三个顺序阶段，每阶段单独落 JSONL 到 intermediate/ 目录，这样失败原因能定位到具体阶段。提交物形态设计得比较灵活：一个 JSONL 文件（每行含 predict 与 file，若无 file 则需带含 Functional Description 与 Wrapper Entry Information 的 instruction）、单个 .py 文件（basename 必须与 data/kernelbenchx/ 中的任务同名，且若文件内含 146 个 # 组成的分隔线，只取线以上内容作为提交）、或一个目录（递归收集 .py 与 .jsonl）。为了保证提交可执行，规定了「顶层可调用函数必须叫 kernel_function 或与任务 stem 同名」的执行契约。性能评测不与固定参考比，而是按机器隔离存放 GPU 匹配的 golden timing（metrics/golden_results/<machine>/），解析优先级为环境变量 KERNELBENCHX_GOLDEN_RESULTS_DIR → KERNELBENCHX_GOLDEN_MACHINE → 默认 5090，缺失的机器可用 run_missing_benchmarks.py 重新生成。输出统一为 metrics.json（逐任务）与 summary.json（通过率与加速比汇总）。相比上游 TritonBench，它强调更严格的正确性校验、扩展的任务覆盖（量化、多精度）与正确性/效率统一的评测流水线。

### [CUDA-Bench/CUDABench](https://github.com/CUDA-Bench/CUDABench)

以自然语言任务而非仅以高层框架代码为输入评测 CUDA 生成。

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 评测三段式: dataset-generate-evaluate（编译 + ncu 剖析） |
| 入口 | `python Generate/main.py`、`python Generate/main.py --api_option deepseek --model_name deepseek-reasoner --samples 3`、`python Evaluate/manager.py full <path_to_results_file>` |
| 基础层 | CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 任务自带 bench.cu/gen.py/compare.py，manager 编译运行并用 ncu 剖析 |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 20 |
| 最近推送 | 2026-03-04 |

> 任务集被压在一个 JSONL 文件里，每条记录自成一体：id 与 task_name 标识任务，inputs/outputs 描述张量形状与数据类型，三档难度 prompt 分别对应引导式实现（给出算法描述与显式 CUDA 实现指引）、算法式规范（只给算法描述、不给硬件提示）与概念检索式（只给任务名），评测三件套 bench.cu（参考 CUDA C++ 实现）、gen.py（生成随机二进制输入与参考输出）和 compare.py（校验生成 kernel）也内嵌在同一条记录里，使得任务定义、参考实现与打分逻辑完全自包含。生成侧由 Generate/main.py 负责，按 --api_option 选择 API provider、--model_name 选模型、--samples 指定采样次数，默认参数集中在 Generate/config.py 中，结果按 Results/<api>/<model>_<level>_pass<k>.jsonl 命名，把 provider、模型、难度与采样序号编码进文件名，便于多模型多难度横向对比。评测侧 Evaluate/manager.py 以 full 子命令接收结果文件路径，负责编译、运行与用 Nsight Compute 剖析，整体是「生成只落 JSONL、评测单独吃同一文件」的解耦结构。仓库还提供 figs/overview.png 说明整体流程图。

### [facebookresearch/kernel_bench_verified](https://github.com/facebookresearch/kernel_bench_verified)

Welcome to KernelBench-Verified. This repository provides a robust, realistic evaluation framework for assessing custom CUDA kernels generated by Large Language Models (LLMs).

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 扩展评测框架: 复用 KernelBench + TF32 基线 + 隐藏测试门控 + 交互式排行榜 |
| 入口 | `python scripts/generate_samples.py run_name=gpt-5.5_level1_test dataset_src=local level=1 num_samples=5 server_type=openai model_name=gpt-5.5`、`python scripts/eval_from_generations.py run_name=... level=1 num_gpu_devices=8 gpu_arch="['Hopper']" build_cache=True precision=fp32 measure_performance=True`、`python scripts/eval_from_generations.py ... use_hidden_tests=True measure_performance=False`、`python scripts/generate_leaderboard.py --use_hidden_eval --baseline baseline_time_torch_tf32 --fp32_tolerance 1e-3 --out leaderboard.html`、`python scripts/generate_hidden_inputs.py --level 1 [--pid 90]` |
| 基础层 | torch、CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200) |
| 评测 | 标准评测 + 四分布隐藏门控 + TF32 基线 + 速度显存双指标榜 |
| 验证机制 | correctness、runtime |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 16 |
| 最近推送 | 2026-07-17 |

> 不重造题库，而是在 KernelBench 之上加三件事：把 PyTorch 基线切到 TF32 以对齐真实部署的 Tensor Core 路径、为每题生成隐藏的四分布测试文件、对 4 个易 reward hack 的题在 prompt 中自动剥离测试输入。评测用 use_hidden_tests 与 use_hidden_eval 两个开关把标准结果和隐藏门控结果分流到不同文件，最后由 generate_leaderboard.py 产出以速度-显存权衡为坐标的交互式 HTML 排行榜。

### [flagos-ai/KernelGenBench](https://github.com/flagos-ai/KernelGenBench)

以共同 Triton 目标研究算子来源和硬件平台变化时的生成能力与成本。

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 多来源算子集 + 双赛道（LLM Pass@K / Agent 迭代）+ 多芯片后端 |
| 入口 | `pip install -r requirements/requirements_nvidia.txt && pip install -e .`、`python scripts/generate_kernel_and_verify.py --op-name aten::add --single-test --api-format openai --model-name your-model --base-url https://your-provider.example/v1 --api-key your-key`、`docs/source/getting-started/index.md`、`docs/source/operation-guide/llm-track/index.md`、`docs/source/operation-guide/agent-track/index.md` |
| 基础层 | Triton、torch |
| 硬件厂商 | NVIDIA、Ascend、Other |
| 硬件架构 | — |
| 评测 | 统一算子集 + 容差比对自动校验，LLM 赛道 Pass@K 与 Agent 赛道迭代 |
| 验证机制 | correctness |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 25 |
| 最近推送 | 2026-09-28 |

> KernelGenBench 是 FlagOS 体系内的基准框架：210 个算子来自 ATen（110）、vLLM（50）、cuBLAS（50）三个来源，评测分 LLM 赛道（Pass@K）与 Agent 赛道（迭代生成）两条。对外统一用 generate_kernel_and_verify.py 入口，--api-format 只描述协议而不限定 provider，任何 OpenAI/Anthropic 兼容端点都能直接接入。工程上把平台差异收敛到 requirements/ 下的分平台依赖文件，硬件侧覆盖 NVIDIA、昇腾 NPU、MUSA、海光 DCU、沐曦与 MetaX。

### [flashinfer-ai/flashinfer-bench](https://github.com/flashinfer-ai/flashinfer-bench)

Building the Virtuous Cycle for AI-driven LLM Systems

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 数据集 + 固定 Schema 驱动的 pypi 基准套件 |
| 入口 | `pip install flashinfer-bench`、`import flashinfer_bench as fib`、`flashinfer-bench run --local flashinfer-trace`、`GIT_LFS_SKIP_SMUDGE=1 git clone https://huggingface.co/datasets/flashinfer-ai/flashinfer-trace` |
| 基础层 | FlashInfer |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 以 Trace 数据集的 kernel 与 workload 测性能并横向比较 |
| 验证机制 | — |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 301 |
| 最近推送 | 2026-09-25 |

> README 极简：flashinfer-bench 以 pip 包发布，提供 Python 模块（import flashinfer_bench as fib）与 CLI（flashinfer-bench run）两条入口。核心资产是官方 FlashInfer-Trace 数据集，包含真实 AI 系统部署环境下的 kernel 与 workload，遵循独立的 FlashInfer Trace Schema。数据集托管在 HuggingFace，用 GIT_LFS_SKIP_SMUDGE=1 只克隆 LFS 指针文件，大张量在跑基准时按需下载，避免一次性拉取巨量数据。整体定位是构建『AI 改进 AI 系统』的正循环。

### [ISO-Bench/ISO-Bench](https://github.com/ISO-Bench/ISO-Bench)

A benchmark framework for evaluating AI agents on software performance optimization tasks

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 评测三段式: 提交挖掘造题(commit→LLM 测试) - agent 运行 CLI(plan/prepare/report) - 三方性能对比 |
| 入口 | `python commit_to_dataset.py configs/experiments.yaml`、`python -m bench.cli plan tasks/vllm.yaml --out state/plan.json`、`python -m bench.cli prepare tasks/vllm.yaml --from-plan state/plan.json --bench-cfg bench.yaml`、`python -m bench.cli report state/runs/<run_id>`、`python -m bench.cli doctor --bench-cfg bench.yaml`、`python scripts/runners/run_3way_benchmarks.py --agent-type trae_gpt5 --commits 8aa1485f`、`python scripts/generate_soft_metrics.py --agent claude_code --project vllm`、`load_dataset('ISO-Bench/ISO-Bench', split='test')` |
| 基础层 | vLLM、SGLang |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200) |
| 评测 | Docker 镜像内做基线/人类/agent 三方 wall-clock 对比 |
| 验证机制 | correctness、runtime |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 0 |
| 最近推送 | 2026-01-29 |

> 仓库把造题与跑 agent 明确分开：commit_to_dataset.py 从真实仓库（vLLM/SGLang）的性能提交出发，经 PerfCommitAnalyzer 与 LLM 生成性能测试，产出 jsonl 数据集；ISO-Bench/ 子目录提供 plan→prepare→report 的 agent 运行 CLI，可在 TRAE、Claude Code、Codex、OpenHands 之间切换。每个任务在同一个 Docker 环境下做三方对比：基线父提交、人类专家提交、agent 补丁，并跑 vLLM serving/throughput 基准。除此之外还有 LLM 软指标分析（任务理解、技术重叠、提速可能性）与基于 lm-eval 的正确性校验作为旁路评估。

### [meta-pytorch/BackendBench](https://github.com/meta-pytorch/BackendBench)

Ship correct and fast LLM kernels to PyTorch

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | PyTorch 后端目录约定 + 三套测试套件 (smoke/opinfo/torchbench) 动态替换算子 |
| 入口 | `pip install .`、`python -m BackendBench.scripts.setup_operator_directories`、`python BackendBench/scripts/main.py --suite smoke --backend aten`、`python BackendBench/scripts/main.py --suite opinfo --backend directory`、`python BackendBench/scripts/main.py --suite torchbench --backend directory` |
| 基础层 | PyTorch-ATen、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | smoke/opinfo/torchbench 三套件；OpInfo+FACTO 测正确性，TorchBench 真实形状测性能 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | BSD-3-Clause |
| 星标 | 156 |
| 最近推送 | 2026-01-14 |

> 核心机制不是独立 runner，而是目录约定：开发者按规范在算子目录下放实现，运行时动态覆盖 PyTorch 核心算子，从而拼出一个可 pip 安装、对现有模型无需改代码的 PyTorch 后端。评测分三套：smoke 快速自检、opinfo 复用 PyTorch OpInfo 与 FACTO 做边界正确性、torchbench 用 Hugging Face 热门模型的真实张量形状测性能。设计上刻意以 PyTorch 自身标准为准，目的是让通过测试的 kernel 具备向上游 PyTorch 合并的资格。

### [NVIDIA/compute-eval](https://github.com/NVIDIA/compute-eval)

Evaluating Large Language Models for CUDA Code Generation ComputeEval is a framework designed to generate and evaluate CUDA code from Large Language Models.

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | datapack 版本化题库 + Podman 沙箱评测 + 单发与 agent 两种生成器 |
| 入口 | `compute_eval_generate generate_samples --model gpt-5 --solutions_per_problem 5`、`compute_eval_harness generate_samples --num_shots 3 --demonstrations_dir ..`、`compute_eval_harness harbor generate --agent claude-code --model <id>`、`compute_eval_harness harbor optimize --agent claude-code --model <id>`、`compute_eval evaluate_functional_correctness --release=2026-2 --mode=podman --k='(1,3)'`、`compute_eval_build_profiler (编译 libcuda_profile.so)` |
| 基础层 | CUDA-C++、CUTLASS、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Blackwell (B200) |
| 评测 | Podman 沙箱内编译执行隐藏测试，按退出码算 pass@k |
| 验证机制 | compile、correctness、runtime、static-check、profile |
| Agent 循环 | 有 |
| 许可 | NOASSERTION |
| 星标 | 149 |
| 最近推送 | 2026-09-14 |

> 题目以目录为单位组织（problem-spec.yaml 加 context/solution/test），生成期模型只见 prompt、context_files 与 build_command，评测期才注入隐藏测试与参考答案，靠目录级可见性分离防止对测试过拟合。题目打包成版本化 datapack（metadata.json 带每题 MD5 + problems.jsonl）发布到 HuggingFace，承诺旧 release 的题目集合与语义永久不变、只修缺陷不加题。执行侧用 Podman 容器隔离未信任的生成代码，功能正确性由 test_command 的退出码决定，性能由可选 CUPTI/NCU 计时；此外用 harbor 子命令让编码 agent 在容器内自行读文件、编译、迭代，并可用 optimize 模式以基线解为起点只优化性能。

### [NVIDIA/SOL-ExecBench](https://github.com/NVIDIA/SOL-ExecBench)

A benchmark of real-world DL kernel problems 

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 问题目录格式 (definition+workload) + 容器内 CLI 评测 + roofline 式 SOL-Score 排名 |
| 入口 | `./scripts/download_data.sh`、`./scripts/run_docker.sh --build`、`sol-execbench <problem_dir> --solution solution.json`、`sol-execbench --definition def.json --workload wkl.jsonl --solution sol.json`、`uv run scripts/run_dataset.py data/SOL-ExecBench/benchmark --solution-name solution.py`、`src/sol_execbench/sol_score.py (SOL-Score 评分)` |
| 基础层 | torch、Triton、CUTLASS、CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Blackwell (B200) |
| 评测 | definition+workload 驱动，容器内编译、数值比对、可复现计时 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 328 |
| 最近推送 | 2026-07-15 |

> 以 problem 目录为评测单元：definition.json 给出函数签名、张量形状、dtype 与参考实现，workload.jsonl 逐行给出具体输入与容差阈值，solution.json 单独提交源码与构建信息。评测在 Docker 容器内由 sol-execbench CLI 完成，先排查多种形式的 reward hacking，再与参考实现做数值正确性比对，最后在可复现条件下计时。排名用 SOL-Score：以 B200 的理论 roofline（由 SOLAR 解析求得）为基准给自定义 kernel 打分，而不是只报相对加速比；同一框架覆盖 PyTorch、Triton、CUTLASS、cuDNN、CuTe DSL、cuTile、CUDA C++ 多种 DSL。

### [parallelcodefoundry/ParEval](https://github.com/parallelcodefoundry/ParEval)

Parallel Code Evaluation Benchmark

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 离线三段式流水线: prompts → generate → drivers → analysis |
| 入口 | `python generate/generate.py (生成 LLM 输出)`、`python drivers/run-all.py (评测输出)`、`python analysis/metrics.py (后处理与指标)`、`cd drivers/cpp && make (构建 C++ driver)` |
| 基础层 | CUDA-C++、HIP |
| 硬件厂商 | CPU、NVIDIA |
| 硬件架构 | — |
| 评测 | C++ driver 编译运行 LLM 产出的并行代码，按 prompt 分组评测并汇总指标 |
| 验证机制 | compile、runtime |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 47 |
| 最近推送 | 2025-11-04 |

> 仓库按流程而非按功能划分目录，prompts 放提示词，generate 产出 LLM 代码，drivers 负责编译运行与评测，analysis 做结果后处理与指标计算，tpl 用 submodule 固定第三方依赖。通用工作流是三步命令串联：generate.py 生成 → run-all.py 评测 → metrics.py 计算指标。C++ driver 用 makefile 构建，检测不到 CUDA、HIP 或 Kokkos 库时会自动跳过对应目标，从而让没有 GPU 的机器也能评 CPU/OpenMP 部分。环境依赖被显式列出：Python 3.7+、支持 C++17 与 OpenMP 的编译器、Make、CMake 与 MPI。

### [SakanaAI/robust-kbench](https://github.com/SakanaAI/robust-kbench)

围绕 Agent 生成 kernel 的稳健性、验证和优化进行评测。

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 任务目录 + 六重过滤校验 + 组件化并行评测 API |
| 入口 | `python run_filter.py --task_dir tasks/mnist_cross_entropy`、`python run_kernel.py --task_dir tasks/mnist_cross_entropy --cuda_code_path highlighted/.../kernel.cu`、`from robust_kbench.parallel import ParallelKernelExecutor`、`from robust_kbench.evaluate import eval_torch_runtime / compile_cuda_kernel / test_cuda_kernel / eval_cuda_kernel / prof_cuda_kernel` |
| 基础层 | CUDA-C++、torch、torch.compile |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 多初始化多输入下对拍参考实现，三套计时交叉验证 |
| 验证机制 | compile、correctness、runtime、static-check、profile |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 107 |
| 最近推送 | 2025-11-22 |

> 每个任务是一个目录（tasks/mnist_linear、tasks/layernorm 等），覆盖基础算子、卷积、Transformer 块与原版 KernelBench 题，并区分 forward 与 backward。run_filter.py 先做六项鲁棒性检查：输出范围不被压到 [-0.01,0.01]、标准差大于 0.01、跨轴变化大于 0.01、初始化设置影响、输入配置影响，以及 LLM 判定的低效代码，先把可被钻空子的题目筛掉。评测侧拆成 compile/test/eval/profile 四个独立函数，由 ParallelKernelExecutor 并行编排，并提供 KernelBench、torch benchmark 与 Triton do_bench 三套计时互相印证，避免单一计时口径被针对性针对。

### [ScalingIntelligence/KernelBench](https://github.com/ScalingIntelligence/KernelBench)

KernelBench: Can LLMs Write GPU Kernels? - Benchmark + Toolkit with Torch -> CUDA (+ more DSLs)

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 评测三段式: 数据集-prompt-生成器 与 评测脚本 分离 + 离线结果分析 |
| 入口 | `uv run python scripts/generate_and_eval_single_sample.py dataset_src=huggingface level=2 problem_id=40 server_type=google model_name=gemini/gemini-2.5-flash`、`uv run python scripts/generate_samples.py run_name=test_hf_level_1 dataset_src=huggingface level=1 num_workers=50`、`uv run python scripts/eval_from_generations.py run_name=test_hf_level_1 dataset_src=local level=1 num_gpu_devices=8 timeout=300`、`uv run python scripts/benchmark_eval_analysis.py run_name=test_hf_level_1 level=1 hardware=L40S_matx3 baseline=baseline_time_torch`、`uv run python scripts/generate_baseline_time.py`、`uv run python scripts/run_and_check.py`、`notebooks/tutorial.ipynb`、`from kernelbench import timing / eval as kb_eval / from kernelbench.utils import set_gpu_arch` |
| 基础层 | torch、CUDA-C++、Triton、TileLang、ThunderKittens、CUTLASS、HIP |
| 硬件厂商 | NVIDIA |
| 硬件架构 | AMD CDNA (MI100/MI200)、AMD CDNA 3 (MI300X) |
| 评测 | 分级数据集 + 随机输入正确性校验 + 与 torch 基线的加速比 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | NOASSERTION |
| 星标 | 1302 |
| 最近推送 | 2026-03-24 |

> README 明确本仓库只提供 KernelBench 核心功能与易用评测脚本，不提供复杂 agentic scaffold，建议 clone 后自行改造或作为 git submodule 使用。数据集分 Level1-4（单 kernel、简单融合、整模型、HF 模型），生成与评测拆成 generate_samples 与 eval_from_generations 两个脚本，runs/ 与 results/ 分别承载运行结果和跨代际 NVIDIA GPU 基线。评测核心在 src/eval.py，指标 fast_p 表示既正确又超过阈值 p 的加速比任务占比。

### [Snowflake-AI-Research/fastkernels](https://github.com/Snowflake-AI-Research/fastkernels)

在生产模型接口和真实调用路径中复核生成 kernel 的有效收益。

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 四级抽象 L1-L4 + baseline/candidate 槽位替换 + benchmark-serve 一体 |
| 入口 | `pip install .`、`fastkernels list [--workloads \| --map]`、`fastkernels capture minimal`、`fastkernels bench --target rms_norm`、`fastkernels eval full`、`docs/model-optimization-guide.md`、`docs/agent-kernels-guide.md`、`docs/serving-framework-guide.md` |
| 基础层 | torch、CUDA-C++、Triton |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200)、NVIDIA Blackwell (B200)、NVIDIA Ampere (A100) |
| 评测 | baseline/candidate 同架构对照，先校验正确性再测加速比与吞吐 |
| 验证机制 | correctness、runtime |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 10 |
| 最近推送 | 2026-09-26 |

> 算子按 L1 单 kernel、L2 融合复合、L3 层/块、L4 端到端管线四级抽象组织，覆盖 dense/MoE LLM、线性注意力、扩散视频音频、多模态、检测、3D/机器人/科学、推荐与 world model。每个架构同时提供参考实现（tasks/baseline/）和候选替换槽位（tasks/candidate/），runner 把候选换入后先校验正确性再测加速比。README 强调在模型优化与 agent kernel 评测中开发的优化 kernel，会在作为服务框架使用时被自动换入部署，使评测产物与部署产物合一。

### [thunlp/TritonBench](https://github.com/thunlp/TritonBench)

TritonBench: Benchmarking Large Language Model Capabilities for Generating Triton Operators

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 双通道评测 (生成式 G / 任务式 T) + 三段式打分: 调用准确-执行准确-性能效率 |
| 入口 | `0_call_acc.py --source source/path/or/folder --target target/path/or/folder --GPUs [0,1,2,3]`、`1_exe_acc.py --folder root/of/multiple/folders/or/folder --GPUs [0,1,2,3]`、`python run_bench/write_file.py --input_folder_path /folder/of/pyfiles --results_path /folder/of/output/results`、`python run_bench/multiprocess_gpu_run.py`、`python 2_efficiency.py --gen_folder /folder/of/output/results` |
| 基础层 | Triton、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | G/T 双通道；调用匹配→执行正确率→多 GPU 性能加速比，G 另加 CodeBLEU |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 143 |
| 最近推送 | 2025-06-14 |

> TritonBench-G 面向模型从指令生成算子，需先做代码相似度评估再评执行；TritonBench-T 面向给定算子的直接改写，不评相似度，只评调用正确性、执行正确性与加速比。打分被拆成三个可独立执行的脚本：0_call_acc.py 做静态调用匹配，1_exe_acc.py 做执行正确率，2_efficiency.py 汇总性能与加速比。性能链路是 write_file.py 生成输入文件、multiprocess_gpu_run.py 多进程多 GPU 跑、再由 2_efficiency.py 汇总；README 明确要求准确率与效率评测必须顺序执行。G 通道额外用 CodeBLEU 衡量代码相似度，把像不像与对不对分开评。数据侧提供 Alpaca 格式的简版/复杂指令、可执行任务目录与统计，以及由 4024 条 BERT 去重爬取语料与 4133 条 Jiuci 合成语料合并的 8k RAG 语料。

### [wzzll123/MultiKernelBench](https://github.com/wzzll123/MultiKernelBench)

MultiArchKernelBench: A Multi-Platform Benchmark for Kernel Generation

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 基准四件套: 任务数据集 + prompt 策略插件 + 参考实现 + 后端评测插件 |
| 入口 | `python generate_and_write.py --model deepseek-chat --language ascendc --strategy add_shot --categories activation`、`python evaluation.py --model deepseek-chat --language ascendc --strategy add_shot --categories activation`、`python eval_single_runner.py --input prompts/ascendc_direct_launch_model_relu.json --op relu --language ascendc_direct_launch --result relu_result.json`、`python generate_baseline_statistics.py`、`config.py 中设置 temperature/top_p 与 arch_list` |
| 基础层 | torch |
| 硬件厂商 | NVIDIA、Ascend、TPU、Intel、Other |
| 硬件架构 | — |
| 评测 | 按 language×strategy 生成后评测，输出含编译/正确性/性能的 result_{category}.json |
| 验证机制 | compile、correctness、runtime、static-check |
| Agent 循环 | 无 |
| 许可 | NOASSERTION |
| 星标 | 75 |
| 最近推送 | 2026-07-08 |

> 生成与评测被拆成两条独立脚本：generate_and_write.py 只负责按 language/strategy/model 生成代码并写入 output 目录，evaluation.py 再对同一产物路径做评测，便于反复跑不同策略而不重生成。语言差异通过 backends/ 下的后端类插件化解，接口固定为 get_device/get_hardware_name/compile/correctness_execution/time_execution/cleanup；prompt 差异通过 prompt_generators/ 下的策略类插件化解，两侧都用装饰器注册。reference/ 按 activation/attention/convolution/matmul 等 category 组织 PyTorch 参考实现，作为所有语言后端共享的正确性基准。

### [zhang677/PTXBench](https://github.com/zhang677/PTXBench)

PTXBench: an open-source environment for kernel agents with architecture-specifc CUDA/PTX

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | Profiling 服务 + 双通道 agent（多轮模型循环 / 编码代理网关）+ Fixit 与 KernelGen 两条 SFT 数据线 |
| 入口 | `python multiturn/scripts/render.py --check`、`python multiturn/run_parallel_v2.py --config <cfg> --definition <name> --test-path <path> --model <model> --service-url http://localhost:10000`、`bash ptxbench-eval/examples/gemini_gemm/run_experiment.sh`、`bash ptxbench-eval/examples/gpt56_gemm/run_experiment.sh`、`bash scripts/reproduce_fixit.sh --check / 00`、`bash scripts/reproduce_kernelgen.sh --check / 00`、`curl -fsS http://localhost:10000/health` |
| 基础层 | Triton、CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200) |
| 评测 | CUDA/Triton evaluator 按 definition 跑，profiling 服务返回耗时并落产物 |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 37 |
| 最近推送 | 2026-10-25 |

> 整套系统围绕一个 GPU profiling 服务（fib-profile，HTTP 暴露 /health）展开：多轮模型循环与编码代理网关两条通路共用同一 profiling 服务和同一 prompt hub（multiturn/prompts/hub.json），因此结果可比。runner 把一份 JSON config 展开成轨迹，产出 plan.json、trajectories、日志与成功产物，并支持 --resume 断点续跑。训练侧分两条数据线：Fixit 挑失败的基础模型 kernel 让 Gemini 修复并合成推理、训 LoRA 适配器；KernelGen 挑正确的 Gemini kernel 合成推理后走同一训练与评测路径；两者都用有序 stage 的脚本驱动并配机器可读的源/评测 manifest。

### [caoshiyi/K-Search](https://github.com/caoshiyi/K-Search)

Automated High-Performance GPU Kernel Generation

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 世界模型引导的迭代优化: 生成器 + 共演化世界模型 + 任务后端适配层 |
| 入口 | `bash scripts/gpumode_trimul_wm.sh`、`bash scripts/mla_decode_wm.sh`、`bash scripts/kernelbench_wm.sh`、`bash scripts/mlx_mamba_wm.sh`、`python -m k_search ... --task-source {flashinfer,gpumode,kernelbench,mlx} --definition ... --max-opt-rounds ... --world-model --wandb` |
| 基础层 | torch、Triton、CUDA-C++ |
| 硬件厂商 | NVIDIA、Other |
| 硬件架构 | NVIDIA Hopper (H100/H200)、NVIDIA Blackwell (B200) |
| 评测 | 多后端任务适配器，复用各 benchmark 自带评测器与 local/Modal 模式 |
| 验证机制 | correctness、runtime |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 144 |
| 最近推送 | 2026-06-01 |

> 核心在 k_search/kernel_generators/：除基础 LLM 生成器外还提供 world-model-aware 生成器，配套 world_model.py（结构化 JSON schema）、world_model_manager.py（init/refine/select 生命周期）与专用 prompt 模板，世界模型编码瓶颈假设、设计备选与优化策略来指导下一轮动作。任务侧由 task_base.py 定义统一协议，各 benchmark 以适配器接入（FlashInfer-Bench、GPUMode TriMul、KernelBench、MLX）。解法、评测报告与世界模型快照全部落盘，可从已有解法或世界模型状态续跑，并内置 OpenEvolve/ShinkaEvolve 基线做同目标对照。

### [Dogacel/auto-gpu-kernel](https://github.com/Dogacel/auto-gpu-kernel)

Winner 🏆 (Agent-only) MLSys 2026 - FlashInfer AI Kernel Generation Contest for the DeepSeek Sparse Attention (DSA) track with an average speedup of 34.93x

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 双 CLI 分层: 优化 agent(kopt) + 验证基准(kbench)，共用统一 BenchmarkAdapter |
| 入口 | `kopt init <definition.json> --backend modal --gpu B200`、`kopt init-task task.toml`、`kopt run work/<task> -n 20 --model anthropic/claude-opus-5 --thinking low`、`kopt watch . (本地 127.0.0.1:8765)`、`kbench bench --quick / --stride 2 / 完整`、`kbench ab --a experiments/exp_3/solution_fused.py`、`omp (运行优化 agent 的宿主 CLI)` |
| 基础层 | FlashInfer |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Blackwell (B200)、NVIDIA Hopper (H100/H200) |
| 评测 | setup agent 生成适配器，kbench 分档跑并做 A/B |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 317 |
| 最近推送 | 2026-09-12 |

> FlashInfer 赛道与任意 Git 仓库共用同一个 BenchmarkAdapter 抽象：FlashInferAdapter 打包 kernel 源码走本地或 Modal 后端执行，GeneratedTaskAdapter 运行 setup agent 生成的 validate.py 与 benchmark.py。任务描述外置为 task.toml（objective/measure/validate/hints 及硬件约束），首轮用一次 setup turn 让 agent 现场生成验证与测量适配器，之后由 kbench 负责 quick/full 基线、归一化测量与配对 A/B。作者明确的设计取舍是只给 agent 关键原则而不给长指令，以免 harness 被逐渐 hack。

### [StigLidu/AdaExplore](https://github.com/StigLidu/AdaExplore)

[COLM-LLA 2026] The official implementation for paper "AdaExplore: Failure-Driven Adaptation and Diversity-Preserving Search for Efficient Kernel Generation"

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 两阶段: Adapt(合成任务-失败蒸馏-技能记忆) + Explore(MCTS 树搜索) |
| 入口 | `python synthesis/generate_data.py --server_type azure --model_name gpt-5-mini --prompt_style composite --input_levels 1 --num_generations 200 --num_examples_per_request 3 --temperature 1.0`、`python synthesis/rename.py --source_path ... --data_path datasets/KernelBench_syn/... --force`、`python agent/agent_entry.py --config config/SYN-v1/config_SYN-v1_none_MCTS.yaml`、`python skill_memory/skill_memory.py --log-dir outputs/example_run --knowledge-store-path outputs/example_run/general_memory.txt --server openai --model-name gpt-5-mini --max-logs 3000 --seed 42`、`bash online_judge/start_server.sh`、`python -m uvicorn online_judge.app_with_queue:app --host 0.0.0.0 --port 12017`、`python tool_scripts/stats.py --log_folder outputs/KB-l2_AdaExplore_50 --step 50`、`python tool_scripts/re_evaluate.py --log_folder outputs/<run> --num_correct_trials 5 --num_perf_trials 100 --use_remote_eval` |
| 基础层 | torch、Triton |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Ampere (A100) |
| 评测 | 在线评测服务 + 子进程隔离，正确性与性能分开测量 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | MIT |
| 星标 | 24 |
| 最近推送 | 2026-08-23 |

> 仓库按 Adapt/Explore 两阶段切分目录：synthesis/ 生成多样化 kernel 任务，agent/ 在其上运行并把重复的编译/运行失败蒸馏成跨任务规则写入技能记忆文件，skill_memory/ 负责离线抽取或更新该记忆，记忆再被注入后续 prompt。Explore 阶段用 MCTS 把候选组织成搜索树，交替进行局部精修与结构性重写以保持多样性。评测走 online_judge/app_with_queue.py 提供的 API 服务，按 GPU 设并发上限并排队，请求路由到最空闲 GPU，执行放在隔离子进程以防崩溃或非法访存拖垮主服务。

### [ucb-bar/autocomp](https://github.com/ucb-bar/autocomp)

Autocomp: Optimize any AI kernel, anywhere.

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | Agent 工具循环 + 束搜索 + 可插拔硬件目标（agent/backend/hw_config 三件套） |
| 入口 | `python -m autocomp.search.run_search`、`python -m autocomp.agent_builder.run_agent_builder --agent-name <name> --source-dir <dir> --agent-scope "..."`、`pip install "autocomp[agent-builder]"`、`WANDB_MODE=disabled pytest` |
| 基础层 | vLLM |
| 硬件厂商 | NVIDIA、TPU、Trainium、CPU、Other |
| 硬件架构 | TPU v6e、TPU v5、NVIDIA Ada (L40S/4090) |
| 评测 | backend 编译并跑分，prob_type/prob_id 选题，支持 spike/firesim 仿真器 |
| 验证机制 | compile、runtime |
| Agent 循环 | 有 |
| 许可 | BSD-3-Clause |
| 星标 | 152 |
| 最近推送 | 2026-07-11 |

> 主循环是 search/ 里的 beam 束搜索：每轮先生成若干策略方案（planning），再据此产出代码实现（code_models 可与规划模型不同），由评测后端打分后保留 beam_size 个候选进入下一轮。硬件被抽象成三元组：每个目标同时需要一个懂该硬件的优化 agent、一个负责编译与跑分的 evaluation backend、一个描述实例的 hw_config 类，三者按固定子目录命名（trn/tpu/gemmini/kernelbench/gpumode/metal/saturn/xnnpack），新增硬件按 ADDING_HARDWARE_SUPPORT.md 接入。Agent Builder 则从本地目录、PDF、网页文档自动生成硬件专属 agent 并落到 agent_builder/.built/。

### [0satan0/KernelMem](https://github.com/0satan0/KernelMem)

以长期专家知识和短期任务轨迹两层记忆协调多 Agent 生成、修复及优化 CUDA kernel。

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 单脚本编排 + 长短期记忆库 + NCU/NSYS 剖析驱动的多轮自进化 |
| 入口 | `python main_memory_latest.py KernelBench/level1/001_xxx.py --gpu A100-80GB --server_type openai --model_name gpt-5.1-chat --round 10 --work_dir run --device 0`、`python main_memory_latest.py KernelBench/level3 --num_tasks 5 --shuffle_seed 42`、`python main_memory_latest.py KernelBench/level3 --filter_from_summary path/to/previous/summary.json` |
| 基础层 | CUDA-C++、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Ampere (A100) |
| 评测 | 以 KernelBench 算子为任务，编译运行后对比 PyTorch 参考的 tol 误差并算 speedup |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 31 |
| 最近推送 | 2026-02-14 |

> 仓库是一个以脚本为中心的实验型系统：main_memory_latest.py 解析 CLI 后，串起「读 PyTorch 任务 → 让 LLM 生成 CUDA kernel → 编译运行 → 剖析 → 修复/再优化」的多轮循环，所有产物按任务落盘到 code/、evaluation/、profile/、figures/ 目录。记忆机制被显式拆成两层：短期记忆是当前轮的 kernel 代码片段、错误日志与剖析结果，经 _build_history_block 组装成 Markdown 直接嵌入优化提示；长期记忆是 memorybank/ 下人工沉淀的硬件瓶颈与常见 kernel 结构知识。结构性决策在于把「评判」拆成 prompts/ 下多个 judger_* 模块（优化策略判断、编译超时分析、运行错误分析），由规则化的判官把 profiler 原始指标翻译成可执行的修复建议，再交回 LLM，而不是让 LLM 直接读原始 profile 文本。另有 optimization_tree.json 记录所有 kernel 的父子谱系与提速比，summary.json/summary.csv 汇总跨任务平均加速比与 token 用量，并支持按 summary 过滤掉不可运行任务以增量重跑。

### [AMD-AGI/AgentKernelArena](https://github.com/AMD-AGI/AgentKernelArena)

AgentKernelArena is a platform for evaluating and training AI agents for GPU kernel optimization, combining realistic tasks, correctness validation, and performance-based rewards for reinforcement learning.

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 受控实验平台: 统一任务契约 + 多 agent 适配层 + 独立评测打分 + A/B 对照 |
| 入口 | `make docker-run CONFIG=example_configs/quickstart_claude_mi300.yaml RUN_ARGS="--run-suffix baseline"`、`make docker-run CONFIG=example_configs/quickstart_claude_mi300.yaml RUN_ARGS="--run-suffix treatment"`、`make docker-parallel-run CONFIG=$CONFIG_PATH GPU_IDS=0,1,2,3`、`make slurm-run CONFIG=config_codex_mi355x_spur.yaml`、`make slurm-parallel-submit CONFIG=example_configs/benchmark_cursor_mi355x.yaml`、`make docker-smoke / make docker-check-agents CONFIG=$CONFIG_PATH`、`python3 src/tools/compare_runs.py workspace_.../run_<ts>_baseline workspace_.../run_<ts>_treatment`、`python3 main.py` |
| 基础层 | HIP、Triton、torch、AITer、vLLM、SGLang |
| 硬件厂商 | AMD |
| 硬件架构 | AMD CDNA 3 (MI300X)、AMD CDNA (MI100/MI200)、AMD RDNA (Radeon) |
| 评测 | 任务自带 config 与评测动作，平台独立编译校验计时并按 speedup 打分 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 123 |
| 最近推送 | 2026-10-28 |

> 核心设计是把「agent 改 kernel」与「评测 kernel」彻底分开：每个任务目录自带一份 config.yaml（schema v2）声明实现、基线、候选与评测动作，平台只负责建工作区、拼提示、跑 agent，然后由 src/evaluator.py、src/performance.py 独立编译、校验、计时，最后由 src/score.py 算出分数并写入 task_result.yaml。agent 通过注册表接入（@register_agent 装饰器 + AgentType 枚举），Cursor Agent、Claude Code、Codex、DeepSeek Harness、KernelForge、GEAK 都实现同一接口，因此同一任务集可以在不同 agent、不同模型、不同 prompt 下反复跑；平台自身不含 RL trainer、replay buffer 或策略更新回路，奖励信号以 task_result.yaml/CSV/JSON 报告形式外供。实验方法论是「只改被测能力」：用相同配置跑两次并以 run-suffix 区分 baseline/treatment，再用 src/tools/compare_runs.py 与可视化看板对照，对随机性 agent 要求重复配对运行并结合方差解读。工程上用每 GPU 一个隔离 Docker worker 从共享 .parallel/ 队列原子领取任务，任务级工作区带时间戳并保留日志、修改后源码与结构化结果，从而支持断点续跑（框架完成且源码证据仍有效的任务不重跑）。

### [AMD-AGI/Apex](https://github.com/AMD-AGI/Apex)

Agents, and RL environment, for optimizing GPU kernels on AMD ROCm using LLM agents. Benchmarks LLM serving workloads end-to-end, profiles bottleneck kernels, optimizes them via Claude Code or Codex, and scores on compilation, correctness, and speedup.

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 端到端优化流水线: benchmark-identify-optimize-grade-integrate + 知识库回注 |
| 入口 | `python3 workload_optimizer.py run -r ./results -b $MAGPIE_ROOT/examples/benchmarks/benchmark_vllm_gptoss_120b.yaml --kernel-types triton --top-k 10 --max-iterations 3 --max-turns 25 --leaderboard`、`python3 workload_optimizer.py benchmark -r $RESULTS -b $BENCH_CONFIG`、`python3 workload_optimizer.py identify -r $RESULTS --kernel-types triton --top-k 10`、`python3 workload_optimizer.py optimize -r $RESULTS --max-iterations 3 --max-turns 25`、`python3 workload_optimizer.py integrate -r $RESULTS`、`python3 workload_optimizer.py benchmark-final -r $RESULTS -b $BENCH_CONFIG`、`python3 workload_optimizer.py score -r $RESULTS --leaderboard`、`python3 workload_optimizer.py report -r $RESULTS -b $BENCH_CONFIG`、`python3 workload_optimizer.py optimize-kernel -r ./results --kernel path/to/baseline_kernel.py --kernel-type triton --correctness-mode pytorch`、`python3 eval.py --dry-run`、`python3 graders/kernel_grader.py / python3 graders/model_grader.py`、`python3 workload_optimizer.py export-rl -r ./results --export-output-dir ./datasets --sft`、`bash setup.sh --non-interactive` |
| 基础层 | HIP、Triton、torch、AITer、vLLM、SGLang |
| 硬件厂商 | AMD |
| 硬件架构 | AMD CDNA 3 (MI300X)、AMD CDNA (MI100/MI200) |
| 评测 | Magpie 负责编译、单测校验与计时，按 compiled/correct/speedup 公式打分 |
| 验证机制 | compile、correctness、runtime、static-check |
| Agent 循环 | 有 |
| 许可 | MIT |
| 星标 | 78 |
| 最近推送 | 2026-09-25 |

> workload_optimizer.py 是唯一 CLI，把整条链路拆成 benchmark → identify → optimize → integrate → benchmark-final → score → report 这些可单步也可一次跑完的子命令，结构上是典型的「剖析驱动选靶 + agent 改写 + 独立评分 + 回注验证」。评分不自己实现，而是委托给外部 Magpie 框架，仓库内只保留 graders/ 下的配置生成、ground truth 注册与缓存隔离（cache_manager）以保证可复现的评测条件。评分公式分为 kernel 级（compiled×20 + correct×100 + 分段 speedup 分，S<1 时给回退惩罚）与模型级（0.7×归一化 kernel 分 + 0.3×端到端吞吐提升比）两层，且只有同时编译并正确才计入加速分。优化产物通过 hot-patch 回注 site-packages：aiter/vllm/sglang 的 Triton .py 可直接替换并由 Triton JIT 自动重编译，aiter 的 .so 用 hipcc 重编译后替换，而系统级共享库与单体 _C.so 明确不支持，需重新编译源码；补丁在基准结束后会被还原。agent 侧不内置 agent 循环，而是通过 agents/backends.py 调 Claude Code / Codex / Cursor CLI，配合两层提示词（系统提示定义角色、MCP 工具清单与反作弊规则；任务提示带 GPU 架构参数、源码位置、剖析数据与知识库洞察）和 5 个 MCP 服务（源码检索、kernel RAG、GPU 信息、融合建议、Magpie 评测）扩展 agent 能力，跨轮经验沉淀在 pipeline/knowledge_base.py，反思在 reflector.py，最终以 export-rl 把轨迹导出为 RL/SFT 数据集，形成训练回流闭环。

### [AMD-AGI/GEAK](https://github.com/AMD-AGI/GEAK)

Generating Efficient AI-Centric Kernels

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 确定性 JS 编排 + 分层多 agent（Director→TechLead→专家工程师） |
| 入口 | `pip install "git+https://github.com/AMD-AGI/GEAK"`、`IS_SANDBOX=1 claude --dangerously-skip-permissions（随后自然语言触发 Workflow）`、`python interface/run_e2e.py run_spec.json result.json`、`node interface/runtime/engine/run_workflow.mjs kernel_workflow/kernel_workflow.js --agent codex --args '{"kernel_path":"/abs/kernel","workflow_dir":"...","budget":6}'`、`bash e2e_workflow/scripts/agentx_smoke.sh`、`node interface/runtime/engine/selftest.mjs` |
| 基础层 | Triton、HIP、torch、vLLM、SGLang |
| 硬件厂商 | AMD |
| 硬件架构 | AMD CDNA 3 (MI300X)、AMD CDNA (MI100/MI200)、AMD RDNA (Radeon) |
| 评测 | 每个补丁独立验证并按 warm-server 交错 A/B 吞吐差 + 输出 parity 判定 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 197 |
| 最近推送 | 2026-10-30 |

> 最重要的架构决策是把控制流从模型里挪出来：预算循环、fan-out、验证与停止条件全部写成确定性 JS（kernel_workflow.js / e2e_workflow.js），LLM 只在分析、策略与优化这些需要判断的环节被调用，因此运行可复现。kernel_workflow 采用 Director → TechLead → 算法/内存/计算/host_runtime 专家的分层结构，多轮且预算可控，并要求每个补丁由独立 agent 验证通过后才被接受，避免生成者自评。e2e_workflow 是包在 kernel 层之上的系统层：先 preflight 环境，再对运行中的 server 做 profile，按 Amdahl（pct_gpu_time × achievable_speedup）给热点排序，然后「先拉成本最低的杠杆」——配置/后端扫描 → 头部 GEMM 与 attention bake-off → 可编辑 kernel 里程碑循环；每个被接受的改动以可逆 overlay 方式叠回，并用 warm-server 交错 A/B（0.5% 带宽 + engagement proof + 输出 parity）作为放行门槛。跨轮记忆被显式建模为 insight blackboard 与 hypothesis ledger 两个构件，最佳补丁产物落在 kb_artifacts 作为下次运行的 warm-start 源。GPU 访问通过 flock 脚本串行化，因此可以一个 kernel 一个 agent 并行跑而安全共享同一 GPU。

### [Anjiang-Wei/Astra](https://github.com/Anjiang-Wei/Astra)

从 SGLang 的现成 CUDA 实现出发，让专门 Agent 协作进行生成、测试、profile 和规划。

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 单脚本多 agent 循环 + 基线对比（compare-kind 参数化分支） |
| 入口 | `python3 cuda_kernel_optimizer_multi.py --api-key <OPENAI_API_KEY> --initial-kernel-path <PATH_TO_INIT_CUDA_FILE> --compare-kind <KERNEL_TYPE> --baseline-func <BASELINE_FUNCTION_NAME> --generated-export-func <EXPORT_FUNCTION_NAME>` |
| 基础层 | CUDA-C++、SGLang |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 与 sgl_kernel 基线函数对比，按 compare-kind 生成对应测试 |
| 验证机制 | correctness、runtime |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 19 |
| 最近推送 | 2026-01-12 |

> README 非常精简，可确证的事实有限。仓库主体是单一脚本 cuda_kernel_optimizer_multi.py，通过 CLI 传入初始 .cu 文件路径、对比类型标签、基线函数名与生成的 PyBind 导出函数名，函数内部按 --compare-kind（rmsnorm / silu / mergestate / generic 等）分支决定测试生成提示。基线默认取 sgl_kernel 模块中的实现（若为空则自动回退到 sglang.sgl_kernel），说明对比对象取自 SGLang 的 kernel 实现。生成代码被期望导出一个与基线同名的顶层函数，供后续正确性与性能对比。迭代次数由 --max-iterations 控制（默认 5）。每次运行的结果写入带时间戳的 cuda_optimization_runs/ 目录以保留多次运行记录。README 未展开 agent 组成、角色划分与具体打分方式，因此这些细节不做推断。

### [meta-pytorch/KernelAgent](https://github.com/meta-pytorch/KernelAgent)

Autonomous GPU Kernel Generation & Optimization via Deep Agents

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 分层多 Agent 流水线: 静态路由-子图融合-并行生成-端到端组合 + 硬件引导优化环 |
| 入口 | `python -m Fuser.auto_agent --problem /abs/path/problem.py --verify`、`python -m Fuser.pipeline --problem ... --extract-model gpt-5 --dispatch-jobs auto --workers 4`、`python scripts/triton_ui.py / kernel-agent / fuser-ui / pipeline-ui`、`python scripts/optimization_ui.py --port 8085`、`python examples/run_opt_manager.py --kernel-dir optimize_01_matvec --strategy beam_search`、`TritonKernelAgent(num_workers=4, max_rounds=8).generate_kernel(...)` |
| 基础层 | Triton、torch |
| 硬件厂商 | NVIDIA、Intel |
| 硬件架构 | — |
| 评测 | 内部校验+基准：沙箱子进程单测对比 PyTorch，NCU 指标与 CUDA event 计时 |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 610 |
| 最近推送 | 2026-09-08 |

> 先用 AutoRouter 对问题做 AST 静态分析（注意力块、转置卷积、控制流、长算子链）决定走轻量直连路径还是完整 Fuser 流水线，路由决策缓存在 .fuse/router_cache.json 并可回退。Fuser 侧由 LLM 输出 JSON 子图描述（算子、shape、dtype、参数），按 shape 签名去重复用 kernel，Dispatcher 并行拉起多个 TritonKernelAgent 进程，Composer 把已验证 kernel 拼回单个 Triton 程序并跑自测。生成侧 worker 池迭代让 LLM 改进代码，在沙箱子进程中执行单测并禁止 PyTorch fallback，只有打印 PASS 且退出码 0 才算成功。优化侧以 NCU 28 项指标 + roofline 判定驱动 LLM 诊断与改写，对 PyTorch 参考做数值校验，再用 CUDA event 计时跟踪 best-so-far 并在性能退化时回滚。所有阶段产物落盘到 .fuse/<run_id> 与 .optimize/<run_id> 以支持复现。

### [mindspore-ai/akg](https://github.com/mindspore-ai/akg)

AKG (Auto Kernel Generator) is an optimizer for operators in Deep Learning Networks, which provides the ability to automatically fuse ops with specific patterns.

| 项 | 内容 |
| --- | --- |
| 角色 | 编译器底座 |
| 架构模式 | 编译器主线 + 大模型 Agent 副线的双子项目仓库 (AKG-MLIR / AKG-AGENT) |
| 入口 | `参考 akg_agents/README_CN.md 安装使用 AKG-AGENT`、`参考 akg-tvm/README.md 使用 AKG-TVM`、`参考 akg-mlir/README.md 使用 AKG-MLIR` |
| 基础层 | AKG、Triton、MLIR |
| 硬件厂商 | NVIDIA、Ascend、CPU、Other |
| 硬件架构 | — |
| 评测 | AKG-AGENT 内置 AscendKernelBench 评测平台与算子知识库 |
| 验证机制 | compile |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 264 |
| 最近推送 | 2026-10-29 |

> 2.4 之后重构为两个子项目：AKG-AGENT 是大模型驱动的算子生成工具，提供基于 Multi-agent 的算子自动生成框架、AscendKernelBench 评测平台与算子知识库，当前支持用 LLM 生成 Triton-Ascend（Atlas A2/A3）与 SWFT（300I DUO）DSL 并完成 kernel 编译；AKG-MLIR 则是基于 MLIR 的深度学习编译器，含 CPU/GPU/Ascend 的完整算子编译 pipeline、MindSpore Dialect 图编译方言以及 Linalg/Affine/GPU 方言扩展，并对接 AscendNPU IR 支持昇腾后端融合算子生成。两个子项目可各自独立安装构建，共用同一仓库的多后端支持目标。

### [OptimAI-Lab/CudaForge](https://github.com/OptimAI-Lab/CudaForge)

Official Repo of CudaForge

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 单入口 Python 多智能体循环: 生成 kernel - 测正确性 - 分析硬件反馈 - 迭代改进 |
| 入口 | `conda env create -f environment.yml`、`python3 main.py KernelBench/level1 --first_n 100 --gpu "Quadro RTX 6000" --server_type openai --model_name o3 --device 0 --round 10 --subproc_id 0`、`python3 main.py KernelBench/level1/1_Square_matrix_multiplication_.py --gpu "Quadro RTX 6000" --round 10`、`nvcc --version / ncu --version (版本自检)` |
| 基础层 | CUDA-C++、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | KernelBench 任务目录 + 正确性测试 + ncu 硬件反馈 |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | MIT |
| 星标 | 94 |
| 最近推送 | 2025-12-02 |

> README 极简，只能确认这是一个免训练的多智能体工作流，模仿人类专家的迭代节奏：先写初始 kernel、测正确性、分析硬件反馈、再迭代改进。所有执行都收敛到一个 main.py 脚本，参数指定 KernelBench 任务目录、GPU 型号、服务与模型类型、轮次数以及 subproc_id 与 device 以支持并行。关键的外部依赖约束是 nvcc 与 Nsight Compute (ncu) 必须与 CUDA Toolkit 版本一致，且 ncu 需要 sudo 权限读取 GPU 性能计数器，README 给出了免密 sudo 的配置方法。仓库内部结构在 README 中完全没有交代。

### [RightNow-AI/autokernel](https://github.com/RightNow-AI/autokernel)

Autoresearch for GPU kernels. Give it any PyTorch model, go to sleep, wake up to optimized Triton kernels.

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 固定评测 + 编辑-评测-保留/回滚 循环，单文件作用域 + Amdahl 定律调度 |
| 入口 | `uv sync && uv run prepare.py`、`uv run profile.py --model models/llama_7b.py --class-name LlamaModel --input-shape 1,512 --dtype float16`、`uv run extract.py --top 5 --backend triton\|cuda`、`uv run bench.py`、`uv run verify.py`、`uv run export_hf.py --name my_matmul`、`uv run kernelbench/bridge.py fetch --source hf --level 1 / setup --level 1 --problem 1`、`uv run kernelbench/bench_kb.py / uv run kernelbench/scorer.py --level 1`、`对 agent 下达指令: Read program.md and let's kick off a new experiment` |
| 基础层 | Triton、CUDA-C++、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200)、NVIDIA Ampere (A100)、NVIDIA Ada (L40S/4090)、AMD CDNA 3 (MI300X) |
| 评测 | bench.py 固定五阶段正确性加 roofline，桥接算 fast_p |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | MIT |
| 星标 | 1614 |
| 最近推送 | 2026-10-23 |

> 把 agent 的作用域限制为只改 kernel.py 一个文件，跑固定 bench.py 后按结果保留或回滚，保证 diff 可读、回滚干净，同时评测脚本本身不被 agent 触碰。流程按 profile（torch.profiler 按 GPU 时间排序并判定 compute/memory bound）→ extract（把瓶颈抽成独立 Triton 或 CUDA C++ kernel）→ orchestrate（用 Amdahl 定律决定下一个优化对象）→ verify（把优化 kernel 塞回模型做端到端正确性与总加速比）串起来。设计上正确性优先于性能：先与 PyTorch 对拍再计时，错的立即回滚；实验结果以 results.tsv 纯文本追加，program.md 里写足 6 层优化手册与崩溃处理，让 agent 能连续跑十小时不卡住。

### [taratt/cutegen](https://github.com/taratt/cutegen)

An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 生成-测试-修正循环 + 节点持久化 (generate-test-refine, 延迟 profiling) |
| 入口 | `python cutegen/main.py (主流程)`、`python -u scripts/smoke_test_ptx_runtime.py (PTX 运行时自检)`、`python -u scripts/run_profiled_sample.py --backend ptx\|triton`、`KERNEL_BACKEND=ptx python -u cutegen/replay_saved_nodes.py --path saved_nodes/ptx/... --num_warmups 5 --num_trials 100`、`KERNEL_BACKEND=triton USE_PROFILING=false python -u -m cutegen.main` |
| 基础层 | CUDA-C++、CUTLASS、Triton |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 编译→全量正确性→CUDA event 计时(5 warmup/100 trial)→可选 NCU→重试修复 |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | NOASSERTION |
| 星标 | 7 |
| 最近推送 | 2026-09-04 |

> 核心抽象是多后端共用一条流水线：CUDA、CuTe、PTX、Triton 四个后端复用同一套编译、正确性检查、CUDA event 计时、Nsight Compute 剖析、重试修复与节点持久化逻辑，后端只由 KERNEL_BACKEND 环境变量切换。PTX 路径走 CUDA Driver API 集成，结果保存在 saved_nodes/ptx/ 下。剖析是可选且可延迟的，USE_PROFILING=false 即关闭 ncu，另有按类别设定剖析深度的样例脚本，以控制 profiling 开销。节点式持久化让每个中间结果都可离线重放复现，replay_saved_nodes.py 能用与评测完全一致的流程重新计时。README 还区分了实验入口与 GPU 集成自检脚本两类命令。

### [zhang677/AccelOpt](https://github.com/zhang677/AccelOpt)

[MLSys 2026] AccelOpt: Self-improving Agents for AI Accelerator Kernel Optimization

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 自改进 Agent 循环 + 优化记忆库 + 结构化 kernel 数据库 + profiling 服务 |
| 入口 | `python setup.py install`、`experiments/full_complete_local (Trainium 上跑 NKIBench)`、`experiments/flb_full_complete_local (NVIDIA 上跑 FlashInfer-Bench)`、`from accelopt.kernel_wrapper import NKIKernel; nki_kernel.profile(save_fields)`、`experiments/full_complete_local/calculate_percentage_of_peak.py` |
| 基础层 | Triton、FlashInfer |
| 硬件厂商 | Trainium、NVIDIA |
| 硬件架构 | NVIDIA Hopper (H100/H200) |
| 评测 | 以 NKIBench/FlashInfer-Bench 任务集驱动，profile 测延迟并算峰值占比 |
| 验证机制 | runtime、profile |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 79 |
| 最近推送 | 2026-07-28 |

> 核心机制是迭代生成 kernel，并把遇到的「慢 kernel→快 kernel」对比 curate 成优化记忆再注入下一轮提示，从而免去专家提供的硬件特定优化知识。角色分工上，executor 负责生成新 kernel，Fixer 专门修复失败的 kernel，README 明确两组 agent 可使用不同模型。产物流转靠结构化存储：生成结果用 templates/schema_v2.txt 的 SQL schema 存入 supabase kernel 数据库，NKIBench 与 FlashInfer-Bench 共用类似 schema。评测侧提供可插拔的 profiling 服务（NKIKernel.profile），并用「相对硬件可达峰值的百分比」衡量 agent 是否真正穷尽优化空间。

### [zhang677/PCL-lite](https://github.com/zhang677/PCL-lite)

[ICML 2025] Adaptive Self-improvement LLM Agentic System for ML Library Development

| 项 | 内容 |
| --- | --- |
| 角色 | Agent 搜索循环 |
| 架构模式 | 自适应自改进 Agent + 结构化 IR（benchcard）+ 脚本化实验矩阵 |
| 入口 | `./scripts/validate.sh`、`./scripts/prepare.sh`、`./experiments/single/run.sh`、`./experiments/agent/run.sh`、`./experiments/iterative/run.sh`、`./experiments/single-ws/run.sh` |
| 基础层 | None |
| 硬件厂商 | Other |
| 硬件架构 | — |
| 评测 | benchmark/ 下 test+reference yaml，先校验再 prepare 出 benchcard |
| 验证机制 | static-check、correctness |
| Agent 循环 | 有 |
| 许可 | MIT |
| 星标 | 17 |
| 最近推送 | 2026-01-06 |

> README 极短，只给出脚本级流程：先跑 validate.sh 校验 /benchmark 与 /prompts 下的 test 与 reference yaml，再跑 prepare.sh 生成 benchcard，然后按 single、agent、iterative、single-ws 四种模式执行实验。实验矩阵用「有无 agent / 有无迭代 / 有无结构化 IR」三个正交开关组合，single-ws 即「single without structural IR」的消融对照，说明结构化 IR 是该系统的关键载体。模型接入靠 MODEL_NAME 加环境变量（ANTHROPIC/OPENAI/TOGETHER/DEEPSEEK 的 base 与 key），采样数与温度可调。

### [AI9Stars/AutoTriton](https://github.com/AI9Stars/AutoTriton)

以监督与强化学习提高 Triton 代码生成能力。

| 项 | 内容 |
| --- | --- |
| 角色 | 数据集 / 模型 |
| 架构模式 | 两段式训练: SFT 打底 + GRPO 强化学习（规则奖励 + 执行奖励顺序叠加） |
| 入口 | — |
| 基础层 | Triton |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 无 |
| 验证机制 | none |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 68 |
| 最近推送 | 2025-07-14 |

> README 极短，实质是一篇工作说明 + 权重发布页：仓库本身不含训练或推理代码。可确证的事实是训练方法为两段式——先用一条高质量数据采集流水线做 SFT 让模型获得必要的 Triton 编程能力，再做 GRPO 强化学习，把规则型奖励与执行型奖励组合起来依次施加。基座模型是 ByteDance-Seed 的 Seed-Coder-8B-Reasoning，权重以 8B 形式发布在 HuggingFace。评测侧引用 TritonBench 与 KernelBench 的五个评测通道，结果声称与 Claude-4-Sonnet、DeepSeek-R1-0528 等主流大模型相当。结构上没有代码目录、脚本或入口点，所有可复用资产（模型与论文）都托管在外部平台。

### [AMD-AGI/AMDKernelVault](https://github.com/AMD-AGI/AMDKernelVault)

AMDKernelVault A research and engineering playground for HIP and Triton kernel generation, optimization, and LLM training, including continued pretraining, SFT, and RL (RLHF/RLVR) pipelines.

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 全栈训练框架: CPT-SFT-RL 三段流水线 + 数据生成器 + 独立验证服务 |
| 入口 | `cd cpt && bash run_train_cpt.sh`、`cd sft && bash run_train_full_sft.sh`、`cd rl/rl4kernel_hip && bash scripts/train/react_single_turn_v1_hip2hip.sh --train <parquet> --val <parquet> --sf-url http://host:8080/run_code`、`cd rl/rl4kernel_hip/hip_kernel_evaluation_server && HIP_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 ./setup_server_req_deploy_hip2hip_batch.sh`、`cd hip-kernel-generator && pip install -e ./torch_modu2func_kit[dev] && pip install -e ./torch2hip_kit[dev] && pip install -e ./py_hip_kernel2kernel_kit[dev]`、`huggingface-cli download amd/hip_llm_dataset --repo-type dataset --local-dir hip_llm_dataset` |
| 基础层 | HIP、Triton、torch |
| 硬件厂商 | AMD |
| 硬件架构 | AMD CDNA 3 (MI300X) |
| 评测 | HIP evaluation server 提供编译/正确性/延迟反馈，供 RL 取奖励 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | Apache-2.0 |
| 星标 | 10 |
| 最近推送 | 2026-10-07 |

> 仓库以三个训练阶段目录 cpt/、sft/、rl/ 平行组织，每个阶段自带 README、启动脚本与 train_yamls/ 配置，运行时只需改 YAML 里的 model_name_or_path、dataset、output_dir 三个字段即可换实验。训练数据完全外置在 HuggingFace 的 amd/hip_llm_dataset，并按 cpt/、sft/、rl/ 三级目录与 pretrain_hip、FIM_hip、rl_raw_hard_3k、rl_mi300x_verl_filtered 等固定数据集名对齐，保证三个阶段共用一套数据契约。RL 侧按目标语言拆成两条技术栈：rl4kernel_hip 是 veRL 单轮训练，必须先独立部署 HIP kernel evaluation server 才能拿到奖励；rl4kernel_triton 则是 Slime 多轮训练，自带 ROCm 执行服务、pin 住的容器配方与 32×MI325X 的训练配置说明。数据生成侧再拆成三个可独立 pip 安装的 kit 包（torch_modu2func_kit / torch2hip_kit / py_hip_kernel2kernel_kit），分别负责模块转函数、模块转 HIP kernel、HIP kernel 到优化版 HIP kernel。值得注意的是准备好的参考实现、测试用例、prompt 与 checkpoint 仍留在仓库之外，各阶段 README 承担了大部分操作性说明。

### [ByteDance-Seed/cudaLLM](https://github.com/ByteDance-Seed/cudaLLM)

基于 Qwen3-8B 的 CUDA 专用模型，模型卡记录两阶段 SFT 与性能反馈 RL。

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 两段式训练: SFT → RL（编译+测试结果作奖励） |
| 入口 | `python3 cuda_dataset.py`、`bash scripts/sft.sh`、`bash scripts/eval.sh`、`bash scripts/rl.sh` |
| 基础层 | CUDA-C++、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 基于 KernelBench 评测 SFT/RL 后模型的生成准确率 |
| 验证机制 | compile、correctness |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 156 |
| 最近推送 | 2025-08-18 |

> 流程被组织成四个显式步骤：先用 cuda_dataset.py 把原始数据处理成 SFT 用 parquet（sft_cuda_llm_r1.parquet）与 RL 用 parquet（rl_cuda_llm_0424.parquet），再跑 SFT、在 KernelBench 上做基线评测、最后进入 RL。训练框架不是自研而是外部克隆的 veRL，且 README 明确要求 pin 到指定 git SHA（abb87bc…）并用 --no-deps 安装，以保证复现。SFT 数据由 DeepSeek R1、DeepSeek Coder-7B、Qwen2-32B 生成，评测集固定用 ScalingIntelligence 的 KernelBench。RL 阶段的设计要点是奖励来源与训练分离：每个节点用 4 张 GPU 跑训练循环，另 4 张 GPU 专门运行模型生成的 CUDA kernel，编译并测试后把结果作为奖励回传，因此硬件配比是 4+4。SFT 后的 eval.sh 结果作为 RL 前的基线，RL 结束后可再跑同一脚本量化提升。

### [BytedTsinghua-SIA/CUDA-Agent](https://github.com/BytedTsinghua-SIA/CUDA-Agent)

CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation

| 项 | 内容 |
| --- | --- |
| 角色 | 数据集 / 模型 |
| 架构模式 | 标准化 agent 工作区模板: 实现-编译-校验-剖析 四步自愈循环 |
| 入口 | `bash utils/compile.sh`、`python3 -m utils.verification`、`python3 -m utils.profiling` |
| 基础层 | CUDA-C++、torch、torch.compile |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 工作区内置 verification 校验数值、profiling 对比基线与 torch.compile |
| 验证机制 | compile、correctness、runtime、profile |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 1346 |
| 最近推送 | 2026-07-08 |

> 仓库给出三件东西：RL 训练出的 CUDA kernel 生成模型、6K 规模的训练数据集 CUDA-Agent-Ops-6K，以及一个标准化 agent 工作区 agent_workdir。工作区把「实现 CUDA kernel → 编译 → 校验正确性 → profile 性能 → 迭代」这条闭环固化成模板：model.py 放原始 PyTorch 基线、model_new.py 放用自定义 CUDA 扩展的优化版本、kernels/ 放自定义 CUDA/C++ kernel 及其绑定，binding.cpp 与 binding_registry.h 提供共享的 Python 绑定注册基础设施以免每个 kernel 重复样板，utils/compile.py 与 compile.sh 负责构建扩展，verification.py 做正确性校验，profiling.py 把性能与基线及 torch.compile 双基线对比，SKILL.md 以技能文件形式向 agent 下发工作流约束与优化规则。数据集的构造是一条明确的合成流水线：从 torch 与 transformers 收集参考算子，用 LLM 把多个算子组合成融合任务，再用规则过滤保留可执行、确定性且非平凡的样本；过滤标准要求样本在 eager 与 torch.compile 两种模式下都能正确执行，剔除随机算子与退化输出，控制运行时长，并移除与 KernelBench 测试高度相似的样本以降低污染风险。

### [CSJianYang/Industrial-Coder](https://github.com/CSJianYang/Industrial-Coder)

32B 工业代码基础模型，统一芯片设计、GPU kernel、嵌入式和编译器优化等场景。

| 项 | 内容 |
| --- | --- |
| 角色 | 数据集 / 模型 |
| 架构模式 | 通用工业代码基础模型: Code-Flow 三段训练 + 多领域工业仿真环境 |
| 入口 | `transformers: AutoModelForCausalLM.from_pretrained("Multilingual-Multimodal-NLP/IndustrialCoder")`、`vllm serve Multilingual-Multimodal-NLP/IndustrialCoder --tensor-parallel-size 4 --max-model-len 32768`、`bash scripts/binarize_data.sh /path/to/data.jsonl /path/to/output /path/to/IndustrialCoder-Base 16384`、`bash scripts/run_sft.sh configs/sft_32b.yaml`、`bash start.sh`、`python download_model.py --repo_id Multilingual-Multimodal-NLP/IndustrialCoder-Base --local_dir /path/to/save/model` |
| 基础层 | CUDA-C++、Triton、torch |
| 硬件厂商 | NVIDIA、Other |
| 硬件架构 | x86 CPU、ARM CPU |
| 评测 | 无 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 118 |
| 最近推送 | 2026-03-27 |

> InCoder-32B 是一个跨工业领域的通用代码基座模型，GPU kernel 优化只是它覆盖的一个域。训练流程被命名为 Code-Flow 三段式：预训练与退火 → 中训练扩展上下文（8K→32K→128K 两级子阶段）→ 执行接地的后训练 SFT。语料侧的可确证做法包括许可过滤、PII 去除与多级去重（精确哈希、token 级近重复、repo 级 fork 合并），并在 4096 GPU 上以自回归 LM 加 FIM 方式训练。中训练阶段会合成工业 QA（场景规格 → 种子代码生成 → 带自动验证的 QA 对合成），并构造 Thought-Action-Observation 形式的 agent 轨迹，反馈来自硬件仿真器、综合工具、C/C++ 编译器与形式验证引擎；后训练用 250 万条真实工业任务样本做执行接地 SFT，并从编译器报错、运行日志、波形差异与性能瓶颈中提炼闭环修复轨迹。正确性判据被绑定到具体工具链：芯片设计用 Icarus Verilog/Verilator/Yosys，GPU 优化用 nvcc 与 @triton.jit（数值正确性 + CUDA 计时），3D 建模用 CadQuery/OpenCascade（体积 IoU），嵌入式用 arm-none-eabi-gcc 加 Renode，编译器优化用 x86-64 GCC/LLVM 测试台。仓库本身主要发布模型权重与一个轻量 sft/ 目录（YAML 配置 + 数据二值化 + 训练脚本），不提供 kernel 专用 pipeline。

### [hgl71964/cuasmrl](https://github.com/hgl71964/cuasmrl)

在 NVIDIA SASS 指令层把调度改写建模为 assembly game，以 PPO 和实机吞吐奖励优化既有 CUDA kernel。

| 项 | 内容 |
| --- | --- |
| 角色 | 编译器底座 |
| 架构模式 | Triton 编译器主仓 + 附加 cuasmrl 包的 fork 结构 |
| 入口 | `python -m venv .venv --prompt triton && pip install -e python`、`pip install -e cuasmrl (需先 clone CuAssembler 并设置 PYTHONPATH)`、`git clone https://github.com/hgl71964/CuAssembler.git` |
| 基础层 | Triton、CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 无 |
| 验证机制 | none |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 19 |
| 最近推送 | 2024-11-09 |

> 该仓库 README 几乎完全是 Triton 上游的源码构建说明（venv 依赖、clang+lld、ccache、vscode compile_commands 配置），仅在 Install 段落追加了 CuAssembler 的 clone 与 PYTHONPATH 设置、以及 pip install -e cuasmrl。README 未描述 cuasmrl 包自身的结构、训练流程或用法，也未提及任何 RL 细节。可确证的结构性事实是：这是一个 Triton 编译器 fork，需要按 triton → pytorch → triton 的顺序依次构建以保证版本匹配。

### [hkust-nlp/KernelGYM](https://github.com/hkust-nlp/KernelGYM)

[KernelGYM & Dr. Kernel] A distributed GPU environment and a collection of RL training methods to support RL for Kernel Generations [ICML 2026]

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 评测服务三段式: API-任务队列-GPU worker，外加可插拔 backend/toolkit/workflow 三层抽象 |
| 入口 | `bash setup.sh`、`./start_all_with_monitor.sh (单机启动 API+worker+监控)`、`./start_worker_multinode.sh (多节点 worker)`、`python -m kernelgym.server.api.server`、`bash scripts/auto_configure.sh (自动生成 .env)`、`POST http://localhost:10907/evaluate`、`POST http://localhost:10907/workflow/submit` |
| 基础层 | CUDA-C++、Triton、torch、torch.compile |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | Redis 队列分发任务，GPU worker 子进程隔离执行，CUDA event 计时并按容差比对参考实现 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 216 |
| 最近推送 | 2026-03-29 |

> 整体是分布式评测服务：客户端 → FastAPI → Redis 任务队列 → 各节点 GPU worker，worker 内部再用子进程池隔离 CUDA 错误。核心抽象拆成 Backend（编译/加载/运行）、Toolkit（正确性与性能逻辑）、Workflow Controller（编排）三层，并以 register_backend/register_toolkit 方式支持扩展到物理模拟、渲染等新 GPU 任务类型。计时统一用 CUDA event 而非 wall-clock，并支持 warmup 与多次 trial。仓库内另有 drkernel/ 目录，提供与 VERL 框架对接的分布式 RL 训练、基于编译/正确性/性能的多维奖励函数与训练脚本。

### [ornith-ai/CUDA-L1](https://github.com/ornith-ai/CUDA-L1)

CUDA-L1: Improving CUDA Optimization via Contrastive Reinforcement Learning

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 对比式 RL 训练 + 产物仓库 (逐行 JSON 记录 ref/custom/cuda_graph 代码与四组 score) |
| 入口 | `取 optimized_cuda_code/<device>.json 中的代码片段在对应 GPU 上逐条运行复现`、`在 KernelBench 的 250 个 PyTorch workload 上评测 speedup 与成功率` |
| 基础层 | CUDA-C++、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Ampere (A100)、NVIDIA Hopper (H100/H200)、NVIDIA Ada (L40S/4090) |
| 评测 | KernelBench 250 任务，跑四组基线配置比较 speedup 与成功数 |
| 验证机制 | runtime |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 327 |
| 最近推送 | 2025-11-03 |

> README 描述的是研究成果与发布产物，而非训练代码入口：核心是对比式强化学习框架，用比较学习的方式增强 CUDA 优化。发布物按 GPU 型号分别组织（h100.json 等），每行一个 JSON 对象，记录 KernelBench 的 level_id/task_id、参考 CUDA 代码、CUDA-L1 生成的 custom_code、CUDA Graph 版本代码，以及 default、torch.compile、torch.compile+ReduceOverhead、CUDA Graph 四种基线下的时间比 score。评测在 A100、3090、H100、H20、L40 上对照四组基线统计 mean/max/分位数加速比与成功数。README 明确披露了 RL 阶段的 reward hacking 风险（利用计时测量与缓存结果）并列出对应修复项。

### [ornith-ai/CUDA-L2](https://github.com/ornith-ai/CUDA-L2)

CUDA-L2: Surpassing cuBLAS Performance for Matrix Multiplication through Reinforcement Learning

| 项 | 内容 |
| --- | --- |
| 角色 | 数据集 / 模型 |
| 架构模式 | RL 产出的 kernel 资产库 + 离线/服务器双模式评测脚本（对标 cuBLAS 系列） |
| 入口 | `./eval_one_file.sh --mnk 64_4096_64 --acc_precise fp32 --device_type a100 --warmup_seconds 5 --benchmark_seconds 10 --base_dir ./results --gpu_device_id 7 --mode offline`、`./eval_one_file.sh ... --mode server --target_qps 100`、`git clone -b v4.2.1 https://github.com/NVIDIA/cutlass.git cutlass` |
| 基础层 | CUTLASS、CUDA-C++、torch |
| 硬件厂商 | NVIDIA |
| 硬件架构 | NVIDIA Ampere (A100)、NVIDIA Hopper (H100/H200) |
| 评测 | eval_one_file.sh 离线/服务端模式测时间与 QPS，对标 torch.matmul 与 cuBLAS 系列 |
| 验证机制 | compile、runtime |
| Agent 循环 | 无 |
| 许可 | MIT |
| 星标 | 486 |
| 最近推送 | 2026-03-30 |

> README 呈现的是一个产物型仓库：系统本体是 LLM 加 RL 自动优化半精度 GEMM 的 CUDA kernel，发布形态是按硬件与累加器精度分批放出的 kernel 集合（已放出 A100、RTX 3090、H100 上 1000 组配置，区分 16 位与 32 位累加器）。评测只有一条路径 eval_one_file.sh，用 mnk、累加器精度、设备类型、warmup/benchmark 秒数、gpu id 与 offline/server 模式等参数驱动，server 模式还需指定目标 QPS。工程上把 CUTLASS 锁死到 v4.2.1 并要求显式设置 CUTLASS_DIR 与 TORCH_CUDA_ARCH_LIST，因为版本或路径不对会静默失败。跨机型复用被明确否定：A100 上训练的 kernel 只保证在 A100 上有加速。

### [QiMeng-IPRC/QiMeng-Kernel](https://github.com/QiMeng-IPRC/QiMeng-Kernel)

[AAAI 2026] QiMeng-Kernel: Macro-Thinking Micro-Coding Paradigm for LLM-Based High-Performance GPU Kernel Generation

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 训练-推理-评测三段脚本化流水线 (train / inference / eval_generations) |
| 入口 | `pip install -r requirements.txt && pip install -e .`、`bash scripts/train.sh <base_model> <num_envs>`、`bash scripts/inference.sh <checkpoint_path> <llm_api_baseurl> <llm_api_key> <llm_api_model> <dataset_name>`、`bash scripts/eval_generations.sh <benchmark> <run_dir> <subset_name>` |
| 基础层 | — |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | eval_generations.sh 按 benchmark 与子集评测 |
| 验证机制 | none |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 10 |
| 最近推送 | 2026-05-24 |

> 论文官方实现的公开版本，核心是 Macro-Thinking Micro-Coding 范式，但 README 基本只给出三个脚本入口：train.sh 启动训练并接受 base_model 与 num_envs 参数（说明是带并行环境的训练），inference.sh 用 checkpoint 配合外部 LLM API 生成 kernel，eval_generations.sh 在指定 benchmark 与子集上评测生成结果。结果以 KernelBench 与 TritonBench 两套榜单图片呈现，仓库未披露内部目录结构、模型结构或奖励设计。README 明确说明仓库仍在积极开发中，训练与离线数据集将于近期发布。

### [QiMeng-IPRC/QiMeng-MuPa](https://github.com/QiMeng-IPRC/QiMeng-MuPa)

[NeurIPS 2025] QiMeng-MuPa: Mutual-Supervised Learning for Sequential-to-Parallel Code Translation

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 互监督双阶段: co-verify (翻译与单测互相验证造数据) - co-evolve (用该数据微调) |
| 入口 | `uv sync 或 pip install -e .`、`bash scripts/build_sft.sh (co-verify: 造 SFT 数据)`、`bash scripts/eval_pass_k.sh (评测 Pass@k)`、`LLaMA-Factory 微调 (外部仓库, 注册 co-verify 产出的数据集)` |
| 基础层 | vLLM |
| 硬件厂商 | CPU、NVIDIA |
| 硬件架构 | — |
| 评测 | 自带单测的测试集 + eval_pass_k.sh 统计 Pass@k |
| 验证机制 | correctness、runtime |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 12 |
| 最近推送 | 2025-11-03 |

> 核心是 mutual-supervised learning：一个模型做串行到并行代码翻译，另一个做单元测试生成，两者互为验证条件，产出可用于 SFT 的数据，scripts/build_sft.sh 用 vllm 做批量推理完成这一步。随后是 co-evolve 阶段，直接复用 LLaMA-Factory 在该数据上微调，得到 Qwen3-0.6B-translator 模型（已发布在 HuggingFace）。评测侧用 eval_pass_k.sh 计算 Pass@k，测试集为 resources 下自带单元测试的 jsonl；环境用 uv.lock 保证完全可复现。README 强调端到端的训练与评测代码尚未发布。

### [RLsys-Foundation/TritonForge](https://github.com/RLsys-Foundation/TritonForge)

🔥 LLM-powered GPU kernel synthesis: Train models to convert PyTorch ops into optimized Triton kernels via SFT+RL. Multi-turn compilation feedback,    cross-platform NVIDIA/AMD, Kernelbook + KernelBench

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 全栈训练框架: 同一 SLIME 框架承载 SFT-RL 两段 + 独立 KBenchEval 评测目录 |
| 入口 | `bash SLIME/scripts/run-qwen3-8B-kernelbook-sft.sh (SFT 阶段)`、`bash SLIME/scripts/run_agent_kbench_qwen3_8B_sft_fixed.sh (RL 阶段)`、`python KBenchEval/scripts/generate_and_eval_single_sample.py dataset_src=huggingface level=1 problem_id=19`、`python -m sglang.launch_server --model-path models/Qwen3-8B-Kernelbook-SFT-HF --tp 2`、`python kernelbench_amd_tools/scripts/run_qwen3_evaluation_robust.py --levels 1,2` |
| 基础层 | Triton、torch、SGLang |
| 硬件厂商 | NVIDIA、AMD |
| 硬件架构 | NVIDIA Hopper (H100/H200)、AMD CDNA 3 (MI300X) |
| 评测 | KBenchEval 基于 KernelBench 200+ 题评正确性与加速比 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 有 |
| 许可 | 未声明 |
| 星标 | 153 |
| 最近推送 | 2025-11-10 |

> 仓库由两块组成：SLIME/ 是打过 bug 修复与优化的 RL 框架，slime_plugins 提供可插拔的自定义生成器与奖励函数；KBenchEval/ 是基于 KernelBench 的评测框架。SFT 与 RL 两阶段共用同一个 SLIME 框架，RL 阶段在 KernelBench Level 1-2 上做最多 3 轮迭代，奖励由编译成功、功能正确与 speedup 三项组成，折扣因子 gamma 取 0.4。训练与推理解耦：用 SGLang 起服务做 rollout，NVIDIA 与 AMD 各有一套 Docker 镜像分别锁定 CUDA 12.6.1 与 ROCm 6.3.4，并开放全部中间 checkpoint 与训练配方以便复现。

### [ScalingIntelligence/kernelbench-tinker](https://github.com/ScalingIntelligence/kernelbench-tinker)

Tinker ↔ KernelBench Integration enabling RL for GPU Kernel Generation

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | RL 闭环: Tinker Env 单轮交互 + Modal 远程评测 + 奖励整形 |
| 入口 | `uv run modal deploy src/kernelbench_tinker/modal/app.py`、`uv run python -m kernelbench_tinker.scripts.train_kernel_rl --config src/kernelbench_tinker/config/rl_kernelbench.yaml log_path=./runs/my_experiment`、`uv run python -m kernelbench_tinker.scripts.eval_kernel_rl checkpoint_path=... level=1 output_path=...`、`just train run=my_experiment`、`just resume run=my_experiment`、`just status run=my_experiment`、`just logs run=my_experiment`、`uv run python -m kernelbench_tinker.scripts.run_and_check` |
| 基础层 | torch、CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 复用 KernelBench 检查器，在 Modal 隔离 GPU 上编译+正确性+计时 |
| 验证机制 | compile、correctness、runtime、static-check |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 31 |
| 最近推送 | 2026-03-05 |

> KernelBench 以 git submodule 嵌入并从本地路径安装成 Python 包，环境从 KernelBench 取题并用 Tinker Renderer 格式化为观测；动作是模型产出的候选 kernel，环境解析响应中的 <KERNEL> 块后送到 Modal 隔离 GPU 容器编译、测试并 profile，再把正确性、加速比与静态检查结果按 RewardConfig 折成标量奖励。扩展点是 KernelBenchEnvGroupBuilder（分组归一化实现 GRPO）与 KernelBenchDatasetBuilder（按 level 划分训练/评估集）。

### [Wangyaoyuu/SparseRL](https://github.com/Wangyaoyuu/SparseRL)

[ICLR'26 Oral] The open-source code release for the SparseRL paper ("Mastering Sparse CUDA Generation Through Pretrained Models and Deep Reinforcement Learning").

| 项 | 内容 |
| --- | --- |
| 角色 | 训练流水线 |
| 架构模式 | 预训练-SFT-PPO 三段式 + 编译器/执行器反馈的层次奖励 |
| 入口 | `python -m sparserl.train_sft --dataset-dir dataset --max-nnz 128 --steps 2`、`python -m sparserl.train_sft --data sft_data/sft_samples.jsonl --steps 2`、`python -m sparserl.train_minimal --steps 1 --max-nnz 128 --model-path /data02/wangyaoyu/models/Qwen/Qwen3-8B --tokenizer-path /data02/wangyaoyu/models/Qwen/Qwen3-8B` |
| 基础层 | CUDA-C++ |
| 硬件厂商 | NVIDIA |
| 硬件架构 | — |
| 评测 | 编译与执行反馈构成正确性与耗时分层奖励 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 9 |
| 最近推送 | 2026-01-27 |

> 把预训练代码 LLM 当作随机策略：输入稀疏矩阵的行/列索引，用正弦嵌入编码动态稀疏模式，模型输出稀疏算子（SpMV、SpMM）的 CUDA kernel。训练链为预训练扩域 → SFT 学映射 → PPO 优化，RL 阶段用编译器与执行器反馈构造含编译、正确性、执行时间的层次奖励。README 自述只提供 SFT 与 PPO 的最小可跑流水线，数据以 .mtx 或 JSONL 两种形式喂入。

### [weich97/NPUKernelBench](https://github.com/weich97/NPUKernelBench)

面向昇腾 NPU 的 AscendC 生成、领域模型与评测一体化框架。

| 项 | 内容 |
| --- | --- |
| 角色 | 评测基准 |
| 架构模式 | 评测三段式: prompt 生成 → CANN 编译 → 数值比对（可选性能） |
| 入口 | `python run_multi_test.py -chat -task_name Sqrt SwiGlu`、`python run_multi_test.py -chat -task_name Sqrt -stages code_gen`、`python run_multi_test.py -chat -task_name Sqrt -stages compile precision`、`python run_multi_test.py -task_name Sqrt -stages compile precision`、`source set_framework_env.sh`、`nohup bash start_vllm_server.sh` |
| 基础层 | AscendC、torch |
| 硬件厂商 | Ascend |
| 硬件架构 | — |
| 评测 | task 自带 PyTorch 参考与用例，分阶段跑生成/编译/精度，默认容差 1e-3 |
| 验证机制 | compile、correctness、runtime |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 14 |
| 最近推送 | 2026-06-06 |

> 任务以 level/Category/OperatorName 三级目录组织，每个任务自带四件套：question/（生成模板与输入）、answer/（官方参考实现）、validation/（PyTorch 参考、输入生成、测试用例）、api_desc.md（算子语义与约束）。执行侧由 run_multi_test.py 用 -stages 把 code_gen、compile、precision 拆成可单独重跑的阶段，生成样本按 runs/msopgen/lvl1/Math/Sqrt/fixed_case_0/sampleN/ 落盘便于溯源。同一脚本既可走 -chat 的 LLM 生成路径，也可评测人工实现的代码。V2.0 还附带用 CoT 领域知识注入训练的模型，可生成 50+ 可用 AscendC kernel。

### [flagos-ai/awesome-LLM-driven-kernel-generation](https://github.com/flagos-ai/awesome-LLM-driven-kernel-generation)

Review automated kernel generation in the era of LLMs

| 项 | 内容 |
| --- | --- |
| 角色 | 综述清单 |
| 架构模式 | 纯文档分类清单: 按 taxonomy 分层索引条目 |
| 入口 | — |
| 基础层 | —（综述清单，不构建于底座） |
| 硬件厂商 | — |
| 硬件架构 | — |
| 评测 | 无 |
| 验证机制 | — |
| Agent 循环 | 无 |
| 许可 | Apache-2.0 |
| 星标 | 325 |
| 最近推送 | 2026-10-12 |

> 仓库不含代码，是综述（arXiv 2601.15727）配套的 awesome 列表。作者把领域工作划为四大流：LLM4Kernel（分 SFT 与 RL 两种后训练）、Agent4Kernel（再按学习机制、外部记忆管理、硬件 profiling 集成、多智能体编排四个维度）、Datasets 与 Benchmarks。条目统一以 [日期] 标题加论文/代码/数据集链接呈现，并附 GitHub star 徽章；数据集部分又细分结构化数据集与源码仓库（算子库、框架集成、DSL）两类。

### [qhy991/Awesome-LLM-Kernel-Agent](https://github.com/qhy991/Awesome-LLM-Kernel-Agent)

A repository with academic works about Kernel generation with LLM Agent

| 项 | 内容 |
| --- | --- |
| 角色 | 综述清单 |
| 架构模式 | YAML 数据源 + Makefile 渲染 Mermaid 分类图/时间线 + 标记区块自动回写 README |
| 入口 | `cd llm_kernel_agent_landscape && make all (校验+渲染+同步 README)`、`cd llm_kernel_agent_landscape && make svg pptx drawio`、`编辑 data/entries.yaml 新增论文或系统`、`编辑 data/timeline.yaml / data/timeline_dates.yaml 调整时间线` |
| 基础层 | —（综述清单，不构建于底座） |
| 硬件厂商 | — |
| 硬件架构 | — |
| 评测 | 无 |
| 验证机制 | none |
| Agent 循环 | 无 |
| 许可 | 未声明 |
| 星标 | 24 |
| 最近推送 | 2026-10-30 |

> 真正的仓库产物是 README 本身：127+ 篇 LLM kernel 生成工作被组织成 Mermaid 时间线与五分类流程图（模型/后训练、Agent 工作流、数据资产、评测、集成系统），正文还用表格给出标题、会议、日期、代码链接、作者、机构与主题标签。图形生成被工程化为一条流水线：条目与时间线存在 YAML 中，由 llm_kernel_agent_landscape/ 下的 make 目标做校验、渲染并回写 README 中带 BEGIN/END 标记的区块，从而避免手改 Mermaid 出错。维护指南直接给出按目标该改哪个 YAML 文件的对照表，并支持额外导出 SVG/PPTX/drawio 用于汇报。
