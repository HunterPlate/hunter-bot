import json
import requests
from emoji import emojize as e
from sanitizer import clean_plates, verify_plates
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


with open('appsettings.json', 'r') as file:
    c = json.load(file)
    
async def fetch_data_from_api(query: str) -> str:
    url = c['apiUrl'].replace('{query}', query)   
    response = requests.get(url, verify=False) 
    
    if response.status_code == 200 and data and isinstance(data, dict) and 'plate' in data and data['plate'] != None:
        data = response.json()
        message = (
            f"{e(c['emoji']['car'])}{e(c['emoji']['light'])}Placa Localizada.{e(c['emoji']['car'])}{e(c['emoji']['light'])}\n"
            f"{data['plate']}\n"
            f"{data['model']}\n"
            f"{data['company']}\n"
            f"Contato:{data['fone']}\n"
            f"{e(c['emoji']['spy']) * 3}\n"
        )
        return message
    elif response.status_code == 200 and str(response.json()) != 'null' and 'plate' not in response.json():
        return f"{e(c['emoji']['expression'])}Placa não encontrada.{e(c['emoji']['expression'])}"
    else:
        return "Erro ao acessar a API."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    plate = clean_plates(user_message)

    if not verify_plates(plate):
        await update.message.reply_text(f"{e(c['emoji']['error'])}Placa inválida.{e(c['emoji']['error'])}")
        return
    
    result = await fetch_data_from_api(plate)
    await update.message.reply_text(result)



app = ApplicationBuilder().token(f"{c['botToken']}").build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
