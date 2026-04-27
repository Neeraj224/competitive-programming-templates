from enum import Enum
from dataclasses import dataclass, field

class UnweightedGraphEnum(Enum):
    UNDIRECTED = "UNDIRECTED"
    DIRECTED = "DIRECTED"

@dataclass
class UnweightedGraph:
    # edges can use arbitrary vertex labels
    # examples:
    # [[0, 1], [1, 2]]
    # [[10, 20], [20, 30]]
    # [["A", "B"], ["B", "C"]]
    edges: list[list]
    
    # graph type defaults to undirected
    graph_type: UnweightedGraphEnum = UnweightedGraphEnum.UNDIRECTED
    
    # list of unique vertex labels in sorted order
    vertices: list = field(default_factory=list)
    
    # maps original vertex label => internal index
    # example: {10: 0, 20: 1, 30: 2}
    vertex_to_index: dict = field(default_factory=dict)
    
    # maps internal index => original vertex label
    # example: [10, 20, 30]
    index_to_vertex: list = field(default_factory=list)
    
    # adjacency structures are built using internal indices
    adjacency_list: list[list[int]] = field(default_factory=list)
    adjacency_matrix: list[list[int]] = field(default_factory=list)
    
    # number of unique vertices
    num_vertices: int = 0
    
    def __post_init__(self):
        # collect all unique vertices from edges
        self.vertices = self.get_unique_vertices(self.edges)
        self.num_vertices = len(self.vertices)
        
        # build both mappings:
        # original label => index
        # index => original label
        self.index_to_vertex = self.vertices.copy()
        self.vertex_to_index = {
            vertex: index for index, vertex in enumerate(self.vertices)
        }
        
        # build adjacency representations using internal indices
        self.adjacency_list = self.build_graph_list(
            self.num_vertices,
            self.edges,
            self.graph_type
        )
        self.adjacency_matrix = self.build_graph_matrix(
            self.num_vertices,
            self.edges,
            self.graph_type
        )

    def build_graph_list(self, num_vertices, edges, graph_type: UnweightedGraphEnum):
        # create empty adjacency list
        adjacency_list = [[] for _ in range(num_vertices)]
        
        if graph_type == UnweightedGraphEnum.UNDIRECTED:
            for u, v in edges:
                # convert original labels to internal indices
                u_i = self.vertex_to_index[u]
                v_i = self.vertex_to_index[v]
                
                # add both directions for undirected graph
                adjacency_list[u_i].append(v_i)
                adjacency_list[v_i].append(u_i)
        
        elif graph_type == UnweightedGraphEnum.DIRECTED:
            for u, v in edges:
                # convert original labels to internal indices
                u_i = self.vertex_to_index[u]
                v_i = self.vertex_to_index[v]
                
                # add only one direction for directed graph
                adjacency_list[u_i].append(v_i)
            
        return adjacency_list
    
    def build_graph_matrix(self, num_vertices, edges, graph_type):
        # create empty adjacency matrix
        adjacency_matrix = [
            [0 for _ in range(num_vertices)] for _ in range(num_vertices)
        ]

        if graph_type == UnweightedGraphEnum.UNDIRECTED:
            for u, v in edges:
                # convert original labels to internal indices
                u_i = self.vertex_to_index[u]
                v_i = self.vertex_to_index[v]
                
                # mark both directions
                adjacency_matrix[u_i][v_i] = 1
                adjacency_matrix[v_i][u_i] = 1
        
        elif graph_type == UnweightedGraphEnum.DIRECTED:
            for u, v in edges:
                # convert original labels to internal indices
                u_i = self.vertex_to_index[u]
                v_i = self.vertex_to_index[v]
                
                # mark only one direction
                adjacency_matrix[u_i][v_i] = 1
        
        return adjacency_matrix
    
    def get_unique_vertices(self, edges):
        # use set to avoid duplicates
        vertices = set()
        
        for u, v in edges:
            vertices.add(u)
            vertices.add(v)
        
        # sort for stable ordering
        return sorted(vertices)

    def __str__(self):
        representation = "Graph: (V, E)\n\n"
        
        representation += "Vertex to Index Mapping:\n"
        representation += "------------------------\n"
        representation += f"{self.vertex_to_index}\n\n"
        
        representation += "Index to Vertex Mapping:\n"
        representation += "------------------------\n"
        representation += f"{self.index_to_vertex}\n\n"
        
        representation += "Adjacency List (internal indices):\n"
        representation += "----------------------------------\n"
        for i in range(len(self.adjacency_list)):
            representation += f"({i} : {self.adjacency_list[i]})\n"
        
        representation += "\nAdjacency List (original labels):\n"
        representation += "---------------------------------\n"
        for i in range(len(self.adjacency_list)):
            neighbors = [
                self.index_to_vertex[neighbor_index]
                for neighbor_index in self.adjacency_list[i]
            ]
            representation += f"({self.index_to_vertex[i]} : {neighbors})\n"
        
        representation += "\nAdjacency Matrix:\n"
        representation += "-----------------\n"
        representation += "    "
        
        for num in range(self.num_vertices):
            representation += f"{num}  "
        
        representation += "\n"
        
        for i in range(len(self.adjacency_matrix)):
            representation += f"{i}: {self.adjacency_matrix[i]}\n"
        
        return representation


def main():
    # example with integer labels
    edges1 = [[10, 20], [10, 30], [20, 30]]
    
    graph1 = UnweightedGraph(edges1, UnweightedGraphEnum.UNDIRECTED)
    print(graph1)
    
    # example with string labels
    edges2 = [["A", "B"], ["A", "C"], ["B", "C"]]
    
    graph2 = UnweightedGraph(edges2, UnweightedGraphEnum.DIRECTED)
    print(graph2)

if __name__ == "__main__":
    main()