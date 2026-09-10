from fastapi import FastAPI, HTTPException

from app.telemetry import configure_telemetry

from opentelemetry import trace

from services.splunk_service import SplunkService

from services.evidence_provider import EvidenceProvider


# ---------------------------------------------------------
# ResolveAI Application
# ---------------------------------------------------------

app = FastAPI(
    title="ResolveAI"
)


# ---------------------------------------------------------
# OpenTelemetry Configuration
# ---------------------------------------------------------

configure_telemetry(app)

tracer = trace.get_tracer("resolveai")


# ---------------------------------------------------------
# Splunk Integration
# ---------------------------------------------------------

evidence_provider: EvidenceProvider = SplunkService()


# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "application": "ResolveAI",
        "version": "0.1",
        "status": "running"
    }


@app.get("/health")
def health():

    with tracer.start_as_current_span("resolveai.health.check"):

        return {
            "status": "UP"
        }


@app.get("/resolve/{transaction_id}")
def resolve_transaction(transaction_id: str):

    try:
        result = evidence_provider.search_transaction(transaction_id)

        return {
            "transaction_id": transaction_id,
            "source": "Splunk",
            "evidence": result
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )