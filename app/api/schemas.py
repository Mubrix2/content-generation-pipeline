# app/api/schemas.py
from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    topic: str = Field(
        min_length=5,
        max_length=300,
        description="The topic to generate content for",
        examples=["How AI is helping small businesses in Nigeria"],
    )
    tone: str = Field(
        default="professional",
        description="Writing tone: professional, casual, inspirational, educational",
    )
    audience: str = Field(
        default="general audience",
        max_length=100,
        description="Target audience for the content",
        examples=["Nigerian entrepreneurs and business owners"],
    )


class CaptionsOutput(BaseModel):
    linkedin: str
    twitter: str
    instagram: str


class EmailOutput(BaseModel):
    subject: str
    preview: str
    body: str
    cta: str


class GenerateResponse(BaseModel):
    topic: str
    tone: str
    audience: str
    outline: str
    blog_post: str
    summary: str
    captions: CaptionsOutput
    email: EmailOutput


class ToneOption(BaseModel):
    value: str
    description: str


class TonesResponse(BaseModel):
    tones: list[ToneOption]


class HealthResponse(BaseModel):
    status: str
    env: str