# 抽象知识：工程实践与项目架构搭建

这份文档从 61 个开源项目里提炼**可复用的工程知识**：一个 kernel 优化项目通常由哪些层组成、常见的架构形态有哪几种、别人已经踩过并且解决掉的工程问题有哪些、以及如果要自己搭一个项目应该怎么起步。

> **证据边界**：结论来自仓库 README、顶层目录结构与 GitHub API 元数据。**没有审计源码实现，没有运行过任何项目，没有复现任何论文数字**。本文描述的是「公开材料显示项目这样组织」，不是「项目实现正确」。

## 1. kernel 项目的参考分层

把这批项目叠在一起看，几乎都能拆进同一套分层里。分层的价值不在于分类学，而在于**定位缺口**：要判断一个项目离「能交付」还差多远，只需要问它缺哪几层。

| 层 | 职责 | 在仓库里长什么样 |
| --- | --- | --- |
| **L1 任务与规格层** | 定义「要优化哪个算子」：参考实现、输入 shape、dtype、语义边界、正确性判据。 | 判据：仓库里能找到一个可枚举的任务集合，并且任务定义不依赖运行时。 |
| **L2 生成层** | 产出候选 kernel：专用模型、推理时搜索、Agent 工具循环、或它们的组合。 | 判据：仓库里存在一个能接受任务并返回 kernel 源码的接口。 |
| **L3 表达层** | 决定候选写成什么语言/DSL：Triton、CUDA C++、TileLang、HIP、AscendC、MUSA。 | 判据：仓库的构建产物是编译器、Python 扩展或算子包，而非纯脚本。 |
| **L4 编译与执行层** | 把源码编译成设备代码并运行：编译器驱动、运行时、内存管理、调度。 | 判据：仓库能独立完成「编译 → 执行」而不需要上层框架。 |
| **L5 验证层** | 判断候选是否正确、是否更快：编译检查、参考输出比对、运行时计时、profiling。 | 判据：仓库里有独立的验证/打分模块，且能对任意候选单独调用。 |
| **L6 评测与度量层** | 组织任务、跑多次、汇总指标、给出基线与阈值。 | 判据：仓库能独立产出一份评测报告，而不只是单次运行结果。 |
| **L7 训练层** | 把数据与反馈变成可分发的模型：继续预训练、SFT、RL、偏好数据。 | 判据：仓库产出权重或数据集，且带训练脚本与评测脚本。 |

缺 L5 的项目只能回答「能不能编译」，缺 L6 的项目只能回答「这一次跑得怎么样」，缺 L1 的项目则无法回答「在什么任务上」。三样都缺的项目基本只有演示价值。

### 各层的项目分布

- **执行运行时底座**（对应 L3 / L4，3 个）：`ROCm/aiter`、`flagos-ai/FlagGems`、`tile-ai/BitBLAS`
- **编译器底座**（对应 L3 / L4，2 个）：`hgl71964/cuasmrl`、`mindspore-ai/akg`
- **DSL / kernel 表达层**（对应 L3，4 个）：`HazyResearch/ThunderKittens`、`NVIDIA/cutlass`、`tile-ai/tilelang`、`triton-lang/triton`
- **训练流水线**（对应 L7，9 个）：`AMD-AGI/AMDKernelVault`、`ByteDance-Seed/cudaLLM`、`QiMeng-IPRC/QiMeng-Kernel`、`QiMeng-IPRC/QiMeng-MuPa`、`RLsys-Foundation/TritonForge`、`ScalingIntelligence/kernelbench-tinker`、`Wangyaoyuu/SparseRL`、`hkust-nlp/KernelGYM`、`ornith-ai/CUDA-L1`
- **Agent 搜索循环**（对应 L2，15 个）：`0satan0/KernelMem`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`Anjiang-Wei/Astra`、`Dogacel/auto-gpu-kernel`、`OptimAI-Lab/CudaForge`、`RightNow-AI/autokernel`、`StigLidu/AdaExplore`、`caoshiyi/K-Search`、`meta-pytorch/KernelAgent`、`taratt/cutegen`、`ucb-bar/autocomp`、`zhang677/AccelOpt`、`zhang677/PCL-lite`、`zhang677/PTXBench`
- **评测基准**（对应 L1 / L6，21 个）：`AMD-AGI/AgentKernelArena`、`AMDResearch/NPUEval`、`BonnieW05/KernelBenchX`、`CUDA-Bench/CUDABench`、`ISO-Bench/ISO-Bench`、`NVIDIA/SOL-ExecBench`、`NVIDIA/compute-eval`、`SakanaAI/robust-kbench`、`ScalingIntelligence/KernelBench`、`Snowflake-AI-Research/fastkernels`、`aisa-group/InferenceBench`、`alibaba/atrex-bench`、`facebookresearch/kernel_bench_verified`、`flagos-ai/KernelGenBench`、`flashinfer-ai/flashinfer-bench`、`meta-pytorch/BackendBench`、`meta-pytorch/tritonbench`、`parallelcodefoundry/ParEval`、`thunlp/TritonBench`、`weich97/NPUKernelBench`、`wzzll123/MultiKernelBench`
- **数据集 / 模型**（对应 L7，5 个）：`AI9Stars/AutoTriton`、`BytedTsinghua-SIA/CUDA-Agent`、`CSJianYang/Industrial-Coder`、`ornith-ai/CUDA-L2`、`tensormux/kernel-skills`
- **综述清单**（对应 —，2 个）：`flagos-ai/awesome-LLM-driven-kernel-generation`、`qhy991/Awesome-LLM-Kernel-Agent`

## 2. 七种架构形态

把 61 个项目按「有没有评测闭环、有没有 Agent 闭环、是不是底座、是不是训练流水线」分类，得到七种形态。形态决定了一个项目的**最小可行交付物**是什么。

| 形态 | 项目数 | 项目 |
| --- | ---: | --- |
| 形态 A：纯评测基准 | 18 | `BonnieW05/KernelBenchX`、`CUDA-Bench/CUDABench`、`ISO-Bench/ISO-Bench`、`NVIDIA/SOL-ExecBench`、`SakanaAI/robust-kbench`、`ScalingIntelligence/KernelBench`、`Snowflake-AI-Research/fastkernels`、`alibaba/atrex-bench`、`facebookresearch/kernel_bench_verified`、`flagos-ai/KernelGenBench`、`flashinfer-ai/flashinfer-bench`、`meta-pytorch/BackendBench`、`meta-pytorch/tritonbench`、`ornith-ai/CUDA-L2`、`parallelcodefoundry/ParEval`、`thunlp/TritonBench`、`weich97/NPUKernelBench`、`wzzll123/MultiKernelBench` |
| 形态 B：评测 + Agent 平台 | 5 | `AMD-AGI/AgentKernelArena`、`AMDResearch/NPUEval`、`BytedTsinghua-SIA/CUDA-Agent`、`NVIDIA/compute-eval`、`aisa-group/InferenceBench` |
| 形态 C：Agent 生成闭环 | 15 | `0satan0/KernelMem`、`AMD-AGI/Apex`、`AMD-AGI/GEAK`、`Anjiang-Wei/Astra`、`Dogacel/auto-gpu-kernel`、`OptimAI-Lab/CudaForge`、`RightNow-AI/autokernel`、`StigLidu/AdaExplore`、`caoshiyi/K-Search`、`meta-pytorch/KernelAgent`、`taratt/cutegen`、`ucb-bar/autocomp`、`zhang677/AccelOpt`、`zhang677/PCL-lite`、`zhang677/PTXBench` |
| 形态 D：训练流水线 | 9 | `AMD-AGI/AMDKernelVault`、`ByteDance-Seed/cudaLLM`、`QiMeng-IPRC/QiMeng-Kernel`、`QiMeng-IPRC/QiMeng-MuPa`、`RLsys-Foundation/TritonForge`、`ScalingIntelligence/kernelbench-tinker`、`Wangyaoyuu/SparseRL`、`hkust-nlp/KernelGYM`、`ornith-ai/CUDA-L1` |
| 形态 E：执行底座 | 9 | `HazyResearch/ThunderKittens`、`NVIDIA/cutlass`、`ROCm/aiter`、`flagos-ai/FlagGems`、`hgl71964/cuasmrl`、`mindspore-ai/akg`、`tile-ai/BitBLAS`、`tile-ai/tilelang`、`triton-lang/triton` |
| 形态 F：综述清单 | 2 | `flagos-ai/awesome-LLM-driven-kernel-generation`、`qhy991/Awesome-LLM-Kernel-Agent` |
| 形态 G：其他 / 单一功能工具 | 3 | `AI9Stars/AutoTriton`、`CSJianYang/Industrial-Coder`、`tensormux/kernel-skills` |

### 形态 A：纯评测基准

**是什么**：只做「给定任务 → 产出结果 → 打分」，不负责生成 kernel 本身。

**骨架**：任务集（目录或 JSON）+ 候选提交入口 + 参考实现 + 判定器 + 基线与指标。

**复用要点**：把任务集与判定器彻底解耦成两个目录，任务集可以替换而判定逻辑不动；基线版本必须写进结果文件，否则跨版本不可比。

**各项目的具体做法**：

- `BonnieW05/KernelBenchX`——评测被切成 call（能否编译运行）→ exe（数值正确性）→ perf（性能）三个顺序阶段，每阶段单独落 JSONL 到 intermediate/ 目录，这样失败原因能定位到具体阶段。提交物形态设计得比较灵活：一个 JSONL 文件（每行含 predict 与 file，若无 file 则需带含 Functional Description 与 Wrapper Entry Information 的 instruction）、单个 .py 文件（basename 必须与 data/kernelbenchx/ 中的任务同名，且若文件内含 146 个 # 组成的分隔线，只取线以上内容作为提交）、或一个目录（递归收集 .py 与 .jsonl）。为了保证提交可执行，规定了「顶层可调用函数必须叫 kernel_function 或与任务 stem 同名」的执行契约。性能评测不与固定参考比，而是按机器隔离存放 GPU 匹配的 golden timing（metrics/golden_results/&lt;machine&gt;/），解析优先级为环境变量 KERNELBENCHX_GOLDEN_RESULTS_DIR → KERNELBENCHX_GOLDEN_MACHINE → 默认 5090，缺失的机器可用 run_missing_benchmarks.py 重新生成。输出统一为 metrics.json（逐任务）与 summary.json（通过率与加速比汇总）。相比上游 TritonBench，它强调更严格的正确性校验、扩展的任务覆盖（量化、多精度）与正确性/效率统一的评测流水线。
- `CUDA-Bench/CUDABench`——任务集被压在一个 JSONL 文件里，每条记录自成一体：id 与 task_name 标识任务，inputs/outputs 描述张量形状与数据类型，三档难度 prompt 分别对应引导式实现（给出算法描述与显式 CUDA 实现指引）、算法式规范（只给算法描述、不给硬件提示）与概念检索式（只给任务名），评测三件套 bench.cu（参考 CUDA C++ 实现）、gen.py（生成随机二进制输入与参考输出）和 compare.py（校验生成 kernel）也内嵌在同一条记录里，使得任务定义、参考实现与打分逻辑完全自包含。生成侧由 Generate/main.py 负责，按 --api_option 选择 API provider、--model_name 选模型、--samples 指定采样次数，默认参数集中在 Generate/config.py 中，结果按 Results/&lt;api&gt;/&lt;model&gt;_&lt;level&gt;_pass&lt;k&gt;.jsonl 命名，把 provider、模型、难度与采样序号编码进文件名，便于多模型多难度横向对比。评测侧 Evaluate/manager.py 以 full 子命令接收结果文件路径，负责编译、运行与用 Nsight Compute 剖析，整体是「生成只落 JSONL、评测单独吃同一文件」的解耦结构。仓库还提供 figs/overview.png 说明整体流程图。
- `ISO-Bench/ISO-Bench`——仓库把造题与跑 agent 明确分开：commit_to_dataset.py 从真实仓库（vLLM/SGLang）的性能提交出发，经 PerfCommitAnalyzer 与 LLM 生成性能测试，产出 jsonl 数据集；ISO-Bench/ 子目录提供 plan→prepare→report 的 agent 运行 CLI，可在 TRAE、Claude Code、Codex、OpenHands 之间切换。每个任务在同一个 Docker 环境下做三方对比：基线父提交、人类专家提交、agent 补丁，并跑 vLLM serving/throughput 基准。除此之外还有 LLM 软指标分析（任务理解、技术重叠、提速可能性）与基于 lm-eval 的正确性校验作为旁路评估。
- `NVIDIA/SOL-ExecBench`——以 problem 目录为评测单元：definition.json 给出函数签名、张量形状、dtype 与参考实现，workload.jsonl 逐行给出具体输入与容差阈值，solution.json 单独提交源码与构建信息。评测在 Docker 容器内由 sol-execbench CLI 完成，先排查多种形式的 reward hacking，再与参考实现做数值正确性比对，最后在可复现条件下计时。排名用 SOL-Score：以 B200 的理论 roofline（由 SOLAR 解析求得）为基准给自定义 kernel 打分，而不是只报相对加速比；同一框架覆盖 PyTorch、Triton、CUTLASS、cuDNN、CuTe DSL、cuTile、CUDA C++ 多种 DSL。
- `SakanaAI/robust-kbench`——每个任务是一个目录（tasks/mnist_linear、tasks/layernorm 等），覆盖基础算子、卷积、Transformer 块与原版 KernelBench 题，并区分 forward 与 backward。run_filter.py 先做六项鲁棒性检查：输出范围不被压到 [-0.01,0.01]、标准差大于 0.01、跨轴变化大于 0.01、初始化设置影响、输入配置影响，以及 LLM 判定的低效代码，先把可被钻空子的题目筛掉。评测侧拆成 compile/test/eval/profile 四个独立函数，由 ParallelKernelExecutor 并行编排，并提供 KernelBench、torch benchmark 与 Triton do_bench 三套计时互相印证，避免单一计时口径被针对性针对。
- `ScalingIntelligence/KernelBench`——README 明确本仓库只提供 KernelBench 核心功能与易用评测脚本，不提供复杂 agentic scaffold，建议 clone 后自行改造或作为 git submodule 使用。数据集分 Level1-4（单 kernel、简单融合、整模型、HF 模型），生成与评测拆成 generate_samples 与 eval_from_generations 两个脚本，runs/ 与 results/ 分别承载运行结果和跨代际 NVIDIA GPU 基线。评测核心在 src/eval.py，指标 fast_p 表示既正确又超过阈值 p 的加速比任务占比。
- `Snowflake-AI-Research/fastkernels`——算子按 L1 单 kernel、L2 融合复合、L3 层/块、L4 端到端管线四级抽象组织，覆盖 dense/MoE LLM、线性注意力、扩散视频音频、多模态、检测、3D/机器人/科学、推荐与 world model。每个架构同时提供参考实现（tasks/baseline/）和候选替换槽位（tasks/candidate/），runner 把候选换入后先校验正确性再测加速比。README 强调在模型优化与 agent kernel 评测中开发的优化 kernel，会在作为服务框架使用时被自动换入部署，使评测产物与部署产物合一。
- `alibaba/atrex-bench`——每个算子是一个自描述目录（reference.py、input.py、shapes.json、metadata.json、roofline.json），评测器分编译、数值正确性、性能三段，性能按缓存的 roofline SOL 效率打分。生成与评测强制分两次独立 clone：生成前用 cleanup_for_generation.py 就地删掉 metadata/roofline/评测器与 .git 历史，避免 agent 读到答案，评测用完整的新 clone。评测支持 torch.compile 基线、A-B-B-A 反向平衡对照、按 shape 分片并用 Ray Data 分发到多 GPU worker，worker 失败只重试受影响分片且已成功分片被提交保留。
- `facebookresearch/kernel_bench_verified`——不重造题库，而是在 KernelBench 之上加三件事：把 PyTorch 基线切到 TF32 以对齐真实部署的 Tensor Core 路径、为每题生成隐藏的四分布测试文件、对 4 个易 reward hack 的题在 prompt 中自动剥离测试输入。评测用 use_hidden_tests 与 use_hidden_eval 两个开关把标准结果和隐藏门控结果分流到不同文件，最后由 generate_leaderboard.py 产出以速度-显存权衡为坐标的交互式 HTML 排行榜。
- `flagos-ai/KernelGenBench`——KernelGenBench 是 FlagOS 体系内的基准框架：210 个算子来自 ATen（110）、vLLM（50）、cuBLAS（50）三个来源，评测分 LLM 赛道（Pass@K）与 Agent 赛道（迭代生成）两条。对外统一用 generate_kernel_and_verify.py 入口，--api-format 只描述协议而不限定 provider，任何 OpenAI/Anthropic 兼容端点都能直接接入。工程上把平台差异收敛到 requirements/ 下的分平台依赖文件，硬件侧覆盖 NVIDIA、昇腾 NPU、MUSA、海光 DCU、沐曦与 MetaX。
- `flashinfer-ai/flashinfer-bench`——README 极简：flashinfer-bench 以 pip 包发布，提供 Python 模块（import flashinfer_bench as fib）与 CLI（flashinfer-bench run）两条入口。核心资产是官方 FlashInfer-Trace 数据集，包含真实 AI 系统部署环境下的 kernel 与 workload，遵循独立的 FlashInfer Trace Schema。数据集托管在 HuggingFace，用 GIT_LFS_SKIP_SMUDGE=1 只克隆 LFS 指针文件，大张量在跑基准时按需下载，避免一次性拉取巨量数据。整体定位是构建『AI 改进 AI 系统』的正循环。
- `meta-pytorch/BackendBench`——核心机制不是独立 runner，而是目录约定：开发者按规范在算子目录下放实现，运行时动态覆盖 PyTorch 核心算子，从而拼出一个可 pip 安装、对现有模型无需改代码的 PyTorch 后端。评测分三套：smoke 快速自检、opinfo 复用 PyTorch OpInfo 与 FACTO 做边界正确性、torchbench 用 Hugging Face 热门模型的真实张量形状测性能。设计上刻意以 PyTorch 自身标准为准，目的是让通过测试的 kernel 具备向上游 PyTorch 合并的资格。
- `meta-pytorch/tritonbench`——它本质上是一组带样例输入的 PyTorch 自定义算子，用来看 Triton 实现本身以及它与 PyTorch 集成后的性能，而不是一个通用 harness。结构上最大的特点是 kernel 来源不自研，而是把 generative-recommenders、Liger-Kernel、tilelang、flash-attention、FBGEMM、ThunderKittens、AITer 等项目以 git submodule 形式引入，其中 CUDA 与 HIP 实现各取所需。同时支持两种用法：命令行按算子名跑，或 pip install -e . 后作为库按名字加载算子基准并注入自定义参数。
- `ornith-ai/CUDA-L2`——README 呈现的是一个产物型仓库：系统本体是 LLM 加 RL 自动优化半精度 GEMM 的 CUDA kernel，发布形态是按硬件与累加器精度分批放出的 kernel 集合（已放出 A100、RTX 3090、H100 上 1000 组配置，区分 16 位与 32 位累加器）。评测只有一条路径 eval_one_file.sh，用 mnk、累加器精度、设备类型、warmup/benchmark 秒数、gpu id 与 offline/server 模式等参数驱动，server 模式还需指定目标 QPS。工程上把 CUTLASS 锁死到 v4.2.1 并要求显式设置 CUTLASS_DIR 与 TORCH_CUDA_ARCH_LIST，因为版本或路径不对会静默失败。跨机型复用被明确否定：A100 上训练的 kernel 只保证在 A100 上有加速。
- `parallelcodefoundry/ParEval`——仓库按流程而非按功能划分目录，prompts 放提示词，generate 产出 LLM 代码，drivers 负责编译运行与评测，analysis 做结果后处理与指标计算，tpl 用 submodule 固定第三方依赖。通用工作流是三步命令串联：generate.py 生成 → run-all.py 评测 → metrics.py 计算指标。C++ driver 用 makefile 构建，检测不到 CUDA、HIP 或 Kokkos 库时会自动跳过对应目标，从而让没有 GPU 的机器也能评 CPU/OpenMP 部分。环境依赖被显式列出：Python 3.7+、支持 C++17 与 OpenMP 的编译器、Make、CMake 与 MPI。
- `thunlp/TritonBench`——TritonBench-G 面向模型从指令生成算子，需先做代码相似度评估再评执行；TritonBench-T 面向给定算子的直接改写，不评相似度，只评调用正确性、执行正确性与加速比。打分被拆成三个可独立执行的脚本：0_call_acc.py 做静态调用匹配，1_exe_acc.py 做执行正确率，2_efficiency.py 汇总性能与加速比。性能链路是 write_file.py 生成输入文件、multiprocess_gpu_run.py 多进程多 GPU 跑、再由 2_efficiency.py 汇总；README 明确要求准确率与效率评测必须顺序执行。G 通道额外用 CodeBLEU 衡量代码相似度，把像不像与对不对分开评。数据侧提供 Alpaca 格式的简版/复杂指令、可执行任务目录与统计，以及由 4024 条 BERT 去重爬取语料与 4133 条 Jiuci 合成语料合并的 8k RAG 语料。
- `weich97/NPUKernelBench`——任务以 level/Category/OperatorName 三级目录组织，每个任务自带四件套：question/（生成模板与输入）、answer/（官方参考实现）、validation/（PyTorch 参考、输入生成、测试用例）、api_desc.md（算子语义与约束）。执行侧由 run_multi_test.py 用 -stages 把 code_gen、compile、precision 拆成可单独重跑的阶段，生成样本按 runs/msopgen/lvl1/Math/Sqrt/fixed_case_0/sampleN/ 落盘便于溯源。同一脚本既可走 -chat 的 LLM 生成路径，也可评测人工实现的代码。V2.0 还附带用 CoT 领域知识注入训练的模型，可生成 50+ 可用 AscendC kernel。
- `wzzll123/MultiKernelBench`——生成与评测被拆成两条独立脚本：generate_and_write.py 只负责按 language/strategy/model 生成代码并写入 output 目录，evaluation.py 再对同一产物路径做评测，便于反复跑不同策略而不重生成。语言差异通过 backends/ 下的后端类插件化解，接口固定为 get_device/get_hardware_name/compile/correctness_execution/time_execution/cleanup；prompt 差异通过 prompt_generators/ 下的策略类插件化解，两侧都用装饰器注册。reference/ 按 activation/attention/convolution/matmul 等 category 组织 PyTorch 参考实现，作为所有语言后端共享的正确性基准。

### 形态 B：评测 + Agent 平台

**是什么**：在基准之上叠加可插拔的 Agent 与执行环境，用来横向比较不同 Agent 策略。

**骨架**：基准任务集 + Agent 适配层 + 隔离执行环境 + 统一打分器 + 多次运行的统计。

**复用要点**：Agent 与任务集通过配置解耦，同一任务集能跑不同 Agent；执行环境容器化并锁定驱动版本，否则 Agent 之间的差异会被环境差异吃掉。

**各项目的具体做法**：

- `AMD-AGI/AgentKernelArena`——核心设计是把「agent 改 kernel」与「评测 kernel」彻底分开：每个任务目录自带一份 config.yaml（schema v2）声明实现、基线、候选与评测动作，平台只负责建工作区、拼提示、跑 agent，然后由 src/evaluator.py、src/performance.py 独立编译、校验、计时，最后由 src/score.py 算出分数并写入 task_result.yaml。agent 通过注册表接入（@register_agent 装饰器 + AgentType 枚举），Cursor Agent、Claude Code、Codex、DeepSeek Harness、KernelForge、GEAK 都实现同一接口，因此同一任务集可以在不同 agent、不同模型、不同 prompt 下反复跑；平台自身不含 RL trainer、replay buffer 或策略更新回路，奖励信号以 task_result.yaml/CSV/JSON 报告形式外供。实验方法论是「只改被测能力」：用相同配置跑两次并以 run-suffix 区分 baseline/treatment，再用 src/tools/compare_runs.py 与可视化看板对照，对随机性 agent 要求重复配对运行并结合方差解读。工程上用每 GPU 一个隔离 Docker worker 从共享 .parallel/ 队列原子领取任务，任务级工作区带时间戳并保留日志、修改后源码与结构化结果，从而支持断点续跑（框架完成且源码证据仍有效的任务不重跑）。
- `AMDResearch/NPUEval`——整体是围绕一个 NPU 评测数据集搭建的最小可复现流水线。install.sh 会拉起 XRT docker 镜像，构建 XRT 与 XDNA debian 包并安装到宿主机，同时准备带齐 NPU 应用编译工具链的 NPUEval 容器。评测被刻意拆成两个可独立运行的脚本：run_completions.py 负责把数据集里的所有 prompt 喂给 AIECoder agent 生成解法（需要 OPENAI_API_KEY，会请求 gpt-4.1 与 gpt-4o-mini），run_functional_tests.py 只负责评估已生成的解法，因此评测端只需要 NPU、不需要 LLM 访问权限，这对无外网或无 key 的环境很友好。所有脚本都可以通过 docker_run_script.sh 作为独立容器会话执行，同时提供 JupyterLab（8888 端口）供交互式探索数据集。底层依赖是 MLIR-AIE / LLVM-AIE 与 AI Engine API，NPU 侧通过实验性未签名内核模块工作。
- `BytedTsinghua-SIA/CUDA-Agent`——仓库给出三件东西：RL 训练出的 CUDA kernel 生成模型、6K 规模的训练数据集 CUDA-Agent-Ops-6K，以及一个标准化 agent 工作区 agent_workdir。工作区把「实现 CUDA kernel → 编译 → 校验正确性 → profile 性能 → 迭代」这条闭环固化成模板：model.py 放原始 PyTorch 基线、model_new.py 放用自定义 CUDA 扩展的优化版本、kernels/ 放自定义 CUDA/C++ kernel 及其绑定，binding.cpp 与 binding_registry.h 提供共享的 Python 绑定注册基础设施以免每个 kernel 重复样板，utils/compile.py 与 compile.sh 负责构建扩展，verification.py 做正确性校验，profiling.py 把性能与基线及 torch.compile 双基线对比，SKILL.md 以技能文件形式向 agent 下发工作流约束与优化规则。数据集的构造是一条明确的合成流水线：从 torch 与 transformers 收集参考算子，用 LLM 把多个算子组合成融合任务，再用规则过滤保留可执行、确定性且非平凡的样本；过滤标准要求样本在 eager 与 torch.compile 两种模式下都能正确执行，剔除随机算子与退化输出，控制运行时长，并移除与 KernelBench 测试高度相似的样本以降低污染风险。
- `NVIDIA/compute-eval`——题目以目录为单位组织（problem-spec.yaml 加 context/solution/test），生成期模型只见 prompt、context_files 与 build_command，评测期才注入隐藏测试与参考答案，靠目录级可见性分离防止对测试过拟合。题目打包成版本化 datapack（metadata.json 带每题 MD5 + problems.jsonl）发布到 HuggingFace，承诺旧 release 的题目集合与语义永久不变、只修缺陷不加题。执行侧用 Podman 容器隔离未信任的生成代码，功能正确性由 test_command 的退出码决定，性能由可选 CUPTI/NCU 计时；此外用 harbor 子命令让编码 agent 在容器内自行读文件、编译、迭代，并可用 optimize 模式以基线解为起点只优化性能。
- `aisa-group/InferenceBench`——每个 agent 在固定时间预算内为一个基座模型编写 server launcher，随后在全新容器中运行它，在四种负载场景下测服务速度，并与 PyTorch 参考实现比对回答质量。生成与评测用 Apptainer 容器加 HTCondor 批作业隔离，容器内预置 torch/vllm/sglang/tgi 后端镜像与锁定的 Python 依赖。另设 Claude 裁判审阅 launcher 与服务日志以识别被禁的取巧手段，并提供同等时间预算的 vLLM/SGLang 随机搜索基线做公平对照。

### 形态 C：Agent 生成闭环

**是什么**：自己带生成循环：模型提出候选 → 编译/测试 → 读取反馈 → 迭代。

**骨架**：提示与模板 + 生成器 + 工具接口（编译、跑测试、profile）+ 循环控制器 + 反馈解析。

**复用要点**：把「工具」抽象成统一接口（输入 kernel 源码，输出结构化反馈），循环控制器与具体工具解耦，这样换编译器或换硬件只改工具实现。

**各项目的具体做法**：

- `0satan0/KernelMem`——仓库是一个以脚本为中心的实验型系统：main_memory_latest.py 解析 CLI 后，串起「读 PyTorch 任务 → 让 LLM 生成 CUDA kernel → 编译运行 → 剖析 → 修复/再优化」的多轮循环，所有产物按任务落盘到 code/、evaluation/、profile/、figures/ 目录。记忆机制被显式拆成两层：短期记忆是当前轮的 kernel 代码片段、错误日志与剖析结果，经 _build_history_block 组装成 Markdown 直接嵌入优化提示；长期记忆是 memorybank/ 下人工沉淀的硬件瓶颈与常见 kernel 结构知识。结构性决策在于把「评判」拆成 prompts/ 下多个 judger_* 模块（优化策略判断、编译超时分析、运行错误分析），由规则化的判官把 profiler 原始指标翻译成可执行的修复建议，再交回 LLM，而不是让 LLM 直接读原始 profile 文本。另有 optimization_tree.json 记录所有 kernel 的父子谱系与提速比，summary.json/summary.csv 汇总跨任务平均加速比与 token 用量，并支持按 summary 过滤掉不可运行任务以增量重跑。
- `AMD-AGI/Apex`——workload_optimizer.py 是唯一 CLI，把整条链路拆成 benchmark → identify → optimize → integrate → benchmark-final → score → report 这些可单步也可一次跑完的子命令，结构上是典型的「剖析驱动选靶 + agent 改写 + 独立评分 + 回注验证」。评分不自己实现，而是委托给外部 Magpie 框架，仓库内只保留 graders/ 下的配置生成、ground truth 注册与缓存隔离（cache_manager）以保证可复现的评测条件。评分公式分为 kernel 级（compiled×20 + correct×100 + 分段 speedup 分，S&lt;1 时给回退惩罚）与模型级（0.7×归一化 kernel 分 + 0.3×端到端吞吐提升比）两层，且只有同时编译并正确才计入加速分。优化产物通过 hot-patch 回注 site-packages：aiter/vllm/sglang 的 Triton .py 可直接替换并由 Triton JIT 自动重编译，aiter 的 .so 用 hipcc 重编译后替换，而系统级共享库与单体 _C.so 明确不支持，需重新编译源码；补丁在基准结束后会被还原。agent 侧不内置 agent 循环，而是通过 agents/backends.py 调 Claude Code / Codex / Cursor CLI，配合两层提示词（系统提示定义角色、MCP 工具清单与反作弊规则；任务提示带 GPU 架构参数、源码位置、剖析数据与知识库洞察）和 5 个 MCP 服务（源码检索、kernel RAG、GPU 信息、融合建议、Magpie 评测）扩展 agent 能力，跨轮经验沉淀在 pipeline/knowledge_base.py，反思在 reflector.py，最终以 export-rl 把轨迹导出为 RL/SFT 数据集，形成训练回流闭环。
- `AMD-AGI/GEAK`——最重要的架构决策是把控制流从模型里挪出来：预算循环、fan-out、验证与停止条件全部写成确定性 JS（kernel_workflow.js / e2e_workflow.js），LLM 只在分析、策略与优化这些需要判断的环节被调用，因此运行可复现。kernel_workflow 采用 Director → TechLead → 算法/内存/计算/host_runtime 专家的分层结构，多轮且预算可控，并要求每个补丁由独立 agent 验证通过后才被接受，避免生成者自评。e2e_workflow 是包在 kernel 层之上的系统层：先 preflight 环境，再对运行中的 server 做 profile，按 Amdahl（pct_gpu_time × achievable_speedup）给热点排序，然后「先拉成本最低的杠杆」——配置/后端扫描 → 头部 GEMM 与 attention bake-off → 可编辑 kernel 里程碑循环；每个被接受的改动以可逆 overlay 方式叠回，并用 warm-server 交错 A/B（0.5% 带宽 + engagement proof + 输出 parity）作为放行门槛。跨轮记忆被显式建模为 insight blackboard 与 hypothesis ledger 两个构件，最佳补丁产物落在 kb_artifacts 作为下次运行的 warm-start 源。GPU 访问通过 flock 脚本串行化，因此可以一个 kernel 一个 agent 并行跑而安全共享同一 GPU。
- `Anjiang-Wei/Astra`——README 非常精简，可确证的事实有限。仓库主体是单一脚本 cuda_kernel_optimizer_multi.py，通过 CLI 传入初始 .cu 文件路径、对比类型标签、基线函数名与生成的 PyBind 导出函数名，函数内部按 --compare-kind（rmsnorm / silu / mergestate / generic 等）分支决定测试生成提示。基线默认取 sgl_kernel 模块中的实现（若为空则自动回退到 sglang.sgl_kernel），说明对比对象取自 SGLang 的 kernel 实现。生成代码被期望导出一个与基线同名的顶层函数，供后续正确性与性能对比。迭代次数由 --max-iterations 控制（默认 5）。每次运行的结果写入带时间戳的 cuda_optimization_runs/ 目录以保留多次运行记录。README 未展开 agent 组成、角色划分与具体打分方式，因此这些细节不做推断。
- `Dogacel/auto-gpu-kernel`——FlashInfer 赛道与任意 Git 仓库共用同一个 BenchmarkAdapter 抽象：FlashInferAdapter 打包 kernel 源码走本地或 Modal 后端执行，GeneratedTaskAdapter 运行 setup agent 生成的 validate.py 与 benchmark.py。任务描述外置为 task.toml（objective/measure/validate/hints 及硬件约束），首轮用一次 setup turn 让 agent 现场生成验证与测量适配器，之后由 kbench 负责 quick/full 基线、归一化测量与配对 A/B。作者明确的设计取舍是只给 agent 关键原则而不给长指令，以免 harness 被逐渐 hack。
- `OptimAI-Lab/CudaForge`——README 极简，只能确认这是一个免训练的多智能体工作流，模仿人类专家的迭代节奏：先写初始 kernel、测正确性、分析硬件反馈、再迭代改进。所有执行都收敛到一个 main.py 脚本，参数指定 KernelBench 任务目录、GPU 型号、服务与模型类型、轮次数以及 subproc_id 与 device 以支持并行。关键的外部依赖约束是 nvcc 与 Nsight Compute (ncu) 必须与 CUDA Toolkit 版本一致，且 ncu 需要 sudo 权限读取 GPU 性能计数器，README 给出了免密 sudo 的配置方法。仓库内部结构在 README 中完全没有交代。
- `RightNow-AI/autokernel`——把 agent 的作用域限制为只改 kernel.py 一个文件，跑固定 bench.py 后按结果保留或回滚，保证 diff 可读、回滚干净，同时评测脚本本身不被 agent 触碰。流程按 profile（torch.profiler 按 GPU 时间排序并判定 compute/memory bound）→ extract（把瓶颈抽成独立 Triton 或 CUDA C++ kernel）→ orchestrate（用 Amdahl 定律决定下一个优化对象）→ verify（把优化 kernel 塞回模型做端到端正确性与总加速比）串起来。设计上正确性优先于性能：先与 PyTorch 对拍再计时，错的立即回滚；实验结果以 results.tsv 纯文本追加，program.md 里写足 6 层优化手册与崩溃处理，让 agent 能连续跑十小时不卡住。
- `StigLidu/AdaExplore`——仓库按 Adapt/Explore 两阶段切分目录：synthesis/ 生成多样化 kernel 任务，agent/ 在其上运行并把重复的编译/运行失败蒸馏成跨任务规则写入技能记忆文件，skill_memory/ 负责离线抽取或更新该记忆，记忆再被注入后续 prompt。Explore 阶段用 MCTS 把候选组织成搜索树，交替进行局部精修与结构性重写以保持多样性。评测走 online_judge/app_with_queue.py 提供的 API 服务，按 GPU 设并发上限并排队，请求路由到最空闲 GPU，执行放在隔离子进程以防崩溃或非法访存拖垮主服务。
- `caoshiyi/K-Search`——核心在 k_search/kernel_generators/：除基础 LLM 生成器外还提供 world-model-aware 生成器，配套 world_model.py（结构化 JSON schema）、world_model_manager.py（init/refine/select 生命周期）与专用 prompt 模板，世界模型编码瓶颈假设、设计备选与优化策略来指导下一轮动作。任务侧由 task_base.py 定义统一协议，各 benchmark 以适配器接入（FlashInfer-Bench、GPUMode TriMul、KernelBench、MLX）。解法、评测报告与世界模型快照全部落盘，可从已有解法或世界模型状态续跑，并内置 OpenEvolve/ShinkaEvolve 基线做同目标对照。
- `meta-pytorch/KernelAgent`——先用 AutoRouter 对问题做 AST 静态分析（注意力块、转置卷积、控制流、长算子链）决定走轻量直连路径还是完整 Fuser 流水线，路由决策缓存在 .fuse/router_cache.json 并可回退。Fuser 侧由 LLM 输出 JSON 子图描述（算子、shape、dtype、参数），按 shape 签名去重复用 kernel，Dispatcher 并行拉起多个 TritonKernelAgent 进程，Composer 把已验证 kernel 拼回单个 Triton 程序并跑自测。生成侧 worker 池迭代让 LLM 改进代码，在沙箱子进程中执行单测并禁止 PyTorch fallback，只有打印 PASS 且退出码 0 才算成功。优化侧以 NCU 28 项指标 + roofline 判定驱动 LLM 诊断与改写，对 PyTorch 参考做数值校验，再用 CUDA event 计时跟踪 best-so-far 并在性能退化时回滚。所有阶段产物落盘到 .fuse/&lt;run_id&gt; 与 .optimize/&lt;run_id&gt; 以支持复现。
- `taratt/cutegen`——核心抽象是多后端共用一条流水线：CUDA、CuTe、PTX、Triton 四个后端复用同一套编译、正确性检查、CUDA event 计时、Nsight Compute 剖析、重试修复与节点持久化逻辑，后端只由 KERNEL_BACKEND 环境变量切换。PTX 路径走 CUDA Driver API 集成，结果保存在 saved_nodes/ptx/ 下。剖析是可选且可延迟的，USE_PROFILING=false 即关闭 ncu，另有按类别设定剖析深度的样例脚本，以控制 profiling 开销。节点式持久化让每个中间结果都可离线重放复现，replay_saved_nodes.py 能用与评测完全一致的流程重新计时。README 还区分了实验入口与 GPU 集成自检脚本两类命令。
- `ucb-bar/autocomp`——主循环是 search/ 里的 beam 束搜索：每轮先生成若干策略方案（planning），再据此产出代码实现（code_models 可与规划模型不同），由评测后端打分后保留 beam_size 个候选进入下一轮。硬件被抽象成三元组：每个目标同时需要一个懂该硬件的优化 agent、一个负责编译与跑分的 evaluation backend、一个描述实例的 hw_config 类，三者按固定子目录命名（trn/tpu/gemmini/kernelbench/gpumode/metal/saturn/xnnpack），新增硬件按 ADDING_HARDWARE_SUPPORT.md 接入。Agent Builder 则从本地目录、PDF、网页文档自动生成硬件专属 agent 并落到 agent_builder/.built/。
- `zhang677/AccelOpt`——核心机制是迭代生成 kernel，并把遇到的「慢 kernel→快 kernel」对比 curate 成优化记忆再注入下一轮提示，从而免去专家提供的硬件特定优化知识。角色分工上，executor 负责生成新 kernel，Fixer 专门修复失败的 kernel，README 明确两组 agent 可使用不同模型。产物流转靠结构化存储：生成结果用 templates/schema_v2.txt 的 SQL schema 存入 supabase kernel 数据库，NKIBench 与 FlashInfer-Bench 共用类似 schema。评测侧提供可插拔的 profiling 服务（NKIKernel.profile），并用「相对硬件可达峰值的百分比」衡量 agent 是否真正穷尽优化空间。
- `zhang677/PCL-lite`——README 极短，只给出脚本级流程：先跑 validate.sh 校验 /benchmark 与 /prompts 下的 test 与 reference yaml，再跑 prepare.sh 生成 benchcard，然后按 single、agent、iterative、single-ws 四种模式执行实验。实验矩阵用「有无 agent / 有无迭代 / 有无结构化 IR」三个正交开关组合，single-ws 即「single without structural IR」的消融对照，说明结构化 IR 是该系统的关键载体。模型接入靠 MODEL_NAME 加环境变量（ANTHROPIC/OPENAI/TOGETHER/DEEPSEEK 的 base 与 key），采样数与温度可调。
- `zhang677/PTXBench`——整套系统围绕一个 GPU profiling 服务（fib-profile，HTTP 暴露 /health）展开：多轮模型循环与编码代理网关两条通路共用同一 profiling 服务和同一 prompt hub（multiturn/prompts/hub.json），因此结果可比。runner 把一份 JSON config 展开成轨迹，产出 plan.json、trajectories、日志与成功产物，并支持 --resume 断点续跑。训练侧分两条数据线：Fixit 挑失败的基础模型 kernel 让 Gemini 修复并合成推理、训 LoRA 适配器；KernelGen 挑正确的 Gemini kernel 合成推理后走同一训练与评测路径；两者都用有序 stage 的脚本驱动并配机器可读的源/评测 manifest。

### 形态 D：训练流水线

**是什么**：不只做推理时搜索，而是产出可分发的模型权重或数据集。

**骨架**：数据构造/清洗 + 继续预训练或 SFT + RL 环境与奖励 + 推理配方 + 评测脚本。

**复用要点**：训练环境和评测环境共用同一套编译执行后端，避免训练时看到的 kernel 在评测时编译行为不同；奖励函数单独成模块以便替换。

**各项目的具体做法**：

- `AMD-AGI/AMDKernelVault`——仓库以三个训练阶段目录 cpt/、sft/、rl/ 平行组织，每个阶段自带 README、启动脚本与 train_yamls/ 配置，运行时只需改 YAML 里的 model_name_or_path、dataset、output_dir 三个字段即可换实验。训练数据完全外置在 HuggingFace 的 amd/hip_llm_dataset，并按 cpt/、sft/、rl/ 三级目录与 pretrain_hip、FIM_hip、rl_raw_hard_3k、rl_mi300x_verl_filtered 等固定数据集名对齐，保证三个阶段共用一套数据契约。RL 侧按目标语言拆成两条技术栈：rl4kernel_hip 是 veRL 单轮训练，必须先独立部署 HIP kernel evaluation server 才能拿到奖励；rl4kernel_triton 则是 Slime 多轮训练，自带 ROCm 执行服务、pin 住的容器配方与 32×MI325X 的训练配置说明。数据生成侧再拆成三个可独立 pip 安装的 kit 包（torch_modu2func_kit / torch2hip_kit / py_hip_kernel2kernel_kit），分别负责模块转函数、模块转 HIP kernel、HIP kernel 到优化版 HIP kernel。值得注意的是准备好的参考实现、测试用例、prompt 与 checkpoint 仍留在仓库之外，各阶段 README 承担了大部分操作性说明。
- `ByteDance-Seed/cudaLLM`——流程被组织成四个显式步骤：先用 cuda_dataset.py 把原始数据处理成 SFT 用 parquet（sft_cuda_llm_r1.parquet）与 RL 用 parquet（rl_cuda_llm_0424.parquet），再跑 SFT、在 KernelBench 上做基线评测、最后进入 RL。训练框架不是自研而是外部克隆的 veRL，且 README 明确要求 pin 到指定 git SHA（abb87bc…）并用 --no-deps 安装，以保证复现。SFT 数据由 DeepSeek R1、DeepSeek Coder-7B、Qwen2-32B 生成，评测集固定用 ScalingIntelligence 的 KernelBench。RL 阶段的设计要点是奖励来源与训练分离：每个节点用 4 张 GPU 跑训练循环，另 4 张 GPU 专门运行模型生成的 CUDA kernel，编译并测试后把结果作为奖励回传，因此硬件配比是 4+4。SFT 后的 eval.sh 结果作为 RL 前的基线，RL 结束后可再跑同一脚本量化提升。
- `QiMeng-IPRC/QiMeng-Kernel`——论文官方实现的公开版本，核心是 Macro-Thinking Micro-Coding 范式，但 README 基本只给出三个脚本入口：train.sh 启动训练并接受 base_model 与 num_envs 参数（说明是带并行环境的训练），inference.sh 用 checkpoint 配合外部 LLM API 生成 kernel，eval_generations.sh 在指定 benchmark 与子集上评测生成结果。结果以 KernelBench 与 TritonBench 两套榜单图片呈现，仓库未披露内部目录结构、模型结构或奖励设计。README 明确说明仓库仍在积极开发中，训练与离线数据集将于近期发布。
- `QiMeng-IPRC/QiMeng-MuPa`——核心是 mutual-supervised learning：一个模型做串行到并行代码翻译，另一个做单元测试生成，两者互为验证条件，产出可用于 SFT 的数据，scripts/build_sft.sh 用 vllm 做批量推理完成这一步。随后是 co-evolve 阶段，直接复用 LLaMA-Factory 在该数据上微调，得到 Qwen3-0.6B-translator 模型（已发布在 HuggingFace）。评测侧用 eval_pass_k.sh 计算 Pass@k，测试集为 resources 下自带单元测试的 jsonl；环境用 uv.lock 保证完全可复现。README 强调端到端的训练与评测代码尚未发布。
- `RLsys-Foundation/TritonForge`——仓库由两块组成：SLIME/ 是打过 bug 修复与优化的 RL 框架，slime_plugins 提供可插拔的自定义生成器与奖励函数；KBenchEval/ 是基于 KernelBench 的评测框架。SFT 与 RL 两阶段共用同一个 SLIME 框架，RL 阶段在 KernelBench Level 1-2 上做最多 3 轮迭代，奖励由编译成功、功能正确与 speedup 三项组成，折扣因子 gamma 取 0.4。训练与推理解耦：用 SGLang 起服务做 rollout，NVIDIA 与 AMD 各有一套 Docker 镜像分别锁定 CUDA 12.6.1 与 ROCm 6.3.4，并开放全部中间 checkpoint 与训练配方以便复现。
- `ScalingIntelligence/kernelbench-tinker`——KernelBench 以 git submodule 嵌入并从本地路径安装成 Python 包，环境从 KernelBench 取题并用 Tinker Renderer 格式化为观测；动作是模型产出的候选 kernel，环境解析响应中的 &lt;KERNEL&gt; 块后送到 Modal 隔离 GPU 容器编译、测试并 profile，再把正确性、加速比与静态检查结果按 RewardConfig 折成标量奖励。扩展点是 KernelBenchEnvGroupBuilder（分组归一化实现 GRPO）与 KernelBenchDatasetBuilder（按 level 划分训练/评估集）。
- `Wangyaoyuu/SparseRL`——把预训练代码 LLM 当作随机策略：输入稀疏矩阵的行/列索引，用正弦嵌入编码动态稀疏模式，模型输出稀疏算子（SpMV、SpMM）的 CUDA kernel。训练链为预训练扩域 → SFT 学映射 → PPO 优化，RL 阶段用编译器与执行器反馈构造含编译、正确性、执行时间的层次奖励。README 自述只提供 SFT 与 PPO 的最小可跑流水线，数据以 .mtx 或 JSONL 两种形式喂入。
- `hkust-nlp/KernelGYM`——整体是分布式评测服务：客户端 → FastAPI → Redis 任务队列 → 各节点 GPU worker，worker 内部再用子进程池隔离 CUDA 错误。核心抽象拆成 Backend（编译/加载/运行）、Toolkit（正确性与性能逻辑）、Workflow Controller（编排）三层，并以 register_backend/register_toolkit 方式支持扩展到物理模拟、渲染等新 GPU 任务类型。计时统一用 CUDA event 而非 wall-clock，并支持 warmup 与多次 trial。仓库内另有 drkernel/ 目录，提供与 VERL 框架对接的分布式 RL 训练、基于编译/正确性/性能的多维奖励函数与训练脚本。
- `ornith-ai/CUDA-L1`——README 描述的是研究成果与发布产物，而非训练代码入口：核心是对比式强化学习框架，用比较学习的方式增强 CUDA 优化。发布物按 GPU 型号分别组织（h100.json 等），每行一个 JSON 对象，记录 KernelBench 的 level_id/task_id、参考 CUDA 代码、CUDA-L1 生成的 custom_code、CUDA Graph 版本代码，以及 default、torch.compile、torch.compile+ReduceOverhead、CUDA Graph 四种基线下的时间比 score。评测在 A100、3090、H100、H20、L40 上对照四组基线统计 mean/max/分位数加速比与成功数。README 明确披露了 RL 阶段的 reward hacking 风险（利用计时测量与缓存结果）并列出对应修复项。

### 形态 E：执行底座

**是什么**：提供 kernel 的表达层或运行时，本身不负责生成。

**骨架**：DSL/编译器 + 算子库 + 调度/内存层 + 多后端适配 + 基准与文档。

**复用要点**：底座决定「可生成的 kernel 空间」，上层生成器的工作量与底座 DSL 的表达能力直接相关；先定底座再写生成器。

**各项目的具体做法**：

- `HazyResearch/ThunderKittens`——整个库是 header-only，clone 后 include kittens.cuh 即可用，库本身不提供安装步骤。2.0 起不再作为 Python 包发布，kernels 目录下每个 kernel 必须单独编译，Makefile、测试与 benchmark 都与对应 kernel 源码同目录。每个 kernel 刻意自包含而不共用统一 harness，目的是让任何人轻松新增 kernel；库本身只提供数据类型（register/shared × tile/vector）与操作，kernel 通过 layout 与模板参数描述算法。
- `NVIDIA/cutlass`——以 CuTe 的多维 layout/tensor 抽象为核心，把 GEMM 层级拆成 collective、mainloop、epilogue 等可复用组件，并按 tile 大小、数据类型、数学指令策略参数化。C++ 侧是 header-only 模板库，客户端只需把 include/ 加进头文件搜索路径；Python 侧是 CuTe DSL，编译期做布局一致性检查，比 C++ 编译快几个数量级并可直接被框架调用。tools/library 预实例化全部受支持模板，tools/profiler 负责批量跑分并同时与 reference_device、cuBLAS 比对，test/unit 用 GoogleTest 覆盖 API 与 GEMM 计算。
- `ROCm/aiter`——同一算子可以有 Triton、Composable Kernel、手写 ASM、Opus、FlyDSL 多种后端实现，贡献规则强制一个 PR 只改一个后端，跨后端改动必须拆成 stacked PR 依次合入。构建期策略集中在 aiter_worker_limits.py 一个共享入口：按 cgroup 的 CPU 与内存配额自动推算编译 worker 数并允许 AITER_MAX_JOBS 覆盖，GPU 执行池另按可见 GPU 数乘 AITER_GPU_WORKERS_PER_DEVICE 限流，嵌套 fan-out 时子进程强制 -j1 防超订。发布侧每两周一个 release 分支与 tag，自动化校验 tag 指向分支 HEAD、并确认各 ROCm/Python 组合的 wheel 数量完整才上传。
- `flagos-ai/FlagGems`——FlagGems 是 FlagOS 全栈中的算子层：用 Triton 写后端中立的算子集合，并通过注册 PyTorch 的 ATen backend，让用户不改动底层 API 即可把算子切到 Triton 实现，实现 develop once, run anywhere。README 列出的工程要点包括 eager 模式即可用（不依赖 torch.compile）、pointwise 算子的自动代码生成（支持任意输入类型与布局）、按函数的快速运行时分发、多后端接口（10+ 后端），以及仍在推进的 C++ Triton 函数分发器。
- `hgl71964/cuasmrl`——该仓库 README 几乎完全是 Triton 上游的源码构建说明（venv 依赖、clang+lld、ccache、vscode compile_commands 配置），仅在 Install 段落追加了 CuAssembler 的 clone 与 PYTHONPATH 设置、以及 pip install -e cuasmrl。README 未描述 cuasmrl 包自身的结构、训练流程或用法，也未提及任何 RL 细节。可确证的结构性事实是：这是一个 Triton 编译器 fork，需要按 triton → pytorch → triton 的顺序依次构建以保证版本匹配。
- `mindspore-ai/akg`——2.4 之后重构为两个子项目：AKG-AGENT 是大模型驱动的算子生成工具，提供基于 Multi-agent 的算子自动生成框架、AscendKernelBench 评测平台与算子知识库，当前支持用 LLM 生成 Triton-Ascend（Atlas A2/A3）与 SWFT（300I DUO）DSL 并完成 kernel 编译；AKG-MLIR 则是基于 MLIR 的深度学习编译器，含 CPU/GPU/Ascend 的完整算子编译 pipeline、MindSpore Dialect 图编译方言以及 Linalg/Affine/GPU 方言扩展，并对接 AscendNPU IR 支持昇腾后端融合算子生成。两个子项目可各自独立安装构建，共用同一仓库的多后端支持目标。
- `tile-ai/BitBLAS`——主体是一个 bitblas Python 包，只暴露 Matmul 与 Linear 两个 API，算子形态由 MatmulConfig（M/N/K、dtype 组合、layout、group_size、scaling/zeros）描述后自动生成内核。功能边界按目录切分：integration/ 接入 PyTorch、GPTQModel、AutoGPTQ、vLLM 与 BitNet，benchmark/ 单独收集各格式与设备基准。扩展方式有两条：一是基于 TIR Script 的 DSL 自定义混合精度算子，FlashAttention 算子新增时直接用 TileLang 实现。
- `tile-ai/tilelang`——tilelang 是建在 TVM 之上的 DSL，@tilelang.jit 会按输入 shape 与编译期参数特化 kernel，用户用 T.Kernel/T.gemm/T.copy 描述 tile 级计算。它正从单后端演进为 TileLang-X 多后端架构：device 与 host CodeGen 都收拢到 backend registry，CUDA/ROCm/Metal 有静态方言，Ascend A2/A3、MUSA、MetaX、HYGON、TANG 等生态适配器则拆到独立仓库。README 把大量篇幅给了编译期可观测性：IR dump、pass 可视化、pass diff、编译器 pass 计时，说明其架构把「可调试」当作一等公民。
- `triton-lang/triton`——Triton 分成 Python DSL 前端与 C++/MLIR/LLVM 编译后端，2.0 把后端重写为 MLIR，并支持背靠背 matmul（flash attention 类）。构建上不绑定系统 LLVM：用 cmake/llvm-info.json 里的 llvm_hash 锁定版本，README 明确说 LLVM 无稳定 API、不能用任意版本。可观测性是核心设计：所有编译与调试开关集中在 python/triton/knobs.py，可用环境变量覆盖，并提供 IR dump、MLIR reproducer、kernel override、interpreter 等机制。测试分 make test（需 GPU）与 make test-nogpu（解释器）两条路径。

### 形态 F：综述清单

**是什么**：不提供代码，只提供领域导航。

**骨架**：分类目录 + 条目链接 + 简短说明。

**复用要点**：作为查表入口，不作为工程依赖；引用其中的条目时回到原始仓库核实。

**各项目的具体做法**：

- `flagos-ai/awesome-LLM-driven-kernel-generation`——仓库不含代码，是综述（arXiv 2601.15727）配套的 awesome 列表。作者把领域工作划为四大流：LLM4Kernel（分 SFT 与 RL 两种后训练）、Agent4Kernel（再按学习机制、外部记忆管理、硬件 profiling 集成、多智能体编排四个维度）、Datasets 与 Benchmarks。条目统一以 [日期] 标题加论文/代码/数据集链接呈现，并附 GitHub star 徽章；数据集部分又细分结构化数据集与源码仓库（算子库、框架集成、DSL）两类。
- `qhy991/Awesome-LLM-Kernel-Agent`——真正的仓库产物是 README 本身：127+ 篇 LLM kernel 生成工作被组织成 Mermaid 时间线与五分类流程图（模型/后训练、Agent 工作流、数据资产、评测、集成系统），正文还用表格给出标题、会议、日期、代码链接、作者、机构与主题标签。图形生成被工程化为一条流水线：条目与时间线存在 YAML 中，由 llm_kernel_agent_landscape/ 下的 make 目标做校验、渲染并回写 README 中带 BEGIN/END 标记的区块，从而避免手改 Mermaid 出错。维护指南直接给出按目标该改哪个 YAML 文件的对照表，并支持额外导出 SVG/PPTX/drawio 用于汇报。

### 形态 G：其他 / 单一功能工具

**是什么**：只覆盖闭环中的一小段，没有形成完整的评测或生成闭环。

**骨架**：视项目而定，通常是单个脚本或单一能力包。

**复用要点**：适合作为参考实现片段借鉴，不适合作为项目骨架。

**各项目的具体做法**：

- `AI9Stars/AutoTriton`——README 极短，实质是一篇工作说明 + 权重发布页：仓库本身不含训练或推理代码。可确证的事实是训练方法为两段式——先用一条高质量数据采集流水线做 SFT 让模型获得必要的 Triton 编程能力，再做 GRPO 强化学习，把规则型奖励与执行型奖励组合起来依次施加。基座模型是 ByteDance-Seed 的 Seed-Coder-8B-Reasoning，权重以 8B 形式发布在 HuggingFace。评测侧引用 TritonBench 与 KernelBench 的五个评测通道，结果声称与 Claude-4-Sonnet、DeepSeek-R1-0528 等主流大模型相当。结构上没有代码目录、脚本或入口点，所有可复用资产（模型与论文）都托管在外部平台。
- `CSJianYang/Industrial-Coder`——InCoder-32B 是一个跨工业领域的通用代码基座模型，GPU kernel 优化只是它覆盖的一个域。训练流程被命名为 Code-Flow 三段式：预训练与退火 → 中训练扩展上下文（8K→32K→128K 两级子阶段）→ 执行接地的后训练 SFT。语料侧的可确证做法包括许可过滤、PII 去除与多级去重（精确哈希、token 级近重复、repo 级 fork 合并），并在 4096 GPU 上以自回归 LM 加 FIM 方式训练。中训练阶段会合成工业 QA（场景规格 → 种子代码生成 → 带自动验证的 QA 对合成），并构造 Thought-Action-Observation 形式的 agent 轨迹，反馈来自硬件仿真器、综合工具、C/C++ 编译器与形式验证引擎；后训练用 250 万条真实工业任务样本做执行接地 SFT，并从编译器报错、运行日志、波形差异与性能瓶颈中提炼闭环修复轨迹。正确性判据被绑定到具体工具链：芯片设计用 Icarus Verilog/Verilator/Yosys，GPU 优化用 nvcc 与 @triton.jit（数值正确性 + CUDA 计时），3D 建模用 CadQuery/OpenCascade（体积 IoU），嵌入式用 arm-none-eabi-gcc 加 Renode，编译器优化用 x86-64 GCC/LLVM 测试台。仓库本身主要发布模型权重与一个轻量 sft/ 目录（YAML 配置 + 数据二值化 + 训练脚本），不提供 kernel 专用 pipeline。
- `tensormux/kernel-skills`——内容真源是 skills/ 下每个技能目录中的 SKILL.md（遵循 11 段模板）加一份 skill.json 元数据，两者配对存放。构建期把全部 skill.json 聚合成 generated/skills.index.json，CLI 与 TypeScript API 只读这份索引，因此运行期不需要解析 Markdown。schema/skill.schema.json 限定允许的 category (cuda/triton/patterns/quantization/portability/inference) 与 difficulty 取值，validate-skills 脚本在提交前拦截缺字段、重复 id、目录名与 category 不符、空 tags、SKILL.md 小于 400 字节等问题。npm 包只是分发层，README 明确声明自己不是编译器、不是 benchmark harness、不是服务运行时、也不是自主 agent，且不执行生成的代码。质量要求靠 proof/ 目录里的实测前后证据来支撑，例如 softmax 技能用 8 组形状的通过/失败矩阵证明指导前后的差异。

## 3. 工程实践清单

从各项目 README 与目录结构中提炼的具体做法，按主题归类。括号里是提到该做法并给出具体机制的项目。

| 主题 | 条目数 |
| --- | ---: |
| 评测与优化分离 | 28 |
| 正确性防线 | 25 |
| 反馈信号升级 | 20 |
| 隔离与稳定性 | 20 |
| Agent 控制与预算 | 22 |
| 任务与数据来源 | 23 |
| 度量口径 | 6 |
| 部署与交付 | 16 |
| 训练工程 | 24 |
| 可复现性 | 65 |
| 评测严谨性 | 15 |
| 可扩展性 | 36 |
| 其他工程细节 | 40 |

### 评测与优化分离

*把「产生候选」和「判定候选」拆成互不信任的两半，是这批项目里最值得抄的一条。*

- 把评判逻辑拆成多个 judger_* 规则化模块，把原始 profile 翻译成可执行修复建议　<sub>（`0satan0/KernelMem`）</sub>
- 规则型奖励与执行型奖励分离，便于区分格式正确性与功能正确性　<sub>（`AI9Stars/AutoTriton`）</sub>
- 数据集外置到 HuggingFace 并按 cpt/sft/rl 分目录，与代码仓库解耦　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- 训练阶段目录与 YAML 配置分离，改配置即可复跑，便于横向对比　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- agent 通过注册表解耦接入，同一任务契约可复用于任意 agent 与模型　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- 评测与优化分离，agent 产出由平台独立编译/校验/计时　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- 把生成与评测拆成两个独立脚本，评测只需 NPU 而不需 LLM 访问权限　<sub>（`AMDResearch/NPUEval`）</sub>
- 基线模块与导出函数名通过参数解耦，便于复用到不同算子　<sub>（`Anjiang-Wei/Astra`）</sub>
- metrics.json 与 summary.json 分离逐任务结果与聚合结果　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 训练硬件与奖励计算硬件分离：4 卡训练 + 4 卡跑 kernel 算奖励　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- model.py 与 model_new.py 分离基线与优化实现，便于自动对比与回退　<sub>（`BytedTsinghua-SIA/CUDA-Agent`）</sub>
- 生成与评测解耦：生成只落 JSONL，评测对同一结果文件独立执行　<sub>（`CUDA-Bench/CUDABench`）</sub>
- quick 与 full 两档基线分离，并用配对 A/B 抑制测量噪声　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- CLI 拆成 plan/prepare/report 三段，任务配置与运行状态分离可断点续跑　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- 任务定义、负载与提交三件套文件分离，题目与提交彻底解耦　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- 生成期与评测期文件可见性分离，隐藏测试与参考解对模型不可见　<sub>（`NVIDIA/compute-eval`）</sub>
- 数据构建与评测脚本分离（build_sft.sh 与 eval_pass_k.sh）　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- server-based 架构把 rollout 推理与训练解耦，用 SGLang 提供推理服务　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- 把 LLM-judge 的低效判定纳入自动过滤环节　<sub>（`SakanaAI/robust-kbench`）</sub>
- 生成与评测解耦成两个脚本，评测支持多 GPU 并行与 build_cache 把编译并行放到 CPU　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- 正确性与性能测量分离，容差与试验次数可配（CORRECTNESS_TOL / KERNEL_EVAL_TOL）　<sub>（`StigLidu/AdaExplore`）</sub>
- 生成与评测强制分离，cleanup 脚本就地删除答案文件与 .git 历史防泄漏　<sub>（`alibaba/atrex-bench`）</sub>
- 用 task_base 协议加适配器把多个 benchmark 后端解耦到同一优化循环　<sub>（`caoshiyi/K-Search`）</sub>
- reference_code 与 kernel_code 分字段传入，grader 与被测 kernel 解耦　<sub>（`hkust-nlp/KernelGYM`）</sub>
- 把 GPU 集成自检脚本与实验脚本分离，便于排查环境问题　<sub>（`taratt/cutegen`）</sub>
- benchmark/ 与 integration/ 分离，性能数据与框架接入互不干扰　<sub>（`tile-ai/BitBLAS`）</sub>
- 生成与评测解耦，产物按 output/{language}/{strategy}/{temp}-{top_p}/{model}/run{n} 组织便于复用　<sub>（`wzzll123/MultiKernelBench`）</sub>
- executor 与 Fixer 角色分离，失败 kernel 走专门修复路径　<sub>（`zhang677/AccelOpt`）</sub>

### 正确性防线

*正确性判据要和性能判据同等对待，且需要防住「看起来通过」的作弊路径。*

- 支持 resume 续跑与 held-out 未见 shape 泛化评测　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- 用统一任务契约（config.yaml + schema v2）把任务定义与评测动作自包含　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- AST 反作弊检测加 speedup 上限，惩罚 sys.exit/硬编码 PASS/伪造计时　<sub>（`AMD-AGI/Apex`）</sub>
- 两层提示结构：系统提示定角色/工具/反作弊，任务提示带硬件参数与源码位置　<sub>（`AMD-AGI/Apex`）</sub>
- 统一执行契约（顶层 kernel_function 或任务 stem 同名函数）保证提交可跑　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 把正确性判据绑定到各领域真实工具链（nvcc/verilator/yosys/renode/cadquery）　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- 用 producer/consumer/finish 模板隐藏同步与搬运细节　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 正确性另用独立 lm-eval 套件校验，防止性能补丁破坏语义　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- Compute Sanitizer 独立门禁，并用 token 侧信道要求隐藏测试证明确实覆盖到目标 kernel　<sub>（`NVIDIA/compute-eval`）</sub>
- 用 CuTe layout/tensor 抽象统一描述线程与数据层级，隐藏机械索引　<sub>（`NVIDIA/cutlass`）</sub>
- 预实例化模板库加 profiler 工具，批量核对吞吐与正确性　<sub>（`NVIDIA/cutlass`）</sub>
- 正确性先于性能，先与 PyTorch 对拍再计时，错的立即回滚　<sub>（`RightNow-AI/autokernel`）</sub>
- 多初始化设置加多输入配置交叉验证正确性与性能稳定性　<sub>（`SakanaAI/robust-kbench`）</sub>
- 算子目录自描述五件套，元数据与 roofline 对 agent 隐藏　<sub>（`alibaba/atrex-bench`）</sub>
- 标准评测与隐藏评测结果分文件产出，避免口径混淆　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- 用四分布变换（×3、×0.01、×-1）隐藏测试抓溢出下溢与符号取巧　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- 用 PyTorch 自身的 OpInfo/FACTO 测试集作为 kernel 正确性标准　<sub>（`meta-pytorch/BackendBench`）</sub>
- 静态 AST 路由决定轻量/完整路径，并缓存决策避免重复分析　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 公开 reward hacking 案例并主动征集反馈　<sub>（`ornith-ai/CUDA-L1`）</sub>
- 区分 fp16 与 fp32 累加器精度以匹配不同 matmul 语义　<sub>（`ornith-ai/CUDA-L2`）</sub>
- npm 包按语义化版本发布，patch/minor/major 分别对应内容修订、新增技能与破坏性变更　<sub>（`tensormux/kernel-skills`）</sub>
- 示例代码内置 torch.testing.assert_close 精度自检　<sub>（`tile-ai/BitBLAS`）</sub>
- run_multi_test.py 用 -stages 拆分生成/编译/精度，可只重跑某阶段　<sub>（`weich97/NPUKernelBench`）</sub>
- 反作弊检测识别用 PyTorch/Python 计算替换自定义 kernel 的生成代码　<sub>（`wzzll123/MultiKernelBench`）</sub>
- 评测结果统一写成 result_{category}.json，含编译状态、正确性、性能、硬件与反作弊字段　<sub>（`wzzll123/MultiKernelBench`）</sub>

### 反馈信号升级

*把「跑得通」升级成「知道该改哪里」，是搜索系统从试错走向优化的分水岭。*

- 生成代码、评测记录、profile 产物按任务分目录落盘，保证可回放　<sub>（`0satan0/KernelMem`）</sub>
- 用 NCU/NSYS 外部 profiler 的原始指标驱动下一轮优化提示，而非只靠 LLM 猜测瓶颈　<sub>（`0satan0/KernelMem`）</sub>
- hot-patch 回注并在基准后自动还原，保证改动可回滚　<sub>（`AMD-AGI/Apex`）</sub>
- E2E 变更以可逆 overlay 叠回，用 warm-server 交错 A/B 加 0.5% 带宽判定放行　<sub>（`AMD-AGI/GEAK`）</sub>
- 按 Amdahl 排序热点并优先执行成本最低的优化杠杆　<sub>（`AMD-AGI/GEAK`）</sub>
- 每个补丁由独立 agent 验证后再接受，避免自评偏差　<sub>（`AMD-AGI/GEAK`）</sub>
- 跨轮记忆显式化为 insight blackboard 与 hypothesis ledger，并沉淀补丁产物库做 warm-start　<sub>（`AMD-AGI/GEAK`）</sub>
- 用执行接地的闭环修复轨迹（编译错误、波形差异、性能瓶颈）构造后训练数据　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- 评测器负责编译与 ncu 剖析，减少人工干预　<sub>（`CUDA-Bench/CUDABench`）</sub>
- 多档计时模式 (process/kernels/region/gpu/custom) 配合可选 CUPTI/NCU 剖析　<sub>（`NVIDIA/compute-eval`）</sub>
- 为 ncu 配置免密 sudo，使硬件反馈可被脚本自动采集　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- 把 nvcc 与 ncu 版本一致性作为前置检查项　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- 用 Amdahl 定律排序优化目标以最大化端到端收益　<sub>（`RightNow-AI/autokernel`）</sub>
- 评测拆成 compile/test/eval/profile 独立函数并支持并行执行　<sub>（`SakanaAI/robust-kbench`）</sub>
- 用 static_roofline_check.py 离线校验缓存 SOL 值并与生产延迟对照　<sub>（`alibaba/atrex-bench`）</sub>
- 排行榜同时给出速度与显存两个几何平均指标呈现权衡　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- pip install --no-build-isolation 避免每次 cmake 软链变化触发 ninja 全量重建 .a　<sub>（`hgl71964/cuasmrl`）</sub>
- 用 roofline 判定 + ≥95% SOL 提前终止，best-so-far 追踪与退化回滚　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 把提示词、生成、驱动评测、指标分析拆成四个独立目录，流程可复现　<sub>（`parallelcodefoundry/ParEval`）</sub>
- profiling 开关化并支持延迟 profiling 以控制 ncu 开销　<sub>（`taratt/cutegen`）</sub>

### 隔离与稳定性

*生成的 kernel 随时可能编译崩溃或非法访存，隔离执行是让系统能长时间跑下去的前提。*

- 每 GPU 一个容器 worker + 原子队列抢占，实现并行与任务隔离　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- 评分外包给 Magpie，并用 cache_manager 做缓存隔离保证复现条件一致　<sub>（`AMD-AGI/Apex`）</sub>
- 用 --max-iterations 显式限制迭代次数以控制成本　<sub>（`Anjiang-Wei/Astra`）</sub>
- golden timing 按机器隔离存放，支持环境变量覆盖或一键重生成　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 只给 agent 关键原则不给长指令，防止 harness 被 hack　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 用 Podman 容器隔离执行未信任的模型生成代码　<sub>（`NVIDIA/compute-eval`）</sub>
- 评测与训练分目录隔离（KBenchEval/ 与 SLIME/）互不污染　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- GPU 执行池按设备数乘每设备 worker 数 round-robin 分配任务　<sub>（`ROCm/aiter`）</sub>
- 嵌套 fan-out 时子进程固定 -j1，避免编译超订拖垮机器　<sub>（`ROCm/aiter`）</sub>
- program.md 写足决策手册与崩溃处理，让 agent 长时间自主运行不卡住　<sub>（`RightNow-AI/autokernel`）</sub>
- 所有 rollout 评测放到 Modal 隔离容器，坏 kernel 不污染训练进程　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- 每 batch 存 checkpoint 并提供 just resume，崩溃后可断点续训　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- kernel 执行放独立子进程，崩溃或非法访存不影响主服务　<sub>（`StigLidu/AdaExplore`）</sub>
- 多个 agent worker 并行但共享同一评测服务，避免 GPU 超卖　<sub>（`StigLidu/AdaExplore`）</sub>
- 用 --max-nnz 限制非零元素数以控制生成代码规模与编译开销　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- 把评测拆成开发种子与评测种子两段，防止在评测集上偷偷调优　<sub>（`aisa-group/InferenceBench`）</sub>
- 用 Apptainer 容器隔离每个 agent 的服务环境，保证评测无宿主干扰　<sub>（`aisa-group/InferenceBench`）</sub>
- 每个 GPU worker 用子进程池隔离 CUDA 错误，避免级联崩溃　<sub>（`hkust-nlp/KernelGYM`）</sub>
- 沙箱子进程执行单测隔离 CUDA 崩溃，并显式禁止 PyTorch fallback 冒充实现　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 构建期生成 skills.index.json，CLI 与 API 只读索引，不在运行期解析 Markdown　<sub>（`tensormux/kernel-skills`）</sub>

### Agent 控制与预算

*Agent 循环必须能被打断、复盘和限制，否则「多试几次」会伪装成「搜索得更聪明」。*

- 把优化经验拆成长期记忆（memorybank/）与短期记忆（逐轮 JSON）两层并注入提示　<sub>（`0satan0/KernelMem`）</sub>
- 为多轮 Triton RL 提供 pin 住的容器配方与纯代码自检工具　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- 用 5 个 MCP 服务（源码检索/RAG/GPU 信息/融合/评测）把领域知识暴露给 agent　<sub>（`AMD-AGI/Apex`）</sub>
- 把控制流写成确定性 JS，LLM 只负责判断，保证运行可靠可复现　<sub>（`AMD-AGI/GEAK`）</sub>
- 用 flock 脚本 gpu_lock.sh 串行化 GPU 访问，支持多 kernel 并行　<sub>（`AMD-AGI/GEAK`）</sub>
- 用 Docker + NVIDIA Container Toolkit 固定评测环境与驱动版本　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- 统一 CLI 参数 (gpu/device/round/server_type/subproc_id) 支持多卡多进程并行　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- 训练脚本参数化 base_model 与 num_envs 以支持环境并行　<sub>（`QiMeng-IPRC/QiMeng-Kernel`）</sub>
- 编译并行度集中到单一策略文件，按 cgroup CPU/内存配额自动计算　<sub>（`ROCm/aiter`）</sub>
- 把评测做成带队列的常驻服务，按 GPU 限并发并路由到最空闲卡　<sub>（`StigLidu/AdaExplore`）</sub>
- 配置驱动（config/ 下按 benchmark 命名的 YAML），并提供 stats/re_evaluate 复算工具　<sub>（`StigLidu/AdaExplore`）</sub>
- 预生成技能记忆随仓库发布，复现实验无需重跑 Adapt 阶段　<sub>（`StigLidu/AdaExplore`）</sub>
- 用同预算的 vLLM/SGLang 随机搜索（random/tpe/smac）做 matched-budget 对照　<sub>（`aisa-group/InferenceBench`）</sub>
- A-B-B-A 反向平衡调度抵消顺序偏差，并配合时钟锁定　<sub>（`alibaba/atrex-bench`）</sub>
- 按 shape 分片 + Ray Data 分发多 GPU，失败只重试受影响分片并提交成功分片　<sub>（`alibaba/atrex-bench`）</sub>
- 把 agent 方法拆成记忆、profiling、编排三个可比较维度　<sub>（`flagos-ai/awesome-LLM-driven-kernel-generation`）</sub>
- 把 backend/toolkit/workflow 抽象成可注册插件，便于接入新 GPU 任务　<sub>（`hkust-nlp/KernelGYM`）</sub>
- 用 Redis 队列做优先级任务调度，从单 GPU 平滑扩到多节点　<sub>（`hkust-nlp/KernelGYM`）</sub>
- 配套算子知识库与 AscendKernelBench 评测平台形成生成-评测闭环　<sub>（`mindspore-ai/akg`）</sub>
- 性能测量支持多 GPU 多进程并行以加速评测　<sub>（`thunlp/TritonBench`）</sub>
- 提供 IR dump、pass 可视化、pass diff、pass 计时等编译期调试工具　<sub>（`tile-ai/tilelang`）</sub>
- 提示把 BASE_PATH 指向非 git 目录，避免 git logging 使并行采样慢 10 倍以上　<sub>（`zhang677/PCL-lite`）</sub>

### 任务与数据来源

*任务从哪来、怎么切分、会不会污染，直接决定评测结论能推广到多远。*

- 提供 Examples.ipynb 演示完整流水线与三种提交格式　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 主动移除与 KernelBench 高度相似的样本以降低评测污染风险　<sub>（`BytedTsinghua-SIA/CUDA-Agent`）</sub>
- 中训练分级扩上下文 8K→32K→128K，先文件级任务再长程调试类任务　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- 语料经许可过滤 + PII 去除 + 三级去重（哈希/token 近重复/fork 合并）后训练　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- 用三级 prompt 难度（引导/规范/仅任务名）区分模型自主补全能力　<sub>（`CUDA-Bench/CUDABench`）</sub>
- 性能测试由 LLM 与题目同批生成，保证测试与任务一致　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- 题目从真实仓库性能提交自动挖掘，避免人工出题的主观偏差　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- 批量脚本自动跳过已通过题目并支持 --rerun 复跑　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- 题目 spec 用 YAML 声明 build/test/benchmark 命令，CI 用参考答案持续回归保证题目可解　<sub>（`NVIDIA/compute-eval`）</sub>
- 题目打包成带 MD5 完整性哈希的版本化 datapack，永久支持旧 release　<sub>（`NVIDIA/compute-eval`）</sub>
- 先用过滤脚本筛掉可被 reward hack 的题目再纳入正式评测　<sub>（`SakanaAI/robust-kbench`）</sub>
- 把稀疏格式选择编码进 prompt 首行（FORMAT: CSR）以对齐 PPO 格式选择逻辑　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- 每个作业把模型权重复制到私有缓存，避免多作业互相污染　<sub>（`aisa-group/InferenceBench`）</sub>
- 把新增输入盲题目配置集中在 STRIP_TEST_CONFIG_PIDS 一处维护　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- 每条记录统一为 [日期] 标题加论文/代码链接加 star 徽章格式便于索引　<sub>（`flagos-ai/awesome-LLM-driven-kernel-generation`）</sub>
- 用统一 taxonomy 四大流分类，便于横向比较不同技术路线　<sub>（`flagos-ai/awesome-LLM-driven-kernel-generation`）</sub>
- 把基准与生产工作流合为同一体系，支撑 AI 自我改进的正循环　<sub>（`flashinfer-ai/flashinfer-bench`）</sub>
- 用固定 Trace Schema 描述 kernel 与 workload，保证跨来源可比　<sub>（`flashinfer-ai/flashinfer-bench`）</sub>
- 子图按 shape 签名去重，让同一 kernel 被多个子图复用　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 同一份数据渲染分类图与时间线两种视图　<sub>（`qhy991/Awesome-LLM-Kernel-Agent`）</sub>
- G 通道同时评代码相似度与执行结果，区分像与对　<sub>（`thunlp/TritonBench`）</sub>
- 训练语料分 crawl（BERT 相似度去重）与 synth（合成）两路并合并供 RAG 使用　<sub>（`thunlp/TritonBench`）</sub>
- 提供 Trace Visualizer 复盘每轮策略与分数变化　<sub>（`ucb-bar/autocomp`）</sub>

### 度量口径

*度量口径决定了「哪个更好」这个问题有没有唯一答案。*

- 同一模型与闭源主流大模型在多通道基准上对齐比较以验证性价比　<sub>（`AI9Stars/AutoTriton`）</sub>
- 项目级 .omp/ 存 agent 指令、.kopt/ 存运行日志与基准历史　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 用理论 roofline 排序而非仅相对加速比，避免自比自　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- 评测按 benchmark 加 subset 切分，便于分维度报告结果　<sub>（`QiMeng-IPRC/QiMeng-Kernel`）</sub>
- 分 LLM Track 与 Agent Track 两条赛道分别度量 Pass@K 与迭代优化能力　<sub>（`flagos-ai/KernelGenBench`）</sub>
- 算子基准按名字注册加载，可作为库在自定义脚本中复用　<sub>（`meta-pytorch/tritonbench`）</sub>

### 部署与交付

*能不能被真实服务用上，是「研究有效」和「可交付」之间的分界。*

- RL 训练前先独立部署 evaluation server，把奖励来源做成稳定外部服务　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- 性能对比同时对 eager 基线与 torch.compile 基线，双基线判定收益　<sub>（`BytedTsinghua-SIA/CUDA-Agent`）</sub>
- 数据过滤要求 eager 与 torch.compile 双通过并剔除随机算子，保证样本确定　<sub>（`BytedTsinghua-SIA/CUDA-Agent`）</sub>
- 同时发布 Base/Thinking/FP8/AWQ-INT4/GPTQ-INT4 多种权重覆盖不同部署约束　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- header-only 免安装，include 即可用，避免构建分发负担　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 训练配置外置为 YAML + dataclass，CLI 可逐项覆盖　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- 集成 KernelBench 的 reward hack 检查器（pass 语句、torch.nn.functional 调用等）　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- 把优化过的 kernel 与服务框架打通，评测产物即部署产物　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- 用统一 CLI（list/capture/bench/eval）承载优化、评测、部署三类工作流　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- 产物目录由 utils/paths.py 统一管理，CLI 侧可覆盖　<sub>（`caoshiyi/K-Search`）</sub>
- 把基线升级为 TF32，使加速比对齐真实部署的 Tensor Core 表现　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- eager 模式即可用，不绑定 torch.compile 降低集成门槛　<sub>（`flagos-ai/FlagGems`）</sub>
- 提供按算子维度的运行时快速分发与 C++ Triton 分发器　<sub>（`flagos-ai/FlagGems`）</sub>
- 以 pip 包加 Python API 加 CLI 三种形态提供入口　<sub>（`flashinfer-ai/flashinfer-bench`）</sub>
- 启动脚本自动探测 IP、端口与 GPU 列表生成 .env，保证一键可复现部署　<sub>（`hkust-nlp/KernelGYM`）</sub>
- backend registry 统一分发 device/host CodeGen，新增后端不改核心　<sub>（`tile-ai/tilelang`）</sub>

### 训练工程

*训练数据的过滤规则和评测集的划分规则必须一起设计，否则很容易在评测集上泄漏。*

- SFT 前置一条高质量数据采集流水线过滤训练语料　<sub>（`AI9Stars/AutoTriton`）</sub>
- 先 SFT 补齐领域编程能力、再用 GRPO 施加组合奖励的分阶段训练顺序　<sub>（`AI9Stars/AutoTriton`）</sub>
- 用固定数据集名（pretrain_hip/FIM_hip/rl_*）登记数据来源与阶段归属　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- A/B 配对运行（run-suffix 命名）+ compare_runs.py + 本地看板做对照　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- 把轨迹导出为 RL/SFT 数据集，打通从线上优化到训练回流的链路　<sub>（`AMD-AGI/Apex`）</sub>
- 提供 JupyterLab notebook 便于交互式理解与使用数据集　<sub>（`AMDResearch/NPUEval`）</sub>
- SFT 与 RL 数据分列为不同 parquet，可独立迭代　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- pin 外部 veRL 仓库的指定 git SHA 并以 --no-deps 安装，保证训练框架可复现　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- 用 KernelBench 作为统一评测集对 SFT 与 RL 两阶段做前后对比　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- SFT 数据先 tokenize 成 .npy 再由 YAML 驱动多机训练　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- SFT 与 RL 共用同一 RL 框架，避免维护两套训练栈　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- 把生成器与奖励函数做成 slime_plugins 可插拔组件　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- 无本地 GPU 时可用 Modal serverless 做云端评测，eval_mode=local/modal 切换　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- reward 计算与静态检查拆成独立模块，并输出可读 WARNING/ERROR 日志　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- SFT 与 PPO 拆成两个可独立运行的模块入口，便于分阶段调试　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- SFT 数据同时支持 .mtx 矩阵与带 rows/cols/shape/format/code 字段的 JSONL　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- kernel 抽取失败时给出负的编译奖励，作为显式失败信号　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- 对易 reward hack 的题自动从 prompt 剥离测试输入　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- 为每条记录打主题标签 (CUDA/Triton/RL/Agent 等) 便于横向检索　<sub>（`qhy991/Awesome-LLM-Kernel-Agent`）</sub>
- 用 scripts/reproduce_*.sh 分阶段复现 SFT 流程并支持 --check 静态检查　<sub>（`zhang677/AccelOpt`）</sub>
- NUM_SAMPLES 与 TEMPERATURE 可调，便于做采样统计　<sub>（`zhang677/PCL-lite`）</sub>
- SFT 用分阶段脚本 reproduce_fixit.sh / reproduce_kernelgen.sh 驱动并支持 --check 预检　<sub>（`zhang677/PTXBench`）</sub>
- profiling 服务独立成 HTTP 服务，模型可用 --service-url 或 Modal 远程接入　<sub>（`zhang677/PTXBench`）</sub>
- runner 把 JSON config 展开成轨迹并写 plan.json/日志/成功产物，--resume 支持续跑　<sub>（`zhang677/PTXBench`）</sub>

### 可复现性

*固定环境、留痕、可回滚，是这类项目的头号工程债来源。*

- 把生成器拆成多个可独立 pip 安装的 kit 包，避免单一巨型依赖　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- 复现脚本明确区分 gpt-4.1 与 gpt-4o-mini 两个被测模型　<sub>（`AMDResearch/NPUEval`）</sub>
- 所有脚本可用 docker_run_script.sh 包装成独立容器会话执行　<sub>（`AMDResearch/NPUEval`）</sub>
- 用 Docker 固定 XRT 与 NPU 编译运行环境　<sub>（`AMDResearch/NPUEval`）</sub>
- 结果目录带时间戳，保留每次优化运行便于横向比较　<sub>（`Anjiang-Wei/Astra`）</sub>
- 同时支持 JSONL/单文件/目录三种提交形态自动识别　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 把评测拆成 call/exe/perf 三个独立阶段并分别落盘，便于定位失败原因　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 把 agent 闭环固化成可复用工作区模板（编译/校验/profiling 脚本 + SKILL.md）　<sub>（`BytedTsinghua-SIA/CUDA-Agent`）</sub>
- 任务定义、参考实现、输入生成与比对脚本全部内聚在同一条 JSONL 记录里　<sub>（`CUDA-Bench/CUDABench`）</sub>
- 结果按 provider/model/level/pass 命名分目录，便于多模型多难度对比　<sub>（`CUDA-Bench/CUDABench`）</sub>
- 验证与测量适配器落盘到 harness/ 目录，可审计、可重跑　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- kernel 自包含加同目录 Makefile/测试/benchmark，方便增量新增　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 基线/人类/agent 三方在同一环境对比，把相对人类专家的差距显式化　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- 用 Docker 镜像固定被测服务与依赖环境　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- 容器内预置多 DSL 编译链，可用同套流程评测不同语言 kernel　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- 持续兼容验证 FlashAttention、FlashInfer、cuDNN-Frontend、PyTorch、TensorRT-LLM 等下游　<sub>（`NVIDIA/cutlass`）</sub>
- 以 KernelBench 任务目录作为标准化输入，便于批量与对照　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- 用 conda environment.yml 一次性固定依赖环境　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- 用 requirements.txt 与 pip install -e . 固定并统一安装环境　<sub>（`QiMeng-IPRC/QiMeng-Kernel`）</sub>
- 训练、推理、评测拆成三个独立脚本入口，各阶段可分别复现　<sub>（`QiMeng-IPRC/QiMeng-Kernel`）</sub>
- 用 uv.lock 锁定完全可复现的依赖环境　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- NVIDIA 与 AMD 各一套 Docker 镜像锁定 CUDA/ROCm 与依赖版本　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- Triton 与 CUDA C++ 双后端共用同一 kernel_fn 接口，bench 脚本无需分叉　<sub>（`RightNow-AI/autokernel`）</sub>
- agent 只改单个 kernel.py 且评测脚本固定不可改，diff 可审、回滚干净　<sub>（`RightNow-AI/autokernel`）</sub>
- 结果以 TSV 纯文本落盘，人可读、可 git、可离线分析　<sub>（`RightNow-AI/autokernel`）</sub>
- 用 uv + pyproject.toml 管理依赖，ROCm 与 GPU 依赖拆成可选 extras　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- 结果按 runs/{run_name} 目录归档，并提供 results/timing 的跨硬件基线参考　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- KernelBench 以 git submodule 固定评测代码版本，避免上游漂移　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- 同一算子同时维护 baseline 与 candidate 目录，保证对照实验结构一致　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- 采集运行期 init/forward 的 shape 与 dtype 元数据以复现真实 workload　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- Python 依赖锁在 containers/locks/ 中固定版本　<sub>（`aisa-group/InferenceBench`）</sub>
- 用 INFERENCE_BENCH_* 环境变量统一指定共享存储路径便于集群迁移　<sub>（`aisa-group/InferenceBench`）</sub>
- 世界模型快照与解法 JSONL 全量落盘，支持断点续跑与事后分析　<sub>（`caoshiyi/K-Search`）</sub>
- 评测提供 local 与 Modal 双后端，便于无 GPU 环境复现　<sub>（`caoshiyi/K-Search`）</sub>
- 把平台依赖拆到 requirements/requirements_&lt;platform&gt;.txt 便于多芯片维护　<sub>（`flagos-ai/KernelGenBench`）</sub>
- 构建顺序固定为 triton → pytorch → 重装 triton，保证 ptxas/cuobjdump 与宿主版本一致　<sub>（`hgl71964/cuasmrl`）</sub>
- 把算子实现按固定目录约定组织，便于上游贡献与运行时动态替换　<sub>（`meta-pytorch/BackendBench`）</sub>
- prompt 用 Jinja 模板管理，便于版本化与统一改造　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 每阶段写 run 目录 (.fuse/&lt;run_id&gt;、.optimize/&lt;run_id&gt;)，可复现并支持单会话重跑　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 安装脚本默认装 PyTorch nightly 并使用其捆绑的 Triton 版本，避免版本错配　<sub>（`meta-pytorch/tritonbench`）</sub>
- 用 git submodule 固定第三方 kernel 来源版本，保证可比与可复现　<sub>（`meta-pytorch/tritonbench`）</sub>
- 离线与 server 双模式评测，server 模式按目标 QPS 压测贴近服务场景　<sub>（`ornith-ai/CUDA-L2`）</sub>
- makefile 在检测不到 CUDA/HIP/Kokkos 库时自动跳过对应目标，降低环境门槛　<sub>（`parallelcodefoundry/ParEval`）</sub>
- requirements.txt 锁定测试过的依赖版本　<sub>（`parallelcodefoundry/ParEval`）</sub>
- 把 Kokkos 等第三方依赖做成 git submodule 并给出独立构建步骤　<sub>（`parallelcodefoundry/ParEval`）</sub>
- 把每个生成结果按节点持久化到 saved_nodes，可离线重放复现　<sub>（`taratt/cutegen`）</sub>
- 用 JSON Schema 加 validate-skills 脚本做提交前静态校验　<sub>（`tensormux/kernel-skills`）</sub>
- 把评测拆成 call/exe/efficiency 三个可独立执行的脚本并规定执行顺序　<sub>（`thunlp/TritonBench`）</sub>
- 提供 pip wheel 与源码两条安装路径并显式声明环境约束　<sub>（`tile-ai/BitBLAS`）</sub>
- @tilelang.jit 按输入 shape 与编译期参数特化 kernel 并缓存　<sub>（`tile-ai/tilelang`）</sub>
- knobs.py 集中所有配置开关并允许环境变量覆盖　<sub>（`triton-lang/triton`）</sub>
- make dev-install-llvm 提供 core/amd/all 三种 LLVM 构建目标　<sub>（`triton-lang/triton`）</sub>
- 用 cmake/llvm-info.json 的 llvm_hash 锁定 LLVM 提交，避免 API 漂移　<sub>（`triton-lang/triton`）</sub>
- Agent Builder 从文档目录/PDF/网页生成 agent，产物落到 .built/ 便于版本化　<sub>（`ucb-bar/autocomp`）</sub>
- 每个硬件目标固定为 agent/backend/hw_config 三个子目录，新增目标沿用同一约定　<sub>（`ucb-bar/autocomp`）</sub>
- 用 provider::model 字符串统一描述 LLM 来源，环境变量优先于 keys.py 配置文件　<sub>（`ucb-bar/autocomp`）</sub>
- base_config.yaml 集中配置模型路径，set_framework_env.sh 固定 CANN 环境　<sub>（`weich97/NPUKernelBench`）</sub>
- 任务目录模板化：question/answer/validation/api_desc.md 四件套，参考答案即基线　<sub>（`weich97/NPUKernelBench`）</sub>
- 实验以 shell 脚本目录化组织（full_complete_local、flb_full_complete_local），模型与硬件参数化　<sub>（`zhang677/AccelOpt`）</sub>
- 显式克隆 zhang677/flashinfer-bench 并以可编辑安装固定依赖版本　<sub>（`zhang677/AccelOpt`）</sub>
- 实验全部脚本化（experiments/*/run.sh），模式之间只换入口脚本便于横向对比　<sub>（`zhang677/PCL-lite`）</sub>
- 提供 single-ws 消融版本对照结构化 IR 的贡献　<sub>（`zhang677/PCL-lite`）</sub>
- 模型接入统一为 MODEL_NAME + API base/key 环境变量，可换多种 LLM　<sub>（`zhang677/PCL-lite`）</sub>
- 两条 agent 通路共用同一评测测试脚本与 prompt，保证可比性　<sub>（`zhang677/PTXBench`）</sub>
- 评测环境用 docker 镜像固定（Dockerfile.eval 构建 ptxbench-multiturn-eval）　<sub>（`zhang677/PTXBench`）</sub>

### 评测严谨性

*把「跑了几次、基线是谁、预算多少」写进结果，比单纯报一个加速比重要得多。*

- 用共享 binding_registry.h 统一注册 Python 绑定，避免每个 kernel 重复样板　<sub>（`BytedTsinghua-SIA/CUDA-Agent`）</sub>
- 按 thread/warp/warpgroup/block/grid 分层对齐 NVIDIA 编程模型　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 提供可选 GPU 锁频以降低测量方差　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- C++ 模板与 Python DSL 对齐同一套抽象，显著降低学习曲线　<sub>（`NVIDIA/cutlass`）</sub>
- 三套独立计时（KernelBench / torch benchmark / do_bench）交叉核对　<sub>（`SakanaAI/robust-kbench`）</sub>
- 分片合并要求覆盖率完整且输入/评测器哈希、硬件、种子一致　<sub>（`alibaba/atrex-bench`）</sub>
- 内置演化搜索基线（OpenEvolve/ShinkaEvolve）做同目标直接对照　<sub>（`caoshiyi/K-Search`）</sub>
- 计时统一用 CUDA event 并把 warmup/trial 次数做成可配参数　<sub>（`hkust-nlp/KernelGYM`）</sub>
- 修正 KernelBench 评测的 stream 计时同步，消除测量误差　<sub>（`ornith-ai/CUDA-L1`）</sub>
- 同时对照 torch.compile、torch.compile RO、CUDA Graph 与自定义 backend flag 四组基线　<sub>（`ornith-ai/CUDA-L1`）</sub>
- 维护指南提供目标到文件的对照表，降低贡献门槛　<sub>（`qhy991/Awesome-LLM-Kernel-Agent`）</sub>
- 统一后端抽象让 CUDA/CuTe/PTX/Triton 共用同一编译-校验-计时-剖析流水线　<sub>（`taratt/cutegen`）</sub>
- 随仓库发布主流模型的生成结果作为基线对照　<sub>（`thunlp/TritonBench`）</sub>
- 支持矩阵以表格列出 dtype 组合与实测平台（SM 号），便于对齐验证　<sub>（`tile-ai/BitBLAS`）</sub>
- 任务按 level1/2/3 难度分层，便于分层统计与难度分析　<sub>（`weich97/NPUKernelBench`）</sub>

### 可扩展性

*把任务、模型、后端、评分器做成可外置的配置，新任务不应需要改核心代码。*

- LLM 后端统一抽象成 query_server 接口，可切换 OpenAI / vLLM / sglang　<sub>（`0satan0/KernelMem`）</sub>
- 用 optimization_tree.json 记录 kernel 父子谱系与提速比，支持经验追溯　<sub>（`0satan0/KernelMem`）</sub>
- 用 13 个 SKILL.md 承载可复用的领域优化知识，扩展成本低　<sub>（`AMD-AGI/Apex`）</sub>
- 用 --compare-kind 标签把不同算子类型的测试生成策略参数化　<sub>（`Anjiang-Wei/Astra`）</sub>
- 任务描述外置成 task.toml（objective/measure/validate/hints）便于扩展新任务　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 通过 concepts (C++20) 做接口约束，错误在编译期暴露　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 把 GEMM 层级组件化并参数化策略，便于复用与二次调优　<sub>（`NVIDIA/cutlass`）</sub>
- 评测集以 jsonl 加配套单元测试的形式自带，可独立复核　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- 开源全部中间 checkpoint、数据与训练配方以支持复现　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- 多后端并存加一个 PR 只改一个后端的评审规则，控制变更面　<sub>（`ROCm/aiter`）</sub>
- 统一 backend 参数抽象（cuda/triton/cute/tilelang/thunderkittens/hip），一套代码多后端　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- 以 L1-L4 四级抽象分层，便于按粒度定位优化收益来源　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- pointwise 算子走自动代码生成，支持任意输入类型与布局　<sub>（`flagos-ai/FlagGems`）</sub>
- 注册进 PyTorch ATen backend，用户无需修改底层 API 即可切换实现　<sub>（`flagos-ai/FlagGems`）</sub>
- 算子实现保持后端中立，一套代码覆盖多类 AI 加速器　<sub>（`flagos-ai/FlagGems`）</sub>
- 算子集按 ATen/vLLM/cuBLAS 三来源分层构建，覆盖通用与推理算子　<sub>（`flagos-ai/KernelGenBench`）</sub>
- 把 compile_commands.json 喂给 VSCode C++ 扩展解决 C++ 补全　<sub>（`hgl71964/cuasmrl`）</sub>
- 基于 MLIR 方言扩展 (MindSpore Dialect/Linalg/Affine/GPU) 复用编译基础设施　<sub>（`mindspore-ai/akg`）</sub>
- 统一多硬件后端适配：CPU、NVIDIA、V100/A100、Atlas 800T A2/A3、300I DUO　<sub>（`mindspore-ai/akg`）</sub>
- 以 YAML 为唯一数据源，Makefile 统一做校验、渲染与 README 回写　<sub>（`qhy991/Awesome-LLM-Kernel-Agent`）</sub>
- token 用量按实验记入 CSV (TOKEN_USAGE_CSV_PATH 可配置) 以核算成本　<sub>（`taratt/cutegen`）</sub>
- 以 SKILL.md 为真源、skill.json 为机器可读元数据，双轨维护　<sub>（`tensormux/kernel-skills`）</sub>
- 用 MatmulConfig 结构化描述 dtype/layout/量化参数，避免配置散落　<sub>（`tile-ai/BitBLAS`）</sub>
- 把生态适配器拆到独立仓库发布，主仓只维护核心与主后端　<sub>（`tile-ai/tilelang`）</sub>
- 编译产物支持跨主机复用已编译 CUDA 二进制缓存　<sub>（`tile-ai/tilelang`）</sub>
- MLIR_ENABLE_DUMP / TRITON_KERNEL_DUMP 支持逐 pass 转储 IR　<sub>（`triton-lang/triton`）</sub>
- TRITON_INTERPRET=1 解释器模式支持在 kernel 中下断点，免 GPU 调试　<sub>（`triton-lang/triton`）</sub>
- backend 抽象 simulator 选项（spike/firesim/gpumode-local），可在无真机时评测　<sub>（`ucb-bar/autocomp`）</sub>
- 大文件用结构化 JSON 编辑（old_str/new_str）而非整文件重写　<sub>（`ucb-bar/autocomp`）</sub>
- 同一入口同时支持 LLM 生成与人工实现两条评测路径（-chat 开关）　<sub>（`weich97/NPUKernelBench`）</sub>
- eval_single_runner.py 支持对单个已生成响应快速复评，缩短调试回路　<sub>（`wzzll123/MultiKernelBench`）</sub>
- reference/ 按 category 提供一份 PyTorch 参考实现服务所有语言后端　<sub>（`wzzll123/MultiKernelBench`）</sub>
- 后端与提示词策略都用装饰器注册（@register_backend / @register_prompt），扩展只需加文件　<sub>（`wzzll123/MultiKernelBench`）</sub>
- validate + prepare 两步前置校验，先确保 test/reference yaml 合法再产出 benchcard　<sub>（`zhang677/PCL-lite`）</sub>
- 实验用 experiment.json 声明 prompt tag、模型、负载与限额，便于复制变体　<sub>（`zhang677/PTXBench`）</sub>
- 提示词集中到 hub.json 共享注册表，render.py --check 做渲染静态校验　<sub>（`zhang677/PTXBench`）</sub>

### 其他工程细节

这些做法没有归入上面任何一类，但同样具体可复用。按项目列出，便于按需查阅。

- 用 BenchmarkAdapter 统一 FlashInfer 与任意仓库两类任务形态　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 编译期校验 layout 兼容性，阻止静默的错误结果　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 用架构加速指令强制要求 90a/100a 等目标架构，避免运行期错误　<sub>（`NVIDIA/cutlass`）</sub>
- 互监督设计：翻译结果与生成的单测互相校验后才进入训练集　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- 复用 LLaMA-Factory 做标准化微调而不是自造训练循环　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- 为每个算子提供独立 op_tests 便于回归与按算子验证　<sub>（`ROCm/aiter`）</sub>
- 发布自动化校验分支/tag 一致性与 wheel 集合完整性，宁可不发也不发半套　<sub>（`ROCm/aiter`）</sub>
- README 明确提示发现异常高加速比时需人工复核　<sub>（`SakanaAI/robust-kbench`）</sub>
- W&amp;B 记录每轮分数、生成代码与世界模型快照　<sub>（`caoshiyi/K-Search`）</sub>
- 以 --api-format 描述协议而非固定 provider，兼容任意兼容端点　<sub>（`flagos-ai/KernelGenBench`）</sub>
- 提供 --single-test 单算子冒烟入口便于快速验证链路　<sub>（`flagos-ai/KernelGenBench`）</sub>
- 区分结构化数据集与源码仓库两类数据资源分别归类　<sub>（`flagos-ai/awesome-LLM-driven-kernel-generation`）</sub>
- 持续接受 PR 补充新工作以跟上快速演进的领域　<sub>（`flagos-ai/awesome-LLM-driven-kernel-generation`）</sub>
- 数据集放 HuggingFace 并用 Git LFS 指针加按需下载，避免巨量张量一次拉取　<sub>（`flashinfer-ai/flashinfer-bench`）</sub>
- 配套文档站与 Slack 协作渠道降低使用门槛　<sub>（`flashinfer-ai/flashinfer-bench`）</sub>
- 用 TRITON_BUILD_WITH_CCACHE 开 ccache 增量编译　<sub>（`hgl71964/cuasmrl`）</sub>
- 用 TRITON_BUILD_WITH_CLANG_LLD 走 clang+lld 加速链接　<sub>（`hgl71964/cuasmrl`）</sub>
- 先跑 smoke 套件做快速自检再跑完整套件，降低试错成本　<sub>（`meta-pytorch/BackendBench`）</sub>
- 性能测试复用 TorchBench/Hugging Face 模型的真实张量形状　<sub>（`meta-pytorch/BackendBench`）</sub>
- CUDA 与 HIP 实现分别从不同 submodule 取，兼顾 NVIDIA 与 AMD 覆盖　<sub>（`meta-pytorch/tritonbench`）</sub>
- 编译器主线与大模型 Agent 副线分仓为独立子项目，各自独立安装构建　<sub>（`mindspore-ai/akg`）</sub>
- 按 GPU 型号分别发布 kernel 与 score，避免跨机型误用　<sub>（`ornith-ai/CUDA-L1`）</sub>
- 移除评测缓存以避免虚假加速结果　<sub>（`ornith-ai/CUDA-L1`）</sub>
- 固定 CUTLASS v4.2.1 并用 CUTLASS_DIR 显式指定路径，避免静默失败　<sub>（`ornith-ai/CUDA-L2`）</sub>
- 按 GPU 型号分别训练与发布 kernel，禁止跨机型直接复用　<sub>（`ornith-ai/CUDA-L2`）</sub>
- 用 TORCH_CUDA_ARCH_LIST 显式指定目标架构（8.0 / 9.0a）编译　<sub>（`ornith-ai/CUDA-L2`）</sub>
- 用 BEGIN/END 标记区块在 README 中插入自动生成内容　<sub>（`qhy991/Awesome-LLM-Kernel-Agent`）</sub>
- 提供 bundle 命令把多个技能组合打包投喂给 agent　<sub>（`tensormux/kernel-skills`）</sub>
- 每个技能必须配 proof/ 下的实测前后证据才被认可　<sub>（`tensormux/kernel-skills`）</sub>
- integration/ 按上游框架分别封装适配器（PyTorch/vLLM/AutoGPTQ/GPTQModel/BitNet）　<sub>（`tile-ai/BitBLAS`）</sub>
- SM120/SM100 等新架构特性各有独立示例与 PR 跟踪　<sub>（`tile-ai/tilelang`）</sub>
- 用 Target 对象统一描述编译目标，auto 目标自动探测 CUDA/HIP/Metal/Ascend　<sub>（`tile-ai/tilelang`）</sub>
- TRITON_REPRODUCER_PATH 在失败 pass 前生成可复现的 MLIR reproducer　<sub>（`triton-lang/triton`）</sub>
- 提供 kernel override 机制逐阶段替换 IR/ptx/amdgcn 做对比实验　<sub>（`triton-lang/triton`）</sub>
- 搜索旋钮集中在 run_search.py（beam_size、num_plan_candidates、num_code_candidates 等）　<sub>（`ucb-bar/autocomp`）</sub>
- 每个任务内嵌 PyTorch 参考实现与输入生成逻辑，保证可复现　<sub>（`weich97/NPUKernelBench`）</sub>
- 为每种语言提供 add_shot/selected_shot 等不同提示词策略做横向对比　<sub>（`wzzll123/MultiKernelBench`）</sub>
- profiling API 以 NKIKernel 类封装，可插接到任意 AI 优化器　<sub>（`zhang677/AccelOpt`）</sub>
- 把生成的 kernel 用 SQL schema 结构化存储，便于检索、复用与跨 bench 迁移　<sub>（`zhang677/AccelOpt`）</sub>
- 计算相对硬件可达峰值的百分比以判断优化空间是否被探索完　<sub>（`zhang677/AccelOpt`）</sub>

## 4. 从零搭建：目录骨架与里程碑

### 4.1 目录骨架

下面是按出现频次排出来的顶层目录。括号内是 61 个项目里采用该目录的数量。这套骨架直接照抄不会错，但**只建需要的**——没有评测就不要建 `benchmarks/`，没有 Agent 就不要建 `agents/`。

| 目录 | 出现数 | 用途 |
| --- | ---: | --- |
| `.github/` | 26 | — |
| `scripts/` | 25 | 可执行脚本入口与数据准备 |
| `docs/` | 25 | 使用文档与设计说明 |
| `tests/` | 14 | 单元测试 |
| `examples/` | 14 | 可运行示例 |
| `src/` | 13 | 核心 Python 包 |
| `assets/` | 11 | 静态资源 |
| `tools/` | 10 | 工具封装（编译、profile、校验） |
| `docker/` | 9 | 容器化的评测环境 |
| `prompts/` | 7 | 提示模板 |
| `utils/` | 7 | 通用工具 |
| `test/` | 7 | 单元测试 |
| `data/` | 7 | 数据集 |
| `.claude/` | 6 | — |
| `agents/` | 5 | Agent 实现与提示 |
| `KernelBench/` | 5 | — |
| `.vscode/` | 5 | — |
| `img/` | 4 | — |
| `benchmark/` | 4 | 评测任务与脚本 |
| `include/` | 4 | — |
| `cmake/` | 4 | — |
| `tasks/` | 3 | 任务定义 |
| `kernels/` | 3 | — |
| `experiments/` | 3 | — |
| `configs/` | 3 | 配置 |
| `bin/` | 3 | — |
| `results/` | 3 | — |
| `python/` | 3 | — |

### 4.2 里程碑

按这个顺序做，每一步都能独立交付一个能用的东西，不会走到一半发现评测跑不通。

| 阶段 | 目标 | 交付物 | 验收方式 |
| --- | --- | --- | --- |
| **M0 任务集** | 定义要优化什么 | 任务定义（目录或 JSON）+ 参考实现 + 正确性判据 | 参考实现自己跑得通，判据能区分正确与错误的实现 |
| **M1 评测闭环** | 有一个能信的口径 | 候选提交入口 + 判定器 + 基线 + 多次运行汇总 | 同一个候选重复跑结果稳定，基线版本被记录 |
| **M2 生成闭环** | 让模型参与进来 | 提示/模型接口 + 编译与执行工具 + 循环控制器 | 至少能产生一个通过正确性判据的候选 |
| **M3 反馈升级** | 让搜索更聪明 | profile 或性能反馈 + 记忆/经验复用 | 在固定预算下比 M2 的随机多试更有效 |
| **M4 训练或交付** | 产出可分发的资产 | 训练脚本 + 权重/数据集，或可部署算子包 | 评测脚本与训练环境共用同一套执行后端 |

### 4.3 常见陷阱

这些不是假想问题，而是这批项目自己写下来、或从其结构里能直接看出来的。

1. **只有编译成功当成功**。编译通过不等于算子正确，必须有参考输出比对；数值算子还要定容差。
2. **单次运行比速度**。GPU 计时波动大，必须多次运行并记录分布，基线与候选必须在同一进程、同一时钟口径下测。
3. **版本漂移**。任务集、基线实现、硬件、驱动版本任一变化都会让历史数字失效。把这些写进结果文件，而不是写进 README 的一段话。
4. **训练评测集泄漏**。合成数据与公开 benchmark 高度重叠时，在 KernelBook 上训练又在 KernelBench 上评测，结论不成立。
5. **环境不固定**。10 个项目提供 `docker/`，说明「Agent 之间的差异」经常被「环境之间的差异」吃掉。
6. **只有 `Profile` 反馈的少数派**。在 59 个有工作关联的开源项目里，只有 13 个声明了 profile 反馈——多数系统的搜索信号仍停留在「编译过 + 跑得通」。

### 4.4 项目自己写下来的限制

这一节直接来自各项目 README 的自述限制，按主题归类。**项目主动写出的限制比读者猜出来的限制更有价值**——它说明作者自己知道边界在哪。

| 限制主题 | 条目数 | 涉及项目数 |
| --- | ---: | ---: |
| 硬件与架构支持边界 | 63 | 41 |
| 环境与依赖门槛 | 49 | 38 |
| 评测可信度 | 7 | 6 |
| 交付不完整 | 15 | 13 |
| 规模与定位受限 | 2 | 2 |

**硬件与架构支持边界**——「支持某张卡」几乎从不等于「支持这一代的全部算子」——检查支持矩阵，不要只看型号。

- 推荐 Linux + NVIDIA GPU；Windows 需自行准备 CUDA 工具链与 Nsight 工具　<sub>（`0satan0/KernelMem`）</sub>
- 频繁编译运行 GPU kernel，需足够显存与超时监控以防 buggy kernel 挂死　<sub>（`0satan0/KernelMem`）</sub>
- 需 Docker 与 AMDGPU 驱动，且必须先在宿主机安装并登录所选 agent CLI　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- hot-patch 不支持系统级 C/C++ 库与单体 _C.so，这类改动需重新编译源码　<sub>（`AMD-AGI/Apex`）</sub>
- 模型级评分需完整 AMD GPU 环境，CPU 只能跑 eval.py 的 mini eval　<sub>（`AMD-AGI/Apex`）</sub>
- codex CLI 尚未支持自然语言启动、需命令行驱动，且须 pin @openai/codex@0.146.1　<sub>（`AMD-AGI/GEAK`）</sub>
- 仅支持 AIE2 与 AIE2P kernel（Phoenix/Hawk 与 Strix/Krackan）　<sub>（`AMDResearch/NPUEval`）</sub>
- 目前只支持单输出 kernel，即 1-in-1-out 与 2-in-1-out　<sub>（`AMDResearch/NPUEval`）</sub>
- 性能 golden 基线按具体 GPU 机器预置，换机器需先跑 run_missing_benchmarks.py　<sub>（`BonnieW05/KernelBenchX`）</sub>
- 需要 PYTHONPATH 指向 data/ 且 GPU 数量通过参数指定　<sub>（`BonnieW05/KernelBenchX`）</sub>
- README 未说明所用 CUDA 工具链版本与 GPU 型号要求　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- RL 阶段每个节点需要 8 张 GPU（4 训练 + 4 奖励计算）　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- 工业代码（RTL、嵌入式固件、GPU kernel）部署前必须经专家人工评审　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- 随附的 SFT 框架较轻量，只支持含 messages 字段的 ChatML JSONL　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- README 未说明生成侧支持的模型清单与采样参数细节　<sub>（`CUDA-Bench/CUDABench`）</sub>
- 生成的 task adapter 目前只能在本地机器运行，目标依赖与所需 GPU 必须本地可用　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 非 Linux/GPU 本机跑 FlashInfer 模式需改用 Modal 后端　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 2.0 起不再支持 Python 包安装，kernel 必须逐个编译　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 主要面向 Hopper 与 Blackwell，不再积极支持 Ampere　<sub>（`HazyResearch/ThunderKittens`）</sub>
- 需要 Docker、NVIDIA GPU、Git LFS 与 HuggingFace 账号（受限模型）　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- Hopper/Blackwell 架构加速指令无前向兼容，必须用 sm_90a/sm_100a 目标编译　<sub>（`NVIDIA/cutlass`）</sub>
- 最低要求 Volta (compute capability 7.0)、C++17 与 CUDA 11.4，推荐 CUDA 12.8　<sub>（`NVIDIA/cutlass`）</sub>
- ncu 需要 sudo/root 才能访问 GPU 性能计数器　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- README 未说明支持的编程语言与目标后端范围　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- AMD MI300X 上多轮 RL 训练两步内节点崩溃（CPU 打满），暂以单轮训练替代　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- 需要指定 Docker 镜像与较大显存（H100 80G 或 MI300X 192G）　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- RDNA 架构仅实验性支持：多数 CK 与 ASM kernel 仅限 CDNA　<sub>（`ROCm/aiter`）</sub>
- 需要 NVIDIA GPU（已在 H100/A100/RTX 4090 上验证）、Python 3.10+ 与 uv　<sub>（`RightNow-AI/autokernel`）</sub>
- ThunderKittens 后端目前仅支持 BF16，且需手动 clone 并设 THUNDERKITTENS_ROOT　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- step 时间受 Modal 并发 GPU 容器数量限制　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- Ampere 仅支持部分 kernel，Hopper/Blackwell 为测试主力　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- README 未给出各架构的算子数量与误差容忍细节　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- 需 Python 3.10+、CUDA 12+ 与较新的 NVIDIA GPU　<sub>（`Snowflake-AI-Research/fastkernels`）</sub>
- TGI 无法忽略 EOS 结束符，故只支持质量参考不支持速度基线　<sub>（`aisa-group/InferenceBench`）</sub>
- 需 H100 80GB 或 A100（用 _a100 镜像）及共享存储　<sub>（`aisa-group/InferenceBench`）</sub>
- GPU 型号/架构与软件运行时必须一致，否则不能合并分片　<sub>（`alibaba/atrex-bench`）</sub>
- 面向算力受限、显存充裕的集群（如 XPU-A、H20）　<sub>（`alibaba/atrex-bench`）</sub>
- GPU 推荐 H100/B200；MLX 后端仅适用于 Apple Silicon　<sub>（`caoshiyi/K-Search`）</sub>
- 评测依赖本地多卡 GPU（示例用 8 卡）与上游 KernelBench 题库　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- README 未列出多后端对应的具体芯片清单　<sub>（`flagos-ai/FlagGems`）</sub>
- README 只列芯片厂商，未说明具体型号与版本要求　<sub>（`flagos-ai/KernelGenBench`）</sub>
- AMD GPU 与 CPU 支持仍在开发中；cuasmrl 需手动 clone CuAssembler 并设置 PYTHONPATH　<sub>（`hgl71964/cuasmrl`）</sub>
- 仅支持 Linux 平台　<sub>（`hgl71964/cuasmrl`）</sub>
- 要求 NVIDIA GPU 计算能力 7.0 及以上　<sub>（`hgl71964/cuasmrl`）</sub>
- 大规模训练需要多 GPU/多节点横向扩展才能承接上千样本批次　<sub>（`hkust-nlp/KernelGYM`）</sub>
- 目前成熟的任务类型是 kernel 生成，其他 GPU 任务需自行实现抽象　<sub>（`hkust-nlp/KernelGYM`）</sub>
- Intel XPU 为附加支持路径，需兼容 GPU 与 Linux 驱动　<sub>（`meta-pytorch/KernelAgent`）</sub>
- AKG-AGENT 当前仅支持生成 Triton-Ascend 与 SWFT(300I DUO) 的 DSL　<sub>（`mindspore-ai/akg`）</sub>
- 5090/4090 支持仍在 to-do 列表中　<sub>（`ornith-ai/CUDA-L1`）</sub>
- A100 上训练的 kernel 只保证在 A100 上有加速　<sub>（`ornith-ai/CUDA-L2`）</sub>
- 矩阵维度不在配置中需取最近邻补零；尚未覆盖更密集配置与更多 GPU 架构　<sub>（`ornith-ai/CUDA-L2`）</sub>
- 测试 CUDA/HIP 题目需 NVIDIA 与 AMD GPU 及各自软件栈　<sub>（`parallelcodefoundry/ParEval`）</sub>
- 需要 Python 3.7+、支持 C++17 与 OpenMP 的编译器、Make、CMake 与 MPI 实现　<sub>（`parallelcodefoundry/ParEval`）</sub>
- FP16×FP8 等组合要求 SM80 以上平台（V100 不支持）　<sub>（`tile-ai/BitBLAS`）</sub>
- wheel 仅支持 Ubuntu 20.04+、CUDA&gt;=11.0、Python&gt;=3.8，其他环境需源码编译　<sub>（`tile-ai/BitBLAS`）</sub>
- TMA/WGMMA/TMEM 等特性依赖对应 GPU 架构，不支持的形状需回退路径　<sub>（`tile-ai/tilelang`）</sub>
- NVIDIA GPU 需 Compute Capability 8.0+，AMD 需 ROCm 6.2+，CPU 后端仍在开发　<sub>（`triton-lang/triton`）</sub>
- 仅支持 Linux　<sub>（`triton-lang/triton`）</sub>
- Apple Metal 与 TPU 支持为较新加入，成熟度与覆盖度不及 Trainium/CUDA　<sub>（`ucb-bar/autocomp`）</sub>
- search_strategy 目前只支持 beam 一种　<sub>（`ucb-bar/autocomp`）</sub>
- MUSA 后端为初步支持（initial），AscendC 直启与 TileLang 后端为近期新增　<sub>（`wzzll123/MultiKernelBench`）</sub>
- README 只给脚本流程，未展开架构、评分口径与反馈细节　<sub>（`zhang677/PCL-lite`）</sub>
- 需 Python 3.12、Docker、tmux 与 H100 主机；SFT 导出还需 host nvcc、cuobjdump 与 TVM-FFI　<sub>（`zhang677/PTXBench`）</sub>

**环境与依赖门槛**——「一条命令跑起来」是稀缺品。上手成本高意味着复现率低，也意味着结论更难被独立检验。

- README 未描述目标硬件与所需 Triton/CUDA 版本　<sub>（`AI9Stars/AutoTriton`）</sub>
- 不含 RL trainer、replay buffer 与策略更新回路，只提供环境与奖励信号　<sub>（`AMD-AGI/AgentKernelArena`）</sub>
- 不捆绑任何 AI 模型或 API，需自行安装并登录 Claude Code/Codex/Cursor　<sub>（`AMD-AGI/Apex`）</sub>
- RDNA4 的 PMC 可能稀疏，只能依赖 kernel trace 计数　<sub>（`AMD-AGI/GEAK`）</sub>
- gfx1201 是共享 ISA，本身不决定 R9700 镜像、标定峰值与服务策略　<sub>（`AMD-AGI/GEAK`）</sub>
- 不安装 kernel 所需工具链（PyTorch/Triton/FlyDSL/hipBLASLt），需自行准备并验证基线可跑　<sub>（`AMD-AGI/GEAK`）</sub>
- 需自行提供初始 CUDA .cu 文件与基线函数名　<sub>（`Anjiang-Wei/Astra`）</sub>
- 需手动克隆指定 SHA 的 verl 并 --no-deps 安装　<sub>（`ByteDance-Seed/cudaLLM`）</sub>
- 必须预装 CUDA Toolkit (nvcc) 与 NVIDIA Nsight Compute (ncu)　<sub>（`CUDA-Bench/CUDABench`）</sub>
- 需要 Python 3.11+、uv、omp 以及模型 provider 就绪　<sub>（`Dogacel/auto-gpu-kernel`）</sub>
- 要求 CUDA 12.8+ 与 C++20（gcc-11+ / clang-11）　<sub>（`HazyResearch/ThunderKittens`）</sub>
- analysis-data 与 vllm-lm-eval 需另行 clone 才能启用软指标与 lm-eval 校验　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- r2e 包从 GitHub 安装，uv sync 失败会导致 PerfCommitAnalyzer 模块缺失　<sub>（`ISO-Bench/ISO-Bench`）</sub>
- cutlass 与 cute-dsl 分组依赖锁定镜像，--mode=local 需自行复现该工具链栈　<sub>（`NVIDIA/compute-eval`）</sub>
- 已知 CTK bug 导致部分 packed 指令在 sm107 生成错误代码，需手动规避　<sub>（`NVIDIA/cutlass`）</sub>
- 部分 conda 依赖无法自动安装，需手动补装　<sub>（`OptimAI-Lab/CudaForge`）</sub>
- 微调依赖外部 LLaMA-Factory 仓库，需自行 clone 并注册数据集　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- AMD 侧需手动补装 pydra_config 等依赖并做软链处理　<sub>（`RLsys-Foundation/TritonForge`）</sub>
- FlyDSL 是必需依赖；部分包安装可能失败需手动处理　<sub>（`ROCm/aiter`）</sub>
- 需先执行 install_triton.sh 或设置 AITER_USE_SYSTEM_TRITON 才能安装　<sub>（`ROCm/aiter`）</sub>
- Triton 通常只能达到 cuBLAS 的 80-95%，极致性能需改用 CUDA C++　<sub>（`RightNow-AI/autokernel`）</sub>
- 依赖 conda 环境与 cu124 版 PyTorch，ncu/clang 剖析需额外开关　<sub>（`SakanaAI/robust-kbench`）</sub>
- ROCm 需 &gt;=7.1，README 建议用 docker 镜像规避环境复杂度　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- 基线时间受集群功耗与软件版本影响，README 建议自行生成基线　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- 生成的 kernel 可能触发 CUDA illegal memory access 导致崩溃　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- 自述为论文的简化开源版本，非完整系统复现　<sub>（`StigLidu/AdaExplore`）</sub>
- 提交脚本默认依赖 HTCondor，换调度器需改 .sub 文件　<sub>（`aisa-group/InferenceBench`）</sub>
- 需要 Linux、Bash、Python 3.10+、Apptainer 与 fakeroot 网络访问　<sub>（`aisa-group/InferenceBench`）</sub>
- 需要 conda 环境、requirements.txt 与各 provider 的 API key　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- 依赖 Python 3.10+、CUDA 11.8+、Redis 服务，官方推荐 Linux (Ubuntu 20.04+)　<sub>（`hkust-nlp/KernelGYM`）</sub>
- Triton 需自行安装并锁版本以匹配驱动与工具链　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 要求 Python 3.8–3.12，Linux 或 macOS　<sub>（`meta-pytorch/KernelAgent`）</sub>
- 默认安装 PyTorch nightly 并使用其自带的 Triton 版本　<sub>（`meta-pytorch/tritonbench`）</sub>
- 各子项目需分别按其文档独立安装构建　<sub>（`mindspore-ai/akg`）</sub>
- 必须使用 CUTLASS v4.2.1，版本或路径错误会静默失败或无结果　<sub>（`ornith-ai/CUDA-L2`）</sub>
- Kokkos 需手动 cmake 编译安装后才纳入测试　<sub>（`parallelcodefoundry/ParEval`）</sub>
- 最近一次更新为 2026 年 8 月，时效性依赖人工维护　<sub>（`qhy991/Awesome-LLM-Kernel-Agent`）</sub>
- CUDA 12.8 及以上需额外重装 cu128 版 torch　<sub>（`taratt/cutegen`）</sub>
- 需手动安装 NCU 与 CUTLASS，并正确设置 NSIGHT_COMPUTE_BIN、CUTLASS_BASE_PATH、CUDACXX　<sub>（`taratt/cutegen`）</sub>
- 需固定 triton 3.1.0 与 torch&gt;=2.5.1，并手动修改 eval_G/eval_T 中的 py_interpreter 路径　<sub>（`thunlp/TritonBench`）</sub>
- Ascend 950 后端需 USE_ASCEND=ON 源码编译，依赖 CANN 与 torch_npu　<sub>（`tile-ai/tilelang`）</sub>
- ROCm 路径需宿主安装 ROCm 运行时，CI 仅覆盖 gfx942，gfx950 尚未覆盖　<sub>（`tile-ai/tilelang`）</sub>
- LLVM 无稳定 API，不能用任意 LLVM 版本构建　<sub>（`triton-lang/triton`）</sub>
- 没有一键跑完所有测试的 turnkey 方式，需按 make 配方手动执行　<sub>（`triton-lang/triton`）</sub>
- 需按平台分别安装 torch-npu / torch xpu / torch_musa 运行环境　<sub>（`wzzll123/MultiKernelBench`）</sub>
- Trainium 路径依赖 AWS Neuron Deep Learning AMI 与 trn1.32xlarge 实例　<sub>（`zhang677/AccelOpt`）</sub>
- 需要 logfire 与 openai-agents 依赖，模型多以本地服务方式接入　<sub>（`zhang677/AccelOpt`）</sub>
- PCL-lite 针对的是 STeP 的早期版本，最新版需参考新论文　<sub>（`zhang677/PCL-lite`）</sub>
- SFT 依赖 Tinker 账号与 Tinker Cookbook　<sub>（`zhang677/PTXBench`）</sub>

**评测可信度**——项目自己写出这类告警的，通常是发现了真实问题——这类告警值得优先读。

- 模型可能生成错误或不安全的代码，需在沙箱中测试并由专家复核　<sub>（`CSJianYang/Industrial-Coder`）</sub>
- 大量小 kernel 的提交对 CPU 启动调度敏感，方差可达 10%　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- 官方评测跑在 B200 且 SM 锁 1500MHz，CPU 差异导致约 5% 运行间方差　<sub>（`NVIDIA/SOL-ExecBench`）</sub>
- README 提醒 LLM 可能以未知方式 reward-hacking，强加速比需人工复核　<sub>（`RightNow-AI/autokernel`）</sub>
- LLM 仍可能以未知方式 reward-hacking，出现强加速比需人工复核　<sub>（`SakanaAI/robust-kbench`）</sub>
- RL 训练对 reward hacking 敏感，已发现利用计时测量与缓存结果的作弊　<sub>（`ornith-ai/CUDA-L1`）</sub>
- 数值容差默认绝对与相对误差均为 1e-3，除非任务自定义 checker　<sub>（`weich97/NPUKernelBench`）</sub>

**交付不完整**——README 明确说「训练流程未发布」的项目，只能用来理解设计，不能用来复现结果。

- 仓库仅含模型权重与引用说明，未提供训练代码、推理脚本或数据　<sub>（`AI9Stars/AutoTriton`）</sub>
- cpt/sft/rl 阶段代码尚未全部加入，代码所有权目前只能按仓库级维护　<sub>（`AMD-AGI/AMDKernelVault`）</sub>
- 数据集许可仅允许用于评测与基准，禁止用于训练 AI 模型　<sub>（`NVIDIA/compute-eval`）</sub>
- 仓库仍在积极开发中　<sub>（`QiMeng-IPRC/QiMeng-Kernel`）</sub>
- 训练流程与离线数据集尚未发布　<sub>（`QiMeng-IPRC/QiMeng-Kernel`）</sub>
- 仓库仍在开发，端到端训练与评测代码尚未发布　<sub>（`QiMeng-IPRC/QiMeng-MuPa`）</sub>
- 自述不提供复杂 agentic scaffold，仅是核心功能与评测脚本　<sub>（`ScalingIntelligence/KernelBench`）</sub>
- 自述为 minimal integration，不含新的 RL 技术，仅是可用性基线　<sub>（`ScalingIntelligence/kernelbench-tinker`）</sub>
- 仅提供 SFT 与 PPO 的最小流水线，非完整论文复现　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- 预训练与 SFT 数据集尚未发布，计划在『齐物』项目下释出　<sub>（`Wangyaoyuu/SparseRL`）</sub>
- 状态标注为 early stage，当前仅 30 个算子　<sub>（`alibaba/atrex-bench`）</sub>
- Verified 口径下 GPT-5.5 几何平均加速比仅 0.88×，说明标准口径高估　<sub>（`facebookresearch/kernel_bench_verified`）</sub>
- C++ Triton 函数分发器仍在开发中（WIP）　<sub>（`flagos-ai/FlagGems`）</sub>
- 仓库仍在建设中（under construction），未包含完整实验矩阵　<sub>（`zhang677/AccelOpt`）</sub>
- 仓库仍在建设中，不含论文结果、绘图或完整实验矩阵　<sub>（`zhang677/PTXBench`）</sub>

**规模与定位受限**——任务集规模小意味着结论的适用范围也小。引用时要把任务集规模一并带上。

- 任务集规模有限，主要是十余个基础算子与网络块任务　<sub>（`SakanaAI/robust-kbench`）</sub>
- 只有部分算子经过手工性能优化　<sub>（`flagos-ai/FlagGems`）</sub>

## 5. 反馈信号漏斗

从 landscape 关联的工作字段统计 59 个有开源仓库的工作，它们声明的反馈信号分布如下。这张表说明**当前开源系统的反馈强度**。

| 反馈信号 | 项目数 | 占比 |
| --- | ---: | ---: |
| Correctness | 49 | 83% |
| Runtime | 48 | 81% |
| Compile | 40 | 68% |
| Profile | 13 | 22% |

正确性（49）和运行时（48）几乎是标配，编译（40）稍低，而真正指导优化的 profile（13）只有四分之一左右。这解释了为什么大多数开源系统的提升主要来自「多试几次」而不是「知道该改哪里」。

### 基准复用

同一份任务集被反复复用，是这个领域可比性的来源，也是它的问题来源。

| 基准 | 被多少个项目使用 | 使用者 |
| --- | ---: | --- |
| KernelBench | 18 | `0satan0/KernelMem`、`AI9Stars/AutoTriton`、`ByteDance-Seed/cudaLLM`、`BytedTsinghua-SIA/CUDA-Agent`、`OptimAI-Lab/CudaForge`、`QiMeng-IPRC/QiMeng-Kernel`、`RLsys-Foundation/TritonForge`、`RightNow-AI/autokernel`、`ScalingIntelligence/KernelBench`、`ScalingIntelligence/kernelbench-tinker`、`StigLidu/AdaExplore`、`caoshiyi/K-Search`、`facebookresearch/kernel_bench_verified`、`hkust-nlp/KernelGYM`、`meta-pytorch/KernelAgent`、`mindspore-ai/akg`、`ornith-ai/CUDA-L1`、`taratt/cutegen` |
| FlashInfer-Bench | 4 | `Dogacel/auto-gpu-kernel`、`caoshiyi/K-Search`、`flashinfer-ai/flashinfer-bench`、`zhang677/AccelOpt` |
| TritonBench | 4 | `AI9Stars/AutoTriton`、`AMD-AGI/AMDKernelVault`、`QiMeng-IPRC/QiMeng-Kernel`、`thunlp/TritonBench` |
| AgentKernelArena | 1 | `AMD-AGI/AgentKernelArena` |
| GEAK-eval | 1 | `AMD-AGI/GEAK` |
| NKIBench | 1 | `zhang677/AccelOpt` |
| InferenceBench | 1 | `aisa-group/InferenceBench` |
| Atrex-Bench | 1 | `alibaba/atrex-bench` |
| NPUEval | 1 | `AMDResearch/NPUEval` |
| KernelBenchX | 1 | `BonnieW05/KernelBenchX` |
| CUDABench | 1 | `CUDA-Bench/CUDABench` |
| KernelGenBench | 1 | `flagos-ai/KernelGenBench` |

KernelBench 被 18 个项目用作评测基准，是事实上的公共任务集。好处是可比，代价是**一个基准上的改进很容易被当成普适能力**——尤其是当生成系统的训练数据也来自同一来源时。

## 6. 证据边界

- 本文的工程结论基于 README、目录结构与 API 元数据，**未做源码审计**。
- 「某项目具备某能力」指的是**公开材料声明具备**，不代表已验证可用。
- 频次统计反映的是**当前收录的 61 个项目**，不代表领域整体分布——收录本身就有偏（GitHub 可见、英文 README、公开许可）。
- 具体的性能、加速比、成功率数字**一律不引用**，因为本仓没有复现它们。
