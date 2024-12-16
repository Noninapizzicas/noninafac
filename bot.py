import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import json
from datetime import datetime
import logging

# Configuración básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Configuración con las credenciales
TELEGRAM_TOKEN = '7528671361:AAF3PduMMTg-QrlNauSKDBxHXoxsuWf4TIU'
AZURE_ENDPOINT = 'https://ocrnonina.cognitiveservices.azure.com'
AZURE_KEY = '2hrHEmLRtti3D0q52Pius7sVJgYjeNfSliJrS1mEkjhBelrUKlK7JQQJ99ALAC5RqLJXJ3w3AAALACOG3l2p'
GMAIL_USER = 'bimbamfood@gmail.com'
GMAIL_PASSWORD = 'tflu envp jujb iocv'
DEST_EMAIL = 'noninapizzicas@gmail.com'

class DocumentProcessor:
    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.key = key

    def analyze_document(self, file_bytes, file_name):
        try:
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                return self._call_azure_api(file_bytes, 'prebuilt-receipt')
            elif file_name.lower().endswith('.pdf'):
                return self._call_azure_api(file_bytes, 'prebuilt-invoice')
            else:
                return self._call_azure_api(file_bytes, 'prebuilt-document')
        except Exception as e:
            logging.error(f"Error en analyze_document: {str(e)}")
            raise

    def _call_azure_api(self, file_bytes, model_id):
        url = f"{self.endpoint}/documentintelligence/documentModels/{model_id}:analyze?api-version=2023-10-31"
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.key
        }
        body = {
            'base64Source': base64.b64encode(file_bytes).decode()
        }

        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 202:
            operation_location = response.headers.get('Operation-Location')
            return self._get_analysis_result(operation_location)
        
        return response.json()

    def _get_analysis_result(self, operation_location):
        headers = {'Ocp-Apim-Subscription-Key': self.key}
        while True:
            response = requests.get(operation_location, headers=headers)
            result = response.json()
            
            if result.get('status') == 'succeeded':
                return result
            elif result.get('status') == 'failed':
                raise Exception("El análisis del documento falló")

def format_email_content(result, filename):
    try:
        fields = result.get('analyzeResult', {}).get('documents', [{}])[0].get('fields', {})
        
        content = f"""
        <html>
        <body>
        <h2>Análisis de Documento</h2>
        <p><strong>Nombre del archivo:</strong> {filename}</p>
        <p><strong>Fecha de procesamiento:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h3>Datos extraídos:</h3>
        <table border="1" cellpadding="5">
            <tr>
                <th>Campo</th>
                <th>Valor</th>
            </tr>
        """
        
        for field_name, field_data in fields.items():
            value = field_data.get('content', 'No disponible')
            content += f"""
            <tr>
                <td>{field_name}</td>
                <td>{value}</td>
            </tr>
            """
        
        content += """
        </table>
        </body>
        </html>
        """
        
        return content
    except Exception as e:
        logging.error(f"Error en format_email_content: {str(e)}")
        return f"<p>Error al formatear el contenido: {str(e)}</p>"

def send_email(content, subject):
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = DEST_EMAIL
        msg['Subject'] = f"Análisis de documento: {subject}"
        
        msg.attach(MIMEText(content, 'html'))
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)
            
    except Exception as e:
        logging.error(f"Error en send_email: {str(e)}")
        raise

def process_document(update: Update, context: CallbackContext) -> None:
    try:
        status_message = update.message.reply_text('🔄 Recibiendo documento...')
        
        file = context.bot.get_file(update.message.document.file_id)
        file_bytes = file.download_as_bytearray()
        file_name = update.message.document.file_name
        
        status_message.edit_text('🔄 Analizando documento con Azure...')
        
        processor = DocumentProcessor(AZURE_ENDPOINT, AZURE_KEY)
        result = processor.analyze_document(file_bytes, file_name)
        
        status_message.edit_text('🔄 Preparando y enviando email...')
        
        email_content = format_email_content(result, file_name)
        send_email(email_content, file_name)
        
        status_message.edit_text('✅ ¡Documento procesado! Resultados enviados por email.')
        
    except Exception as e:
        error_message = f"❌ Error procesando el documento: {str(e)}"
        if 'status_message' in locals():
            status_message.edit_text(error_message)
        else:
            update.message.reply_text(error_message)

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

def main():
    try:
        # Crear el Updater y pasar el token de bot.
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
