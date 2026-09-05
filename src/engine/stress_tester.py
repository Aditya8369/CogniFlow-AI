from src.core.llm_client import LLMClient

class CounterfactualStressTester:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_scenario(self, topic: str, user_explanation: str) -> dict:
        prompt = f"""
        Concept: {topic}
        Student's Mental Model: "{user_explanation}"

        Generate an adversarial, counterfactual 'what-if' thought experiment designed to stress-test their first-principles grasp.
        Alter one core assumption or physical/computational constraint (e.g., infinite latency, zero friction, strictly linear activation, zero gravity).

        Return strictly a JSON object:
        {{
            "altered_premise": "Short headline of the altered reality",
            "scenario_setup": "2-3 sentences presenting the dilemma and asking what consequence emerges",
            "first_principles_solution": "The correct physical/logical consequence and why it happens"
        }}
        """
        return self.llm.generate_json(prompt, schema={})

    def evaluate_response(self, topic: str, scenario: dict, student_answer: str) -> str:
        prompt = f"""
        Topic: {topic}
        Counterfactual Scenario: {scenario.get('scenario_setup')}
        Expected First-Principles Outcome: {scenario.get('first_principles_solution')}
        Student's Answer: "{student_answer}"

        Critique the student's reasoning in 2-3 concise, punchy paragraphs:
        1. Did they correctly extrapolate the altered boundary condition?
        2. Where did their intuition succeed, or what secondary consequence did they miss?
        """
        return self.llm.generate(prompt)