# Day 65 — AI Agent Observability

## Objective

Implement AI Agent Observability for ResolveAI by combining:

- LangSmith for AI/agent execution observability
- OpenTelemetry for technical telemetry
- Prometheus for AI operational metrics
- Grafana for operational visualization

The objective is to observe not only whether ResolveAI is running, but also what the AI agent did, which tools it used, which LLM was invoked, token consumption,
latency, and AI-related failures.

---

## 1. ResolveAI AI Agent Flow

```text
Customer Care Request
        |
        v
ResolveAI
        |
        v
agent.investigation
        |
        +---- tool.redis.get
        |
        +---- tool.splunk.search
        |
        +---- llm.diagnosis
        |
        v
Diagnosis / Result


Day-65-AI-Agent-Observability.md
│
├── 1. Objective
├── 2. ResolveAI AI Agent Flow
├── 3. AI Observability Architecture
├── 4. LangSmith Observability
├── 5. LLM Observability
├── 6. Prometheus AI Metrics
├── 7. Prometheus Scraping
├── 8. Grafana AI/LLM Dashboard
├── 9. Failure Injection Exercise
├── 10. Trace vs Metrics
├── 11. Important Observability Principle
├── 12. Metrics vs Individual Traces
├── 13. ResolveAI Observability Architecture
├── 14. Key Day-65 Learning
├── 15. Future Extensions
└── Day-65 Status