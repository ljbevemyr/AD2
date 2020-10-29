from typing import List, Optional, Tuple, Union
__all__ = ['Graph']


class Graph(object):
    _accepted_node_type = str
    _weight_type = int
    _capacity_type = int

    def __init__(self, is_directed: bool):
        """
        Creates a directed or undirected Graph (V, E)

        Sig:  bool ->
        Pre:
        Post:

        Parameters:
        is_directed (bool): True if the graph is directed, and
                            False otherwise.
        """
        self._capacities = dict()
        self._edge_list = []
        self._edges = dict()
        self._flows = dict()
        self._is_directed = is_directed
        self._node_list = []
        self._nodes = set()
        self._weights = dict()

    @property
    def is_directed(self) -> bool:
        """
        Returns True if the graph is directed and False otherwise.

        Sig:  -> bool
        Pre:
        Post:
        """
        return self._is_directed

    @property
    def edges(self) -> List[Tuple[str, str]]:
        """
        Returns the edge list.
        Assume that it takes constant time to invoke this function.
        Traversing the list still takes O(|E|).

        Sig: -> List[Tuple[str, str]]
        Pre:
        Post:

        Example: for (u, v) in graph.edges:
        """
        return list(
            (u, v) for u, nodes in self._edges.items()
            for v in nodes if self._is_directed or u < v
        )

    @property
    def nodes(self) -> List[str]:
        """
        Sig: -> List[str]
        Pre:
        Post:

        Returns the nodes in the graph.
        Assume that it takes constant time to invoke this function.
        Traversing the list still takes O(|V|).

        Example: for u in graph.nodes:
        """
        return list(self._nodes)

    def add_edge(self, u: str, v: str,
                 weight: Optional[int] = None,
                 capacity: Optional[int] = None,
                 flow: Optional[int] = None):
        """
        Adds an edge to the graph

        Sig:  str, str, Optional[int], Optional[int], Optional[int] ->
        Pre:  None
        Post: the edge (u, v) is added to the graph.

        Parameters:
        u (str): the node the edge is traversing from
        v (str): the node the edge is traversing to
        weight (Optional[int]): the weight associated
                                with the edge if any,
                                else None
        capacity (Optional[int]): the capacity associated
                                  with the edge if any,
                                  else None.
        flow (Optional[int]): the flow associated
                              with the edge if any,
                              else None.

        Examples: graph.add_edge('a', 'b')
                  graph.add_edge('b', 'c', weight=5)
                  graph.add_edge('e', 'f', capacity=15)
                  graph.add_edge('g', 'ad2', weight=10, flow=5)
        """
        for node in [u, v]:
            if not type(node) == self._accepted_node_type:
                raise TypeError(
                    "Nodes must be of type "
                    f"{self._accepted_node_type}, "
                    f"'{type(node)}' given"
                )

        if u == v:
            raise ValueError(
                "Edges must be a tuple of two different nodes, "
                f"'({u}, {v})' given"
            )

        if v in self._edges.get(u, set()):
            raise ValueError(
                f"Edge '({u}, {v})' already in graph."
            )

        if weight is not None and not type(weight) == self._weight_type:
            raise TypeError(
                "Weight must be either 'None' or "
                "of the following types: "
                f"{self._weight_type}, "
                f"'{type(weight)}' given."
            )

        if capacity is not None and type(capacity) != self._capacity_type:
            raise TypeError(
                "Capacity must be either 'None' or "
                "of the following types: "
                f"{self._capacity_type}, "
                f"'{type(capacity)}' given."
            )

        if flow is not None and type(flow) != self._capacity_type:
            raise TypeError(
                "Flow must be either 'None' or "
                "of the following types: "
                f"{self._capacity_type}, "
                f"'{type(flow)}' given."
            )

        for node in [u, v]:
            if node in self._nodes:
                continue
            self._nodes.add(node)
            self._edges[node] = set()
            self._capacities[node] = dict()
            self._flows[node] = dict()
            self._weights[node] = dict()

        edges = [(u, v)] if self.is_directed else [(u, v), (v, u)]

        for a, b in edges:
            self._edges[a].add(b)
            self._capacities[a][b] = capacity
            self._flows[a][b] = flow
            self._weights[a][b] = weight

    def remove_edge(self, u: str, v: str):
        """
        Removes an exisiting edge.

        Sig: str, str ->
        Pre: (u, v) exists in the graph.
        Post: The edge (u, v) is removed from the graph.

        Parameters:
        u (str): The node the edge to be removed traverses from
        v (str): The node the edge to be removed traverses to

        Examples: graph.remove_edge('a', 'b')
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges.get(u, set()):
            raise ValueError(f"Edge '({u}, {v})' not in graph.")

        edges = [(u, v)] if self.is_directed else [(u, v), (v, u)]
        for a, b in edges:
            self._edges[a].remove(b)
            del self._capacities[a][b]
            del self._flows[a][b]
            del self._weights[a][b]

    def neighbors(self, node: str) -> List[str]:
        """
        Retrieves the neighbors of a node. The neighbors
        of a node u are all the nodes v: (u, v) in E.
        Assume that it takes constant time to invoke this function.
        Traversing the neighbors list still takes linear
        time complexity.

        Sig: str -> List[str]
        Pre:
        Post:

        Parameters:
        node (str): The node

        Examples: graph.neighbors('a') = ['b', 'c']
        """
        if node not in self._nodes:
            raise KeyError(f"Node '{node}' not in graph")
        return list(self._edges[node])

    def set_weight(self, u: str, v: str, weight: Union[int, None]):
        """
        Sets the weight of an edge.

        Sig: str, str, Union[int, None] ->
        Pre: The weight is non negative
        Post:

        Parameters:
        u (str): the start node of the edge
        v (str): the end node of the edge
        weight({int, None}): the new weight of
                                        the edge.

        Examples: graph.set_weight('a', 'b', 5)
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges[u]:
            raise ValueError(f"Edge '({u}, {v})' not in graph.")
        if (weight is not None and not type(weight) == self._weight_type):
            raise TypeError(
                f"Weight must be of type '{self._weight_type}', "
                f"'{type(weight)} given."
            )
        self._weights[u][v] = weight
        if not self._is_directed:
            self._weights[v][u] = weight

    def weight(self, u: str, v: str) -> Union[int, None]:
        """
        Returns the weight of an edge.

        Sig: str, str -> Union[int, None]
        Pre:
        Post:

        Parameters:
        u (str): the start node of the edge
        v (str): the end node of the edge

        Returns:
        The weight of the edge (u, v)

        Examples: graph.weight('a', 'b') = 5
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges[u]:
            raise ValueError(f"Edge '({u}, {v})' not in graph.")
        return self._weights[u][v]

    def set_capacity(self, u: str, v: str, capacity: Union[int, None]):
        """
        Sets the capacity of an edge.

        Sig: str, str, Union[int, None] ->
        Pre: The capacity is positive
        Post:

        Parameters:
        u (str): the start node of the edge
        v (str): the end node of the edge
        capacity({int, None}): the new weight of the
                                   edge.

        Examples: graph.set_capacity('a', 'b', 10)
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges[u]:
            raise ValueError(f"Edge '({u}, {v})' not in graph.")
        if capacity is not None and type(capacity) != self._capacity_type:
            raise TypeError(
                f"Capacity must be None or of type '{self._capacity_type}', "
                f"'{type(capacity)} given."
            )
        self._capacities[u][v] = capacity
        if not self._is_directed:
            self._capacities[v][u] = capacity

    def capacity(self, u: str, v: str) -> Union[int, None]:
        """
        Returns the capacity of an edge.

        Sig: str, str -> Union[int, None]
        Pre:
        Post:


        Parameters:
        u (str): the start node of the edge
        v (str): the end node of the edge

        Returns:
        The capacity of the edge (u, v)

        Examples: graph.capacity('a', 'b') = 10
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges[u]:
            raise ValueError(f"Edge '({u}, {v})' not in graph.")
        return self._capacities[u][v]

    def set_flow(self, u: str, v: str, flow: Union[int, None]):
        """
        Sets the flow of an edge.

        Sig: str, str, Union[int, None] ->
        Pre: The flow is non negative
        Post:

        Parameters:
        u (str): the start node of the edge
        v (str): the end node of the edge
        flow({int, None}): the new weight of the
                                   edge.

        Examples: graph.set_flow('a', 'b', 10)
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges[u]:
            raise ValueError(f"Edge '({u}, {v})' not in graph.")
        if flow is not None and type(flow) != self._capacity_type:
            raise TypeError(
                f"Flow must be None or of type '{self._capacity_type}', "
                f"'{type(flow)} given."
            )
        self._flows[u][v] = flow
        if not self._is_directed:
            self._flows[v][u] = flow

    def flow(self, u: str, v: str) -> Union[int, None]:
        """
        Returns the flow of an edge.

        Sig: str, str -> Union[int, None]
        Pre:
        Post:

        Parameters:
        u (str): the start node of the edge
        v (str): the end node of the edge

        Returns:
        The flow of the edge (u, v)

        Examples: graph.flow('a', 'b') = 10
        """
        if u not in self._nodes:
            raise ValueError(f"Node '{u}' not in graph.")
        if v not in self._nodes:
            raise ValueError(f"Node '{v}' not in graph.")
        if v not in self._edges[u]:
            raise ValueError(f"Edge '({u}, {v})' not in graph.")
        return self._flows[u][v]

    def copy(self):
        """
        Creates and returns a deep copy of the graph.

        Sig: -> Graph
        Pre:
        Post:

        Parameters:

        Returns:
        A deep copy of the graph.
        """
        graph = Graph(self.is_directed)
        for u, v in self.edges:
            graph.add_edge(
                u,
                v,
                self.weight(u, v),
                self.capacity(u, v),
                self.flow(u, v)
            )
        return graph

    def __contains__(self, x: Union[str, Tuple[str, str]]) -> bool:
        """
        Allows for easy checking if a node or edge exists in the graph.

        Sig: Union[str, Tuple[str, str]] -> bool

        Parameters:
        x (Union[str, Tuple[str, str]]): x must either be a node or an edge

        Returns:
        If x is a node, then True if x is in the graph, and False otherwise;
        else if x is an edge, (u, v), then True if (u, v) exists in the graph,
        and False otherwise.

        Examples: 'ad2' in Graph
                  ('a', 'b') in Graph
        """
        if type(x) == self._accepted_node_type:
            return x in self._nodes
        if type(x) != tuple:
            raise TypeError(
                "Input must be a node or an edge,"
                f"'{type(x)}' given."
            )
        if len(x) != 2:
            raise TypeError(
                "An edge contains two values,"
                f"'{len(x)}' values given."
            )
        if any((not type(n) == self._accepted_node_type) for n in x):
            raise TypeError(
                "Input must be a node or an edge of two nodes,"
                f"'({type(x[0])}, {type(x[1])})' given."
            )
        return x[1] in self._edges.get(x[0], set())

    def __str__(self) -> str:
        nodes = sorted(self._nodes)
        edges = []
        weights = []
        capacities = []
        for u in nodes:
            for v in sorted(self.neighbors(u)):
                edges.append(f"({u}, {v})")

                if self._weights[u][v] is not None:
                    weights.append(
                        f"w(({u},{v}))={self._weights[u][v]}"
                    )
                if self._capacities[u][v] is not None:
                    capacities.append(
                        f"c(({u},{v}))={self._capacities[u][v]}"
                    )
        if len(weights) > 0:
            weight_str = f", ({','.join(weights)})>"
        else:
            weight_str = ""

        if len(capacities) > 0:
            capacity_str = f", ({','.join(capacities)})>"
        else:
            capacity_str = ""

        return (
            f"<V=({','.join(map(str, nodes))})"
            f", E=({','.join(map(str, edges))})"
            f"{weight_str}"
            f"{capacity_str}"
            ">"
        )
