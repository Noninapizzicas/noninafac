#!/usr/bin/env python3
import os
import sys

def create_directory_structure():
    # Project root - cambiado para usar el directorio actual
    root_dir = "."  # Este es el cambio clave
    
    # Directory structure with files
    structure = {
        "invoice_processor": {
            "__init__.py": "",
            "email_reader.py": "from models import Email\n\ndef process_email():\n    pass",
            "azure_processor.py": "def process_document():\n    pass",
            "webhook_sender.py": "def send_webhook():\n    pass",
            "models.py": "from pydantic import BaseModel\n\nclass Invoice(BaseModel):\n    pass",
            "utils.py": "def format_date(date_str: str) -> str:\n    pass",
            "config.py": "import os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\nAZURE_KEY = os.getenv('AZURE_KEY')",
            "invoice_processor.py": "from models import Invoice\n\ndef process_invoice():\n    pass"
        },
        "telegram_bot": {
            "__init__.py": "",
            "main.py": "from telegram.ext import Updater, CommandHandler\n\ndef start(update, context):\n    pass\n\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()"
        }
    }
    
    # Root level files
    root_files = {
        ".env": "AZURE_KEY=your-key-here\nTELEGRAM_TOKEN=your-token-here",
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo
""",
        "README.md": """# NoninaFac

Invoice processing system with Azure OCR integration and Telegram bot interface.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\\Scripts\\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your credentials
6. Run the system

## Components

- invoice_processor: Main invoice processing logic
- telegram_bot: Telegram bot interface

## Configuration

Configure the system through the `.env` file:

- AZURE_KEY: Your Azure API key
- TELEGRAM_TOKEN: Your Telegram bot token""",
        "requirements.txt": """python-dotenv==1.0.0
python-telegram-bot==20.7
pydantic==2.5.2
requests==2.31.0
azure-ai-formrecognizer==3.3.0"""
    }

    # Create directory structure
    for directory, files in structure.items():
        dir_path = os.path.join(root_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        
        # Create files in directory
        for file_name, content in files.items():
            file_path = os.path.join(dir_path, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    # Create root level files
    for file_name, content in root_files.items():
        file_path = os.path.join(root_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    create_directory_structure()
    print("Project structure created successfully!")
