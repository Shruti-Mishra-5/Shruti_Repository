import random

import numpy as np
import plotly.graph_objects as go
import streamlit as st

import core

st.set_page_config(page_title="Hyperlocal Delivery OR", layout="wide", page_icon="🛵")
st.markdown("""
<style>
html, body, [class*="css"]  { font-size: 18px !important; }
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1300px;
    margin: 0 auto;
}
h1 { font-size: 2.4rem !important; }
h2 { font-size: 1.8rem !important; }
h3 { font-size: 1.4rem !important; }
[data-testid="stSidebar"] { min-width: 340px !important; }
[data-testid="stMetricValue"] { font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { font-size: 1rem !important; }
.stButton button, .stSlider, .stSelectbox { font-size: 1rem !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INIT
# ============================================================================
def init_state():
    if "G" not in st.session_state:
        st.session_state.G = core.build_city_graph(rows=12, cols=12, traffic_zone_prob=0.15, seed=42)
        st.session_state.pos = {n: st.session_state.G.nodes[n]["pos"] for n in st.session_state.G.nodes()}
        rng = random.Random(7)
        st.session_state.restaurant_nodes = rng.sample(list(st.session_state.G.nodes()), 6)
        st.session_state.random_orders = make_random_orders(
            st.session_state.G, st.session_state.restaurant_nodes, 24, seed=7
        )
        st.session_state.custom_orders = []
        st.session_state.last_click = None


def make_random_orders(G, restaurant_nodes, n, seed):
    rng = random.Random(seed)
    nodes = list(G.nodes())
    orders = []
    for i in range(n):
        r = rng.choice(restaurant_nodes)
        d = rng.choice(nodes)
        t = rng.randint(0, 60)
        orders.append({"id": f"R{i}", "restaurant": r, "delivery": d, "order_time": t})
    return orders


def all_orders():
    combined = list(st.session_state.random_orders) + list(st.session_state.custom_orders)
    return combined


init_state()
G = st.session_state.G
pos = st.session_state.pos
restaurant_nodes = st.session_state.restaurant_nodes

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
st.sidebar.title("🛵 Controls")

st.sidebar.markdown("### 🏙️ City")
if st.sidebar.button("🔄 Regenerate city graph"):
    seed = random.randint(0, 99999)
    st.session_state.G = core.build_city_graph(rows=12, cols=12, traffic_zone_prob=0.15, seed=seed)
    st.session_state.pos = {n: st.session_state.G.nodes[n]["pos"] for n in st.session_state.G.nodes()}
    st.session_state.restaurant_nodes = random.sample(list(st.session_state.G.nodes()), 6)
    st.session_state.random_orders = make_random_orders(
        st.session_state.G, st.session_state.restaurant_nodes, 24, seed=random.randint(0, 99999)
    )
    st.session_state.custom_orders = []
    st.rerun()

num_random = st.sidebar.slider("Number of random orders", 5, 40, 24)
if st.sidebar.button("🎲 Regenerate random orders"):
    st.session_state.random_orders = make_random_orders(
        G, restaurant_nodes, num_random, seed=random.randint(0, 99999)
    )
    st.rerun()

st.sidebar.markdown("### 📍 Zoning (DBSCAN)")
eps = st.sidebar.slider("eps — max travel time (min) within a zone", 2.0, 12.0, 5.0, 0.5)
min_samples = st.sidebar.slider("min_samples — min orders to form a zone", 2, 6, 2)

st.sidebar.markdown("### 📦 Batching")
max_batch_size = st.sidebar.slider("Max orders per rider trip", 1, 5, 3)
time_window = st.sidebar.slider("Time window for batching (min)", 5, 30, 15)

st.sidebar.markdown("### ➕ Add a custom order")
st.sidebar.caption("Pick a restaurant, then click a spot on the map in the **Live Dashboard** tab to drop a delivery there.")
restaurant_choice = st.sidebar.selectbox(
    "Restaurant", restaurant_nodes, format_func=lambda n: f"Restaurant @ {pos[n]}"
)
new_order_time = st.sidebar.slider("Order time (min into simulation)", 0, 60, 30)
if st.sidebar.button("🗑️ Clear my custom orders"):
    st.session_state.custom_orders = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Built with NetworkX + scikit-learn (DBSCAN) + Google OR-Tools (VRP)")

orders = all_orders()

# ============================================================================
# PLOTTING HELPERS
# ============================================================================
def base_edge_trace(G, pos):
    xs, ys = [], []
    cxs, cys = [], []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        if data.get("congested"):
            cxs += [x0, x1, None]
            cys += [y0, y1, None]
        else:
            xs += [x0, x1, None]
            ys += [y0, y1, None]
    normal = go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#e0e0e0", width=1),
                         hoverinfo="skip", showlegend=False)
    congested = go.Scatter(x=cxs, y=cys, mode="lines", line=dict(color="#ffb3b3", width=2.5),
                            hoverinfo="skip", showlegend=False, name="Congested road")
    return [normal, congested]


def node_click_trace(G, pos):
    xs = [pos[n][0] for n in G.nodes()]
    ys = [pos[n][1] for n in G.nodes()]
    return go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=10, color="rgba(0,0,0,0.02)"),
                       hoverinfo="skip", showlegend=False, name="clickgrid")


def restaurant_trace(restaurant_nodes, pos):
    xs = [pos[n][0] for n in restaurant_nodes]
    ys = [pos[n][1] for n in restaurant_nodes]
    return go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=16, color="black", symbol="square"),
                       name="Restaurants", hovertext=[f"Restaurant {i}" for i in range(len(restaurant_nodes))])


def path_trace(pos, path, color, width=3, name=""):
    xs = [pos[n][0] for n in path]
    ys = [pos[n][1] for n in path]
    return go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color=color, width=width),
                       marker=dict(size=6, color=color), name=name)


def make_layout(title, height=560):
    return dict(
        title=dict(text=title, y=0.98),
        height=height,
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=50, b=90),
        plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="center", x=0.5, font=dict(size=11)),
    )

ZONE_COLORS = ["#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4",
               "#46f0f0", "#f032e6", "#bcf60c", "#fabebe", "#008080"]

# ============================================================================
# TABS
# ============================================================================
tab_intro, tab_graph, tab_zone, tab_batch, tab_route, tab_dash = st.tabs(
    ["🏙️ The Big Idea", "🗺️ Shortest Paths", "📍 Hyperlocal Zoning",
     "📦 Order Batching", "🚴 Routing (VRP)", "🎛️ Live Dashboard"]
)

# ----------------------------------------------------------------------
with tab_intro:
    st.title("Rebuilding a Food Delivery Dispatch Engine with Operations Research")
    st.markdown("""
A working reimplementation of the optimization stack behind platforms
like Zomato and Swiggy — zoning, batching, and routing — built end to
end. Every number shown in this app comes from an algorithm executing
on a real graph, not a static mockup.

A delivery platform must continuously solve three coupled decisions:
1. Which zone an order belongs to.
2. Which orders should be batched into a single trip.
3. What sequence minimizes travel time for that trip.

Each decision depends on accurate distance data and constrains the
next. Errors compound — an incorrect zone assignment produces a batch
with no real time overlap, and a suboptimal route adds delay to an
already-formed batch.

This app builds all three stages from scratch and lets you watch each one work.
""")
    st.markdown("### The pipeline")
    st.graphviz_chart("""
    digraph {
        rankdir=LR;
        node [shape=box, style="rounded,filled", fillcolor="#f0f2f6", fontname="Helvetica"];
        A [label="City road graph\\n(travel-time weighted)"];
        B [label="Hyperlocal zoning\\n(DBSCAN on travel time)"];
        C [label="Order batching\\n(same zone + time window)"];
        D [label="Routing\\n(OR-Tools open VRP)"];
        E [label="Rider trips\\non the map"];
        A -> B -> C -> D -> E;
    }
    """)
    st.markdown("""
### Approach

**Zoning.** DBSCAN clustering over a pairwise travel-time matrix
computed via Dijkstra, rather than clustering on raw coordinates. Two
delivery points can be geographically close but separated by
congestion or a missing direct road; travel-time distance captures
this, coordinate distance does not.

**Batching.** A greedy grouping algorithm operating within each zone:
orders are sorted by order time and packed into trips bounded by both
a maximum batch size and a rolling time window, so orders assigned to
the same zone at different times are not forced into a single trip.

**Routing.** Framed as an open-path Vehicle Routing Problem — a rider
starts at the restaurant, visits every drop-off, and does not return.
Solved with Google OR-Tools. The solver's default formulation assumes
a round trip; this is handled by introducing a zero-cost sink node
that terminates the route without a return-leg cost.

Two things make the real problems harder, and this app
actually implements both:

- **Distance ≠ straight line.** Two points 300m apart can be a 15-minute
  detour if there's no direct road or there's traffic. So zoning here
  clusters on a *travel-time matrix* computed with Dijkstra, not raw
  coordinates.
- **Batching + routing is a small VRP, not a TSP.** Once orders are
  batched, finding the best delivery sequence is an *open* Vehicle Routing
  Problem (start at the restaurant, visit all drop-offs, no return trip) —
  solved here with Google OR-Tools, not a greedy nearest-neighbor guess.

Use the tabs above to walk through each stage, then go to **Live Dashboard**
to run the whole thing end-to-end and click on the map to add your own orders.
""")

# ----------------------------------------------------------------------
with tab_graph:
    st.header("1. The city as a graph — Dijkstra vs A*")
    st.markdown("""
The city is modeled as a weighted graph: intersections are nodes, roads are
edges, and edge weight = travel time in minutes. Some roads (shown in
**red**) are randomly congested, so the shortest path is not always the
most direct-looking one.
""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Dijkstra's algorithm** explores outward by cumulative cost:")
        st.latex(r"d(v) = \min_{u \in N(v)} \big[ d(u) + w(u,v) \big]")
        st.caption("It guarantees the optimum but explores in every direction equally.")
    with col2:
        st.markdown("**A\\*** adds a heuristic to bias the search toward the target:")
        st.latex(r"f(n) = g(n) + h(n)")
        st.caption("h(n) = straight-line distance to target. Admissible here since roads are never shorter than straight-line, so A* still finds the true shortest path — just faster.")

    node_list = list(G.nodes())
    c1, c2 = st.columns(2)
    with c1:
        src = st.selectbox("Source node", node_list, index=0, format_func=lambda n: f"Node {n} @ {pos[n]}")
    with c2:
        tgt = st.selectbox("Target node", node_list, index=len(node_list) - 1, format_func=lambda n: f"Node {n} @ {pos[n]}")

    if src != tgt:
        dpath, dcost, dvisited = core.dijkstra_with_stats(G, src, tgt)
        apath, acost, avisited = core.astar_with_stats(G, src, tgt)

        fig = go.Figure()
        for tr in base_edge_trace(G, pos):
            fig.add_trace(tr)
        fig.add_trace(path_trace(pos, dpath, "#3cb44b", width=5, name=f"Shortest path (cost={dcost:.1f} min)"))
        fig.add_trace(go.Scatter(x=[pos[src][0], pos[tgt][0]], y=[pos[src][1], pos[tgt][1]],
                                  mode="markers+text", marker=dict(size=14, color=["green", "red"]),
                                  text=["Start", "End"], textposition="top center", showlegend=False))
        fig.update_layout(**make_layout("Shortest path (Dijkstra == A* in cost)"))
        st.plotly_chart(fig, width='stretch')

        m1, m2, m3 = st.columns(3)
        m1.metric("Path cost (both algorithms)", f"{dcost:.1f} min")
        m2.metric("Nodes settled — Dijkstra", dvisited)
        m3.metric("Nodes settled — A*", avisited, delta=f"{avisited - dvisited}")
        st.info("A* reaches the same optimal cost while typically settling fewer nodes, because the heuristic "
                "steers the search toward the target instead of expanding uniformly in all directions.")
    else:
        st.warning("Pick two different nodes.")

# ----------------------------------------------------------------------
with tab_zone:
    st.header("2. Hyperlocal zoning — DBSCAN on travel-time distance")
    st.markdown("""
**DBSCAN** groups points that are densely packed together, without needing
to pre-specify the number of zones (unlike k-means). A point is a **core
point** if it has enough neighbors within `eps`:
""")
    st.latex(r"|\,N_{\varepsilon}(p)\,| \geq \text{minSamples} \quad \text{where } N_{\varepsilon}(p) = \{q : \text{dist}(p,q) \leq \varepsilon\}")
    st.markdown("""
The critical design choice: **`dist(p,q)` here is real road travel time**
(computed via Dijkstra from every order to every other order), not
straight-line distance. This means two delivery points that look close on
a map but are separated by a highway or traffic will correctly end up in
*different* zones. Adjust `eps` / `min_samples` in the sidebar and watch
the zones reshape live.

Two parameters control this:
- **eps** — the maximum travel time, in minutes, for two delivery
  points to count as neighbors. Computed from the Dijkstra travel-time
  matrix, not straight-line distance. Lower values produce tighter,
  more numerous zones; higher values merge more orders into fewer,
  larger zones.
- **min_samples** — the minimum number of points required within eps
  of each other for that group to form a zone. Lower values make zones
  easier to form; higher values enforce a stricter density requirement,
  and orders that don't meet it are marked standalone rather than
  forced into a nearby cluster.

The distance function used here is travel time between delivery
points, not coordinate distance. Two points close on a map but
separated by congestion or a missing direct route will not be grouped
into the same zone under this metric, even though they would be under
Euclidean distance.
""")

    if orders:
        delivery_nodes = [o["delivery"] for o in orders]
        D_orders = core.travel_time_matrix(G, delivery_nodes)
        zone_labels = core.cluster_into_zones(D_orders, eps=eps, min_samples=min_samples)
        num_zones = len(set(zone_labels)) - (1 if -1 in zone_labels else 0)

        fig = go.Figure()
        for tr in base_edge_trace(G, pos):
            fig.add_trace(tr)
        for z in sorted(set(zone_labels)):
            idxs = [i for i in range(len(orders)) if zone_labels[i] == z]
            xs = [pos[orders[i]["delivery"]][0] for i in idxs]
            ys = [pos[orders[i]["delivery"]][1] for i in idxs]
            color = "gray" if z == -1 else ZONE_COLORS[z % len(ZONE_COLORS)]
            label = "Standalone" if z == -1 else f"Zone {z}"
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="markers", marker=dict(size=12, color=color),
                                      name=label))
        fig.add_trace(restaurant_trace(restaurant_nodes, pos))
        fig.update_layout(**make_layout(f"{num_zones} hyperlocal zones formed from {len(orders)} orders"))
        st.plotly_chart(fig, width='stretch')
        st.caption(f"{list(zone_labels).count(-1)} orders were too isolated to join any zone (shown in gray).")
    else:
        st.warning("No orders yet — add some in the sidebar or Live Dashboard tab.")

# ----------------------------------------------------------------------
with tab_batch:
    st.header("3. Order batching — greedy grouping within a zone + time window")
    st.markdown("""
Batching decides which of those same-zone orders should actually travel together in one trip on the basis of time,
since location alone doesn't guarantee two orders are compatible — an order
placed at minute 5 and another at minute 55 may fall in the same zone
but shouldn't share a rider.

### Formulation

For a zone containing orders O = {o_1, ..., o_n} with timestamps
t(o_i), the algorithm produces a partition B = {B_1, ..., B_k} such
that for every batch B_j:

  |B_j| <= max_batch_size
  max(t(o) for o in B_j) - min(t(o) for o in B_j) <= time_window

Two parameters control this, both adjustable in the sidebar:

- **max_batch_size** — the maximum number of orders a single rider trip
  can carry. Lower values keep trips small and easier to route quickly;
  higher values reduce the number of trips needed but increase route
  complexity per trip.
- **time_window** — the maximum spread, in minutes, between the first
  and last order in a trip. Lower values keep batches tightly
  synchronized in time; higher values allow more orders to combine at
  the cost of earlier orders waiting longer.
""")
    

    if orders:
        delivery_nodes = [o["delivery"] for o in orders]
        D_orders = core.travel_time_matrix(G, delivery_nodes)
        zone_labels = core.cluster_into_zones(D_orders, eps=eps, min_samples=min_samples)
        batches = core.batch_orders(orders, zone_labels, max_batch_size=max_batch_size, time_window=time_window)

        st.metric("Rider trips needed", len(batches), delta=f"vs {len(orders)} if unbatched", delta_color="inverse")
        rows = []
        for bi, batch in enumerate(batches):
            for i in batch:
                o = orders[i]
                rows.append({"Trip #": bi, "Order ID": o["id"], "Order time": o["order_time"],
                              "Zone": int(zone_labels[i]), "Restaurant node": o["restaurant"],
                              "Delivery node": o["delivery"]})
        st.dataframe(rows, width='stretch', hide_index=True)
    else:
        st.warning("No orders yet — add some in the sidebar or Live Dashboard tab.")

# ----------------------------------------------------------------------
with tab_route:
    st.header("4. Routing — open Vehicle Routing Problem (OR-Tools)")
    st.markdown("Given a batch, we need the visiting order that minimizes total travel time, starting at the restaurant and *not* returning:")
    st.latex(r"""
    \min \sum_{(i,j)} c_{ij} x_{ij} \quad \text{s.t.} \quad
    \sum_j x_{ij} = 1 \ \forall i, \quad \sum_i x_{ij} = 1 \ \forall j, \quad \text{no subtours}
    """)
    st.caption("Solved here with Google OR-Tools' routing solver (PATH_CHEAPEST_ARC construction heuristic). A dummy zero-cost sink node removes the 'return to depot' constraint of a classic VRP.")

    if orders:
        delivery_nodes = [o["delivery"] for o in orders]
        D_orders = core.travel_time_matrix(G, delivery_nodes)
        zone_labels = core.cluster_into_zones(D_orders, eps=eps, min_samples=min_samples)
        batches = core.batch_orders(orders, zone_labels, max_batch_size=max_batch_size, time_window=time_window)
        multi_batches = [b for b in batches if len(b) > 1]

        if multi_batches:
            choice = st.selectbox("Pick a multi-order batch to inspect", range(len(multi_batches)),
                                   format_func=lambda i: f"Batch {i} ({len(multi_batches[i])} orders)")
            batch = multi_batches[choice]
            batch_orders_list = [orders[i] for i in batch]
            depot = batch_orders_list[0]["restaurant"]
            stop_nodes = [depot] + [o["delivery"] for o in batch_orders_list]
            D_sub = core.travel_time_matrix(G, stop_nodes)

            route_idx = core.solve_batch_route(D_sub)
            naive_idx = list(range(len(stop_nodes)))
            opt_time = sum(D_sub[route_idx[k], route_idx[k + 1]] for k in range(len(route_idx) - 1))
            naive_time = sum(D_sub[naive_idx[k], naive_idx[k + 1]] for k in range(len(naive_idx) - 1))

            opt_path = core.full_path_for_route(G, stop_nodes, route_idx)
            naive_path = core.full_path_for_route(G, stop_nodes, naive_idx)

            c1, c2 = st.columns(2)
            with c1:
                fig = go.Figure()
                for tr in base_edge_trace(G, pos):
                    fig.add_trace(tr)
                fig.add_trace(path_trace(pos, naive_path, "#e6194b", name=f"Naive order ({naive_time:.1f} min)"))
                fig.update_layout(**make_layout("Naive visiting order", height=440))
                st.plotly_chart(fig, width='stretch')
            with c2:
                fig = go.Figure()
                for tr in base_edge_trace(G, pos):
                    fig.add_trace(tr)
                fig.add_trace(path_trace(pos, opt_path, "#3cb44b", name=f"OR-Tools optimized ({opt_time:.1f} min)"))
                fig.update_layout(**make_layout("OR-Tools optimized order", height=440))
                st.plotly_chart(fig, width='stretch')

            saved_pct = 100 * (1 - opt_time / naive_time) if naive_time > 0 else 0
            st.metric("Time saved by optimizing this batch's route", f"{saved_pct:.1f}%",
                       f"{naive_time - opt_time:.1f} min")
        else:
            st.info("No multi-order batches yet with current settings — widen `time_window` or `eps`, or add more orders.")
    else:
        st.warning("No orders yet — add some in the sidebar or Live Dashboard tab.")

# ----------------------------------------------------------------------
with tab_dash:
    st.header("🎛️ Live Dashboard — full pipeline, click to add orders")
    st.markdown(f"Currently simulating **{len(orders)} orders** "
                f"({len(st.session_state.random_orders)} random + {len(st.session_state.custom_orders)} custom). "
                f"Click anywhere on the map below to add a delivery for **the restaurant selected in the sidebar**.")

    result = core.run_full_pipeline(G, orders, eps, min_samples, max_batch_size, time_window)
    zone_labels = result["zone_labels"]
    batch_routes = result["batch_routes"]

    fig = go.Figure()
    for tr in base_edge_trace(G, pos):
        fig.add_trace(tr)
    fig.add_trace(node_click_trace(G, pos))

    for bi, br in enumerate(batch_routes):
        color = ZONE_COLORS[bi % len(ZONE_COLORS)]
        fig.add_trace(path_trace(pos, br["path"], color, width=2.5, name=f"Trip {bi} ({len(br['order_ids'])} orders)"))
    st.caption(f"{len(batch_routes)} rider trips shown on map, one color each (hover over a line to see which).")

    fig.add_trace(restaurant_trace(restaurant_nodes, pos))
    fig.update_layout(**make_layout("Delivery map", height=1000))
    st.plotly_chart(fig, width='stretch')

    st.markdown("#### ➕ Add a delivery order")
    add_col1, add_col2 = st.columns(2)
    with add_col1:
        drop_node = st.selectbox(
            "Delivery location (intersection)",
            list(G.nodes()),
            format_func=lambda n: f"Node {n} @ {pos[n]}",
            key="drop_node_select",
        )
    with add_col2:
        if st.button("Add order here"):
            new_id = f"C{len(st.session_state.custom_orders)}"
            st.session_state.custom_orders.append({
                "id": new_id, "restaurant": restaurant_choice,
                "delivery": drop_node, "order_time": new_order_time,
            })
            st.rerun()

    st.markdown("### 📊 Pipeline results")
    num_zones = len(set(zone_labels.tolist())) - (1 if -1 in zone_labels else 0) if len(zone_labels) else 0
    saved_pct = (100 * (1 - result["total_optimized_time"] / result["total_naive_time"])
                 if result["total_naive_time"] > 0 else 0)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Hyperlocal zones", num_zones)
    m2.metric("Rider trips", len(result["batches"]))
    m3.metric("Avg orders/trip", f"{len(orders)/len(result['batches']):.2f}" if result["batches"] else "0")
    m4.metric("Time saved by batching+routing vs naive", f"{saved_pct:.1f}%")
