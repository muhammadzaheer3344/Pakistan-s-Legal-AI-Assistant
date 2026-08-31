from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from services.groq_client import GroqLegalAssistant
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    assistant = GroqLegalAssistant()
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    assistant = None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/assistant')
def assistant_view():
    query = request.args.get('query', '')
    language = request.args.get('lang', 'en')
    if language not in Config.SUPPORTED_LANGUAGES:
        language = 'en'
    return render_template('assistant.html', query=query, language=language)

@app.route('/ask', methods=['POST'])
def ask():
    if not assistant:
        logger.error("Groq assistant was not initialized. Check GROQ_API_KEY and TAVILY_API_KEY configuration.")
        return render_template('error.html', message="The application is not properly configured. Please set the GROQ_API_KEY and TAVILY_API_KEY."), 500

    question = request.form.get('question', '').strip()
    language = request.form.get('language', 'en').strip()

    logger.info("Received /ask request: language=%s, question_length=%s", language, len(question))

    if not question:
        flash("Please describe your legal issue.", "error")
        return redirect(url_for('assistant_view'))
    if len(question) > Config.MAX_INPUT_LENGTH:
        flash(f"Your question is too long. Please limit to {Config.MAX_INPUT_LENGTH} characters.", "error")
        return redirect(url_for('assistant_view'))
    if language not in Config.SUPPORTED_LANGUAGES:
        language = 'en'

    try:
        result = assistant.ask(question, language)
        if result is None:
            raise Exception("Empty response from AI")
        return render_template('result.html', result=result, question=question, language=language)
    except Exception:
        logger.exception("Groq/Tavily request failed for /ask: language=%s, question=%s", language, question)
        return render_template('error.html', message="Unable to retrieve legal information at the moment. Please try again shortly."), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)