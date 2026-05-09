# tests/test_pipeline.py
import pytest
from unittest.mock import patch
from app.services.pipeline import (
    run_pipeline,
    _parse_captions,
    _parse_email,
)


def test_parse_captions_correctly():
    raw = """LINKEDIN: Exciting news for entrepreneurs! Check this out. #AI #Business #Growth
TWITTER: AI is changing business. Read more! #AI #Startups
INSTAGRAM: Transform your workflow today! #AI #Tech #Business #Nigeria #Growth"""

    result = _parse_captions(raw)
    assert "Exciting news" in result["linkedin"]
    assert "#AI #Business #Growth" in result["linkedin"]
    assert "AI is changing" in result["twitter"]
    assert "Transform your workflow" in result["instagram"]


def test_parse_email_correctly():
    raw = """SUBJECT: How AI Is Changing Nigerian Business
PREVIEW: Discover tools that save you time
BODY: Dear reader, AI tools are transforming how businesses operate. 
From automation to data analysis, the possibilities are endless.
CTA: Read the Full Article"""

    result = _parse_email(raw)
    assert result["subject"] == "How AI Is Changing Nigerian Business"
    assert result["preview"] == "Discover tools that save you time"
    assert "AI tools" in result["body"]
    assert result["cta"] == "Read the Full Article"


def test_pipeline_raises_on_empty_topic():
    with pytest.raises(ValueError, match="Topic cannot be empty"):
        run_pipeline(topic="", tone="professional", audience="entrepreneurs")


@patch("app.services.pipeline.generate")
def test_pipeline_runs_five_steps(mock_generate):
    """Confirm pipeline calls generate exactly 5 times."""
    mock_generate.side_effect = [
        "Outline content",           # Step 1
        "Full blog post content",    # Step 2
        "Two sentence summary.",     # Step 3
        "LINKEDIN: Caption\nTWITTER: Tweet\nINSTAGRAM: Gram",  # Step 4
        "SUBJECT: Sub\nPREVIEW: Pre\nBODY: Body\nCTA: Click",  # Step 5
    ]

    result = run_pipeline(
        topic="AI tools for small businesses",
        tone="professional",
        audience="Nigerian entrepreneurs",
    )

    assert mock_generate.call_count == 5
    assert result["outline"] == "Outline content"
    assert result["blog_post"] == "Full blog post content"
    assert result["summary"] == "Two sentence summary."
    assert result["captions"]["linkedin"] == "Caption"
    assert result["email"]["subject"] == "Sub"


@patch("app.services.pipeline.generate")
def test_pipeline_returns_all_keys(mock_generate):
    mock_generate.side_effect = [
        "outline", "blog", "summary",
        "LINKEDIN: l\nTWITTER: t\nINSTAGRAM: i",
        "SUBJECT: s\nPREVIEW: p\nBODY: b\nCTA: c",
    ]

    result = run_pipeline("topic", "casual", "audience")
    expected_keys = [
        "topic", "tone", "audience", "outline",
        "blog_post", "summary", "captions", "email",
    ]
    for key in expected_keys:
        assert key in result