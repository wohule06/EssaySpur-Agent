from typing import Optional
# 导入项目核心模块
from Memory封装 import Memory
from llm_client import EssayLLMClient
# 导入三段式作文Prompt模板
from prompt import (
    INITIAL_PROMPT_TEMPLATE,
    REFLECT_PROMPT_TEMPLATE,
    REFINE_PROMPT_TEMPLATE
)


class ReflectionAgent:
    def __init__(self, llm_client, max_iterations: int = 3):
        """
        作文迭代鞭策智能体初始化
        :param llm_client: LLM通用调用客户端
        :param max_iterations: 最大迭代优化轮次
        """
        self.llm_client = llm_client
        self.memory = Memory()
        self.max_iterations = max_iterations

    def run(self, task: str) -> Optional[str]:
        """
        启动作文生成-反思鞭策-迭代优化完整流程
        :param task: 作文写作任务（题目+字数+文体要求）
        :return: 迭代完成后的最终作文
        """
        print(f"\n📌 开始执行作文任务")
        print(f"任务详情: {task}")

        # ========== 1. 初始执行：生成作文初稿 ==========
        print("\n✨ 正在生成作文初稿...")
        initial_prompt = INITIAL_PROMPT_TEMPLATE.format(task=task)
        initial_essay = self._get_llm_response(initial_prompt, temperature=0.7)

        # 容错：初始生成失败直接终止
        if not initial_essay:
            print("❌ 作文初稿生成失败，任务终止！")
            return None

        self.memory.add_record("execution", initial_essay)

        # ========== 2. 循环迭代：反思鞭策 + 作文优化 ==========
        for i in range(self.max_iterations):
            print(f"\n🔄 进入第 {i+1}/{self.max_iterations} 轮迭代优化")

            # a. 获取最新作文内容
            last_essay = self.memory.get_last_execution()
            if not last_essay:
                print("❌ 未查询到历史作文记录，终止迭代！")
                break

            # b. 反思鞭策：生成作文优化反馈
            print("\n🧐 正在对作文进行评审鞭策...")
            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(
                task=task,
                last_essay_attempt=last_essay
            )
            feedback = self._get_llm_response(reflect_prompt, temperature=0.2)

            if not feedback:
                print("❌ 反思评审失败，跳过本轮迭代！")
                continue

            self.memory.add_record("reflection", feedback)

            # c. 终止条件：作文无需优化，提前结束迭代
            if "无需优化" in feedback:
                print("\n✅ 作文已达到优质标准，无需继续优化，迭代提前终止！")
                break

            # d. 根据反馈优化重写作文
            print("\n✍️ 正在根据鞭策反馈优化作文...")
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(
                task=task,
                last_essay_attempt=last_essay,
                feedback=feedback
            )
            refined_essay = self._get_llm_response(refine_prompt, temperature=0.6)

            if not refined_essay:
                print("❌ 作文优化失败，保留上一版本内容！")
                continue

            self.memory.add_record("execution", refined_essay)

        # ========== 3. 输出最终作文结果 ==========
        final_essay = self.memory.get_last_execution()
        print(f"\n🎉 作文迭代任务全部完成！")
        print(f"\n📝 最终优化版作文：\n{final_essay}")

        return final_essay

    def _get_llm_response(self, prompt: str, temperature: float) -> str:
        """
        通用LLM调用辅助方法，统一处理请求、容错、温度参数
        :param prompt: 拼装完成的提示词
        :param temperature: 模型温度
        :return: LLM完整响应文本
        """
        messages = [{"role": "user", "content": prompt}]
        # 空值兜底，避免程序报错
        response_text = self.llm_client.chat(messages=messages, temperature=temperature) or ""
        return response_text


# 项目入口测试
if __name__ == '__main__':
    try:
        # 初始化作文专用LLM客户端
        llm_client = EssayLLMClient()
    except Exception as e:
        print(f"❌ LLM客户端初始化失败: {e}")
        exit()

    # 初始化作文鞭策智能体，默认最大迭代3轮
    agent = ReflectionAgent(llm_client=llm_client, max_iterations=3)

    # 测试作文任务（可自行修改）
    essay_task = "请以《难忘的一件事》为题，写一篇1000字左右的高中记叙文，立意积极，细节丰富，语句通顺。"
    agent.run(essay_task)