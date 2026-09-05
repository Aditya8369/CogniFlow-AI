import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Config(BaseModel):
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    model_name: str = "gemini-2.5-flash"
    embedding_model: str = "text-embedding-004"
    chroma_db_dir: str = "./data/chroma_db"

config = Config()