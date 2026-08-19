import requests
import time

LOAD_BALANCER_URL = "http://localhost:8000"

num_requests = 200

start = time.time()

for _ in range(num_requests):
    requests.get(LOAD_BALANCER_URL)
    time.sleep(0.01)
    
end = time.time()

total_time = end - start

print("Total Time:", total_time)
print("Requests per second:", num_requests / total_time)

stats = requests.get(LOAD_BALANCER_URL + "/stats")
print("Load Balancer Stats:", stats.json())