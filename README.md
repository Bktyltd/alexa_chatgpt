# Alexa ChatGPT Skill

This project provides a **Flask-based Alexa Skill** that integrates with **OpenAI’s GPT models**.  
It allows you to ask Alexa natural language questions (in English or Turkish), and get real-time answers powered by ChatGPT.

---

## 🚀 Features
- Alexa Skill endpoint built with Flask.
- Integration with OpenAI’s GPT (currently using `gpt-4o-mini`).
- Supports both **English and Turkish** queries.
- Maintains **session-based conversation history** for more natural interactions.
- Includes `/health` and `/alexa-chat/health` endpoints for monitoring.

---

## 📦 Requirements
The required dependencies are listed in `requirements.txt`:

```txt
flask>=2.3.0
python-dotenv>=1.0.0
openai>=1.0.0
gunicorn>=21.2.0
requests>=2.31.0
