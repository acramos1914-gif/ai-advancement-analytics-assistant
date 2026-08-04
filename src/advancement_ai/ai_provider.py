"""Provider-independent AI interface."""

from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    @abstractmethod
    def generate(self, task: str, analytics: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def answer(self, question: str, analytics: dict) -> str:
        raise NotImplementedError

