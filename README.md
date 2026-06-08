# EssaySpur-Agent
本项目是一款基于大模型的作文自省迭代智能体，专为中小学作文写作优化设计。区别于普通的 AI 作文生成器，本项目采用 ReAct 执行 + Reflection 反思鞭策 双循环架构，模拟学生「写作→自查问题→自我鞭策→迭代重写」的真实学习闭环。

# EssaySpur-Agent：作文自我鞭策迭代智能体 ✍️🤖

基于 **ReAct+Reflection 架构** 的 AI 作文自我鞭策迭代智能体，全自动完成「作文生成 → 反思评审 → 鞭策优化 → 多轮迭代」全流程，模拟学生写作学习闭环，助力作文水平持续提升。

---

## 📁 项目结构
```
作文鞭策AGENT/
├── .env                  # 环境变量配置（API Key、模型地址、超时等）
├── llm_client.py         # 通用 LLM 客户端，兼容 OpenAI 接口，支持流式输出
├── Memory封装.py         # 记忆模块，持久化存储作文执行与反思轨迹
├── prompt.py             # 三段式 Prompt 模板（初始写作/反思鞭策/迭代优化）
└── Reflection.py          # 核心 ReflectionAgent，驱动作文迭代闭环
```

---

## 🎯 核心架构
本项目采用「记忆 + LLM 调用 + Prompt 工程 + 智能体循环」四层解耦设计：

| 模块               | 职责                                                                 |
|--------------------|----------------------------------------------------------------------|
| **Memory 记忆模块** | 存储每一轮「作文执行记录（execution）」和「反思鞭策反馈（reflection）」，提供完整轨迹上下文 |
| **LLM 客户端**     | 封装 OpenAI 兼容接口，统一管理模型调用、流式输出、异常容错             |
| **Prompt 模板**    | 三段式专业化 Prompt：<br>1. 初始作文生成 Prompt<br>2. 作文反思鞭策 Prompt<br>3. 迭代优化重写 Prompt |
| **ReflectionAgent**| 核心智能体，自动循环：<br>`初稿生成 → 评审鞭策 → 优化重写`，支持自定义最大迭代轮数 |

---

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install openai python-dotenv typing
```

### 2. 配置环境变量（.env）
在项目根目录创建 `.env` 文件，填入你的大模型配置：
```env
# 大模型配置
LLM_MODEL_ID=你的模型名称（如 qwen-plus）
LLM_API_KEY=你的 API Key
LLM_BASE_URL=https://你的模型接口地址/v1
LLM_TIMEOUT=120  # 超时时间（秒）
```

### 3. 运行作文迭代智能体
直接运行 `Reflection.py`，或在其中修改作文任务：
```python
# 在 Reflection.py 的 __main__ 部分修改作文任务
essay_task = "请以《难忘的一件事》为题，写一篇600字左右的初中记叙文，立意积极，细节丰富，语句通顺。"
agent.run(essay_task)
```

启动后，智能体会自动完成：
1. 生成作文初稿
2. 对初稿进行严格评审鞭策
3. 根据反馈优化重写作文
4. 重复迭代直到达到最优或达到最大轮数

---

## 📄 文件说明

| 文件               | 作用                                                                 |
|--------------------|----------------------------------------------------------------------|
| `.env`             | 存储敏感配置（API Key、模型地址等），**请勿上传至代码仓库**           |
| `llm_client.py`    | 提供 `EssayLLMClient` 类，统一封装大模型调用，支持流式输出和异常处理 |
| `Memory封装.py`    | 提供 `Memory` 类，管理作文迭代轨迹，支持添加记录、获取完整轨迹、查询最新作文 |
| `prompt.py`        | 定义三段式 Prompt 模板：<br>`INITIAL_PROMPT_TEMPLATE`（初始作文）<br>`REFLECT_PROMPT_TEMPLATE`（反思鞭策）<br>`REFINE_PROMPT_TEMPLATE`（迭代优化） |
| `Reflection.py`    | 提供 `ReflectionAgent` 类，是项目核心入口，驱动完整作文迭代流程       |

---

## 💡 使用示例

### 运行完整迭代流程
```python
from Reflection import ReflectionAgent
from llm_client import EssayLLMClient

# 初始化 LLM 客户端
llm_client = EssayLLMClient()

# 初始化智能体（最多迭代 3 轮）
agent = ReflectionAgent(llm_client=llm_client, max_iterations=3)

# 定义作文任务
task = "请以《我的校园生活》为题，写一篇500字左右的初中记叙文，内容真实，情感真挚。"

# 启动迭代
final_essay = agent.run(task)
```

### 输出效果
智能体会在控制台实时打印：
- 作文初稿生成过程（流式输出）
- 反思鞭策评审内容
- 优化后作文重写过程
- 最终迭代完成的优质作文

---

## ⚠️ 注意事项
1. **环境变量安全**：`.env` 文件包含敏感信息，**务必添加到 `.gitignore`**，不要上传至公开仓库。
2. **迭代轮数**：默认最大迭代 3 轮，可通过 `max_iterations` 参数调整，轮数越多作文质量越高但耗时越长。
3. **温度参数**：
   - 初稿生成：`temperature=0.7`（保证创意性）
   - 反思鞭策：`temperature=0.2`（保证客观性）
   - 优化重写：`temperature=0.6`（平衡创意与严谨）
4. **异常处理**：若某轮调用失败，智能体会自动跳过该轮并保留上一版本内容，不会导致程序崩溃。

---

## 📌 项目亮点
✅ **自我鞭策机制**：不只是生成作文，而是主动找短板、提问题、给可落地优化建议  
✅ **完整记忆轨迹**：留存每一轮写作+反思全过程，可追溯、可复盘学习  
✅ **高度解耦设计**：模块职责清晰，易于扩展新功能（如新增作文润色、续写等场景）  
✅ **工业级健壮性**：完善的异常容错机制，空响应拦截、迭代熔断，运行稳定可靠  

---

## 🤝 贡献
欢迎提交 Issue 或 PR 一起完善项目！

---

## 📄 许可证
MIT License

记得在主目录下配置好如下图的.env文件
<img width="950" height="269" alt="image" src="https://github.com/user-attachments/assets/31fd3cfa-8be3-4da6-9ce3-7e2d882a5afb" />
<img width="1753" height="516" alt="image" src="https://github.com/user-attachments/assets/848993c5-155b-486f-93d6-44186221a3af" />
<img width="1750" height="418" alt="image" src="https://github.com/user-attachments/assets/934fa68d-8119-4ef2-9a78-d63749863b83" />

