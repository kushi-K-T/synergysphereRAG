import re
from typing import Tuple
from app.config.settings import settings

class PrivacyGate:
    def __init__(self):
        self.keywords = settings.sensitive_keyword_list
        self.patterns = [
            (re.compile(r'\b(?:sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,})\b'), "API key / Token pattern"),
            (re.compile(r'\b(?:\d{3}-\d{2}-\d{4})\b'), "SSN pattern"),
            (re.compile(r'\b(?:password|passwd|secret|apikey|api_key)\s*[:=]\s*\S+', re.IGNORECASE), "Credential assignment"),
            (re.compile(r'\b(?:confidential|proprietary|internal\s+use\s+only)\b', re.IGNORECASE), "Confidential classification pattern"),
            (re.compile(r'\b(?:our\s+project|our\s+codebase|local\s+system|our\s+architecture)\b', re.IGNORECASE), "Internal system reference"),
            (re.compile(r'\b(?:my\s+document|uploaded\s+file|private\s+doc)\b', re.IGNORECASE), "Private document reference")
        ]

    def evaluate(self, query: str) -> Tuple[bool, str]:
        normalized = query.lower()

        # Check explicit sensitive keywords first
        for kw in self.keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', normalized):
                return True, f"Deterministic match on sensitive keyword: '{kw}'"

        # Check regex security patterns
        for pattern, label in self.patterns:
            match = pattern.search(query)
            if match:
                return True, f"Security pattern matched: {label} ('{match.group(0)}')"

        return False, "Query contains no protected tokens or private indicators"

privacy_gate = PrivacyGate()
