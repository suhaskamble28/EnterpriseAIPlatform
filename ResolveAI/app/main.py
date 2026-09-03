from fastapi import FastAPI

from app.telemetry import configure_telemetry

from opentelemetry import trace


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