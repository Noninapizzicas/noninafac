import logging
from telegram import Update
from telegram.ext import CallbackContext
from services.azure_service import DocumentProcessor
from services.email_service import send_email
from utils.formatters import format_email_content

def start(update: Update, context: CallbackContext) -> None:
    welcome_text = """
    ¡Bienvenido al Bot de Procesamiento de Documentos! 📄
    
    Puedo procesar:
    - Facturas en PDF 📑
    - Tickets/recibos en imagen 🧾
    
    Solo envíame el documento y:
    1. Lo procesaré automáticamente
    2. Extraeré la información importante
    3. Enviaré los resultados por email
    
    ¡Empecemos! 🚀
    """
    update.message.reply_text(welcome_text)
    logging.info("Comando start ejecutado")

def process_document(update: Update, context: CallbackContext) -> None:
    try:
        status_message = update.message.reply_text('🔄 Recibiendo documento...')
        
        file = context.bot.get_file(update.message.document.file_id)
        file_bytes = file.download_as_bytearray()
        file_name = update.message.document.file_name
        
        logging.info(f"Documento recibido: {file_name}")
        status_message.edit_text('🔄 Analizando documento con Azure...')
        
        processor = DocumentProcessor()
        result = processor.analyze_document(file_bytes, file_name)
        
        logging.info("Documento analizado correctamente")
        status_message.edit_text('🔄 Preparando y enviando email...')
        
        email_content = format_email_content(result, file_name)
        send_email(email_content, file_name)
        
        status_message.edit_text('✅ ¡Documento procesado! Resultados enviados por email.')
        
    except Exception as e:
        error_message = f"❌ Error procesando el documento: {str(e)}"
        logging.error(error_message)
        if 'status_message' in locals():
            status_message.edit_text(error_message)
        else:
            update.message.reply_text(error_message)