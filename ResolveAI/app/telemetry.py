from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


def configure_telemetry():

    resource = Resource.create({
        "service.name": "resolveai",
        "service.version": "0.1",
        "deployment.environment": "development"
    })

    tracer_provider = TracerProvider(
        resource=resource
    )

    tracer_provider.add_span_processor(
        SimpleSpanProcessor(
            ConsoleSpanExporter()
        )
    )

    trace.set_tracer_provider(tracer_provider)

    return tracer_provider