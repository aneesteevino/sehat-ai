"""Narrow, application-owned emergency red-flag routing."""

import re
from dataclasses import dataclass
from typing import Literal

SafetyLevel = Literal["continue", "emergency"]


@dataclass(frozen=True, slots=True)
class SafetyDecision:
    level: SafetyLevel
    categories: tuple[str, ...]
    message: str
    actions: tuple[str, ...]


EMERGENCY_MESSAGE = (
    "This may describe a medical emergency. Contact your local emergency services now. "
    "Do not wait for this app or an online answer."
)


class RedFlagPolicy:
    """Conservative phrase rules; not a diagnosis or exhaustive triage system."""

    _rules = {
        "breathing": re.compile(
            r"\b(can(?:not|'t) breathe|stopped breathing|severe shortness of breath|choking)\b",
            re.IGNORECASE,
        ),
        "chest": re.compile(
            r"\b(severe chest (?:pain|pressure)|crushing chest pain)\b", re.IGNORECASE
        ),
        "consciousness": re.compile(
            r"\b(unconscious|unresponsive|won't wake up|will not wake up)\b", re.IGNORECASE
        ),
        "bleeding": re.compile(
            r"\b(severe bleeding|heavy bleeding|bleeding (?:will not|won't) stop)\b",
            re.IGNORECASE,
        ),
        "stroke": re.compile(
            r"\b(face (?:is )?droop(?:ing)?|one arm (?:is )?weak|slurred speech|"
            r"suddenly (?:unable|can't) to speak)\b",
            re.IGNORECASE,
        ),
    }

    def evaluate(self, text: str) -> SafetyDecision:
        categories = tuple(name for name, rule in self._rules.items() if rule.search(text))
        if categories:
            return SafetyDecision(
                level="emergency",
                categories=categories,
                message=EMERGENCY_MESSAGE,
                actions=(
                    "Contact local emergency services now.",
                    "Do not wait for Sehat AI to respond.",
                ),
            )
        return SafetyDecision(
            level="continue",
            categories=(),
            message="No configured emergency phrase was detected. This is not medical clearance.",
            actions=(),
        )
