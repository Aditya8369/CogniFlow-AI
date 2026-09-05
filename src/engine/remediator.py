from src.core.llm_client import LLMClient

class ConceptRemediator:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_micro_lesson(self, topic: str, gaps: list[str]) -> str:
        gaps_text = "\n".join([f"- {g}" for g in gaps]) if gaps else "General intuition"
        prompt = f"""
        Topic: {topic}
        Identified Conceptual Gaps:
        {gaps_text}

        Create a concise 60-second targeted micro-lesson that repairs these exact gaps.
        Format your response in Markdown with:
        1. **The Core Intuition** (A relatable, real-world everyday analogy)
        2. **First-Principles Breakdown** (What is physically/mathematically happening under the hood)
        3. **The 'Aha!' Moment** (Why the common mistake happens and how to avoid it)
        Keep it clear, engaging, and under 250 words.
        """
        return self.llm.generate(prompt)