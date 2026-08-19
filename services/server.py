from flask import Flask, jsonify
import random
import sys
import time

app = Flask(__name__)

server_id = sys.argv[1]
active_connections = 0
cpu_load = random.randint(10, 90)


@app.route("/")
def handle_request():
    global active_connections, cpu_load
    active_connections += 1

    cpu_load = random.randint(10, 90)
    time.sleep(random.uniform(0.1, 0.5))  # simulate processing delay

    response = {
        "server_id": server_id,
        "cpu_load": cpu_load,
        "active_connections": active_connections
    }

    active_connections -= 1
    return jsonify(response)


@app.route("/metrics")
def metrics():
    return jsonify({
        "server_id": server_id,
        "cpu_load": cpu_load,
        "active_connections": active_connections
    })


if __name__ == "__main__":
    port = int(sys.argv[2])
    print(f"Server {server_id} starting on port {port}")
    app.run(port=port)
