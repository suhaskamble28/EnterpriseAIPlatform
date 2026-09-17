from fastapi import FastAPI, HTTPException

from app.telemetry import configure_telemetry

from opentelemetry import trace

from langsmith import traceable

from services.splunk_service import SplunkService
from services.evidence_provider import EvidenceProvider
from services.redis_service import RedisService
from services.llm_service import LLMService

from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


app = FastAPI(title="ResolveAI")

configure_telemetry(app)

tracer = trace.get_tracer("resolveai")

evidence_provider: EvidenceProvider = SplunkService()
redis_service = RedisService()
llm_service = LLMService()


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
    
@traceable(
    name="agent.investigation",
    run_type="chain",
)

@traceable(
    name="tool.redis.get",
    run_type="tool",
    process_outputs=lambda result: {
        "cache_hit": result is not None
    },
)

def traced_redis_get(cache_key: str):
    return redis_service.get_json(cache_key)

@traceable(
    name="tool.splunk.search",
    run_type="tool",
    process_outputs=lambda result: {
        "result_count": 1 if result is not None else 0
    },
)
def traced_splunk_search(transaction_id: str):
    return evidence_provider.search_transaction(transaction_id)

def investigate_transaction(transaction_id: str):

    cache_key = f"resolveai:evidence:{transaction_id}"

    # 1. Try Redis cache
   # cached_result = redis_service.get_json(cache_key)
    cached_result = traced_redis_get(cache_key)

    if cached_result is not None:

        diagnosis = llm_service.diagnose(cached_result)   # added for LLM
        return {
            "source": "Redis",
            "cache": "HIT",
            "evidence": cached_result,
             "diagnosis": diagnosis,   # Added for LLM
        }

    # 2. Cache miss → retrieve authoritative evidence from Splunk
    try:
       # result = evidence_provider.search_transaction(transaction_id)

        result = traced_splunk_search(transaction_id)

        # 3. Cache normalized evidence
        redis_service.set_json(
            cache_key,
            result,
            CACHE_TTL_SECONDS,
        )

        diagnosis = llm_service.diagnose(result)   # added for LLM

        return {
            "source": "Splunk",
            "cache": "MISS",
            "evidence": result,
            "diagnosis": diagnosis,                 # added for LLM
        }

    except ValueError as exc:
        raise exc

@app.get("/resolve/{transaction_id}")
def resolve_transaction(transaction_id: str):

    try:
        result = investigate_transaction(transaction_id)

        return {
            "transaction_id": transaction_id,
            **result,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )