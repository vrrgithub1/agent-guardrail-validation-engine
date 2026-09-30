"""Audit logging utilities for recording prompt security results.

This module creates deterministic audit records for each invocation, including
safety status, detected threats, and sanitized prompt metadata.
"""

import hashlib
from datetime import datetime
from pydantic import BaseModel

class DataVaultAuditRecord(BaseModel):
    hk_invocation_id: str
    invocation_id: str
    load_timestamp: str
    record_source: str
    is_safe: bool
    detected_threats: str
    sanitized_prompt: str

class AuditLogger:
    def __init__(self, record_source: str = "AGENT_GUARDRAIL_ENGINE"):
        self.record_source = record_source

    def generate_hash_key(self, business_key: str) -> str:
        """Generates deterministic SHA-256 hash key according to Data Vault 2.0 standards."""
        return hashlib.sha256(business_key.strip().upper().encode('utf-8')).hexdigest()

    def build_audit_record(
        self,
        invocation_id: str,
        is_safe: bool,
        threats: list[str],
        sanitized_prompt: str
    ) -> DataVaultAuditRecord:
        
        hk_invocation_id = self.generate_hash_key(invocation_id)
        load_timestamp = datetime.utcnow().isoformat()
        
        return DataVaultAuditRecord(
            hk_invocation_id=hk_invocation_id,
            invocation_id=invocation_id,
            load_timestamp=load_timestamp,
            record_source=self.record_source,
            is_safe=is_safe,
            detected_threats="; ".join(threats) if threats else "NONE",
            sanitized_prompt=sanitized_prompt
        )