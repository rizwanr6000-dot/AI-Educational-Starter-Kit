from .llm_client import call_llm

SYSTEM_PROMPT = (
    "You are an expert long-form article writer. Write in-depth, well-researched "
    "feeling articles with a clear headline, an engaging introduction, 3-5 body "
    "sections with subheadings, and a concise conclusion. Use a {tone} tone."
)


def generate(topic: str, tone: str = "professional", extra_instructions: str = "") -> str:
    system_prompt = SYSTEM_PROMPT.format(tone=tone)
    user_prompt = (
        f"Write a full article about: {topic}\n\n"
        "Format:\n"
        "# Headline\n"
        "Introduction paragraph\n"
        "## Subheading 1\n...\n## Subheading 2\n...\n## Conclusion\n...\n\n"
        f"Extra instructions: {extra_instructions or 'None'}"
    )
    return call_llm(system_prompt, user_prompt, max_tokens=1600)
