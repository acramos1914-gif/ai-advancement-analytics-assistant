"""Optional OpenAI-compatible provider using only privacy-safe aggregates."""

from __future__ import annotations

import os

import requests

from .ai_provider import AIProvider
from .prompting import build_prompt, question_is_supported


class LiveProvider(AIProvider):
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required for live AI mode.")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    def generate(self, task: str, analytics: dict) -> str:
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "temperature": 0, "messages": [{"role": "user", "content": build_prompt(task, analytics)}]},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def answer(self, question: str, analytics: dict) -> str:
        if not question_is_supported(question):
            return "This question requires unsupported or record-level data and was not sent to the AI provider."
        return self.generate(question, analytics)

