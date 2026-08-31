import logging
from tavily import TavilyClient
from config import Config

logger = logging.getLogger(__name__)

class LegalSearch:
    def __init__(self):
        if not Config.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is not set")
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)

    def build_queries(self, question):
        base = question.strip()
        queries = [
            f"{base} Pakistani law official sources",
            f"{base} Pakistan legal provisions official",
            f"{base} Pakistan court judgment official",
            f"site:pakistancode.gov.pk {base} Pakistan law",
            f"site:supremecourt.gov.pk {base} Pakistan legal judgment",
            f"site:lahorehighcourt.gov.pk {base} Pakistan law",
            f"site:sindhhighcourt.gov.pk {base} Pakistan law",
            f"site:peshawarhighcourt.gov.pk {base} Pakistan law",
            f"site:balochistanhighcourt.gov.pk {base} Pakistan law",
            f"site:ihc.gov.pk {base} Pakistan law",
        ]
        return list(dict.fromkeys(queries))

    def search(self, question, max_results=10):
        queries = self.build_queries(question)
        all_results = []

        for query in queries[:3]:
            try:
                response = self.client.search(
                    query=query,
                    search_depth="advanced",
                    max_results=max_results,
                    include_domains=[
                        "pakistancode.gov.pk",
                        "supremecourt.gov.pk",
                        "lahorehighcourt.gov.pk",
                        "sindhhighcourt.gov.pk",
                        "peshawarhighcourt.gov.pk",
                        "balochistanhighcourt.gov.pk",
                        "ihc.gov.pk",
                    ],
                )
                results = response.get("results", [])
                for item in results:
                    all_results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "content": item.get("content", "")
                    })
            except Exception:
                logger.exception("Tavily search failed for query=%s", query)

        seen = set()
        deduped = []
        for item in all_results:
            key = (item.get("title", ""), item.get("url", ""))
            if key not in seen and item.get("url"):
                seen.add(key)
                deduped.append(item)

        return deduped[:10]
