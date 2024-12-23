# NoninaFac

Invoice processing system with Azure OCR integration and Telegram bot interface.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
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
- TELEGRAM_TOKEN: Your Telegram bot token