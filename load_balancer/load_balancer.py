from flask import Flask, jsonify, request
import requests as http_requests
import time
import joblib
import numpy as np
import os
import threading

request_count = 0
total_response_time = 0
request_distribution = {
    "http://localhost:5001": 0,
    "http://localhost:5002": 0,
    "http://localhost:5003": 0
}

app = Flask(__name__)

servers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

server_metrics = {
    "http://localhost:5001": {"cpu": 50, "conn": 0},
    "http://localhost:5002": {"cpu": 50, "conn": 0},
    "http://localhost:5003": {"cpu": 50, "conn": 0}
}

# Load the ML model using a path relative to this file's location
model_path = os.path.join(os.path.dirname(__file__), "ml", "model.pkl")
model = joblib.load(model_path)
print(f"ML model loaded from {model_path}")

current = 0
algorithm = "ml"


def round_robin():
    global current
    server = servers[current]
    current = (current + 1) % len(servers)
    return server


def least_connection():
    min_connections = float('inf')
    selected_server = None

    for server in servers:
        try:
            response = http_requests.get(server + "/metrics", timeout=2)
            connections = response.json()["active_connections"]
        except Exception:
            connections = float('inf')

        if connections < min_connections:
            min_connections = connections
            selected_server = server

    return selected_server


def ml_balancer():
    metrics = []

    for server in servers:
        cpu = server_metrics[server]["cpu"]
        conn = server_metrics[server]["conn"]
        metrics.extend([cpu, conn])

    features = np.array(metrics).reshape(1, -1)
    prediction = model.predict(features)[0]

    return servers[prediction]


def update_metrics():
    """Background thread that polls server metrics every 2 seconds."""
    global server_metrics
    print("Background metrics collector started")

    while True:
        for server in servers:
            try:
                response = http_requests.get(server + "/metrics", timeout=2)
                data = response.json()

                server_metrics[server]["cpu"] = data.get("cpu_load", 50)
                server_metrics[server]["conn"] = data.get("active_connections", 0)
            except Exception:
                pass

        time.sleep(2)


@app.route("/")
def route_request():
    global request_count, total_response_time

    start = time.time()

    if algorithm == "round_robin":
        server = round_robin()
    elif algorithm == "least_connection":
        server = least_connection()
    else:
        server = ml_balancer()

    response = http_requests.get(server)

    end = time.time()
    response_time = end - start

    request_count += 1
    total_response_time += response_time
    request_distribution[server] = request_distribution.get(server, 0) + 1

    return jsonify(response.json())


@app.route("/stats")
def stats():
    if request_count == 0:
        avg_time = 0
    else:
        avg_time = total_response_time / request_count

    return jsonify({
        "total_requests": request_count,
        "average_response_time": avg_time
    })


@app.route("/algorithm")
def set_algorithm():
    """Switch the active load balancing algorithm at runtime."""
    global algorithm

    new_algo = request.args.get("set")

    if new_algo in ("ml", "round_robin", "least_connection"):
        algorithm = new_algo
        return jsonify({"algorithm": algorithm, "status": "updated"})
    else:
        return jsonify({
            "error": "Invalid algorithm. Use: ml, round_robin, or least_connection",
            "current": algorithm
        }), 400


@app.route("/distribution")
def distribution():
    """Return the request distribution across servers."""
    return jsonify({
        "Server 1": request_distribution.get("http://localhost:5001", 0),
        "Server 2": request_distribution.get("http://localhost:5002", 0),
        "Server 3": request_distribution.get("http://localhost:5003", 0)
    })


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "algorithm": algorithm})


if __name__ == "__main__":
    thread = threading.Thread(target=update_metrics)
    thread.daemon = True
    thread.start()

    print(f"Load Balancer starting on port 8000 (algorithm: {algorithm})")
    app.run(port=8000)
