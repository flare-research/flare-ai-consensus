def parse_chat_response(response: dict) -> str:
    """Parse response from chat completion endpoint"""
    return response.get("choices", [])[0].get("message", {}).get("content", "")
