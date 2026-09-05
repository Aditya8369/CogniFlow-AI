from src.core.llm_client import LLMClient

class SocraticTutor:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def get_scaffolding_response(self, topic: str, gaps: list[str], conversation_history: list[dict]) -> str:
        system_instruction = (
            "You are Socrates incarnated as a master educator. Never give the direct answer right away. "
            "Use targeted counter-examples, thought experiments, or guided questions to lead the user "
            "to bridge their own knowledge gaps. Keep questions concise and engaging."
        )

        history_str = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in conversation_history[-5:]])
        gaps_str = "\n".join([f"- {g}" for g in gaps]) if gaps else "None detected. Deepen mastery."

        prompt = f"""
        Current Topic: {topic}
        Known Misconceptions/Gaps:
        {gaps_str}

        Conversation History:
        {history_str}

        Craft the next response:
        1. Validate any partially correct intuition.
        2. Pose ONE specific, thought-provoking scenario or counter-question to help them resolve their gap.
        """
        return self.llm.generate(prompt, system_instruction=system_instruction)