# app.py
import os
from flask import Flask  # import flask
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = Flask(__name__)  # create an app instance

trace.set_tracer_provider(TracerProvider())

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

trace.get_tracer_provider().add_span_processor(
   BatchSpanProcessor(OTLPSpanExporter(endpoint=os.environ["LMOTEL_ENDPOINT"], insecure=True))
)

FlaskInstrumentor().instrument_app(app)


@app.route("/hello")
def hello():
    return "Hello World!"


if __name__ == "__main__":  # on running python app.py
    app.run()  # run the flask app
