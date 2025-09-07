# Alexa ChatGPT Skill

This project provides a **Flask-based backend** for an **Amazon Alexa Skill** that integrates with **OpenAI’s GPT models**.  
It enables Alexa to handle free-form conversations by forwarding user queries to ChatGPT and returning intelligent responses.

---

##  Features
- Flask-based Alexa Skill endpoint with JSON response format.
- Integration with OpenAI GPT models (`gpt-4o-mini` by default).
- Session-based conversation history for natural multi-turn interactions.
- `/health` and `/alexa-chat/health` endpoints for monitoring and debugging.
- Works seamlessly with **Cloudflare Tunnel** for secure HTTPS exposure.

---

##  Requirements
The required dependencies are listed in `requirements.txt`:

```txt
flask>=2.3.0
python-dotenv>=1.0.0
openai>=1.0.0
gunicorn>=21.2.0
requests>=2.31.0
