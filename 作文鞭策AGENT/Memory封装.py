from typing import List, Dict, Any
from llm_client import EssayLLMClient

# --- 模块 1: 记忆模块 ---
class Memory:
    """
    作文鞭策Agent - 短期记忆模块
    用于存储智能体的【作文生成执行】与【反思鞭策】完整轨迹
    """
    def __init__(self):
        # 初始化空列表，存储所有记录（execution=作文生成，reflection=作文鞭策）
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str):
        """
        向记忆中添加一条新记录。

        参数:
        - record_type (str): 记录的类型 ('execution' 或 'reflection')。
        - content (str): 记录的具体内容 (生成的作文 或 反思鞭策的反馈)。
        """
        self.records.append({"type": record_type, "content": content})
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """
        将所有记忆记录格式化为连贯文本，用于构建Agent提示词上下文
        （作文尝试 + 鞭策反馈 完整轨迹）
        """
        trajectory = ""
        for record in self.records:
            if record['type'] == 'execution':
                # 适配作文场景：替换原代码文案
                trajectory += f"--- 上一轮作文尝试 ---\n{record['content']}\n\n"
            elif record['type'] == 'reflection':
                # 适配作文场景：替换原评审反馈文案
                trajectory += f"--- 作文反思与鞭策 ---\n{record['content']}\n\n"
        return trajectory.strip()

    def get_last_execution(self) -> str:
        """
        获取最近一次的执行结果（最新生成的作文内容）
        """
        for record in reversed(self.records):
            if record['type'] == 'execution':
                return record['content']
        return None