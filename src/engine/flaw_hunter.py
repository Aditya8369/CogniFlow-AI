from src.core.llm_client import LLMClient

class ReverseTuringHunter:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_flawed_concept(self, topic: str) -> dict:
        prompt = f"""
        Topic: {topic}

        Write an explanation of this topic that is 90% convincing and technically accurate, 
        but contains ONE critical, subtle misconception commonly made by intermediate students.

        Return strictly valid JSON:
        {{
            "flawed_explanation": "The explanation containing the intentional flaw",
            "the_hidden_flaw": "Exact description of what was wrong",
            "correction": "How a master would correct it"
        }}
        """
        return self.llm.generate_json(prompt, schema={})

    def verify_hunt(self, user_critique: str, hidden_flaw: str) -> dict:
        prompt = f"""
        True Hidden Flaw: "{hidden_flaw}"
        User's Diagnosis: "{user_critique}"

        Did the user correctly spot and explain the hidden flaw?
        Return strictly JSON:
        {{
            "found_flaw": bool,
            "feedback": "Short encouraging assessment of their diagnosis"
        }}
        """
        return self.llm.generate_json(prompt, schema={})