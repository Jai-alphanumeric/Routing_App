import heapq
from .models import Edge

def find_shortest_path(source_name: str, destination_name: str):
    """
    Dijkstra algo
    Returns (total_latency, path_list) or (None, None) if no path exists.
    """
    if source_name == destination_name:
        return 0.0, [source_name]

    # Priority queue: (latency, current_node, path)
    pq = [(0.0, source_name, [source_name])]
    visited = set()

    while pq:
        current_latency, current_node, path = heapq.heappop(pq)
        if current_node == destination_name:
            return current_latency, path

        if current_node in visited:
            continue

        visited.add(current_node)

        # Query only the necessary outgoing edges for the current node
        # This avoids loading the entire graph into memory
        outgoing_edges = Edge.objects.filter(source__name=current_node).select_related('destination')

        for edge in outgoing_edges:
            neighbor = edge.destination.name
            if neighbor not in visited:
                heapq.heappush(pq, (current_latency + edge.latency, neighbor, path + [neighbor]))

    return None, None
