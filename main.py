import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# Port dinleyicisi (Render Web Service kapanmasın diye)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot calisiyor!")

def run_fake_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ai_client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = (
    "Sen arkadaş canlısı, samimi, esprili, zeki ve doğal bir Türkçe konuşan "
    "bir Telegram grup asistanısın. Yanıtlarını gereksiz uzatmadan, doğrudan ve grup içi "
    "sohbete uygun akıcı bir üslupla ver."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text
    chat_type = update.message.chat.
