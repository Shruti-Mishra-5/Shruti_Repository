"""
core.py -- Reusable OR engine for the Hyperlocal Delivery Streamlit app.

Every function here is deliberately instrumented (returns extra stats like
nodes-visited, or intermediate matrices) so the Streamlit app can *show the
algorithm working*, not just its final answer.
"""

import heapq
import math
import random
from collections import defaultdict

import networkx as nx
import numpy as np
from sklearn.cluster import DBSCAN
from ortools.constraint_solver import routing_enums_pb2, pywrapcp


# ----------------------------------------------------------------------
# 1. CITY GRAPH
# ----------------------------------------------------------------------
def build_city_graph(rows=12, cols=12, traffic_zone_prob=0.15, seed=42):
    rng = random.Random(seed)
    G = nx.grid_2d_graph(rows, cols)
    G = nx.convert_node_labels_to_integers(G, label_attribute="pos")

    for u, v in G.edges():
        base_time = rng.uniform(1.0, 2.0)
        congested = rng.random() < traffic_zone_prob
        if congested:
            base_time *= rng.uniform(2.5, 4.0)
        G.edges[u, v]["weight"] = base_time
        G.edges[u, v]["congested"] = congested

    for _ in range(rows):
        a, b = rng.sample(list(G.nodes()), 2)
        if not G.has_edge(a, b):
            pa, pb = G.nodes[a]["pos"], G.nodes[b]["pos"]
            dist = math.dist(pa, pb)
            if dist < 3:
                G.add_edge(a, b, weight=dist * rng.uniform(1.0, 1.5), congested=False)

    return G


def nearest_node(G, x, y):
    """Find the graph node whose (x,y) position is closest to a click point."""
    best, best_d = None, float("inf")
    for n, data in G.nodes(data=True):
        px, py = data["pos"]
        d = (px - x) ** 2 + (py - y) ** 2
        if d < best_d:
            best_d, best = d, n
    return best


# ----------------------------------------------------------------------
# 2. DIJKSTRA & A* -- instrumented for teaching (returns nodes visited)
# ----------------------------------------------------------------------
def dijkstra_with_stats(G, source, target):
    """Classic Dijkstra. Returns (path, cost, num_nodes_settled)."""
    dist = {source: 0.0}
    prev = {}
    visited = set()
    pq = [(0.0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == target:
            break
        for v in G.neighbors(u):
            w = G.edges[u, v]["weight"]
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if target not in dist:
        return None, float("inf"), len(visited)

    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()
    return path, dist[target], len(visited)


def astar_with_stats(G, source, target, weight_scale_for_heuristic=1.0):
    """
    A* with a Euclidean-distance heuristic (admissible since grid edges are
    >= straight-line distance). Returns (path, cost, num_nodes_settled).
    """
    pos = nx.get_node_attributes(G, "pos")

    def h(n):
        return math.dist(pos[n], pos[target]) * weight_scale_for_heuristic

    g = {source: 0.0}
    prev = {}
    visited = set()
    pq = [(h(source), source)]
    while pq:
        f, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if u == target:
            break
        for v in G.neighbors(u):
            w = G.edges[u, v]["weight"]
            ng = g[u] + w
            if ng < g.get(v, float("inf")):
                g[v] = ng
                prev[v] = u
                heapq.heappush(pq, (ng + h(v), v))

    if target not in g:
        return None, float("inf"), len(visited)

    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    path.reverse()
    return path, g[target], len(visited)


# ----------------------------------------------------------------------
# 3. HYPERLOCAL ZONING
# ----------------------------------------------------------------------
def travel_time_matrix(G, nodes):
    n = len(nodes)
    D = np.zeros((n, n))
    for i, u in enumerate(nodes):
        lengths = nx.single_source_dijkstra_path_length(G, u, weight="weight")
        for j, v in enumerate(nodes):
            D[i, j] = lengths.get(v, 1e6)
    return D


def cluster_into_zones(D, eps=5.0, min_samples=2):
    model = DBSCAN(eps=eps, min_samples=min_samples, metric="precomputed")
    return model.fit_predict(D)


# ----------------------------------------------------------------------
# 4. ORDER BATCHING
# ----------------------------------------------------------------------
def batch_orders(orders, zone_labels, max_batch_size=3, time_window=15):
    zone_groups = defaultdict(list)
    for idx, o in enumerate(orders):
        zone_groups[zone_labels[idx]].append(idx)

    batches = []
    for zone, idxs in zone_groups.items():
        if zone == -1:
            for i in idxs:
                batches.append([i])
            continue
        idxs_sorted = sorted(idxs, key=lambda i: orders[i]["order_time"])
        current, anchor_time = [], None
        for i in idxs_sorted:
            t = orders[i]["order_time"]
            if not current:
                current, anchor_time = [i], t
            elif len(current) < max_batch_size and (t - anchor_time) <= time_window:
                current.append(i)
            else:
                batches.append(current)
                current, anchor_time = [i], t
        if current:
            batches.append(current)
    return batches


# ----------------------------------------------------------------------
# 5. ROUTING (OPEN VRP via OR-Tools)
# ----------------------------------------------------------------------
def solve_batch_route(D_sub):
    """Open VRP: start at depot (index 0), visit all stops, no return leg."""
    n_real = D_sub.shape[0]
    if n_real == 1:
        return [0]
    n = n_real + 1
    dummy = n - 1

    D_ext = np.zeros((n, n))
    D_ext[:n_real, :n_real] = D_sub
    D_ext[:, dummy] = 0
    D_ext[dummy, :] = 0

    manager = pywrapcp.RoutingIndexManager(n, 1, [0], [dummy])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        i = manager.IndexToNode(from_index)
        j = manager.IndexToNode(to_index)
        return int(D_ext[i, j] * 100)

    transit_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    solution = routing.SolveWithParameters(params)

    route = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        if node != dummy:
            route.append(node)
        index = solution.Value(routing.NextVar(index))
    return route


def full_path_for_route(G, stop_nodes, route_idx):
    """Expand a batch route (sequence of stop indices) into a full node path."""
    full_path = []
    for k in range(len(route_idx) - 1):
        u, v = stop_nodes[route_idx[k]], stop_nodes[route_idx[k + 1]]
        seg = nx.shortest_path(G, u, v, weight="weight")
        full_path += seg[:-1]
    full_path.append(stop_nodes[route_idx[-1]])
    return full_path


def run_full_pipeline(G, orders, eps, min_samples, max_batch_size, time_window):
    """
    Runs zoning -> batching -> routing end to end and returns everything
    the dashboard needs to display.
    """
    if len(orders) == 0:
        return {
            "zone_labels": np.array([]), "batches": [], "batch_routes": [],
            "total_naive_time": 0.0, "total_optimized_time": 0.0,
        }

    delivery_nodes = [o["delivery"] for o in orders]
    D_orders = travel_time_matrix(G, delivery_nodes)
    zone_labels = cluster_into_zones(D_orders, eps=eps, min_samples=min_samples)

    batches = batch_orders(orders, zone_labels, max_batch_size=max_batch_size, time_window=time_window)

    batch_routes = []
    total_naive_time = 0.0
    total_optimized_time = 0.0

    for batch in batches:
        batch_orders_list = [orders[i] for i in batch]
        depot = batch_orders_list[0]["restaurant"]
        stop_nodes = [depot] + [o["delivery"] for o in batch_orders_list]
        D_sub = travel_time_matrix(G, stop_nodes)

        route_idx = solve_batch_route(D_sub)
        optimized_time = sum(D_sub[route_idx[k], route_idx[k + 1]] for k in range(len(route_idx) - 1))
        naive_order = list(range(len(stop_nodes)))
        naive_time = sum(D_sub[naive_order[k], naive_order[k + 1]] for k in range(len(naive_order) - 1))

        total_optimized_time += optimized_time
        total_naive_time += naive_time

        full_path = full_path_for_route(G, stop_nodes, route_idx)
        batch_routes.append({
            "path": full_path,
            "order_ids": [o["id"] for o in batch_orders_list],
            "optimized_time": optimized_time,
            "naive_time": naive_time,
            "depot": depot,
        })

    return {
        "zone_labels": zone_labels,
        "batches": batches,
        "batch_routes": batch_routes,
        "total_naive_time": total_naive_time,
        "total_optimized_time": total_optimized_time,
    }
