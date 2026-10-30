"""
llm_client.py
--------------
Small wrapper around the Anthropic API (Claude) used by every content
generator. Centralising it here means each generator file only has to
supply a prompt template - not deal with API setup.

If ANTHROPIC_API_KEY is not set, call_llm() falls back to a clearly
labeled placeholder response so the app still runs end-to-end for demos.
"""

import os

try:
    import anthropic
    _client = None
    if os.environ.get("ANTHROPIC_API_KEY"):
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
except ImportError:
    anthropic = None
    _client = None


def call_llm(system_prompt: str, user_prompt: str, max_tokens: int = 1200) -> str:
    """
    Sends a prompt to Claude and returns the plain text response.
    Falls back to a placeholder string if no API key/library is configured,
    so the rest of the app (routing, formatting, frontend) can still be
    tested without live credentials.
    """
    if _client is None:
        return (
            "[DEMO MODE - no ANTHROPIC_API_KEY set]\n\n"
            "This is where the AI-generated content would appear.\n"
            f"System instructions used:\n{system_prompt}\n\n"
            f"User brief:\n{user_prompt}\n\n"
            "Add your API key to backend/.env as ANTHROPIC_API_KEY=... "
            "to get real generated output."
        )

    message = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    parts = [block.text for block in message.content if getattr(block, "type", "") == "text"]
    return "\n".join(parts).strip()
