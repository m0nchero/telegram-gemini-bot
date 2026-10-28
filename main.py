import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

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
    chat_type = update.message.chat.type
    bot_username = context.bot.username

    is_group = chat_type in ["group", "supergroup"]
    is_mentioned = f"@{bot_username}" in user_text
    is_reply_to_bot = (
        update.message.reply_to_message 
        and update.message.reply_to_message.from_user.id == context.bot.id
    )

    if is_group and not (is_mentioned or is_reply_to_bot):
        return

    cleaned_prompt = user_text.replace(f"@{bot_username}", "").strip()
    if not cleaned_prompt:
        await update.message.reply_text("Dinliyorum, buyur?")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = ai_client.models.generate_content(
            model=MODEL_NAME,
            contents=cleaned_prompt,
            config={"system_instruction": SYSTEM_INSTRUCTION}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Hata detayı: {e}")
        await update.message.reply_text("Şu an sistemsel bir yoğunluk var, birazdan tekrar dener misin?")

if name == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot devrede...")
    app.run_polling()
