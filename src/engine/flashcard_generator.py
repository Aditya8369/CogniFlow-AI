import csv
import io
from src.core.llm_client import LLMClient

class FlashcardGenerator:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_cards(self, topic: str, gaps: list[str]) -> list[dict]:
        gaps_list = "\n".join([f"- {g}" for g in gaps]) if gaps else f"Core foundations of {topic}"
        
        prompt = f"""
        Topic: {topic}
        Identified Conceptual Gaps:
        {gaps_list}

        Generate 4-6 high-yield, active-recall Anki flashcards specifically designed to eliminate these gaps.
        Return strictly JSON with key "cards" containing a list of objects with "front" and "back":
        {{
            "cards": [
                {{"front": "Question / Prompt", "back": "Concise, intuitive explanation"}}
            ]
        }}
        """
        data = self.llm.generate_json(prompt, schema={})
        return data.get("cards", [])

    def export_anki_csv(self, cards: list[dict]) -> str:
        output = io.StringIO()
        writer = csv.writer(output, delimiter="\t")
        for card in cards:
            writer.writerow([card.get("front", ""), card.get("back", "")])
        return output.getvalue()