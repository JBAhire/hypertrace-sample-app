from flask import Flask, request
import pandas as pd
import book_ratings
import recommendations
from twilio.twiml.messaging_response import MessagingResponse

import requests

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)
from opentelemetry.exporter import zipkin
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

trace.set_tracer_provider(TracerProvider())

zipkin_exporter = zipkin.ZipkinSpanExporter(
    service_name="zipkin-BookWorm-service",
)

# Create a BatchExportSpanProcessor and add the exporter to it
span_processor = BatchExportSpanProcessor(zipkin_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)



app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
@app.route('/sms', methods=['POST'])
def sms():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("incoming-request"):
        resp = MessagingResponse()
        inbMsg = request.values.get('Body')
    with tracer.start_as_current_span("prediction"):
        rec = recommendations.corpus_recommendations(inbMsg)
        df = pd.read_csv('clean_books.csv')
    with tracer.start_as_current_span("outgoing-request"):
        resp.message('Recommendations based on your input:')
        for i in rec:
            resp.message (df['original_title'].iloc[i+2]+ "\n")
    return str(resp)
 

if __name__ == '__main__':
    app.run()