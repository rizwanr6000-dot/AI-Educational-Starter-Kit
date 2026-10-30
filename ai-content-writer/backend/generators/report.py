from .llm_client import call_llm

SYSTEM_PROMPT = (
    "You are a professional business report writer. Write structured, "
    "formal reports with an Executive Summary, Background, Findings "
    "(with subheadings), Recommendations, and Conclusion. Use a {tone} tone."
)


def generate(topic: str, tone: str = "formal", extra_instructions: str = "") -> str:
    system_prompt = SYSTEM_PROMPT.format(tone=tone)
    user_prompt = (
        f"Write a business report about: {topic}\n\n"
        "Format:\n"
        "# Report Title\n## Executive Summary\n...\n## Background\n...\n"
        "## Findings\n...\n## Recommendations\n...\n## Conclusion\n...\n\n"
        f"Extra instructions: {extra_instructions or 'None'}"
    )
    return call_llm(system_prompt, user_prompt, max_tokens=1600)
