import json
import requests
from emoji import emojize as e
from database import fetch_data_from_base
from sanitizer import clean_plates, verify_plates
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

with open('appsettings.json', 'r') as file:
    c = json.load(file)

async def fetch_data_from_api(query: str) -> str:
    response = await fetch_data_from_base(query)

    data = response
    if len(data) > 0 and data[0].auto_plate is not None:
        return (
            f"🚗🚨 Placa Localizada 🚗🚨\n"
            f"🛑 {data[0].auto_plate}\n"
            f"🚗 {data[0].auto_model}\n"
            f"🏢 {data[0].company}\n"
            f"📞 {data[0].contact}\n"
            f"🕵️🕵️🕵️"
        )
    else:
        return "😑 Placa não encontrada. 😑"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    plate = clean_plates(user_message)

    if not verify_plates(plate):
        await update.message.reply_text("🚫 Placa inválida. 🚫")
        return
    
    result = await fetch_data_from_api(plate)
    await update.message.reply_text(result, parse_mode="Markdown")



def start_bot():
    app = ApplicationBuilder().token(c['botToken']).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    start_bot()
