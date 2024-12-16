import base64
import logging
import requests
from config.settings import AZURE_ENDPOINT, AZURE_KEY

class DocumentProcessor:
    def __init__(self):
        self.endpoint = AZURE_ENDPOINT
        self.key = AZURE_KEY

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
        logging.info(f"Respuesta de Azure: {response.status_code}")
        
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
