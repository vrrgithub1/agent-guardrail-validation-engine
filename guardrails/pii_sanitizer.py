"""PII redaction helpers for sanitizing sensitive user input.

This module detects common personally identifiable information in text and
replaces it with anonymized values before the content is processed further.
"""

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIISanitizer:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def sanitize(self, text: str) -> str:
        # Analyze text for PII entities
        results = self.analyzer.analyze(
            text=text,
            entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "US_SSN"],
            language="en"
        )
        # Anonymize detected entities
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        return anonymized_result.text
