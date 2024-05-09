import requests
import base64
from telegram import Update
from telegram.ext import ContextTypes , ApplicationBuilder , CommandHandler , MessageHandler , filters

async def start (update:Update , context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(text="hi welcome to our bot! \n please send your config code subscribetion link to give you copyable config codes" , chat_id= update.message.from_user.id )

async def send_configs(update:Update , context:ContextTypes.DEFAULT_TYPE):
    try:
        url = update.message.text
        response = requests.get(url)
        if response.status_code == 200:
            encoded_text = response.text
            decoded_text = base64.b64decode(encoded_text).decode('utf-8')
            config_codes = decoded_text.split('\n')
            for config in config_codes:
                await context.bot.send_message(text=config,chat_id=update.message.chat_id)
            else:
                await context.bot.send_message(text='Done ✅' , chat_id=update.message.chat_id)
        else:
            await context.bot.send_message(text='❌ please send valid link ❌' , chat_id=update.message.chat_id)
            await context.bot.delete_message(chat_id=update.message.chat_id , message_id=update.message.message_id)
    except:
        await context.bot.send_message(text='❌ please send valid link ❌' , chat_id=update.message.chat_id)
        await context.bot.delete_message(chat_id=update.message.chat_id , message_id=update.message.message_id)

if __name__ == "__main__" :
    application = ApplicationBuilder().token("7177527014:AAFt17jx1mINOvRBINzMQi2zFJPB-b7nmeo").build()

    start_handler = CommandHandler('start' , start)
    link_handler = MessageHandler(filters.ALL , send_configs)
    application.add_handler(start_handler)
    application.add_handler(link_handler)

    application.run_polling()
