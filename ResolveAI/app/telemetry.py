from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter
)


def configure_telemetry(app):

    resource = Resource.create({
        "service.name": "resolveai",
        "service.version": "0.1",
        "deployment.environment": "development"
    })

    tracer_provider = TracerProvider(
        resource=resource
    )

    otlp_exporter = OTLPSpanExporter(
        endpoint="http://localhost:4318/v1/traces"
    )

    span_processor = BatchSpanProcessor(
        otlp_exporter
    )

    tracer_provider.add_span_processor(
        span_processor
    )

    trace.set_tracer_provider(
        tracer_provider
    )

    FastAPIInstrumentor.instrument_app(app)

    return trace.get_tracer("resolveai")