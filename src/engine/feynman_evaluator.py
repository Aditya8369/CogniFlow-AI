from src.core.llm_client import LLMClient

class FeynmanEvaluator:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def evaluate_explanation(self, topic: str, user_explanation: str, ground_truth: str = "") -> dict:
        system_instruction = (
            "You are an expert pedagogical evaluator specializing in the Feynman Technique. "
            "Your job is to identify student misconceptions, circular definitions, jargon without explanation, "
            "and missing intuitive links. Output must be strictly valid JSON."
        )

        prompt = f"""
        Topic: {topic}
        Reference Material: {ground_truth if ground_truth else "Use standard scientific/academic consensus."}
        Student's Explanation:
        \"\"\"{user_explanation}\"\"\"

        Evaluate the explanation based on:
        1. Clarity & Simplicity (0-10)
        2. Depth & Accuracy (0-10)
        3. Jargon Trap (Did they hide behind complex words without understanding?)
        4. Identified Knowledge Gaps / Misconceptions (List of strings)
        5. Feynman Verdict (Short 2-sentence summary)

        Return response as JSON with keys:
        {{
            "clarity_score": int,
            "accuracy_score": int,
            "uses_unexplained_jargon": bool,
            "jargon_terms_flagged": [str],
            "misconceptions": [str],
            "verdict": str
        }}
        """
        return self.llm.generate_json(prompt, schema={})