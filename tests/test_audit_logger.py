import sys
import os

# Dynamically add root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data_vault.audit_logger import AuditLogger

def test_audit_record_creation():
    logger = AuditLogger()
    record = logger.build_audit_record(
        invocation_id="INV_2026_0930_001",
        is_safe=False,
        threats=["Forbidden Pattern Detected: 'ignore previous instructions'"],
        sanitized_prompt=""
    )
    
    print("--- Data Vault Audit Record Test ---")
    print(f"HK_INVOCATION_ID : {record.hk_invocation_id}")
    print(f"LOAD_TIMESTAMP   : {record.load_timestamp}")
    print(f"IS_SAFE          : {record.is_safe}")
    print(f"THREATS          : {record.detected_threats}")

if __name__ == "__main__":
    test_audit_record_creation()