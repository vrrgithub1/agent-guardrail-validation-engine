"""Utilities for checking prompt text against known malicious patterns.

This module provides a lightweight AST-style guardrail inspector that flags
suspicious instructions and returns a validation result with threat details.
"""

import re
from pydantic import BaseModel, Field

class GuardrailValidationResult(BaseModel):
    is_safe: bool
    detected_threats: list[str] = Field(default_factory=list)
    sanitized_prompt: str

class ASTInspector:
    def __init__(self):
        # Known prompt injection and system override patterns
        self.forbidden_patterns = [
            r"ignore previous instructions",
            r"disregard prior commands",
            r"system prompt override",
            r"you are now in developer mode",
            r"jailbreak",
            r"drop table",
            r"exec\s*\(",
            r"eval\s*\("
        ]

    def inspect_prompt(self, prompt: str) -> GuardrailValidationResult:
        threats = []
        normalized_prompt = prompt.lower()

        # Check against malicious patterns
        for pattern in self.forbidden_patterns:
            if re.search(pattern, normalized_prompt):
                threats.append(f"Forbidden Pattern Detected: '{pattern}'")

        is_safe = len(threats) == 0
        return GuardrailValidationResult(
            is_safe=is_safe,
            detected_threats=threats,
            sanitized_prompt=prompt if is_safe else ""
        )
