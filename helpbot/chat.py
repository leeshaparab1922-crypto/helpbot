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
    def __init__(self, settings: Settings):
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self._settings = settings

    def chat(self, conversation: Conversation, temperature: float | None = None) -> ChatResult:
        temp = temperature if temperature is not None else self._settings.temperature
        response = self._client.messages.create(
            model=self._settings.model,
            messages=conversation.to_api_format(),
            max_tokens=self._settings.max_tokens,
            system=SYSTEM_PROMPT,
            temperature=temp,
        )

        return ChatResult(
            text=response.content[0].text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens
        )
    
