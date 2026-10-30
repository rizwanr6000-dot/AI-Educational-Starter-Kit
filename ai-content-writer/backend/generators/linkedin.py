from .llm_client import call_llm

SYSTEM_PROMPT = (
    "You are a LinkedIn content strategist. Write short, high-engagement "
    "LinkedIn posts: a strong first line (hook), short line breaks, "
    "personal/professional insight, and 3-5 relevant hashtags at the end. "
    "Keep it under 200 words. Use a {tone} tone."
)


def generate(topic: str, tone: str = "professional", extra_instructions: str = "") -> str:
    system_prompt = SYSTEM_PROMPT.format(tone=tone)
    user_prompt = (
        f"Write a LinkedIn post about: {topic}\n\n"
        f"Extra instructions: {extra_instructions or 'None'}"
    )
    return call_llm(system_prompt, user_prompt, max_tokens=500)
