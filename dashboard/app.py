from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

SERVERS = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

LOAD_BALANCER = "http://localhost:8000"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/metrics")
def metrics():

    server_data = []

    for server in SERVERS:
        try:
            res = requests.get(server + "/metrics")
            server_data.append(res.json())
        except:
            server_data.append({"cpu_load":0,"active_connections":0})

    lb_stats = requests.get(LOAD_BALANCER + "/stats").json()
    distribution = requests.get(LOAD_BALANCER + "/distribution").json()

    return jsonify({
        "servers": server_data,
        "stats": lb_stats,
        "distribution": distribution
    })

if __name__ == "__main__":
    app.run(port=9000)