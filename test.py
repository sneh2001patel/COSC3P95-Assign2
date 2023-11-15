from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Set up the Jaeger exporter
jaeger_exporter = JaegerExporter(service_name="my-python-service")

# Set up the tracer provider with the Jaeger exporter
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(SimpleSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(tracer_provider)

# Get a tracer
tracer = trace.get_tracer(__name__)

# Instrument your code
with tracer.start_as_current_span("my-span"):
    # Your code logic goes here
    print("Hello, OpenTelemetry!")
