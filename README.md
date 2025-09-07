# Alexa ChatGPT Skill – Amazon Alexa Custom Skill with OpenAI GPT  

This project provides a **Flask-based backend** for an **Amazon Alexa Custom Skill** integrated with **OpenAI’s GPT models (ChatGPT)**.  
It enables Alexa to answer natural language questions in real time by forwarding user queries to ChatGPT and returning intelligent responses.  

---

##  Key Features  
- **Alexa Custom Skill** integration with Flask backend.  
- Uses **OpenAI GPT models** (`gpt-4o-mini` by default).  
- **Session-based conversation history** for natural multi-turn conversations.  
- Includes **health check endpoints**: `/health` and `/alexa-chat/health`.  
- Works seamlessly with **Cloudflare Tunnel** for secure HTTPS exposure.  
- Ready-to-use **systemd service file** and **Cloudflare config examples**.  

---

##  Installation & Setup  

### 1. Clone Repository  
```bash
git clone https://github.com/Bktyltd/alexa_chatgpt.git
cd alexa_chatgpt
```

### 2. Create Virtual Environment  
```bash
python3 -m venv alexa
source alexa/bin/activate
```

### 3. Install Requirements  
```bash
pip install -r requirements.txt
```

### 4. Environment Variables  
Create a `.env` file in the project root:  
```env
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the Application  
```bash
python alexa_chatgpt.py
```

App runs on port **5060** by default.  

---

## 🛠️ Deployment  

### Using Gunicorn  
```bash
gunicorn -b 0.0.0.0:5060 alexa_chatgpt:app
```

### Systemd Service  
See `alexa-chatgpt.service.example` for production deployment.  

### Cloudflare Tunnel  
Use the provided `cloudflared-config.yml.example` to expose your local server securely.  

---

##  Files Included  
- `alexa_chatgpt.py` → Flask backend for Alexa Skill.  
- `requirements.txt` → Required Python dependencies.  
- `.gitignore` → To exclude sensitive files like `.env`.  
- `alexa-chatgpt.service.example` → Example systemd service.  
- `cloudflared-config.yml.example` → Example Cloudflare tunnel config.  
- `README_installation_guide.md` → Step-by-step installation instructions.  
- `alexa_skill_json.txt` → Example Alexa Skill interaction model.  

---

##  Alexa Skill Setup  
1. Go to the **Amazon Developer Console** → [Alexa Skills Kit](https://developer.amazon.com/alexa/console/ask).  
2. Create a new custom skill and set invocation name, e.g., **“chat with me”**.  
3. Import the JSON interaction model from `alexa_skill_json.txt`.  
4. Set your skill endpoint to the **Cloudflare tunnel URL** (e.g., `https://bktyconsultancy.co.uk/alexa-chat`).  
5. Enable testing in **Development mode**.  

