# Jai Kumar Assignment - Leegality

## Network Route Optimization API

This project provides a REST API to manage network nodes and edges, as well as calculate the shortest path between them using Dijkstra's algorithm.

## Sample API Requests

### Create a Node
```bash
curl -X POST http://127.0.0.1:8000/api/nodes/ -H "Content-Type: application/json" -d '{"name": "ServerA"}'
```

### Create an Edge
```bash
curl -X POST http://127.0.0.1:8000/api/edges/ -H "Content-Type: application/json" -d '{"source": "ServerA", "destination": "ServerB", "latency": 12.5}'
```

### Calculate Shortest Route
```bash
curl -X POST http://127.0.0.1:8000/api/routes/shortest/ -H "Content-Type: application/json" -d '{"source": "ServerA", "destination": "ServerB"}'
```

### Get Route History
```bash
curl -X GET "http://127.0.0.1:8000/api/routes/history/?source=ServerA&limit=2"
```