def dfs(graph: Graph, visited: Set[str], node: str, came_from: str) -> bool:
    """
    Sig:  graph: Graph, visited: Set[str], node: str, came_from: str) -> bool
    Pre:  (none)
    Post: visited contains all visited nodes
    Ex:   graph = <V=(a,b,c,d), E=((a, b),(b, c),(c, d),(d, a))>
          visited = {}
          node = 'a'
          came_from = None
          dfs(graph, visited, node, came_from)
          The return value from dfs is True, visited is now {a,b,c,d}
    """
    visited.add(node)
    for neighbour in graph.neighbors(node):
        # Invariant: visited contains one new neighbour and all previous neighbours
        # Variant: len(graph.neighbors(node)) - graph.neighbors.index(neighbour)
        if neighbour not in visited:
            if dfs(graph, visited, neighbour, node):
                # Variant: len(graph.nodes) - len(visited)
                return True
        elif neighbour != came_from:
            return True

    return False


def dfs_extended(graph: Graph, visited: List[str], path: Set[str], node: str, came_from: str) -> Tuple[bool, List[Tuple[str, str]]]:
    """
    Sig:  graph: Graph, visited: Set[str], path: List[str], node: str, came_from: str) -> Tuple[bool, List[Tuple[str, str]]]
    Pre:  (none)
    Post: visited contains all visited nodes
    Ex:   graph = <V=(a,b,c,d), E=((a, b),(b, c),(c, d),(d, a))>
          visited = {}
          path = []
          node = 'a'
          came_from = None
          dfs_extended(graph, visited, path, node, came_from)
          The return value from dfs is True and a list of all
          edges in a ring, visited is now {a,b,c,d}
    """
    if came_from == None:
        visited.add(node)
        path.append(node)

    for i, neighbour in enumerate(graph.neighbors(node)):
        # Invariant: visited contains one new neighbour and all previous neighbours
        # Variant: len(graph.neighbors(node)) - i
        visited.add(neighbour)
        path = path[:path.index(node)+1]
        if neighbour not in path:
            path.append(neighbour)
            found, edge_path = dfs_extended(graph, visited, path, neighbour, node)
            # Variant: len(graph.nodes) - len(visited)
            if found:
                return True, edge_path
        elif neighbour != came_from:
            path.append(neighbour)
            node_path = path[path.index(neighbour):]
            edge_path = []
            for i in range(len(node_path)-1):
                #Variant: len(node_path) - i
                edge_path.append((node_path[i], node_path[i+1]))
            return True, edge_path
    return False, []

def ring(G: Graph) -> bool:
    """
    Sig:  Graph G(V, E) -> bool
    Pre:
    Post:
    Ex:   Sanity tests below
          ring(g1) = False
          ring(g2) = True
    """

    nodes = G.nodes
    visited = set()
    for node in nodes:
        # Variant: len(nodes) - nodes.index(node)
        if node not in visited:
           if dfs(G, visited, node, None):
               return True
    return False


def ring_extended(G: Graph) -> Tuple[bool, Set[Tuple[str, str]]]:
    """
    Sig:  Graph G(V,E) -> Tuple[bool, List[Tuple[str, str]]]
    Pre:
    Post:
    Ex:   Sanity tests below
          ring_extended(g1) = False, []
          ring_extended(g2) = True, [('a','c'),('c','f'),
                                     ('f','h'),('h','g'),('g','d'),('d','f'),
                                     ('f','a')]
    """

    visited = set()
    path = []
    nodes = G.nodes

    for node in nodes:
        # Variant: len(nodes) - nodes.index(node)
        if node not in visited: 
            found, edge_path = dfs_extended(G, visited, path, node, None)
            if found:
                return True, edge_path

    return False, []