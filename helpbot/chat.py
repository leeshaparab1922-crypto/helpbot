import anthropic
from pydantic import BaseModel

from helpbot.conversation import Conversation
from helpbot.config import SYSTEM_PROMPT, Settings

class ChatResult(BaseModel):
    text:str
    input_tokens:int
    output_tokens:int
    total_tokens:int
    


class HelpBot:
    def __init__(self, settings: Settings, client: anthropic.Anthropic | None = None) -> None:
        self._client=client
        self._settings = settings

    def chat_streaming(self, conversation: Conversation, temperature: float | None = None,opener:str="") -> ChatResult:

        messages = conversation.to_api_format()

        if opener:
            messages.append({ "role": "assistant", "content": opener })

        temp = temperature if temperature is not None else self._settings.temperature
        with self._client.messages.stream(
            model=self._settings.model,
            messages=messages,
            max_tokens=self._settings.max_tokens,
            system=SYSTEM_PROMPT,
            temperature=temp,
        ) as stream:
            
            if opener:
                print(opener, end="", flush=True)
            for chunk in stream.text_stream:
                print(chunk, end="", flush=True)
            print()
            final = stream.get_final_message()

        full_text =opener + final.content[0].text
        conversation.add_assistant(full_text)
        return ChatResult(
            text=full_text,
            input_tokens=final.usage.input_tokens,
            output_tokens=final.usage.output_tokens,
            total_tokens=final.usage.input_tokens + final.usage.output_tokens,
        )
