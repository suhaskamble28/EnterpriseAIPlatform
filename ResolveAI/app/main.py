from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.telemetry import configure_telemetry

from opentelemetry import trace


# ---------------------------------------------------------
# OpenTelemetry
# ---------------------------------------------------------

configure_telemetry()

tracer = trace.get_tracer("resolveai")
# ---------------------------------------------------------
# ResolveAI Application
# ---------------------------------------------------------

app = FastAPI(
    title="ResolveAI"
)


# ---------------------------------------------------------
# OpenTelemetry FastAPI Instrumentation
# ---------------------------------------------------------

FastAPIInstrumentor.instrument_app(app)


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