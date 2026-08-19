import requests

servers = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003"
]

def get_least_loaded_server():
    min_connections = float('inf')
    selected_server = None

    for server in servers:
        response = requests.get(server + "/metrics")
        connections = response.json()["active_connections"]

        if connections < min_connections:
            min_connections = connections
            selected_server = server

    return selected_server


for i in range(10):
    server = get_least_loaded_server()
    response = requests.get(server)
    print(response.json())
