# GEMINI.md

## Project Overview
**HelpBot** is an AI-powered customer support chatbot designed for **PageTurner Books**, an independent online bookstore. It is built as an interactive CLI application using Python and the Anthropic API.

### Main Technologies
- **Python:** Requires Python `>=3.13` (as specified in `pyproject.toml`).
- **AI Integration:** Anthropic Python SDK (`anthropic`). The default model is `claude-haiku-4-5` (specified in `helpbot/config.py`).
- **Dependency Management:** Configured via `pyproject.toml` and managed with `uv` (`uv.lock` is included).
- **Configuration & Validation:** Pydantic and Pydantic Settings are used to manage environment variables and application settings.

---

## Building and Running

### Environment Configuration
The application expects environment variables to be set in a `.env` file at the root of the project.
1. Copy the example environment template:
   ```bash
   cp helpbot/.env.example .env
   ```
2. Open `.env` and set your `ANTHROPIC_API_KEY`:
   ```env
   ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
   ```

### Installing Dependencies
The project utilizes `uv` for python package management.
- To install all dependencies into a local virtual environment:
  ```bash
  uv sync
  ```
- Alternatively, standard dependencies can be installed using standard `pip`:
  ```bash
  pip install -r requirements.txt
  ```

### Running the Application
To run the interactive CLI chat session, execute `main.py` using your virtual environment or via `uv`:
```bash
uv run main.py
```
Or if you're using standard Python with an activated virtual environment:
```bash
python main.py
```

### Slash Commands & Controls
While interacting with HelpBot, you can use the following controls:
- `/temp <0.0 to 1.0>`: Set a new temperature value for responses.
- `exit`: Quit the CLI chat session safely.

---

## Codebase Architecture & Directory Structure

```
D:\chatbot\
├───GEMINI.md             # This instructions file (context and conventions)
├───main.py               # Application entry point; implements CLI loop and command routing
├───pyproject.toml        # Project definitions, Python requirements, and dependencies
├───README.md             # Public README file
├───requirements.txt      # Generated requirements file
├───uv.lock               # Pin-point dependencies lockfile for uv package manager
├───helpbot\              # Core library directory for the support bot
│   ├───__init__.py       # Exports high-level APIs (Settings, HelpBot, Conversation, etc.)
│   ├───.env.example      # Example environment configuration template
│   ├───chat.py           # Implements the HelpBot class and streaming responses
│   ├───config.py         # App settings and the HelpBot system prompt (persona and policies)
│   ├───conversation.py   # Stores user & assistant conversation messages
│   └───output.py         # Intent detection and field extraction helpers
```

### Module Descriptions
- **`helpbot/config.py`**: Exports the `Settings` class inheriting from Pydantic `BaseSettings` which reads variables from `.env`. It also defines the detailed `SYSTEM_PROMPT` containing the PageTurner Books assistant persona, bookshop guidelines, and instructions on how to leverage `<policy_context>`.
- **`helpbot/conversation.py`**: Defines standard Pydantic models `Message` and `Conversation` to collect interaction history and output it in a format compatible with the Anthropic Messages API.
- **`helpbot/chat.py`**: Contains the `HelpBot` class which orchestrates calls to `client.messages.stream`. It appends prefill openers when an intent opener is present and updates `Conversation` history automatically when the stream finishes.
- **`helpbot/output.py`**: Deals with structured extraction and categorization:
  - `detect_intent`: Classifies user input into one of the pre-defined support intents (e.g., `order_status`, `return_request`, `book_recommendation`).
  - `INTENT_EXTRACTOR_MAP`: A mapping of intent names to their corresponding data extractor functions, built using a clean factory pattern `_make_extractor`. Data extraction works via a smart prompt template asking for a JSON output and using Claude's prefill response (prefilling ` ```json ` and stopping at ` ``` `) to reliably extract parameters as a dictionary without full tool calls.

---

## Development Conventions

1. **Environment Variables:** Always keep the `.env` file git-ignored. Do not expose or commit API keys under any circumstances.
2. **Settings Management:** If you add a new configuration field, declare it inside `Settings` within `helpbot/config.py` with appropriate types and default values.
3. **Adding Support for a New Intent:**
   - Add the intent name to the `_INTENTS` list in `helpbot/output.py`.
   - Add a corresponding entry to `_EXTRACTOR_SPECS` inside `helpbot/output.py` defining its extraction description and expected schema.
   - If a custom opener is desired, add it to `_INTENT_OPENERS` in `main.py`.
4. **Structured JSON Extraction:** Prefer the prefill and stop-sequence pattern implemented in `_extract()` over raw text manipulation or complex parsing libraries for extraction tasks.
5. **Types and Warnings:** Use explicit typing, standard library models, and clean Pydantic schemas. Avoid type-ignores, generic casts, or reflection methods unless absolutely necessary.
