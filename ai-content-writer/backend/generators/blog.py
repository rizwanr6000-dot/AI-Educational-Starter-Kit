from .llm_client import call_llm

SYSTEM_PROMPT = (
    "You are a skilled blog writer. Write in a conversational, engaging, "
    "personality-driven style with short paragraphs, a catchy title, a hook "
    "opening line, scannable subheadings, and a call-to-action at the end. "
    "Use a {tone} tone."
)


def generate(topic: str, tone: str = "casual", extra_instructions: str = "") -> str:
    system_prompt = SYSTEM_PROMPT.format(tone=tone)
    user_prompt = (
        f"Write a blog post about: {topic}\n\n"
        "Format:\n"
        "# Catchy Title\n"
        "Hook opening line\n"
        "## Section 1\n...\n## Section 2\n...\n## Wrap Up / CTA\n...\n\n"
        f"Extra instructions: {extra_instructions or 'None'}"
    )
    return call_llm(system_prompt, user_prompt, max_tokens=1400)
