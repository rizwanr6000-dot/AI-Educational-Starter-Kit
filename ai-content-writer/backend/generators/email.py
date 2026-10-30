from .llm_client import call_llm

SYSTEM_PROMPT = (
    "You are an expert email copywriter. Write clear, concise professional "
    "emails with a subject line, greeting, short purposeful body paragraphs, "
    "and a polite sign-off. Use a {tone} tone."
)


def generate(topic: str, tone: str = "professional", extra_instructions: str = "") -> str:
    system_prompt = SYSTEM_PROMPT.format(tone=tone)
    user_prompt = (
        f"Write an email about: {topic}\n\n"
        "Format:\n"
        "Subject: ...\n\nDear ...,\n\nBody...\n\nBest regards,\n[Your Name]\n\n"
        f"Extra instructions: {extra_instructions or 'None'}"
    )
    return call_llm(system_prompt, user_prompt, max_tokens=700)
