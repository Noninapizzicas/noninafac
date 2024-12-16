import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config.settings import TELEGRAM_TOKEN
from services.telegram_service import start, process_document

def main():
    try:
        # Crear el Updater y pasar el token de bot
        updater = Updater(TELEGRAM_TOKEN, use_context=True)

        # Obtener el dispatcher para registrar manejadores
        dispatcher = updater.dispatcher

        # Registrar comandos
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(MessageHandler(Filters.document, process_document))

        # Iniciar el bot
        updater.start_polling(clean=True)
        logging.info("Bot iniciado correctamente")
        
        # Ejecutar el bot hasta que se presione Ctrl-C
        updater.idle()
        
    except Exception as e:
        logging.error(f"Error al iniciar el bot: {str(e)}")

if __name__ == '__main__':
    main()