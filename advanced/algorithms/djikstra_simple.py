import heapq

def dijkstra(graph, start):
    # Dijkstra computes shortest path from source to all nodes
    #
    # Core idea:
    # always expand the node with smallest known distance first
    #
    # once a node is popped from min-heap,
    # its shortest path is finalized (greedy correctness)

    dist = {node: float('inf') for node in graph}
    dist[start] = 0

    # min-heap stores (distance, node)
    pq = [(0, start)]

    while pq:
        curr_dist, node = heapq.heappop(pq)

        # skip if this is an outdated distance
        # happens because multiple entries may exist in heap
        if curr_dist > dist[node]:
            continue

        # try relaxing all edges from current node
        # relaxation = improve shortest known distance
        for nei, weight in graph[node]:
            new_dist = curr_dist + weight

            # if shorter path found, update and push to heap
            if new_dist < dist[nei]:
                dist[nei] = new_dist
                heapq.heappush(pq, (new_dist, nei))

    return dist


def main():
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }

    print(dijkstra(graph, 0))


if __name__ == "__main__":
    main()