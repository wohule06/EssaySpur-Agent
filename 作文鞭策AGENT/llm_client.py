import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

class EssayLLMClient:
    """
    作文Agent 通用LLM客户端
    兼容标准OpenAI接口，默认流式输出
    对外仅提供统一对话接口，执行(写作文)、反思(鞭策批改)由上层业务/Reflection模块组装Prompt
    """

    def __init__(
            self,
            model: Optional[str] = None,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None,
            timeout: Optional[int] = None
    ):
        # 配置优先级：传入参数 > 环境变量
        self.model = model or os.getenv("LLM_MODEL_ID")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")

        # 超时时间，默认120秒，做类型容错
        env_timeout = os.getenv("LLM_TIMEOUT", "120")
        self.timeout = timeout or int(env_timeout)

        # 校验必填配置
        self._check_config()

        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout
        )

    def _check_config(self) -> None:
        """私有方法：校验关键配置是否齐全"""
        missing_fields = []
        if not self.model:
            missing_fields.append("LLM_MODEL_ID")
        if not self.api_key:
            missing_fields.append("LLM_API_KEY")
        if not self.base_url:
            missing_fields.append("LLM_BASE_URL")

        if missing_fields:
            raise ValueError(f"缺少必要配置项，请检查 .env 文件：{', '.join(missing_fields)}")

    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        通用对话入口（统一调用LLM）
        :param messages: 对话上下文列表，遵循OpenAI消息格式
        :param temperature: 温度系数，控制随机性
            - 作文生成(execution): 0.6 ~ 0.8
            - 反思/批改(reflection): 0.1 ~ 0.3 (偏客观严谨)
        :return: 模型完整返回文本，调用失败返回空字符串
        """
        print(f"\n🤖 调用模型 {self.model} ...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True  # 保持流式实时输出
            )

            content_buffer = []
            print("📝 模型流式输出：")
            for chunk in response:
                delta_content = chunk.choices[0].delta.content or ""
                print(delta_content, end="", flush=True)
                content_buffer.append(delta_content)

            # 换行分隔输出
            print()
            full_content = "".join(content_buffer).strip()
            return full_content

        except Exception as e:
            print(f"\n❌ LLM 调用异常：{str(e)}")
            return ""

# 本地测试入口
if __name__ == "__main__":
    try:
        llm = EssayLLMClient()

        # 示例1：执行环节(execution) —— 生成作文
        print("===== 【执行环节】生成作文 =====")
        essay_prompt = [
            {"role": "system", "content": "你是专业语文老师，根据题目完成一篇600字左右记叙文，行文流畅、立意积极。"},
            {"role": "user", "content": "作文题目：难忘的一件事"}
        ]
        essay_result = llm.chat(essay_prompt, temperature=0.7)

    except ValueError as e:
        print(f"客户端初始化失败：{e}")

