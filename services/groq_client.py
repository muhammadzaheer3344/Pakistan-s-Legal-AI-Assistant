import json
import logging
from groq import Groq
from config import Config
from services.search import LegalSearch
from services.prompt import build_system_prompt, build_user_prompt
from services.response_parser import parse_response

logger = logging.getLogger(__name__)


class GroqLegalAssistant:
    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set")
        if not Config.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is not set")

        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.search_client = LegalSearch()

    def ask(self, question, language):
        question = (question or '').strip()
        if not question:
            raise ValueError("Question is required")

        logger.info("Searching for legal context for question=%s", question[:120])
        search_results = self.search_client.search(question, max_results=10)
        logger.info("Tavily returned %s result(s)", len(search_results))

        system_prompt = build_system_prompt(language)
        user_prompt = build_user_prompt(question, search_results)

        try:
            response = self.client.chat.completions.create(
                model=Config.GROQ_MODEL,
                temperature=0.2,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            )

            raw_text = response.choices[0].message.content
            logger.info("Groq returned %s chars", len(raw_text or ""))
            parsed = parse_response(raw_text)
            return parsed
        except Exception:
            logger.exception("Groq API call failed for question=%s", question)
            raise
