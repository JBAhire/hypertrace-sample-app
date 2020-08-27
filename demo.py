from flask import Flask, request
import pandas as pd
import book_ratings
from twilio.twiml.messaging_response import MessagingResponse

import requests

import opentelemetry.ext.requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import SimpleExportSpanProcessor
from opentelemetry.ext.flask import FlaskInstrumentor
from opentelemetry.ext import jaeger

trace.set_tracer_provider(TracerProvider())


jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name="BookWorm-service", agent_host_name="localhost", agent_port=6831
)

trace.get_tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(jaeger_exporter)
)


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
@app.route('/sms', methods=['POST'])
def sms():
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("example-request"):
        resp = MessagingResponse()
        #hey = MessagingResponse()
        inbMsg = request.values.get('Body')
        book_list = book_ratings.get_matches(inbMsg)
        df = pd.read_csv('clean_books.csv')

        for i in book_list:
            resp.message(
                'Title of the book: ' + df['original_title'].iloc[i] + '\nWritten by: ' + df['authors'].iloc[i] +'\nAverage user rating: ' + str(df['average_rating'].iloc[i])+'\nReviewed by: '+ str(df['work_text_reviews_count'].iloc[i])+' people.\n ---------------------------------------')
    return str(resp)
 

if __name__ == '__main__':
    app.run()