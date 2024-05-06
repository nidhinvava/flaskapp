from flask import Flask, render_template
from prometheus_flask_exporter import PrometheusMetrics
import time

app = Flask(__name__)
PrometheusMetrics(app)

# Record the start time
start_time = time.time()

# Define how long we wait until the app is ready
initialization_period = 30  # seconds

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hello')
def hello_world():
    return render_template('hello.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/health')
def health_check():
    return {'status': 'UP'}, 200

@app.route('/startup')
def startup_probe():
    # Check if the initialization period has passed
    current_time = time.time()
    if (current_time - start_time) > initialization_period:
        return {'status': 'ready'}, 200
    else:
        return {'status': 'initializing'}, 503

@app.route('/ready')
def readiness_probe():
    # This uses the same logic as startup_probe, but could be adapted to different checks in the future
    current_time = time.time()
    if (current_time - start_time) > initialization_period:
        return {'status': 'ready'}, 200
    else:
        return {'status': 'initializing'}, 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)