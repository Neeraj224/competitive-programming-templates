from enum import Enum
from collections import deque

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
            
    ################ CLASSIC GRAPH ALGORITHMS #####################
    
    def validPathBFS(self, source: int, destination: int) -> bool:
        # we will initialize a deque
        # NOTE: deque needs an iterable, so pass the source in an array
        # we will start searching for a path from the source, so we initialize
        # our deque with thde source node here
        queue = deque([source])
        # our visited set to keep track of what all nodes we have visited so far
        # initially since we will be visiting source, initialize the visited set with it
        visited = set([source])
        
        # while there are nodes to be processed in the queue
        while queue:
            # pop from the left end of the deque (our double-ended queue)
            node = queue.popleft()
            
            # check if this is our destination, because if so
            # we will terminate here and return True
            if node == destination:
                return True
            
            # otherwise process each neighbor of the node
            for neighbor in self.adjacency_list[node]:
                # if the neighbor was not previously seen/visited
                if neighbor not in visited:
                    # mark the neighbor as visited/add it in the visited set
                    visited.add(neighbor)
                    # then just append it to the queue to be processed
                    # remember: for this case, we pop from the left and append 
                    # from the right in a FIFO manner!
                    queue.append(neighbor)
            
        # if we did not find the destination starting from the source
        # it means that the source and the destination are in separate
        # disconnected components of the graph, so return False
        return False
    
    def calculateDistancesBFSUnweightedGraph(self, source):
        """
            calculate_distances() will calculate the distance
            from the source vertex passed in the parameters
            to all the other vertices
        """
        # we will need a separate map for distances:
        distances = {}
        
        # for all the nodes we need to initialize the
        # distances as infinity
        for node in self.adjacency_list:
            # no node will already be in distances
            # i know - we are just intializing:
            if node not in distances:
                distances[node] = float('inf')
        
        # our source vertex's distance from iteself will be
        # zero since, no distance needs to be calculated at it
        distances[source] = 0
        
        # add our source vertex to our queue:
        queue = deque([source])
        
        while queue:
            # get a node from the queue:
            node = queue.popleft()

            # process its neighbors from its adjacency list:
            for neighbor in self.adjacency_list[node]:
                # if the distance of the neighbor (from the source) 
                # is still infinity (means it hasn't been calculated yet)
                if distances[neighbor] == float('inf'):
                    # we need to update the distance with 
                    # the distance of the source vertex to the node, plus 1:
                    distances[neighbor] = distances[node] + 1
                    # and then add the neighbor to the queue to be processed
                    queue.append(neighbor)
        
        return distances
    
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
    
        
def main():
    G1 = Graph([(0, 1), (0, 2), (0, 3), (1, 3), (1, 4)], GraphInputType.EDGE_INPUT)
    G1.build_adjacency_list()
    G1.print_graph()
    
    G2 = Graph([('A', 'B'), ('A', 'C'), ('C', 'D'), ('D', 'B')], GraphInputType.EDGE_INPUT)
    G2.build_adjacency_list()
    G2.print_graph()
    
    G3 = Graph([[1, 2, 3], [0, 3], [0, 4], [0, 1], [2]], GraphInputType.INDEX_INPUT)
    G3.build_adjacency_list()
    G3.print_graph()
    
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
    G4.print_graph()

    # ---------- nodes_given (1-based, with isolated node) ----------
    G5 = Graph(
        [(1, 2), (2, 3), (4, 5)],
        GraphInputType.EDGE_INPUT,
        nodes_given=6,
        zero_indexed=False
    )
    G5.build_adjacency_list()
    G5.print_graph()

    print("BFS valid path (1 -> 3):", G5.validPathBFS(1, 3))   # True
    print("BFS valid path (1 -> 6):", G5.validPathBFS(1, 6))   # False

    print("Distances from 1:", G5.calculate_distances_BFS_Unweighted_Graph(1))

    # ---------- nodes_given (0-based, with isolated node) ----------
    G6 = Graph(
        [(0, 1), (1, 2), (3, 4)],
        GraphInputType.EDGE_INPUT,
        nodes_given=6,
        zero_indexed=True
    )
    G6.build_adjacency_list()
    G6.print_graph()

    print("BFS valid path (0 -> 2):", G6.validPathBFS(0, 2))   # True
    print("BFS valid path (0 -> 5):", G6.validPathBFS(0, 5))   # False

    print("Distances from 0:", G6.calculate_distances_BFS_Unweighted_Graph(0))


if __name__ == "__main__":
    main()