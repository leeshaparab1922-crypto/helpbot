import anthropic

from pydantic import BaseModel
from helpbot import conversation
from helpbot.config import SYSTEM_PROMPT, Settings


class ChatResult(BaseModel):
    text:str
    input_tokens:int
    output_tokens:int
    total_tokens:int
    


class Helpbot:
    def __init__(self, settings: Settings):
        self._settings = settings
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    def chat(self, conversation: conversation.Conversation) -> ChatResult:
        response = self.client.messages.create(
            model=self._settings.model,
            max_tokens=self._settings.max_tokens,
            temperature=self._settings.temperature,
            messages=conversation.messages,
            system=SYSTEM_PROMPT
        )

        return ChatResult(
            text=response.content[0].text,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens
        )

