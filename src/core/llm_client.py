import json
from google import genai
from google.genai import types
from src.core.config import config

class LLMClient:
    def __init__(self):
        self.client = genai.Client(api_key=config.gemini_api_key)
        self.model = config.model_name

    def generate(self, prompt: str, system_instruction: str = None) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )
        return response.text
    def get_embedding(self, text: str) -> list[float]:
        """Generates semantic vector embeddings using Google GenAI."""
        response = self.client.models.embed_content(
            model=config.embedding_model,
            contents=text
        )
        return response.embeddings[0].values
    def generate_json(self, prompt: str, schema: dict) -> dict:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        try:
            return json.loads(response.text)
        except Exception:
            return {}