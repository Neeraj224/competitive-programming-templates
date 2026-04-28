from enum import Enum
from typing import List

class GraphInputType(Enum):
    """
        EDGE_INPUT means, that for the inputs,
        we are given the edges only - and we have to 
        extract the vertices and edges and build the 
        adjacency list representation of the graph.
        for ex:
            [(10, 20), (10, 30), (20, 40), (30, 40)]
        
        in this, we have:
            V: (10, 20, 30, 40)
            E: (
                (10, 20), (20, 10) -> because undirected graph!
                (10, 30), (30, 10),
                (20, 40), (40, 20),
                (30, 40), (40, 30)
            )
    """
    EDGE_INPUT = "EDGE_INPUT"
    
    """
        INDEX_INPUT means we are given an array, and we
        have to map the indices to the nodes/vertices and
        build the  adjacency list representation of the graph.
        for ex:
            [[1, 2, 3], [0, 3], [0, 4], [0, 1], [2]]
        
        so in this, we have:
            V: (0, 1, 2, 3, 4)
            E: (
                (0, 1), (0, 2), (0, 3),
                (1, 0), (1, 3),
                (2, 0), (2, 4),
                (3, 0), (3, 1),
                (4, 2)
            )
    """
    INDEX_INPUT = "INDEX_INPUT"
    
    """
        ADJACENCY_LIST type of input means, we have been
        provided with the adjacency list itself.
    """
    ADJACENCY_LIST = "ADJACENCY_LIST"

class Graph:    
    def __init__(self, 
                 input, 
                 graph_input_type: GraphInputType, 
                 nodes_given: int = None,
                 zero_indexed: bool = False):
        
        self.input = input
        self.graph_input_type = graph_input_type
        # by default, nodes_given would be false
        # if nodes are given then we would build the graph
        # using the number of nodes given and the edges array
        self.nodes_given = nodes_given
        # and for nodes_given, we would have to define if the nodes
        # are zero indexed - i.e. starting from zero, or not - i.e.
        # starting from 1
        self.zero_indexed = zero_indexed
        
        self.vertices = set()
        self.adjacency_list = {}
        self.vertex_degrees = {}
        self.adjacency_matrix = []
    
    def get_vertices(self):
        # we need to add all the vertices in the
        # vertices set that we have so that we can
        # keep a track of them
        for (u, v) in self.input:
            self.vertices.add(u)
            self.vertices.add(v)
    
    def build_adjacency_list(self):
        # if we are also given the number of nodes, then we build using that:
        if self.nodes_given is not None and self.graph_input_type == GraphInputType.EDGE_INPUT:
            self.build_node_edge_input_adjacency_list()
        elif self.graph_input_type == GraphInputType.EDGE_INPUT:
            self.build_edge_input_adjacency_list()
        elif self.graph_input_type == GraphInputType.INDEX_INPUT:
            self.build_index_input_adjacency_list()
        elif self.graph_input_type == GraphInputType.ADJACENCY_LIST:
            # we can assign the adjacency list as the input itself
            self.adjacency_list = self.input
            # but we still need to add the degrees, so:
            for (node, neighbors) in self.adjacency_list.items():
                if node not in self.vertex_degrees:
                    self.vertex_degrees[node] = len(neighbors)
        
        return self.adjacency_list
            
    def print_graph(self):
        print(f"******************************")
        print(f"Graph:")
        for node in self.adjacency_list:
            print(f"{node}: {self.adjacency_list[node]}; deg: {self.vertex_degrees[node]}")
        print(f"******************************\n\n")
    
    ################ ADJACENCY LIST BUILDER HELPERS #####################
    
    def build_edge_input_adjacency_list(self):
        """
            Assuming that we are given the edges
            of a generic, unweighted, undirected graph, 
            we will be building an adjacency
            list representation for it:
        """
        for (u, v) in self.input:
            """
                while building the adjacency list, 
                we will also be increasing the vertex degrees
            """
            # we check if the first vertex in the edge
            # is in the adjacency list already or not
            # NOTE: we do not need to check if the vertex
            # is in the vertex_degrees map or not, because
            # if it is not in the adjacency list, then 
            # a degree for it would not have been noted:
            if u not in self.adjacency_list:
                # so if not we first create a list for it
                self.adjacency_list[u] = []
                # as well as add it to the vertex map 
                # so that we can count its degrees:
                self.vertex_degrees[u] = 0
                
                # and then add the neighbor
                self.adjacency_list[u].append(v)
                # and increment the vertex degree:
                self.vertex_degrees[u] += 1
            # else if it is already there, add it:
            else:
                # append the neighbor to its list of neighbors
                self.adjacency_list[u].append(v)
                # and increment its degree
                self.vertex_degrees[u] += 1
            
            # now since this is an undirected graph
            # for an edge (u, v), we would also have 
            # and edge (v, u), so we add that - 
            # for that we do the same as above:
            # first check if it is in our adjacency list
            if v not in self.adjacency_list:
                # if not, initialize in the adjacency list
                # as well as the vertex degrees map:
                self.adjacency_list[v] = []
                self.vertex_degrees[v] = 0
                
                # and append u as the neighbor
                # and increment the degree
                self.adjacency_list[v].append(u)
                self.vertex_degrees[v] += 1
            # otherwise, no need to create it since it
            # already exists in the adjacency list
            else:
                # so simply add to adjacency list
                # and increment the degree:
                self.adjacency_list[v].append(u)
                self.vertex_degrees[v] += 1
    
    def build_index_input_adjacency_list(self):
        """
            for this type of graph input, we would
            need to build the adjacency list by simply adding
            the neighbors using the list of lists we are given
            where index is the node and the list at that index
            is the list of neighbors for that node
        """
        for node in range(0, len(self.input)):
            # if the node is not in the list - which it wont be
            # since we would have to scan the list linearly and go through it
            if node not in self.adjacency_list:
                # we simply add the list of neighbors to it's key in the
                # adjacency list for our graph
                self.adjacency_list[node] = self.input[node]
                # and update the degree for it:
                if node not in self.vertex_degrees:
                    self.vertex_degrees[node] = len(self.input[node])
    
    def build_node_edge_input_adjacency_list(self):
        if self.zero_indexed:
            self.adjacency_list = {i: [] for i in range(0, self.nodes_given)}
            self.vertex_degrees = {i: 0 for i in range(0, self.nodes_given)}
        else:
            self.adjacency_list = {i: [] for i in range(1, self.nodes_given + 1)}
            self.vertex_degrees = {i: 0 for i in range(1, self.nodes_given + 1)}
        
        self.build_edge_input_adjacency_list()
    
class Solution:
    def __init__(self):
        pass
    
    def solver(self, input):
        self.input = input
        
def main():
    solver1 = Solution()
    solver2 = Solution()
    solver3 = Solution()
    
    print(solver1.solver())
    print(solver2.solver())
    print(solver3.solver())
    

if __name__ == "__main__":
    main()