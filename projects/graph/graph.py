"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.nodes = {}

    def add_vertex(self, node_id):
        """
        Add a vertex to the graph.
        """
        if node_id not in self.nodes:
            self.nodes[node_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.nodes and v2 in self.nodes:
            self.nodes[v1].add(v2)
        else:
            if v1 in self.nodes:
                raise IndexError(f'{v2} is not in graph')
            else:
                raise IndexError(f'{v1} is not in graph')

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.nodes:
            return self.nodes[vertex_id]
        else:
            raise IndexError(f'{vertex_id} is not in graph')

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        visited = set()
        q.enqueue(starting_vertex)
        while q.size() > 0:
            n = q.dequeue()
            if n not in visited:
                print(n)
                visited.add(n)
                for x in self.nodes[n]:
                    q.enqueue(x)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        s.push(starting_vertex)
        visited = set()
        while s.size() > 0:
            n = s.pop()
            if n not in visited:
                print(n)
                visited.add(n)
                for x in self.nodes[n]:
                    s.push(x)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        visited = visited if visited else set()
        if starting_vertex not in visited:
            print(starting_vertex)
            visited.add(starting_vertex)
            for x in self.nodes[starting_vertex]:
                self.dft_recursive(x, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        paths = {starting_vertex: [starting_vertex]}
        visited = set()
        q = Queue()
        q.enqueue((starting_vertex, None))
        while destination_vertex not in visited:
            n, t = q.dequeue()  # t is the previous calling node
            if n not in visited:
                visited.add(n)
                if t is not None:
                    paths[n] = paths[t] + [n]
                for x in self.nodes[n]:
                    q.enqueue((x, n))
        return paths[destination_vertex]

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        paths = {starting_vertex: [starting_vertex]}
        visited = set()
        q = Stack()
        q.push((starting_vertex, None))
        while destination_vertex not in visited:
            n, t = q.pop()  # t is the previous calling node
            if n not in visited:
                visited.add(n)
                if t is not None:
                    paths[n] = paths[t] + [n]
                for x in self.nodes[n]:
                    q.push((x, n))
        return paths[destination_vertex]

    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO


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

    print('''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    ''')
    print(graph.nodes)

    print('''
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
    ''')
    graph.bft(1)

    print('''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    ''')
    graph.dft(1)
    print('recursive')
    graph.dft_recursive(1)

    print('''
    Valid BFS path:
        [1, 2, 4, 6]
    ''')
    print(graph.bfs(1, 6))

    print('''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    ''')
    print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
