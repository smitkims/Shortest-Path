import argparse
from typing import List
import sys
import heapq

from helpers import AbstractShortestPath


class ShortestPathPositiveWeights(AbstractShortestPath):
    def __init__(self, graph_txt_path='graph0.txt'):
        super().__init__(graph_txt_path)
        self.vertices: List[int] = []
        self.distance: List[int] = []

    def run(self) -> None:
        self.vertices = [-1 for _ in range(self.num_vertices)]
        self.distance = [sys.maxsize for _ in range(self.num_vertices)]
        self.distance[0] = 0

        edges = list(range(self.num_vertices))
        while edges:
            m = heapq.heappop(edges)
            for n, weight in enumerate(self.adjacency_matrix[m]):
                if weight != 0:
                    if self.distance[m] != sys.maxsize and self.distance[n] > self.distance[m] + weight:
                        self.distance[n] = self.distance[m] + weight
                        self.vertices[n] = m
            heapq.heapify(edges)

    def get_shortest_path(self, vertex_idx: int) -> List[int]:
        # If shortest path does not exist, return [0].
        if self.vertices:
            result = []
            while vertex_idx != -1:
                result.append(vertex_idx)
                vertex_idx = self.vertices[vertex_idx]
            return result[::-1]
        return [0]

    def get_shortest_weight(self, vertex_idx: int) -> int:
        # If shortest path does not exist, return 0. 
        if self.vertices:
            return self.distance[vertex_idx]
        return 0


class ShortestPathNegativeWeights(AbstractShortestPath):
    def __init__(self, graph_txt_path='graph1.txt'):
        super().__init__(graph_txt_path)
        # You may add any class members below
        self.vertices: List[int] = []
        self.distance: List[int] = []

    def run(self) -> None:
        self.vertices = [-1 for _ in range(self.num_vertices)]
        self.distance = [sys.maxsize for _ in range(self.num_vertices)]
        self.distance[0] = 0

        edges: List[List[int]] = []
        [edges.append([weight, m, n])  for m, neighbor in enumerate(self.adjacency_matrix) for n, weight in enumerate(neighbor) if weight != 0]
        for _ in range(self.num_vertices - 1):
            dist = self.distance[:]
            for weight, i, j in edges:
                if self.distance[i] != sys.maxsize and self.distance[j] > self.distance[i] + weight:
                    self.distance[j] = self.distance[i] + weight
                    self.vertices[j] = i
        for weight, u, v in edges:
            if self.distance[v] > self.distance[u] + weight:  # negative cycle detected
                self.vertices = []
                return
        return

    def get_shortest_path(self, vertex_idx: int) -> List[int]:
        # Your code here. Return the shortest path in the form of a list of vertices.
        # If shortest path does not exist, return [0]. Dummy return value shown below.
        if self.vertices:
            result = []
            while vertex_idx != -1:
                result.append(vertex_idx)
                vertex_idx = self.vertices[vertex_idx]
            return result[::-1]
        return [0]

    def get_shortest_weight(self, vertex_idx: int) -> int:
        # If shortest path does not exist, return 0. 
        if self.vertices:
            return self.distance[vertex_idx]
        return 0


if __name__ == "__main__":
    """
    Example for running with graph0
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="graph0.txt", help="Path for adjacency matrix")
    parser.add_argument("--weight_type", type=str, choices=['positive', 'negative'], default='negative',
                        help="Which algorithm to use")
    parser.add_argument("--dst", type=int, default=9, help="Target vertex")
    args = parser.parse_args()

    txt_path = args.path
    target_vertex = args.dst
    cls = ShortestPathPositiveWeights if args.weight_type == "positive" else ShortestPathNegativeWeights

    solver = cls(txt_path)
    solver.run()
    print(f"Shortest path total weight: {solver.get_shortest_weight(target_vertex)}")
    print(f"Shortest path: {solver.get_shortest_path(target_vertex)}")
