import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    MAX_INPUT_LENGTH = 2000
    SUPPORTED_LANGUAGES = ["en", "ur"]

    @classmethod
    def debug_info(cls):
        """Print configuration status for debugging."""
        print(f"GROQ API Key loaded: {'YES' if cls.GROQ_API_KEY else 'NO'}")
        print(f"GROQ API Key prefix: {cls.GROQ_API_KEY[:10] if cls.GROQ_API_KEY else 'None'}")
        print(f"TAVILY API Key loaded: {'YES' if cls.TAVILY_API_KEY else 'NO'}")
        print(f"Using model: {cls.GROQ_MODEL}")