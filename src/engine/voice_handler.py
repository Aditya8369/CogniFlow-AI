from google.genai import types
from src.core.llm_client import LLMClient

class VoiceHandler:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def transcribe_audio(self, audio_bytes: bytes, mime_type: str = "audio/wav") -> str:
        prompt = "Transcribe the spoken explanation accurately. Do not add commentary or corrections, only output the verbatim transcription."
        
        response = self.llm.client.models.generate_content(
            model=self.llm.model,
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                prompt
            ]
        )
        return response.text.strip()