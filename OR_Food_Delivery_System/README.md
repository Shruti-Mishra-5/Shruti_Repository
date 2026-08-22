# Hyperlocal Delivery OR — Streamlit App

Replicates the Zomato/Swiggy-style delivery pipeline: hyperlocal zoning (DBSCAN on
travel-time), order batching, and routing (open VRP via OR-Tools) — with a full
theory walkthrough alongside a live, clickable city map.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Tabs
- **The Big Idea** — overview of the 3-stage pipeline and why it's harder than a
  textbook TSP/k-means demo.
- **Shortest Paths** — Dijkstra vs A*, pick any two nodes and compare.
- **Hyperlocal Zoning** — DBSCAN on a Dijkstra-computed travel-time matrix, live
  eps/min_samples sliders.
- **Order Batching** — greedy batching by zone + time window, shown as a table.
- **Routing (VRP)** — OR-Tools open VRP solve, naive vs optimized route compared
  side by side.
- **Live Dashboard** — full pipeline end-to-end. Click anywhere on the map to drop
  a new delivery order for the restaurant selected in the sidebar, and watch
  zones/batches/routes update live.

## Notes
- Everything runs on a synthetic 12x12 grid city graph (random travel times +
  simulated traffic), so there's no dependency on external map data.
- Swap `core.build_city_graph` for a real OSM-based graph (via `osmnx`) later if
  you want to extend this to a real city — the rest of the pipeline is unchanged.
