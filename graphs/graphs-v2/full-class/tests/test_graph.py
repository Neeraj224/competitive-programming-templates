import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from graphs_adj_list import Graph, GraphInputType

# Test 1:
# Basic integer graph using edge input
# -> fully connected graph
# -> verifies BFS path finding and that only 1 connected component exists
def test_G1_basic_int_graph():
    G1 = Graph([(0, 1), (0, 2), (0, 3), (1, 3), (1, 4)], GraphInputType.EDGE_INPUT)
    G1.build_adjacency_list()

    assert G1.validPathBFS(0, 4) is True
    assert G1.connectedComponentsDFS() == 1


# Test 2:
# Graph with string-based nodes
# -> ensures implementation is generic (not restricted to integers)
# -> verifies BFS and connected components work with non-numeric nodes
def test_G2_string_graph():
    G2 = Graph([('A', 'B'), ('A', 'C'), ('C', 'D'), ('D', 'B')], GraphInputType.EDGE_INPUT)
    G2.build_adjacency_list()

    assert G2.validPathBFS('A', 'D') is True
    assert G2.connectedComponentsDFS() == 1


# Test 3:
# Graph provided as index-based adjacency list
# -> verifies INDEX_INPUT parsing
# -> ensures BFS and DFS logic work with pre-structured graph input
def test_G3_index_input():
    G3 = Graph([[1, 2, 3], [0, 3], [0, 4], [0, 1], [2]], GraphInputType.INDEX_INPUT)
    G3.build_adjacency_list()

    assert G3.validPathBFS(0, 4) is True
    assert G3.connectedComponentsDFS() == 1


# Test 4:
# Graph provided directly as adjacency list (dictionary form)
# -> ensures ADJACENCY_LIST input type is handled correctly
# -> verifies no transformation errors and correct traversal
def test_G4_given_adjacency_list():
    G4 = Graph(
        {
            'A': ['B', 'C'],
            'B': ['D', 'A'],
            'C': ['A', 'D'],
            'D': ['B', 'C']
        },
        GraphInputType.ADJACENCY_LIST
    )
    G4.build_adjacency_list()

    assert G4.validPathBFS('A', 'D') is True
    assert G4.connectedComponentsDFS() == 1


# Test 5:
# 1-based graph with nodes_given and an isolated node
# -> verifies correct handling of nodes not present in edges
# -> checks:
#       - BFS path existence
#       - disconnected case (should return False)
#       - connected components count
#       - BFS distance calculation including unreachable nodes (inf)
def test_G5_1_based_with_isolated_node():
    G5 = Graph(
        [(1, 2), (2, 3), (4, 5)],
        GraphInputType.EDGE_INPUT,
        nodes_given=6,
        zero_indexed=False
    )
    G5.build_adjacency_list()

    assert G5.validPathBFS(1, 3) is True
    assert G5.validPathBFS(1, 6) is False
    assert G5.connectedComponentsDFS() == 3

    distances = G5.calculateDistancesBFSUnweightedGraph(1)
    assert distances[1] == 0
    assert distances[3] == 2
    assert distances[6] == float('inf')


# Test 6:
# 0-based graph with nodes_given and an isolated node
# -> ensures correct handling of zero-indexed graphs
# -> verifies consistency with Test 5 but in 0-based indexing
# -> checks BFS, connected components, and distance logic
def test_G6_0_based_with_isolated_node():
    G6 = Graph(
        [(0, 1), (1, 2), (3, 4)],
        GraphInputType.EDGE_INPUT,
        nodes_given=6,
        zero_indexed=True
    )
    G6.build_adjacency_list()

    assert G6.validPathBFS(0, 2) is True
    assert G6.validPathBFS(0, 5) is False
    assert G6.connectedComponentsDFS() == 3

    distances = G6.calculateDistancesBFSUnweightedGraph(0)
    assert distances[0] == 0
    assert distances[2] == 2
    assert distances[5] == float('inf')