# app/core/prompts.py


def outline_prompt(topic: str, tone: str, audience: str) -> str:
    return f"""Create a structured blog post outline for the following:

Topic: {topic}
Tone: {tone}
Target Audience: {audience}

Return a clean outline with:
- A compelling title
- 4-5 main sections with brief descriptions
- A conclusion point

Return only the outline. No extra commentary."""


def blog_post_prompt(topic: str, outline: str, tone: str, audience: str) -> str:
    return f"""Write a complete, high-quality SEO blog post using this outline.

Topic: {topic}
Tone: {tone}
Target Audience: {audience}

Outline to follow:
{outline}

Requirements:
- 600-900 words
- Use the outline sections as headings
- Write in the specified tone throughout
- Include a strong opening hook
- End with a clear call to action
- Do not add meta descriptions or SEO notes — just the article content"""


def social_captions_prompt(topic: str, blog_summary: str, tone: str) -> str:
    return f"""Write 3 social media captions for this blog post.

Topic: {topic}
Tone: {tone}
Blog Summary: {blog_summary}

Requirements:
- Caption 1: LinkedIn (professional, 150-200 characters, include 3 hashtags)
- Caption 2: Twitter/X (punchy, under 240 characters, include 2 hashtags)
- Caption 3: Instagram (engaging, 100-150 characters, include 5 hashtags)

Format your response exactly like this:
LINKEDIN: [caption here]
TWITTER: [caption here]
INSTAGRAM: [caption here]"""


def email_prompt(topic: str, blog_summary: str, tone: str, audience: str) -> str:
    return f"""Write a marketing email promoting this blog post.

Topic: {topic}
Tone: {tone}
Target Audience: {audience}
Blog Summary: {blog_summary}

Requirements:
- Subject line (compelling, under 60 characters)
- Preview text (under 100 characters)
- Email body (150-200 words)
- Clear call to action button text

Format your response exactly like this:
SUBJECT: [subject line]
PREVIEW: [preview text]
BODY: [email body]
CTA: [call to action text]"""


def summary_prompt(blog_post: str) -> str:
    """
    Creates a short summary of the blog post.
    This summary is passed to both the social captions
    and email prompts — keeps the downstream prompts focused.
    """
    return f"""Summarise this blog post in 2-3 sentences.
Capture the main argument and value proposition.
Return only the summary — no labels or extra text.

Blog post:
{blog_post[:3000]}"""