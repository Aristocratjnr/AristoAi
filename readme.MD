# AristoAi

A professional Telegram bot and TypeScript runner for interacting with the Gemini API.

## Features
- Telegram bot (Python) that responds to user commands and prompts using Gemini API
- TypeScript runner for sending prompts to Gemini API from the command line
- Environment variable support for secure API key management

## Setup

### 1. Clone the repository
```sh
git clone https://github.com/Aristocratjnr/AristoAi
cd AristoAi
```

### 2. Environment Variables
Create a `.env` file in the root directory with the following content:
```
BOT_TOKEN=your-telegram-bot-token
GEMINI_API_KEY=your-gemini-api-key
```

### 3. Python Bot Setup
Install dependencies:
```sh
pip install -r requirements.txt
```

Run the bot:
```sh
python main.py
```

### 4. TypeScript Runner Setup
Install Node.js dependencies:
```sh
npm install axios dotenv
```

Run a prompt:
```sh
npx ts-node runner.ts "Your prompt here"
```

## File Structure
- `main.py` — Telegram bot (Python)
- `runner.ts` — TypeScript Gemini API runner
- `requirements.txt` — Python dependencies
- `.env` — Environment variables (not committed)
- `readme.MD` — Project documentation

## License
See [LICENSE](LICENSE).

## Contact
- Developer: @aristocratjnr
- Email: ayimobuobi@gmail.com
- GitHub: [aristocratjnr](https://github.com/aristocratjnr)
