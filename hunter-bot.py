import json
import requests
from emoji import emojize as e
from sanitizer import clean_plates, verify_plates
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Carregar configurações do arquivo JSON
with open('appsettings.json', 'r') as file:
    c = json.load(file)

async def fetch_data_from_api(query: str) -> str:
    url = c['apiUrl'].replace('{query}', query)   
    response = requests.get(url, verify=False) 

    # Obter JSON da resposta
    if response.status_code == 200:
        data = response.json()
        
        if data and isinstance(data, dict) and 'plate' in data and data['plate'] is not None:
            return (
                f"🚗🚨 Placa Localizada 🚗🚨\n"
                f"🛑 **Placa:** {data['plate']}\n"
                f"🚗 **Modelo:** {data['model']}\n"
                f"🏢 **Empresa:** {data['company']}\n"
                f"📞 **Contato:** {data['fone']}\n"
                f"🕵️🕵️🕵️"
            )
        else:
            return "😑 Placa não encontrada. 😑"

    return "🚫 Erro ao acessar a API. 🚫"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    plate = clean_plates(user_message)

    if not verify_plates(plate):
        await update.message.reply_text("🚫 Placa inválida. 🚫")
        return
    
    result = await fetch_data_from_api(plate)
    await update.message.reply_text(result, parse_mode="Markdown")

# Criar aplicação do bot
app = ApplicationBuilder().token(c['botToken']).build()

# Adicionar handler para mensagens de texto
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Rodar bot
app.run_polling()
