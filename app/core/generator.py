# app/core/generator.py
import logging
from groq import Groq
from app.config import GROQ_API_KEY, LLM_MODEL, TEMPERATURE

logger = logging.getLogger(__name__)

_client: Groq | None = None


def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
        logger.info("Groq client initialised")
    return _client


def generate(prompt: str, max_tokens: int = 1500) -> str:
    """
    Single Groq call. Returns the response text.
    All pipeline steps call this same function.

    Args:
        prompt: The full prompt to send
        max_tokens: Upper limit on response length

    Returns:
        The LLM response as a plain string
    """
    client = get_client()

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=TEMPERATURE,
        max_tokens=max_tokens,
    )

    text = response.choices[0].message.content.strip()
    logger.info(f"Generated {len(text)} characters")
    return text