# SynergySphere Architecture Specification

## Isolated Multi-Path Intelligence
SynergySphere enforces strict security compartmentalization between private internal workflows and external cloud providers.

### Core Guarantees:
1. **Confidential Isolation**: Documents indexed inside ChromaDB are accessible only by the local Ollama LLM.
2. **Deterministic Routing**: Requests containing internal project tokens or confidential phrases are forced into Path A (Local Processing).
3. **Zero Fallback**: If Ollama goes offline, internal queries fail closed. No sensitive query is forwarded to external providers.
