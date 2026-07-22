from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class LifeDomain(str, Enum):
    CAREER = "career"
    FINANCE = "finance"
    MARRIAGE = "marriage"
    RELATIONSHIPS = "relationships"
    CHILDREN = "children"
    HEALTH = "health"
    EDUCATION = "education"
    BUSINESS = "business"
    SPIRITUALITY = "spirituality"


@dataclass(frozen=True)
class Evidence:
    factor: str
    source: str  # e.g. "planet:Jupiter", "house:10", "sign:Sagittarius", "yoga:Raj Yoga"
    impact: float  # -1.0 to +1.0
    explanation: str


@dataclass(frozen=True)
class ReasoningStep:
    step: int
    description: str
    detail: str


@dataclass(frozen=True)
class PlanetaryEvidence:
    planet: str
    house: int | None = None
    sign: str | None = None
    isRetrograde: bool = False
    role: str = ""  # e.g. "lord_of_10th", "yoga_karaka"
    contribution: float = 0.0  # -1.0 to +1.0


@dataclass
class DomainResult:
    domain: str
    score: float  # 0-10
    confidence: float  # 0-1
    supportingFactors: list[Evidence] = field(default_factory=list)
    challengingFactors: list[Evidence] = field(default_factory=list)
    planetaryEvidence: list[PlanetaryEvidence] = field(default_factory=list)
    reasoningSteps: list[ReasoningStep] = field(default_factory=list)
    explanationSummary: str = ""
