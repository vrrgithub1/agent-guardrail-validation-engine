"""Coordinates prompt validation, PII sanitization, and audit record creation.

This module orchestrates the security pipeline for incoming user prompts by
inspecting for malicious patterns, sanitizing sensitive content, and logging the
result for traceability.
"""

import uuid
from pydantic import BaseModel
from guardrails.ast_inspector import ASTInspector
from guardrails.pii_sanitizer import PIISanitizer
from data_vault.audit_logger import AuditLogger, DataVaultAuditRecord

class PromptValidationRequest(BaseModel):
    user_prompt: str
    client_id: str = "DEFAULT_CLIENT"

class PromptValidationResponse(BaseModel):
    invocation_id: str
    is_safe: bool
    detected_threats: list[str]
    sanitized_prompt: str
    audit_record: DataVaultAuditRecord

class GuardrailOrchestrator:
    def __init__(self):
        self.inspector = ASTInspector()
        self.sanitizer = PIISanitizer()
        self.audit_logger = AuditLogger()

    def process_prompt(self, request: PromptValidationRequest) -> PromptValidationResponse:
        invocation_id = f"INV_{uuid.uuid4().hex[:12].upper()}"
        
        # 1. AST Inspection
        ast_result = self.inspector.inspect_prompt(request.user_prompt)
        
        # 2. PII Sanitization (if safe)
        sanitized_prompt = ""
        if ast_result.is_safe:
            sanitized_prompt = self.sanitizer.sanitize(request.user_prompt)
            
        # 3. Construct Data Vault Audit Entry
        audit_record = self.audit_logger.build_audit_record(
            invocation_id=invocation_id,
            is_safe=ast_result.is_safe,
            threats=ast_result.detected_threats,
            sanitized_prompt=sanitized_prompt
        )

        return PromptValidationResponse(
            invocation_id=invocation_id,
            is_safe=ast_result.is_safe,
            detected_threats=ast_result.detected_threats,
            sanitized_prompt=sanitized_prompt,
            audit_record=audit_record
        )