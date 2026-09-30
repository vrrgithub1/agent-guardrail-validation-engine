"""FastAPI entry point for the AI guardrail validation service.

This service exposes endpoints for prompt validation, PII sanitization, and
security audit handling through the orchestrator pipeline.
"""

import sys
import os

# Add root directory to path for clean imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, status
from engine.orchestrator import GuardrailOrchestrator, PromptValidationRequest, PromptValidationResponse

app = FastAPI(
    title="Adversarial AI Agent Guardrail & Validation Engine",
    description="Real-time Prompt Guardrails, PII Sanitization, and Data Vault Audit Engine",
    version="1.0.0"
)

orchestrator = GuardrailOrchestrator()

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "service": "agent-guardrail-validation-engine"}

@app.post(
    "/api/v1/guardrails/validate",
    response_model=PromptValidationResponse,
    status_code=status.HTTP_200_OK
)
def validate_prompt(request: PromptValidationRequest):
    if not request.user_prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User prompt cannot be empty."
        )
    
    response = orchestrator.process_prompt(request)
    return response