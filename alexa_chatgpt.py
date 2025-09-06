from flask import Flask, request, jsonify
import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
from flask import redirect

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Conversation history per session
conversations = {}


def build_response(output_text, should_end_session=False, reprompt=None):
    """Build Alexa-compatible response format"""
    response = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": output_text
            },
            "shouldEndSession": should_end_session
        }
    }
    if reprompt:
        response["response"]["reprompt"] = {
            "outputSpeech": {"type": "PlainText", "text": reprompt}
        }
    return response


@app.route("/alexa-chat/health", methods=["GET"])
def alexa_health_check():
    """Health check endpoint for Alexa integration"""
    return jsonify({"status": "healthy", "service": "alexa-chat"})


@app.route("/alexa-chat/", methods=["POST", "GET"])
def alexa_chat_slash():
    """Alias route with trailing slash"""
    return alexa_chat()


@app.route("/alexa-chat", methods=["POST", "GET"])
@app.route("/alexa-chat/", methods=["POST", "GET"])
def alexa_chat():
    """Main Alexa skill endpoint"""
    if request.method == "GET":
        return "Alexa Skill Endpoint is working!"

    data = request.get_json()
    app.logger.info(f"Received data: {data}")

    try:
        request_type = data.get("request", {}).get("type", "")
        session = data.get("session", {})
        session_id = session.get("sessionId", "default")
        app.logger.info(f"Request type: {request_type}, Session: {session_id}")

        # LaunchRequest - when the skill is opened
        if request_type == "LaunchRequest":
            # Reset conversation history for a new session
            conversations[session_id] = [
                {"role": "system", "content": "You are a helpful AI assistant."}
            ]
            return jsonify(build_response(
                "Hello! I'm your AI assistant. Ask me anything.",
                should_end_session=False,
                reprompt="For example, say: what is Python?"
            ))

        # IntentRequest - forward everything to ChatGPT
        elif request_type == "IntentRequest":
            intent = data["request"].get("intent", {})
            intent_name = intent.get("name", "")
            slots = intent.get("slots", {})
            user_message = ""

            app.logger.info(f"Intent: {intent_name}, Slots: {slots}")

            # For ChatIntent, extract UserInput slot
            if intent_name == "ChatIntent":
                if "UserInput" in slots and slots["UserInput"].get("value"):
                    user_message = slots["UserInput"]["value"]
                else:
                    user_message = "Hello, how can I help you?"
            
            # Handle FallbackIntent - when Alexa doesn’t understand
            elif intent_name == "AMAZON.FallbackIntent":
                # Pass a default clarification message to ChatGPT
                user_message = "Could you please explain that in a different way?"

            app.logger.info(f"Intent: {intent_name}, User message: {user_message}")

            # Built-in intents
            if intent_name == "AMAZON.HelpIntent":
                return jsonify(build_response(
                    "You can ask me anything, for example: what is the weather today?",
                    should_end_session=False
                ))

            if intent_name in ["AMAZON.CancelIntent", "AMAZON.StopIntent"]:
                conversations.pop(session_id, None)  # clear history
                return jsonify(build_response("Goodbye!", should_end_session=True))

            # Initialize conversation history if not already set
            if session_id not in conversations:
                conversations[session_id] = [
                    {"role": "system", "content": "You are a helpful AI assistant."}
                ]

            # Add user message to history
            conversations[session_id].append({"role": "user", "content": user_message})

            # Call OpenAI API
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=conversations[session_id],
                    max_tokens=150,
                    temperature=0.7
                )
                reply = response.choices[0].message.content.strip()

                if len(reply) > 300:
                    reply = reply[:297] + "..."

                # Add assistant response to history
                conversations[session_id].append({"role": "assistant", "content": reply})

                app.logger.info(f"OpenAI response: {reply}")
                return jsonify(build_response(reply, should_end_session=False))

            except Exception as e:
                app.logger.error(f"OpenAI API error: {str(e)}")
                return jsonify(build_response(
                    "Sorry, I'm having trouble processing your request right now.",
                    should_end_session=False
                ))

        # SessionEndedRequest - when Alexa session ends
        elif request_type == "SessionEndedRequest":
            conversations.pop(session_id, None)  # clear history
            return jsonify(build_response("Goodbye!", should_end_session=True))

        # Unknown request type
        else:
            return jsonify(build_response(
                "Sorry, I didn't understand. Please try again.",
                should_end_session=False
            ))

    except Exception as e:
        app.logger.error(f"General error: {str(e)}")
        return jsonify(build_response(
            "Sorry, I encountered an error. Please try again.",
            should_end_session=False
        ))


@app.route("/health", methods=["GET"])
def health_check():
    """Generic health check endpoint"""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5060, debug=True)
