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
    
def _make_extractor(description: str, fields: list[str]):
    def extractor(customer_message: str, settings: Settings) -> dict:
        fields_str = ", ".join(fields)
        prompt = f"""Extract structured data from this customer message for a {description}.

Customer message: {customer_message}

Respond with JSON containing these fields: {fields_str}
Use null for any field not mentioned."""
        try:
            return _extract(prompt, settings)
        except Exception:
            return {f: None for f in fields}
    return extractor


INTENT_EXTRACTOR_MAP: dict[str, callable] = {
    "order_status":        _make_extractor("order status enquiry",      ["order_id"]),
    "order_cancellation":  _make_extractor("order cancellation",        ["order_id", "reason"]),
    "order_wrong_item":    _make_extractor("wrong item received",       ["order_id", "item_received", "item_ordered"]),
    "order_missing_item":  _make_extractor("missing item in order",     ["order_id", "missing_item"]),
    "return_request":      _make_extractor("return request",            ["order_id", "reason", "urgency"]),
    "refund_status":       _make_extractor("refund status enquiry",     ["order_id"]),
    "account_login_issue": _make_extractor("account login issue",       ["email"]),
    "account_update":      _make_extractor("account update request",    ["field_to_update", "new_value"]),
    "book_recommendation": _make_extractor("book recommendation",       ["genre", "author", "mood"]),
    "book_availability":   _make_extractor("book availability enquiry", ["title", "author"]),
    "complaint":           _make_extractor("complaint",                 ["topic", "severity"]),
}