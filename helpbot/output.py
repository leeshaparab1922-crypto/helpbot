import json
from helpbot.config import Settings

INTENTS = [
    "order_status", "order_cancellation", "order_wrong_item", "order_missing_item",
    "return_request", "refund_status",
    "account_login_issue", "account_update",
    "book_recommendation", "book_availability",
    "complaint", "general_enquiry",
]

def _extract(prompt: str, settings: Settings) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    response = client.messages.create(
        model=settings.model,
        max_tokens=256,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "```json"},
        ],
        stop_sequences=["```"],
    )
    return json.loads(response.content[0].text)


def detect_intent(customer_message: str, settings: Settings) -> str:
    prompt = f"""Classify this customer message into exactly one intent.

Valid intents: {", ".join(INTENTS)}

Customer message: {customer_message}

Respond with JSON: {{"intent": "<intent_string>"}}"""

    try:
        result = _extract(prompt, settings)
        intent = result.get("intent", "general_enquiry")
        return intent if intent in INTENTS else "general_enquiry"
    except Exception:
        return "general_enquiry"