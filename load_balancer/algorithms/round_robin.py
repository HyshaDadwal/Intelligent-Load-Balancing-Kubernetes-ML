import requests

servers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

current = 0

def get_next_server():
    global current
    server = servers[current]
    current = (current + 1) % len(servers)
    return server

for i in range(10):
    server = get_next_server()
    response = requests.get(server)
    print(response.json())
