from fastapi import FastAPI, HTTPException

from app.telemetry import configure_telemetry

from opentelemetry import trace

from services.splunk_service import SplunkService
from services.evidence_provider import EvidenceProvider
from services.redis_service import RedisService


app = FastAPI(title="ResolveAI")

configure_telemetry(app)

tracer = trace.get_tracer("resolveai")

evidence_provider: EvidenceProvider = SplunkService()
redis_service = RedisService()

CACHE_TTL_SECONDS = 300


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
        return {"status": "UP"}


@app.get("/resolve/{transaction_id}")
def resolve_transaction(transaction_id: str):

    cache_key = f"resolveai:evidence:{transaction_id}"

    # 1. Try Redis cache
    cached_result = redis_service.get_json(cache_key)

    if cached_result is not None:
        return {
            "transaction_id": transaction_id,
            "source": "Redis",
            "cache": "HIT",
            "evidence": cached_result
        }

    # 2. Cache miss → retrieve authoritative evidence from Splunk
    try:
        result = evidence_provider.search_transaction(transaction_id)

        # 3. Cache the normalized evidence
        redis_service.set_json(
            cache_key,
            result,
            CACHE_TTL_SECONDS
        )

        return {
            "transaction_id": transaction_id,
            "source": "Splunk",
            "cache": "MISS",
            "evidence": result
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc)
        )