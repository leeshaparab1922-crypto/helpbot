# HelpBot: AI Customer Support for PageTurner Books

HelpBot is an interactive AI-powered customer support chatbot built specifically for **PageTurner Books**, an independent online bookstore. It provides a conversational interface to help customers with order tracking, returns, account issues, and book recommendations.

## Overview

HelpBot serves as a bridge between the customer and bookstore support systems. It uses Anthropic's Claude models to interpret customer intent, extract relevant information, and provide friendly, brand-aligned responses. It is designed to be a lightweight, CLI-based tool for demonstration or integration into support workflows.

## Features

- **Conversational Support:** Provides a warm, approachable, book-themed persona.
- **Intent Detection:** Automatically categorizes customer messages into intents like `order_status`, `return_request`, `book_recommendation`, `complaint`, etc.
- **Structured Data Extraction:** Reliably extracts parameters (like `order_id` or `missing_item`) as JSON without full tool calls using Claude's capabilities.
- **Streaming Responses:** Provides real-time typing of assistant responses for a better user experience.
- **Customizable:** Allows easy configuration of response temperature via slash commands.
- **Context-Aware:** Maintains conversation history to provide helpful, context-aware assistance.

## Tech Stack

| Area | Technology |
|---|---|
| Language | Python (>=3.13) |
| AI API | Anthropic Python SDK (`anthropic`) |
| Validation/Config | Pydantic, Pydantic Settings |
| Dependency Management | uv / pip |

## Installation Instructions

This project uses `uv` for efficient package management.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd chatbot
   ```

2. **Install dependencies:**
   Using `uv`:
   ```bash
   uv sync
   ```
   Or using standard `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

The application requires an Anthropic API key to function.

1. Copy the example configuration:
   ```bash
   cp helpbot/.env.example .env
   ```
2. Open `.env` and configure your key:
   ```env
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
   ```

## Usage Examples

Run the application:
```bash
# With uv
uv run main.py

# With standard python
python main.py
```

### Slash Commands
- `/temp <0.0 to 1.0>`: Set a new temperature value (e.g., `/temp 0.5`).
- `exit`: Quit the chat session.

### Interaction
```text
You: My book arrived with a ripped cover.
[Intent: complaint] {'complaint_type': 'product_quality', 'order_id': null, 'severity': 'high'}
HelpBot: Oh no — a damaged book is such a disappointment, especially when you're excited to read it. I'll get this sorted right away...
```

## Project Structure

```text
D:\chatbot\
├───GEMINI.md             # Instructions for AI agents
├───main.py               # Application entry point & CLI loop
├───pyproject.toml        # Project definitions & dependencies
├───README.md             # This file
├───requirements.txt      # Generated requirements
├───uv.lock               # Dependency lockfile
└───helpbot\              # Core library
    ├───chat.py           # HelpBot class & streaming logic
    ├───config.py         # App settings & persona definitions
    ├───conversation.py   # Conversation message models
    └───output.py         # Intent classification & data extraction
```

## Development Workflow

### Adding a New Intent
1.  **Define Intent:** Add the new intent name to `_INTENTS` in `helpbot/output.py`.
2.  **Define Extractor:** Add an entry to `_EXTRACTOR_SPECS` in `helpbot/output.py` with a description and fields schema.
3.  **Add Opener:** (Optional) Add a custom greeting to `_INTENT_OPENERS` in `main.py`.

### Configuration
Update `helpbot/config.py` to add new settings fields to the `Settings` Pydantic class.

## Contributing Guidelines

We welcome contributions! Please follow these guidelines:
1.  **Maintain Type Safety:** Use explicit type hints for new code.
2.  **Follow Patterns:** Adhere to existing Pydantic models and the intent extraction factory pattern.
3.  **Test:** If adding new logic, ensure corresponding tests are created or updated.
4.  **Formatting:** Keep code clean and idiomatic.
