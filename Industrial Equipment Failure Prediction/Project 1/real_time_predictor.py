import numpy as np
import networkx as nx
import random

class RealTimeFailurePredictor:
    def __init__(self, graph, failure_threshold=0.8, window_size=10):
        self.graph = graph
        self.failure_threshold = failure_threshold
        self.window_size = window_size
        self.node_loads = {node: [] for node in graph.nodes()}
        self.edge_loads = {edge: [] for edge in graph.edges()}

    def update_loads(self, active_nodes, active_edges):
        for node in self.graph.nodes():
            self.node_loads[node].append(1 if node in active_nodes else 0)
            if len(self.node_loads[node]) > self.window_size:
                self.node_loads[node].pop(0)

        for edge in self.graph.edges():
            self.edge_loads[edge].append(1 if edge in active_edges else 0)
            if len(self.edge_loads[edge]) > self.window_size:
                self.edge_loads[edge].pop(0)

    def predict_failures(self):
        failing_nodes = [node for node, loads in self.node_loads.items() if np.mean(loads) >= self.failure_threshold]
        failing_edges = [edge for edge, loads in self.edge_loads.items() if np.mean(loads) >= self.failure_threshold]
        return failing_nodes, failing_edges
