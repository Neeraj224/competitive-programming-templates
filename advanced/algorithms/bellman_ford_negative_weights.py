def bellman_ford(n, edges, src):
    # Bellman-Ford handles negative weights
    #
    # Key idea:
    # relax all edges repeatedly
    #
    # after n-1 iterations, shortest paths stabilize
    # if still improving => negative cycle exists

    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # check for negative cycle
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return "Negative cycle detected"

    return dist


def main():
    edges = [
        (0, 1, 4),
        (0, 2, 5),
        (1, 2, -3),
        (2, 3, 4)
    ]

    print(bellman_ford(4, edges, 0))


if __name__ == "__main__":
    main()