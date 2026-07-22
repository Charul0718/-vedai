from __future__ import annotations

from typing import Any

from knowledge_engine import KnowledgeEngine, get_engine

from .types import LifeDomain, DomainResult
from .domain_evaluator import evaluate_domain


_ALL_DOMAINS = list(LifeDomain)


class ExplainabilityEngine:
    """Deterministic explainability engine for VedAI birth chart analysis.

    Produces structured, evidence-backed scores for every life domain
    without any LLM involvement. Every score traces back to specific
    planets, houses, signs, yogas, doshas, and the current dasha period.
    """

    def __init__(self, knowledge_engine: KnowledgeEngine | None = None):
        self._ke = knowledge_engine or get_engine()

    def evaluate_all(self, chart: dict) -> dict[str, DomainResult]:
        """Evaluate all 9 life domains from a birth chart.

        Args:
            chart: Output of astrology_engine.calculate_birth_chart()

        Returns:
            Dict mapping domain name -> DomainResult
        """
        results: dict[str, DomainResult] = {}
        for domain in _ALL_DOMAINS:
            results[domain.value] = evaluate_domain(chart, domain, self._ke)
        return results

    def evaluate(self, chart: dict, domain: str) -> DomainResult:
        """Evaluate a single life domain.

        Args:
            chart: Output of astrology_engine.calculate_birth_chart()
            domain: One of: career, finance, marriage, relationships, children,
                    health, education, business, spirituality

        Returns:
            DomainResult with score, confidence, evidence, and reasoning
        """
        ld = LifeDomain(domain)
        return evaluate_domain(chart, ld, self._ke)

    def to_dict(self, result: DomainResult) -> dict[str, Any]:
        """Convert a DomainResult to a JSON-serializable dict."""
        return {
            "domain": result.domain,
            "score": result.score,
            "confidence": result.confidence,
            "supportingFactors": [
                {
                    "factor": e.factor,
                    "source": e.source,
                    "impact": e.impact,
                    "explanation": e.explanation,
                }
                for e in result.supportingFactors
            ],
            "challengingFactors": [
                {
                    "factor": e.factor,
                    "source": e.source,
                    "impact": e.impact,
                    "explanation": e.explanation,
                }
                for e in result.challengingFactors
            ],
            "planetaryEvidence": [
                {
                    "planet": pe.planet,
                    "house": pe.house,
                    "sign": pe.sign,
                    "isRetrograde": pe.isRetrograde,
                    "role": pe.role,
                    "contribution": pe.contribution,
                }
                for pe in result.planetaryEvidence
            ],
            "reasoningSteps": [
                {
                    "step": rs.step,
                    "description": rs.description,
                    "detail": rs.detail,
                }
                for rs in result.reasoningSteps
            ],
            "explanationSummary": result.explanationSummary,
        }

    def evaluate_all_to_dict(self, chart: dict) -> dict[str, dict[str, Any]]:
        """Evaluate all domains and return as JSON-serializable dicts."""
        results = self.evaluate_all(chart)
        return {domain: self.to_dict(result) for domain, result in results.items()}
