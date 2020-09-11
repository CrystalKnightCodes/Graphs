"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
        self.search_path = None

    def vertex_search(self, starting_vertex, destination_vertex = None):
        if starting_vertex not in self.vertices:
            raise KeyError("Invalid starting vertex.")
        if destination_vertex not in self.vertices and destination_vertex:
            raise KeyError("Invalid destination vertex.")
    
    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
        else:
            raise KeyError("Vertex already exists.")

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 not in self.vertices:
            raise IndexError(f"Failed to add edge {v1}, {v2} because {v1} does not exist.")
        if v2 not in self.vertices:
            raise IndexError(f"Failed to add edge {v1}, {v2} because {v2} does not exist.")
        
        self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        self.vertex_search(starting_vertex)

        pending = Queue()
        visited = set()

        if starting_vertex in self.vertices:
            pending.enqueue(starting_vertex)
        while len(pending.queue) > 0:
            vertex = pending.dequeue()
            if vertex and vertex not in visited:
                visited.add(vertex)
                print(vertex)
                for neighbor in self.get_neighbors(vertex):
                    pending.enqueue(neighbor)
                

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        self.vertex_search(starting_vertex)

        pending = Stack()
        visited = set()

        if starting_vertex in self.vertices:
            pending.push(starting_vertex)
        while len(pending.stack) > 0:
            vertex = pending.pop()
            if vertex not in visited:
                visited.add(vertex)
                print(vertex)
                for neighbor in self.get_neighbors(vertex):
                    pending.push(neighbor)

    def dft_recursive(self, starting_vertex, visited = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        self.vertex_search(starting_vertex)
        
        if visited == None:
            visited = set()

        if starting_vertex not in visited:
            visited.add(starting_vertex)
            print(starting_vertex)
            for neighbor in self.get_neighbors(starting_vertex):
                self.dft_recursive(neighbor, visited)


    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        self.vertex_search(starting_vertex, destination_vertex)

        pending = Queue()
        visited = set()
        path = [starting_vertex]
        
        pending.enqueue(path)
        while len(pending.queue) > 0:
            path = pending.dequeue()
            vertex = path[-1]

            if vertex == destination_vertex:
                return path

            if vertex not in visited:
                visited.add(vertex)
                for neighbor in self.get_neighbors(vertex):
                    new_path = list(path)
                    new_path.append(neighbor)
                    pending.enqueue(new_path)
        
        return None


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        self.vertex_search(starting_vertex, destination_vertex)

        pending = Stack()
        visited = set()
        path = [starting_vertex]

        pending.push(path)

        while len(pending.stack) > 0:
            path = pending.pop()
            vertex = path[-1]
            if vertex == destination_vertex:
                return path

            if vertex not in visited:
                visited.add(vertex)
                for neighbor in self.get_neighbors(vertex):
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        pending.push(new_path)

        return None


    def dfs_recursive(self, starting_vertex, destination_vertex, visited = None, path = None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited == None:
            visited = set()
            path = [starting_vertex]

        self.vertex_search(starting_vertex, destination_vertex)

        if starting_vertex not in visited:
            new_visited = set(visited)
            new_visited.add(starting_vertex)
            for neighbor in self.get_neighbors(starting_vertex):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    if neighbor == destination_vertex:
                        self.search_path = new_path
                        return new_path
                    else:
                        result = self.dfs_recursive(neighbor, destination_vertex, new_visited, new_path)
                        if result is not None:
                            return result
        return None                   

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print("Graph vertices.")
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    print("Breadth first transveral.")
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    print("Depth first transveral.")
    graph.dft(1)
    print("Recursive depth first transveral.")
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print("Breadth first search.")
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print("Depth first search.")
    print(graph.dfs(1, 6))
    print("Recursive depth first search.")
    print(graph.dfs_recursive(1, 6))

    print("End of tests.")
