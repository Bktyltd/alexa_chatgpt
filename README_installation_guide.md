# Alexa ChatGPT Skill (Flask + Cloudflare Tunnel)

This project integrates OpenAI's GPT model with Amazon Alexa through a Flask backend, exposed securely via Cloudflare Tunnel.  
You can ask Alexa natural language questions in **English** or **Turkish**, and receive responses powered by ChatGPT.

---

##  Features
- Alexa Skill endpoint built with Flask
- Supports both English and Turkish questions
- Session-based conversation memory
- Secure tunneling with Cloudflare
- Runs as a systemd service for auto-start on boot

---

##  Project Structure

```
alexa_chatgpt/
├── alexa_chatgpt.py          # Main Flask application
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignored files
├── .env.example              # Example environment file
├── alexa-chatgpt.service.example  # Example systemd service file
└── cloudflared-config.yml.example # Example Cloudflare tunnel config
```

---

##  Installation

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

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and add your OpenAI API Key:
```bash
cp .env.example .env
nano .env
```

Example:
```
OPENAI_API_KEY=your-openai-api-key-here
```

---

##  Running the Application

### Local Run
```bash
python alexa_chatgpt.py
```
The service will start at `http://127.0.0.1:5060`

### Health Check
```bash
curl http://127.0.0.1:5060/health
```

---

##  Cloudflare Tunnel

To make the Alexa Skill accessible over HTTPS, configure Cloudflare Tunnel.

1. Install cloudflared  
   [Installation Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/)

2. Example tunnel configuration:  
   `~/.cloudflared/cloudflared-config.yml.example`
   ```yaml
   tunnel: <your-tunnel-id>
   credentials-file: /home/<user>/.cloudflared/<your-tunnel-id>.json

   ingress:
     - hostname: alexa.yourdomain.com
       path: /alexa-chat*
       service: http://127.0.0.1:5060

     - service: http_status:404
   ```

3. Start tunnel
```bash
cloudflared tunnel --config /home/<user>/.cloudflared/cloudflared-config.yml run
```

---

##  Systemd Service Setup

To auto-start the application on boot, use the included example service file:

`alexa-chatgpt.service.example`
```ini
[Unit]
Description=Alexa ChatGPT Flask Service
After=network.target

[Service]
User=<your-username>
WorkingDirectory=/home/<your-username>/alexa_chatgpt
Environment="PATH=/home/<your-username>/alexa_chatgpt/alexa/bin"
ExecStart=/home/<your-username>/alexa_chatgpt/alexa/bin/python alexa_chatgpt.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Enable Service
```bash
sudo cp alexa-chatgpt.service.example /etc/systemd/system/alexa-chatgpt.service
sudo systemctl daemon-reload
sudo systemctl enable alexa-chatgpt
sudo systemctl start alexa-chatgpt
```

Check status:
```bash
systemctl status alexa-chatgpt
```

---

##  Alexa Developer Console Setup

1. Go to [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
2. Create a new skill → **Custom**
3. Set the endpoint to your Cloudflare Tunnel domain:
   ```
   https://alexa.yourdomain.com/alexa-chat
   ```
4. Use the provided interaction model (example JSON included in repo)

---

##  Testing

Example requests:
- **English**:  
  - "What is Python?"  
  - "Who is Alan Turing?"  
- **Turkish**:  
  - "Türkiye'nin başkenti neresi?"  
  - "Yapay zeka nedir?"  

---

##  License
MIT License
