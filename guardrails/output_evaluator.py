"""Grounding checks for evaluating model output against provided context.

This module estimates whether a generated response stays grounded in source
context and flags potential hallucinations when semantic overlap is low.
"""

from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    is_grounded: bool
    grounding_score: float = Field(ge=0.0, le=1.0)
    detected_hallucinations: list[str] = Field(default_factory=list)

class OutputEvaluator:
    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def evaluate_grounding(self, context: str, response: str) -> EvaluationResult:
        """Evaluates whether the generated model response is grounded in the provided context."""
        context_words = set(context.lower().split())
        response_words = set(response.lower().split())

        if not response_words:
            return EvaluationResult(
                is_grounded=False,
                grounding_score=0.0,
                detected_hallucinations=["Empty response received."]
            )

        # Basic overlap ratio score calculation
        overlap = response_words.intersection(context_words)
        score = len(overlap) / len(response_words)

        hallucinations = []
        if score < self.threshold:
            hallucinations.append(f"Low semantic overlap with context payload (Score: {score:.2f})")

        return EvaluationResult(
            is_grounded=score >= self.threshold,
            grounding_score=round(score, 2),
            detected_hallucinations=hallucinations
        )