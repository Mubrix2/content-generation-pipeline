# app/services/pipeline.py
import logging
from app.core.generator import generate
from app.core.prompts import (
    blog_post_prompt,
    email_prompt,
    outline_prompt,
    social_captions_prompt,
    summary_prompt,
)

logger = logging.getLogger(__name__)


# ── Parsers ────────────────────────────────────────────────────────────────────

def _parse_captions(raw: str) -> dict:
    """
    Parse the social captions response into a dict.
    Expects: LINKEDIN: ... TWITTER: ... INSTAGRAM: ...
    """
    result = {"linkedin": "", "twitter": "", "instagram": ""}
    current_key = None

    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("LINKEDIN:"):
            current_key = "linkedin"
            result["linkedin"] = line.replace("LINKEDIN:", "").strip()
        elif line.startswith("TWITTER:"):
            current_key = "twitter"
            result["twitter"] = line.replace("TWITTER:", "").strip()
        elif line.startswith("INSTAGRAM:"):
            current_key = "instagram"
            result["instagram"] = line.replace("INSTAGRAM:", "").strip()
        elif current_key and line:
            # Handle multi-line captions
            result[current_key] += " " + line

    return result


def _parse_email(raw: str) -> dict:
    """
    Parse the email response into a dict.
    Expects: SUBJECT: ... PREVIEW: ... BODY: ... CTA: ...
    """
    result = {"subject": "", "preview": "", "body": "", "cta": ""}
    current_key = None
    body_lines = []

    for line in raw.splitlines():
        line_stripped = line.strip()
        if line_stripped.startswith("SUBJECT:"):
            current_key = "subject"
            result["subject"] = line_stripped.replace("SUBJECT:", "").strip()
        elif line_stripped.startswith("PREVIEW:"):
            current_key = "preview"
            result["preview"] = line_stripped.replace("PREVIEW:", "").strip()
        elif line_stripped.startswith("BODY:"):
            current_key = "body"
            body_lines = [line_stripped.replace("BODY:", "").strip()]
        elif line_stripped.startswith("CTA:"):
            current_key = "cta"
            if body_lines:
                result["body"] = " ".join(body_lines).strip()
            result["cta"] = line_stripped.replace("CTA:", "").strip()
        elif current_key == "body" and line_stripped:
            body_lines.append(line_stripped)

    if body_lines and not result["body"]:
        result["body"] = " ".join(body_lines).strip()

    return result


# ── Pipeline ───────────────────────────────────────────────────────────────────

def run_pipeline(
    topic: str,
    tone: str,
    audience: str,
) -> dict:
    """
    Run the full content generation pipeline.

    Steps:
    1. Generate blog outline
    2. Expand outline into full blog post
    3. Summarise the blog post
    4. Generate social media captions from summary
    5. Generate email copy from summary

    Args:
        topic: The content topic e.g. "AI tools for small businesses"
        tone: Writing tone e.g. "professional", "casual", "inspirational"
        audience: Target audience e.g. "Nigerian entrepreneurs"

    Returns:
        Dict with all generated content pieces
    """
    if not topic.strip():
        raise ValueError("Topic cannot be empty")

    logger.info(f"Starting pipeline: topic='{topic}', tone='{tone}'")

    # Step 1 — Outline
    logger.info("Step 1: Generating outline")
    outline = generate(
        prompt=outline_prompt(topic, tone, audience),
        max_tokens=400,
    )

    # Step 2 — Blog post (outline passed as context)
    logger.info("Step 2: Writing blog post")
    blog_post = generate(
        prompt=blog_post_prompt(topic, outline, tone, audience),
        max_tokens=1200,
    )

    # Step 3 — Summary (used by both steps 4 and 5)
    logger.info("Step 3: Summarising blog post")
    summary = generate(
        prompt=summary_prompt(blog_post),
        max_tokens=150,
    )

    # Step 4 — Social captions (summary passed as context)
    logger.info("Step 4: Generating social captions")
    raw_captions = generate(
        prompt=social_captions_prompt(topic, summary, tone),
        max_tokens=400,
    )
    captions = _parse_captions(raw_captions)

    # Step 5 — Email copy (summary passed as context)
    logger.info("Step 5: Generating email copy")
    raw_email = generate(
        prompt=email_prompt(topic, summary, tone, audience),
        max_tokens=400,
    )
    email = _parse_email(raw_email)

    logger.info("Pipeline complete")

    return {
        "topic": topic,
        "tone": tone,
        "audience": audience,
        "outline": outline,
        "blog_post": blog_post,
        "summary": summary,
        "captions": captions,
        "email": email,
    }