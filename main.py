import sys
import anthropic
from pydantic import ValidationError  # Added import

from helpbot import Settings, Conversation, Helpbot

def main():
    try:
        # Changed from Settings.from_env() to Settings()
        settings = Settings()
    except ValidationError as e:  # Changed from EnvironmentError
        sys.exit(f"Configuration error:\n{e}")

    conversation = Conversation()

    temperature = settings.temperature
    bot = Helpbot(settings)

    while True:

        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("Goodbye!")
            break

        if not user_input:
            continue

        # handle temperature command
        if user_input.lower().startswith("/temp"):
            parts = user_input.split()
            # show current temperature if no argument
            if len(parts) == 1:
                print(f"Current temperature: {temperature}")
                continue
            # try to set new temperature
            try:
                new_temp = float(parts[1])
            except ValueError:
                print("Temperature must be a number.")
                continue
            if not 0.0 <= new_temp <= 1.0:
                print("Temperature must be between 0.0 and 1.0.")
                continue
            temperature = new_temp
            print(f"Temperature set to {temperature}")
            continue

        # handle quit commands
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Goodbye!")
            break

        conversation.add_user(user_input)

        reply = bot.chat(conversation)
        

        conversation.add_assistant(reply.text)

        print(f"HelpBot: {reply.text}")
        print(f"(Input Tokens: {reply.input_tokens}, Output Tokens: {reply.output_tokens}, Total Tokens: {reply.total_tokens})\n")

if __name__ == "__main__":
    main()
