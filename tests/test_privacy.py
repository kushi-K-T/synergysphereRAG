from app.security.privacy_gate import privacy_gate

def test_privacy_gate_identifies_keywords():
    is_sensitive, reason = privacy_gate.evaluate("Show our internal architecture and confidential budget.")
    assert is_sensitive is True
    assert "confidential" in reason or "internal" in reason

def test_privacy_gate_allows_general_queries():
    is_sensitive, _ = privacy_gate.evaluate("Write a Python script for binary search.")
    assert is_sensitive is False
