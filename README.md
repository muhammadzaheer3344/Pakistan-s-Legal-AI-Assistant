# Pakistan Legal Information Assistant

A Flask-based legal information assistant for Pakistan that helps users ask legal questions in English or Urdu, searches authoritative legal sources, and answers using a Groq-hosted language model with Tavily-powered retrieval.

## Overview

This app is designed to provide general legal information for educational purposes. It is not a replacement for legal advice from a licensed lawyer.

The system works as follows:

- User asks a legal question in English or Urdu
- Tavily searches Pakistani legal sources and official government/legal portals
- The search results are passed to a Groq model
- The model returns structured legal information in JSON format
- The result page shows a summary, relevant law, legal position, sources, and disclaimer

## Tech Stack

- Python 3.13+
- Flask
- Groq API
- Tavily API
- Jinja2 templates
- HTML/CSS

## Features

- English and Urdu support
- Search-grounded legal answers
- Structured output with summary, law references, and source links
- Responsive simple UI
- Legal disclaimer for educational use only
- Privacy-friendly setup using local environment variables

## Local Setup

1. Clone the repository.

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a local environment file named `.env` in the project root with your real keys:
   ```env
   GROQ_API_KEY=your_real_groq_key
   TAVILY_API_KEY=your_real_tavily_key
   GROQ_MODEL=openai/gpt-oss-20b
   ```

5. Start the app:
   ```bash
   python app.py
   ```

6. Open the app in your browser:
   ```text
   http://127.0.0.1:5000
   ```

## GitHub Safety

Do not commit your real `.env` file.

Use `.env.example` as the public template:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

The real `.env` file should stay local and should be ignored by Git via `.gitignore`.

## Project Structure

```text
pakistan-legal-ai/
├── app.py
├── config.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── services/
│   ├── __init__.py
│   ├── groq_client.py
│   ├── prompt.py
│   ├── response_parser.py
│   └── search.py
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── assistant.html
    ├── base.html
    ├── error.html
    ├── home.html
    └── result.html
```

## Notes

- This app is intended for general informational purposes.
- It does not provide legal advice or create a lawyer-client relationship.
- Results should be cross-checked with official Pakistani legal sources and a qualified local lawyer for specific legal matters.

## License

This project is provided for educational and research use.
