def build_system_prompt(language):
    """Constructs the system prompt for the legal assistant."""
    base_prompt = """
You are a Pakistani Legal Information Assistant.

Your purpose is to help users understand Pakistani legal information using authoritative and current sources.

Prioritize official Pakistani legislation, court decisions, and government sources.

Use the provided search results to ground your answer in real legal sources. Never invent laws, sections, cases, judgments, citations, procedures, penalties, or sources.

Distinguish between statutory law, case law, procedural information, and general explanatory information.

Only mention case law when it is genuinely relevant and supported by the search results.

Clearly communicate uncertainty where facts are incomplete.

Do not guarantee legal outcomes.

Do not pretend to be a lawyer.

Explain complex legal concepts in accessible language.

Respond in the language selected by the user.

Provide relevant sources whenever available and cite official or court sources when possible.
"""
    lang_instruction = f"\nThe user has selected {language} language. Respond entirely in {language}."
    return base_prompt + lang_instruction


def build_user_prompt(question, search_results=None):
    search_context = ""
    if search_results:
        search_context = "\n\nRelevant search results:\n" + "\n\n".join(
            f"- Title: {item.get('title', '')}\n  URL: {item.get('url', '')}\n  Content: {item.get('content', '')}"
            for item in search_results[:10]
        )

    return f"""
Please provide legal information for the following situation in Pakistan:

"{question}"

Use the provided legal search results as the basis for your answer when available.
{search_context}

Follow these instructions strictly:

1. Use only authoritative Pakistani legal sources and the supplied search results.
2. Structure your response as a JSON object with the following keys:
   - summary: A brief summary of the legal context.
   - relevant_law: An object or array containing law name, section/article, provision, and explanation if available. If none, set to null.
   - legal_position: Explanation of how the law applies to the user's situation, including limits, uncertainty, and need for more facts.
   - case_law: An array of relevant cases, each with case_name, court, year, citation, facts, decision, principle, relevance. If none, set to empty array.
   - possible_steps: General legal or procedural options that may be relevant, with careful language.
   - sources: An array of sources used, each with title, organization, reference, url. If no sources, empty array.
   - disclaimer: A short legal disclaimer.

Output ONLY the JSON object. Do not include any other text before or after the JSON.
"""