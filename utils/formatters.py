import logging
from datetime import datetime

def format_email_content(result, filename):
    try:
        documents = result.get('analyzeResult', {}).get('documents', [{}])
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
                <th>Confianza</th>
            </tr>
        """
        
        if documents:
            fields = documents[0].get('fields', {})
            for field_name, field_data in fields.items():
                value = field_data.get('content', 'No disponible')
                confidence = field_data.get('confidence', 0) * 100
                content += f"""
                <tr>
                    <td>{field_name}</td>
                    <td>{value}</td>
                    <td>{confidence:.2f}%</td>
                </tr>
                """
        
        # Añadir texto completo extraído
        text = ""
        for page in result.get('analyzeResult', {}).get('pages', []):
            for line in page.get('lines', []):
                text += line.get('content', '') + "\n"
        
        content += f"""
        </table>
        <h3>Texto completo extraído:</h3>
        <pre>{text}</pre>
        </body>
        </html>
        """
        
        return content
    except Exception as e:
        logging.error(f"Error en format_email_content: {str(e)}")
        return f"<p>Error al formatear el contenido: {str(e)}</p>"