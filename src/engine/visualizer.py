from src.core.llm_client import LLMClient

class ConceptVisualizer:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_flowchart(self, topic: str, explanation: str) -> str:
        prompt = f"""
        Create a clean Mermaid.js flowchart (graph TD) illustrating the cause-effect or conceptual structure
        of: '{topic}'.
        Based on: {explanation}

        Only output raw mermaid code starting with 'graph TD'. Do not wrap in backticks or markdown fences.
        Keep node labels short (under 6 words).
        """
        raw = self.llm.generate(prompt)
        cleaned = raw.replace("```mermaid", "").replace("```", "").strip()
        return cleaned