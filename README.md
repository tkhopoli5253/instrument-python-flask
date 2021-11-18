**# app.py**

**Prerequisites:**
```
1. We need python installed. (3.7 version would be great).
2. Pycharm community ide.
3. Once you have the ide, create a project. I named mine instrument-flask-app.
4. Virtualenv if youre using pycharm you dont have to worry about this.
```

**1. Initialize the project:**

We would need a couple of libraries for all this to work.

>pip install flask.  
>pip install opentelemetry-api.  
>pip install opentelemetry-sdk.  
>pip install opentelemetry-opentelemetry-instrumentation-flask.  
>pip install opentelemetry-exporter-otlp.  

**2. Create a file app. Py under the root project directory instrument-flask-app:**

>instrument-flask-app  
|___ app. Py

**3. Import the following libraries:**

>from flask import flask  
from opentelemetry import trace  
from opentelemetry.sdk.trace import tracerprovider  
from opentelemetry.instrumentation.flask import flaskinstrumentor  
from opentelemetry.sdk.trace.export import batchspanprocessor, consolespanexporter  
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import otlpspanexporter  

**4. Create a flask app instance:**

>app = flask(__name__)

**5. Construct trace provider:**

>trace. Set_tracer_provider(tracerprovider())

**6. Init span exporter:**

The exporter is the component in sdk responsible for exporting the telemetry signal (trace) out of the application to a remote backend, log to a file, stream to stdout. Etc. In this example, we are creating a grpc exporter to send out traces to an opentelemetry receiver backend running on localhost. Possibly an opentelemetry collector.
>trace.get_tracer_provider().add_span_processor(batchspanprocessor
(otlpspanexporter(endpoint=os.environ.get("LM_OTEL_ENDPOINT"), insecure=true)))

Note: optionally, you can also print the traces emitted from the application on the console by doing the following:  
>trace. Get_tracer_provider(). Add_span_processor(batchspanprocessor(consolespanexporter()))

**7. Setting up otel collector endpoint:**
You will have to set the environment variable lmotel_endpoint which the endpoint of the otel collector to the which the traces would be emitted by following:
>export LM_OTEL_ENDPOINT= http://host:port

**8. Creating resource detector:**
The resource describes the object that generated the telemetry signals. Essentially, it must be the name of the service or application.

>service.namespace: it is used to group the services. For example, you can use this to distinguish services across environments like qa, uat, prod.  
service.name: it is the logical name of the service.  
host.name: name of the host where the service is running

Set the environment variable as following:
>export otel_resource_attributes=service.namespace=opentelemetry, service.name=instrument-flask-app, host.name=localhost

**9. Auto-instrumenting the flask app object:**

>flaskinstrumentor().instrument_app(app)

**10. Lets define an endpoint to test the instrumentation:**

>@app. Route("/hello")  
def hello():  
return "hello world!"  

**11. Finally running the app (flask app by default runs on port 5000):**

>if __name__ == "__main__": 	# on running python app. Py  
app.run() 		  	            # run the flask app
