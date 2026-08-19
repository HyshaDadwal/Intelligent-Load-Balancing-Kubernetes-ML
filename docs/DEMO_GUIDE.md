# 🎤 Live Demo Guide — Intelligent Load Balancer

> Follow these steps **exactly in order**. You need **5 terminal windows** open side by side (or use tabs). Each step tells you **what to type**, **what happens**, and **what to explain**.

---

## Before You Begin (Preparation)

1. Open your project folder in a terminal
2. Make sure Python 3.8+ is installed — verify with:
   ```
   python --version
   ```
3. Open **5 separate terminal windows** (or tabs) — label them mentally:
   - Terminal 1 → Server 1
   - Terminal 2 → Server 2
   - Terminal 3 → Server 3
   - Terminal 4 → Load Balancer
   - Terminal 5 → Dashboard
4. Keep a **browser tab** ready (you'll open the dashboard later)

---

## Step 1 — Install Dependencies
**🖥️ Use any terminal** | ⏱️ ~30 seconds

```bash
cd intelligent-load-balancer
pip install -r requirements.txt
```

**🗣️ What to say:**
> "First, we install the required Python libraries — Flask for the web servers, scikit-learn for the ML model, NumPy and Pandas for data processing."

**✅ You should see:** `Successfully installed flask-3.0.0 requests-2.31.0 numpy-1.26.2 ...`

---

## Step 2 — Train the ML Model
**🖥️ Use any terminal** | ⏱️ ~5 seconds

```bash
python load_balancer/ml/train_model.py
```

**🗣️ What to say:**
> "Now we train our Random Forest classifier. It generates 5,000 synthetic data samples — each sample has the CPU load and active connections of 3 servers. The model learns which server is the best to route to, based on a weighted score of CPU (60%) and connections (40%)."

**✅ You should see:**
```
[1/4] Generating synthetic training data (5000 samples)...  ✓
[2/4] Splitting into train/test sets (80/20)...             ✓
[3/4] Training Random Forest classifier...                  ✓
[4/4] Evaluating model performance...
      Test Accuracy: 0.93 (93%)
```

**🗣️ Point out:**
> "We get around 93% accuracy, and the model is saved as `model.pkl` for the load balancer to use."

---

## Step 3 — Start the 3 Backend Servers
**🖥️ Use Terminals 1, 2, 3** | ⏱️ ~5 seconds each

**Terminal 1:**
```bash
python services/server.py 1 5001
```

**Terminal 2:**
```bash
python services/server.py 2 5002
```

**Terminal 3:**
```bash
python services/server.py 3 5003
```

**🗣️ What to say:**
> "These are our 3 backend application servers. Each one simulates a real server — it tracks its own CPU load, memory usage, and active connections. They run on ports 5001, 5002, and 5003."

**✅ Each terminal should show:** `Server X starting on port 500X` and `Running on http://127.0.0.1:500X`

---

## Step 4 — Start the Load Balancer
**🖥️ Use Terminal 4** | ⏱️ ~3 seconds

```bash
python load_balancer/load_balancer.py
```

**🗣️ What to say:**
> "This is the core of our project — the intelligent load balancer. It loads the trained ML model and starts a background thread that polls all 3 servers every 2 seconds for their CPU and connection metrics. When a request comes in, it uses the ML model to predict which server is best."

**✅ You should see:**
```
ML model loaded from .../model.pkl
Background metrics collector started
Load Balancer starting on port 8000 (algorithm: ml)
```

---

## Step 5 — Start the Dashboard
**🖥️ Use Terminal 5** | ⏱️ ~3 seconds

```bash
python dashboard/app.py
```

**🗣️ What to say:**
> "Finally, we start our monitoring dashboard — a web UI that shows real-time server metrics and request distribution."

**✅ You should see:** `Dashboard starting on http://localhost:9000`

### 🌐 Now open your browser and go to: **http://localhost:9000**

**🗣️ What to say while showing the dashboard:**
> "This is our real-time monitoring dashboard. You can see:
> - **Server status cards** showing CPU load, memory, and connections for each server
> - **Charts** showing CPU load comparison and request distribution
> - **Statistics** panel with total requests and average response time
> - **Algorithm selector** — we can switch between ML, Round Robin, and Least Connection live"

---

## Step 6 — Demo the Load Balancer (Live Requests)
**🖥️ Open a 6th terminal (or use the browser)** | ⏱️ ~2 minutes

### 6a. Send a request using ML algorithm
```bash
curl http://localhost:8000/
```

**🗣️ What to say:**
> "When we send a request to the load balancer, it uses the ML model to pick the best server based on current metrics."

**✅ You'll see a JSON response showing which server was chosen, its CPU load, and processing time.**

### 6b. Check the stats
```bash
curl http://localhost:8000/stats
```
> "We can see total requests handled and average response time."

### 6c. Switch to Round Robin
```bash
curl http://localhost:8000/algorithm?set=round_robin
```
```bash
curl http://localhost:8000/
```
```bash
curl http://localhost:8000/
```
```bash
curl http://localhost:8000/
```

**🗣️ What to say:**
> "Now I've switched to Round Robin. Watch — it cycles through Server 1, then 2, then 3, in order. It doesn't care about load — it just rotates."

### 6d. Switch to Least Connection
```bash
curl http://localhost:8000/algorithm?set=least_connection
```
```bash
curl http://localhost:8000/
```

**🗣️ What to say:**
> "Least Connection picks whichever server has the fewest active connections right now."

### 6e. Switch back to ML
```bash
curl http://localhost:8000/algorithm?set=ml
```

**🗣️ What to say:**
> "And switching back to ML — the smart one that uses our trained model."

### 6f. Check distribution
```bash
curl http://localhost:8000/distribution
```

**🗣️ What to say:**
> "This shows how many requests each server received — you can see the ML algorithm favors the less-loaded servers."

### 🔄 **Keep the dashboard open** — it auto-refreshes every 2 seconds, so the audience can see the charts updating live as you send requests!

---

## Step 7 — Run the Benchmark
**🖥️ Use the 6th terminal** | ⏱️ ~2-3 minutes

```bash
python services/simulator.py
```

**🗣️ What to say:**
> "Now let's run our benchmark suite. This sends 100 concurrent requests for each of the 3 algorithms and compares their performance — average response time, throughput, and how they distribute traffic."

**✅ You should see output like:**
```
Running 100 requests with 'round_robin' algorithm...
  ✓ Completed: 100/100 successful
    Avg response time: ~4.27s
    Distribution: Server 1: 33, Server 2: 34, Server 3: 33

Running 100 requests with 'least_connection' algorithm...
  ✓ Completed: 100/100 successful
    Avg response time: ~4.31s

Running 100 requests with 'ml' algorithm...
  ✓ Completed: 100/100 successful
    Avg response time: ~4.33s
```

**🗣️ Key points to explain:**
> - "**Round Robin** distributes evenly — ~33 requests to each server"
> - "**Least Connection** tends to pile onto one server during bursts because the metrics don't update fast enough"
> - "**ML** intelligently routes most traffic to the least-loaded servers based on real-time CPU and connection data"
> - "All 300 requests succeeded with 0 failures — the system is robust"

**🗣️ Wrap up:**
> "The results are saved to `results/benchmark_results.csv` for further analysis."

---

## Quick Reference — All Commands in Order

```bash
# 1. Install
pip install -r requirements.txt

# 2. Train model
python load_balancer/ml/train_model.py

# 3. Start servers (3 separate terminals)
python services/server.py 1 5001
python services/server.py 2 5002
python services/server.py 3 5003

# 4. Start load balancer
python load_balancer/load_balancer.py

# 5. Start dashboard
python dashboard/app.py

# 6. Open browser → http://localhost:9000

# 7. Test requests
curl http://localhost:8000/
curl http://localhost:8000/stats
curl http://localhost:8000/algorithm?set=round_robin
curl http://localhost:8000/algorithm?set=ml
curl http://localhost:8000/distribution
curl http://localhost:8000/health

# 8. Run benchmark
python services/simulator.py
```

---

## 🛑 To Stop Everything

Press `Ctrl+C` in each of the 5 terminal windows, starting from Dashboard → Load Balancer → Servers.

---

## 💡 Pro Tips for the Demo

1. **Keep the dashboard visible** while sending requests — the audience loves seeing live updates
2. **Send 3 requests with Round Robin** to show the cycling pattern (1 → 2 → 3)
3. **Switch algorithms live** via `curl` while the dashboard is open — the algorithm label updates in real-time
4. **If asked about accuracy**: "93% — because some edge cases where two servers have nearly identical loads are hard to distinguish"
5. **If asked why ML is slower than Round Robin**: "ML has slightly higher latency because it runs the model prediction, but it makes smarter routing decisions under varied load"
6. **If `curl` isn't available**, just type `http://localhost:8000/` in your browser — it works the same way
