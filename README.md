# 🧠 Intelligent Load Balancer

An ML-powered load balancer that uses a **Random Forest classifier** to intelligently route traffic across multiple backend servers based on real-time CPU load and connection metrics. Includes traditional algorithms (Round Robin, Least Connection) for benchmarking comparison.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-orange?logo=scikit-learn&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Benchmarks](#-benchmarks)
- [Docker & Kubernetes](#-docker--kubernetes)
- [Documentation](#-documentation)
- [License](#-license)

---

## ✨ Features

- **ML-Based Routing** — Random Forest model predicts the optimal server based on CPU load and active connections
- **Multiple Algorithms** — Switch between ML, Round Robin, and Least Connection strategies at runtime
- **Real-Time Dashboard** — Live monitoring with Chart.js showing server metrics and request distribution
- **Background Metrics Collection** — Asynchronous polling of server health every 2 seconds
- **Benchmarking Suite** — Compare algorithm performance with automated load testing
- **Docker & Kubernetes Ready** — Containerized deployment with Horizontal Pod Autoscaler (HPA) configs

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │   Dashboard     │
                    │  (Port 9000)    │
                    └────────┬────────┘
                             │ polls metrics
                             ▼
┌──────────┐      ┌─────────────────────┐      ┌──────────────┐
│  Client  │─────▶│   Load Balancer     │─────▶│  Server 1    │
│ Requests │      │    (Port 8000)      │      │  (Port 5001) │
└──────────┘      │                     │─────▶│──────────────│
                  │  ML / Round Robin   │      │  Server 2    │
                  │  / Least Connection │      │  (Port 5002) │
                  │                     │─────▶│──────────────│
                  └─────────────────────┘      │  Server 3    │
                    ▲ trained model             │  (Port 5003) │
                    │                           └──────────────┘
              ┌─────────────┐
              │  model.pkl  │
              │ (Random     │
              │  Forest)    │
              └─────────────┘
```

---

## 📁 Project Structure

```
intelligent-load-balancer/
├── load_balancer/
│   ├── load_balancer.py        # Core load balancer with ML, RR, LC algorithms
│   ├── algorithms/
│   │   ├── round_robin.py      # Round Robin algorithm (standalone)
│   │   └── least_connection.py # Least Connection algorithm (standalone)
│   ├── ml/
│   │   ├── train_model.py      # ML model training script
│   │   ├── predictor.py        # ML prediction wrapper class
│   │   └── model.pkl           # Trained model (generated, git-ignored)
│   └── utils/
│       ├── helpers.py          # Utility functions
│       └── metrics.py          # Response time calculation
├── services/
│   ├── server.py               # Backend Flask server (simulates workload)
│   └── simulator.py            # Benchmark / load testing script
├── dashboard/
│   ├── app.py                  # Dashboard Flask app
│   └── templates/
│       └── index.html          # Dashboard UI with Chart.js
├── docker/
│   ├── Dockerfile              # Container image definition
│   └── docker-compose.yml      # Multi-service orchestration
├── kubernetes/
│   ├── deployment.yaml         # K8s Deployment manifest
│   ├── service.yaml            # K8s Service manifest
│   └── hpa.yaml                # Horizontal Pod Autoscaler
├── docs/
│   ├── DEMO_GUIDE.md           # Step-by-step live demo guide
│   ├── architecture.png        # Architecture diagram
│   ├── workflow.png             # Workflow diagram
│   └── project_report.pdf      # Detailed project report
├── results/
│   ├── benchmark_results.csv   # Generated benchmark data
│   ├── graphs/                 # Generated performance graphs
│   └── screenshots/            # Dashboard screenshots
├── datasets/
│   └── training_data.csv       # Training dataset
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/intelligent-load-balancer.git
cd intelligent-load-balancer
pip install -r requirements.txt
```

### 2. Train the ML Model

```bash
python load_balancer/ml/train_model.py
```

This generates 5,000 synthetic samples and trains a Random Forest classifier (~93% accuracy). The model is saved to `load_balancer/ml/model.pkl`.

### 3. Start Backend Servers (3 terminals)

```bash
python services/server.py 1 5001
python services/server.py 2 5002
python services/server.py 3 5003
```

### 4. Start the Load Balancer

```bash
python load_balancer/load_balancer.py
```

### 5. Start the Dashboard

```bash
python dashboard/app.py
```

Open **http://localhost:9000** in your browser to see the real-time monitoring dashboard.

### 6. Send Requests

```bash
# Send a request (routed by ML model)
curl http://localhost:8000/

# Check stats
curl http://localhost:8000/stats

# Switch algorithm
curl http://localhost:8000/algorithm?set=round_robin
curl http://localhost:8000/algorithm?set=least_connection
curl http://localhost:8000/algorithm?set=ml

# View distribution
curl http://localhost:8000/distribution

# Health check
curl http://localhost:8000/health
```

### 7. Run Benchmarks

```bash
python services/simulator.py
```

---

## 📡 API Reference

### Load Balancer (Port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Route a request to the best backend server |
| `/stats` | GET | Get total requests and average response time |
| `/algorithm?set=<name>` | GET | Switch algorithm (`ml`, `round_robin`, `least_connection`) |
| `/distribution` | GET | Get request distribution across servers |
| `/health` | GET | Health check endpoint |

### Backend Servers (Ports 5001-5003)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Handle a request (returns server ID, CPU load, connections) |
| `/metrics` | GET | Get current server metrics |

### Dashboard (Port 9000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Real-time monitoring dashboard |
| `/metrics` | GET | Aggregated metrics from all servers |

---

## 📊 Benchmarks

| Algorithm | Avg Response Time | Requests/sec | Distribution |
|-----------|------------------|--------------|--------------|
| **Round Robin** | ~4.27s | ~0.23 | Even (33/34/33) |
| **Least Connection** | ~4.31s | ~0.09 | Varies by load |
| **ML (Random Forest)** | ~4.33s | Adaptive | Favors least-loaded |

> **Note:** ML has slightly higher latency due to model inference, but makes smarter routing decisions under varied load conditions.

---

## 🐳 Docker & Kubernetes

### Docker

```bash
cd docker
docker-compose up --build
```

### Kubernetes (Minikube)

```bash
# Start Minikube
minikube start

# Deploy
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Verify
kubectl get pods
kubectl get svc
kubectl get hpa
```

---

## 📚 Documentation

- [Live Demo Guide](docs/DEMO_GUIDE.md) — Step-by-step instructions for presenting a live demo
- [Architecture Diagram](docs/architecture.png)
- [Workflow Diagram](docs/workflow.png)
- [Project Report](docs/project_report.pdf)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
