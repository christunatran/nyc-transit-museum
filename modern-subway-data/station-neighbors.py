import csv
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(SCRIPT_DIR, "raw")
COMPLEXES_FILE = os.path.join(RAW_DIR, "MTA_Subway_Stations_and_Complexes.csv")
PATHS_FILE = os.path.join(RAW_DIR, "subway-paths.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "station-neighbors.csv")


def load_complexes():
    """Load station complexes and build a GTFS Stop ID -> complex lookup."""
    lookup = {}
    with open(COMPLEXES_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for sid in row["GTFS Stop IDs"].replace(";", " ").split():
                sid = sid.strip()
                if sid:
                    lookup[sid] = row
    return lookup


def load_paths():
    """Load all subway paths, grouped by Stop Path ID."""
    by_path = defaultdict(list)
    with open(PATHS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            by_path[row["Stop Path ID"]].append(row)
    for rows in by_path.values():
        rows.sort(key=lambda x: int(x["Stop Order"]))
    return by_path


def build_route_adjacency(by_path):
    """
    For each route, build a set of adjacent station pairs and collect all
    stations.

    Uses all paths (both directions) and resolves canonical direction for each
    edge by counting how often A precedes B vs B precedes A. Then removes
    express edges (A->C where intermediate local stops exist between A and C).
    """
    # Build edges using N-direction paths as primary, supplementing with
    # reversed S-direction edges for stations that only appear in S paths.
    n_pair_counts = defaultdict(lambda: defaultdict(int))
    s_pair_counts = defaultdict(lambda: defaultdict(int))
    route_stations = defaultdict(set)

    for pid, rows in by_path.items():
        route = rows[0]["Line"]
        direction = rows[0]["Direction"]
        for row in rows:
            route_stations[route].add(row["Station ID"])
        for i in range(len(rows) - 1):
            a = rows[i]["Station ID"]
            b = rows[i + 1]["Station ID"]
            if a != b:
                if direction == "N":
                    n_pair_counts[route][(a, b)] += 1
                else:
                    s_pair_counts[route][(a, b)] += 1

    route_pairs = defaultdict(set)
    for route in route_stations:
        n_counts = n_pair_counts[route]
        s_counts = s_pair_counts[route]

        # Start with N-direction edges, resolving bidirectional conflicts
        seen = set()
        for (a, b), count in n_counts.items():
            key = tuple(sorted([a, b]))
            if key in seen:
                continue
            seen.add(key)
            reverse_count = n_counts.get((b, a), 0)
            if count >= reverse_count:
                route_pairs[route].add((a, b))
            else:
                route_pairs[route].add((b, a))

        # Add reversed S-direction edges for pairs not covered by N-direction
        for (a, b), count in s_counts.items():
            key = tuple(sorted([a, b]))
            if key in seen:
                continue
            seen.add(key)
            # Reverse S-direction: S goes A->B means N goes B->A
            reverse_count = s_counts.get((b, a), 0)
            if count >= reverse_count:
                route_pairs[route].add((b, a))
            else:
                route_pairs[route].add((a, b))

    # Remove express edges: (A, C) is express if there exists B != C in
    # forward[A] such that B can reach C without passing through A.
    route_adjacency = {}
    for route, pairs in route_pairs.items():
        forward = defaultdict(set)
        for a, b in pairs:
            forward[a].add(b)

        local_pairs = set()
        for a, c in pairs:
            is_express = False
            for b in forward[a]:
                if b == c:
                    continue
                if _can_reach(b, c, forward, max_hops=80, excluded={a}):
                    is_express = True
                    break
            if not is_express:
                local_pairs.add((a, c))

        route_adjacency[route] = local_pairs

    return route_adjacency, route_stations


def _can_reach(start, target, forward, max_hops, excluded=None):
    """BFS to check if target is reachable from start within max_hops.
    Nodes in 'excluded' are not traversed as intermediaries."""
    visited = set(excluded) if excluded else set()
    frontier = {start} - visited
    for _ in range(max_hops):
        if not frontier:
            return False
        if target in frontier:
            return True
        visited |= frontier
        next_frontier = set()
        for node in frontier:
            next_frontier |= forward[node] - visited
        frontier = next_frontier
    return target in frontier


def build_route_order(route_adjacency, route_stations):
    """
    For each route, establish a canonical stop order by traversing the
    adjacency graph from terminal stations. Handles branches.
    Returns a dict: route -> list of (station_id, stop_order).
    Also returns the neighbor info: route -> station_id -> (before_set, after_set).
    """
    route_orders = {}
    route_neighbors = {}

    for route, pairs in route_adjacency.items():
        # Build forward (N direction) and backward adjacency
        forward = defaultdict(set)
        backward = defaultdict(set)
        for a, b in pairs:
            forward[a].add(b)
            backward[b].add(a)

        all_stations = route_stations[route]

        # Find start stations (no backward edges = southern terminals)
        starts = [s for s in all_stations if s not in backward or not backward[s]]
        if not starts:
            # Cycle (shouldn't happen, but handle it) - pick any station
            starts = [next(iter(all_stations))]

        # BFS from all starts to assign stop order
        visited = set()
        order = []
        queue = list(starts)
        # Sort starts for determinism
        queue.sort()
        while queue:
            next_queue = []
            for station in queue:
                if station in visited:
                    continue
                # Check if all predecessors have been visited
                preds = backward.get(station, set())
                if preds and not preds.issubset(visited) and station not in starts:
                    next_queue.append(station)
                    continue
                visited.add(station)
                order.append(station)
                for neighbor in sorted(forward.get(station, set())):
                    if neighbor not in visited:
                        next_queue.append(neighbor)
            if next_queue == queue:
                # Break potential infinite loops - force visit remaining
                for station in next_queue:
                    if station not in visited:
                        visited.add(station)
                        order.append(station)
                        for neighbor in sorted(forward.get(station, set())):
                            if neighbor not in visited:
                                next_queue.append(neighbor)
                break
            queue = next_queue

        # Add any stations not reached (shouldn't happen but be safe)
        for s in sorted(all_stations):
            if s not in visited:
                order.append(s)

        route_orders[route] = [(sid, i + 1) for i, sid in enumerate(order)]

        # Build neighbor info - forward = after (in N direction), backward = before
        neighbors = {}
        for sid in all_stations:
            before = sorted(backward.get(sid, set()))
            after = sorted(forward.get(sid, set()))
            neighbors[sid] = (before, after)
        route_neighbors[route] = neighbors

    return route_orders, route_neighbors


def main():
    complexes = load_complexes()
    by_path = load_paths()
    route_adjacency, route_stations = build_route_adjacency(by_path)
    route_orders, route_neighbors = build_route_order(route_adjacency, route_stations)

    # Build station name lookup from paths data (for neighbor names)
    path_station_names = {}
    stop_by_direction = {}
    for rows in by_path.values():
        for row in rows:
            path_station_names[row["Station ID"]] = row["Station Name"]
            stop_by_direction[row["Station ID"]] = row["Direction"]

    output_rows = []
    for route in sorted(route_orders.keys()):
        for station_id, stop_order in route_orders[route]:
            complex_info = complexes.get(station_id, {})
            before_ids, after_ids = route_neighbors[route][station_id]

            # Look up neighbor names
            before_names = [path_station_names.get(sid, sid) for sid in before_ids]
            after_names = [path_station_names.get(sid, sid) for sid in after_ids]

            output_rows.append(
                {
                    "station_id": station_id,
                    "station_name": path_station_names.get(station_id, station_id),
                    "stop_order": stop_order,
                    "route": route,
                    "stop_name": complex_info.get("Stop Name", ""),
                    "borough": complex_info.get("Borough", ""),
                    "latitude": complex_info.get("Latitude", ""),
                    "longitude": complex_info.get("Longitude", ""),
                    "ada": complex_info.get("ADA", ""),
                    "ada_notes": complex_info.get("ADA Notes", ""),
                    "stations_before": "; ".join(before_names),
                    "stations_after": "; ".join(after_names),
                    "direction": stop_by_direction[station_id]
                }
            )

    fieldnames = [
        "station_id",
        "station_name",
        "stop_order",
        "route",
        "stop_name",
        "borough",
        "latitude",
        "longitude",
        "ada",
        "ada_notes",
        "stations_before",
        "stations_after",
        "direction",
    ]
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Wrote {len(output_rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
