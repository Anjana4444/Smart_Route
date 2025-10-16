# graph_manager.py
import heapq
import matplotlib.pyplot as plt
import networkx as nx
import datetime
from collections import deque


class GraphManager:
    def __init__(self):
        self.graph = {}
        self.original_graph = {}
        self.road_speeds = {}

    def add_route(self, city1, city2, distance):
        """Add a bidirectional route to both graph and original_graph."""
        d = float(distance)
        for g in (self.graph, self.original_graph):
            if city1 not in g:
                g[city1] = {}
            if city2 not in g:
                g[city2] = {}
            g[city1][city2] = d
            g[city2][city1] = d

        if d < 30:
            speed = 40.0   
        elif d < 100:
            speed = 60.0   
        else:
            speed = 90.0   

        self.road_speeds[(city1, city2)] = speed
        self.road_speeds[(city2, city1)] = speed

    def get_all_routes(self):
        """Return list of unique routes as (city, neighbor, distance)."""
        routes = []
        seen = set()
        for city in self.graph:
            for neighbor, dist in self.graph[city].items():
                if (neighbor, city) in seen:
                    continue
                routes.append((city, neighbor, dist))
                seen.add((city, neighbor))
        return routes

    # Dijkstra
    def dijkstra(self, start, goal):
        """Return (path_list, total_distance) or (None, None) if unreachable."""
        if start not in self.graph or goal not in self.graph:
            return None, None

        pq = [(0.0, start, [])]
        visited = set()

        while pq:
            cost, node, path = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            path = path + [node]

            if node == goal:
                return path, round(cost, 2)

            for neigh, w in self.graph[node].items():
                if neigh not in visited:
                    heapq.heappush(pq, (cost + w, neigh, path))

        return None, None

    # A*
    def a_star(self, start, goal):
        """A* search returning (path, distance)."""
        if start not in self.graph or goal not in self.graph:
            return None, None

        def heuristic(a, b):
            return abs(len(a) - len(b)) * 5

        open_heap = [(heuristic(start, goal), start)]
        came_from = {}
        g_score = {start: 0.0}

        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1], round(g_score[goal], 2)

            for neigh, w in self.graph[current].items():
                tentative_g = g_score[current] + w
                if neigh not in g_score or tentative_g < g_score[neigh]:
                    came_from[neigh] = current
                    g_score[neigh] = tentative_g
                    f = tentative_g + heuristic(neigh, goal)
                    heapq.heappush(open_heap, (f, neigh))

        return None, None

    # Bellman Ford
    def bellman_ford(self, start, goal):
        """Compute shortest path even with negative weights."""
        if start not in self.graph or goal not in self.graph:
            return None, None

        dist = {node: float("inf") for node in self.graph}
        prev = {node: None for node in self.graph}
        dist[start] = 0.0

        for _ in range(len(self.graph) - 1):
            for u in self.graph:
                for v, w in self.graph[u].items():
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        prev[v] = u

        for u in self.graph:
            for v, w in self.graph[u].items():
                if dist[u] + w < dist[v]:
                    print("Warning: Negative weight cycle detected!")
                    return None, None

        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()

        if dist[goal] == float("inf"):
            return None, None

        return path, round(dist[goal], 2)

    # BFS/DFS
    def bfs(self, start, goal):
        if start not in self.graph or goal not in self.graph:
            return None
        if start == goal:
            return [start]

        visited = set([start])
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            node = path[-1]
            for neigh in self.graph.get(node, {}):
                if neigh in visited:
                    continue
                new_path = list(path) + [neigh]
                if neigh == goal:
                    return new_path
                queue.append(new_path)
                visited.add(neigh)
        return None

    def dfs(self, start, goal, visited=None, path=None):
        if start not in self.graph or goal not in self.graph:
            return None
        if visited is None:
            visited = set()
        if path is None:
            path = []
        visited.add(start)
        path = path + [start]
        if start == goal:
            return path
        for neigh in self.graph.get(start, {}):
            if neigh not in visited:
                res = self.dfs(neigh, goal, visited, path)
                if res:
                    return res
        return None

    # Prim's MST

    def prim_mst(self):
        if not self.graph:
            return [], 0.0

        start = next(iter(self.graph))
        visited = set([start])
        edges = []
        total = 0.0

        while len(visited) < len(self.graph):
            candidate = None
            candidate_w = float("inf")
            for u in visited:
                for v, w in self.graph[u].items():
                    if v not in visited and w < candidate_w:
                        candidate = (u, v, w)
                        candidate_w = w
            if candidate is None:
                break
            u, v, w = candidate
            edges.append((u, v, w))
            total += w
            visited.add(v)

        return edges, round(total, 2)

    # Kruskal MST
    def kruskal_mst(self):
        parent = {}
        rank = {}

        def make_set(x):
            parent[x] = x
            rank[x] = 0

        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra == rb:
                return False
            if rank[ra] < rank[rb]:
                parent[ra] = rb
            else:
                parent[rb] = ra
                if rank[ra] == rank[rb]:
                    rank[ra] += 1
            return True

        for node in self.graph:
            make_set(node)

        edge_list = []
        seen = set()
        for u in self.graph:
            for v, w in self.graph[u].items():
                if (v, u) in seen:
                    continue
                edge_list.append((u, v, w))
                seen.add((u, v))

        edge_list.sort(key=lambda x: x[2])

        mst = []
        total = 0.0
        for u, v, w in edge_list:
            if union(u, v):
                mst.append((u, v, w))
                total += w

        return mst, round(total, 2)

    
    def calculate_travel_time(self, distance, speed):
        if speed <= 0:
            return "N/A"
        hours = distance / speed
        h = int(hours)
        m = int(round((hours - h) * 60))
        return f"{h}h {m}m" if h > 0 else f"{m}m"

    def compare_algorithms(self, start, goal):
        d_path, d_dist = self.dijkstra(start, goal)
        a_path, a_dist = self.a_star(start, goal)
        b_path, b_dist = self.bellman_ford(start, goal)

        if not d_path or not a_path or not b_path:
            return "Comparison failed (invalid path)."

        result = (
            f"Dijkstra: {d_dist:.2f} km\n"
            f"A*: {a_dist:.2f} km\n"
            f"Bellman-Ford: {b_dist:.2f} km\n"
        )
        best = min((d_dist, "Dijkstra"), (a_dist, "A*"), (b_dist, "Bellman-Ford"))
        result += f"→ Best (shortest) path: {best[1]}"
        return result

    # Traffic
    def simulate_traffic(self, factor):
        if not self.original_graph:
            return "No routes available."

        for city, neighbors in self.original_graph.items():
            for dest, base_dist in neighbors.items():
                if city in self.graph and dest in self.graph[city]:
                    self.graph[city][dest] = round(base_dist * factor, 2)

        new_speeds = {}
        for (a, b), base_speed in self.road_speeds.items():
            new_speed = max(10.0, round(base_speed / factor, 1))
            new_speeds[(a, b)] = new_speed
        self.road_speeds = new_speeds

        hour = datetime.datetime.now().hour
        rush = (7 <= hour <= 9) or (16 <= hour <= 18)
        if rush:
            for k in list(self.road_speeds.keys()):
                self.road_speeds[k] = max(10.0, round(self.road_speeds[k] * 0.85, 1))
            return "Traffic updated (with Rush Hour slowdown)."
        return "Traffic updated."

    def reset_traffic(self):
        if not self.original_graph:
            return "Nothing to reset."
        self.graph = {k: v.copy() for k, v in self.original_graph.items()}
        self._restore_speeds()
        return "Traffic reset to normal flow."

    def _restore_speeds(self):
        self.road_speeds.clear()
        for a in self.graph:
            for b, dist in self.graph[a].items():
                if dist < 30:
                    speed = 40.0
                elif dist < 100:
                    speed = 60.0
                else:
                    speed = 90.0
                self.road_speeds[(a, b)] = speed

    
    def visualize_graph(self, highlight_path=None, is_tree=False):
        if not self.graph:
            print("Graph is empty.")
            return

        G = nx.Graph()
        for u in self.graph:
            for v, w in self.graph[u].items():
                G.add_edge(u, v, weight=w)

        pos = self._hierarchical_pos(G) if is_tree else nx.spring_layout(G, seed=42)

        highlight_edges = set()
        if highlight_path:
            if all(isinstance(item, tuple) for item in highlight_path):
                for e in highlight_path:
                    if len(e) >= 2:
                        a, b = e[0], e[1]
                        highlight_edges.add((a, b))
                        highlight_edges.add((b, a))
            else:
                for i in range(len(highlight_path) - 1):
                    a = highlight_path[i]
                    b = highlight_path[i + 1]
                    highlight_edges.add((a, b))
                    highlight_edges.add((b, a))

        edge_colors = []
        for (u, v) in G.edges():
            if (u, v) in highlight_edges or (v, u) in highlight_edges:
                edge_colors.append("red")
            else:
                edge_colors.append("#999999")

        plt.figure(figsize=(9, 7))
        plt.title("SmartRoute+ Network Visualization", color="white", fontsize=13)
        nx.draw(G, pos, with_labels=True, node_color="#00FFAA", edge_color=edge_colors,
                node_size=1300, font_weight='bold', font_color='black')
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='mediumseagreen')
        plt.show()

    def _hierarchical_pos(self, G, root=None):
        if root is None:
            root = max(G.nodes(), key=lambda n: G.degree(n))

        layers = []
        visited = set([root])
        q = deque([root])
        while q:
            level_size = len(q)
            layer = []
            for _ in range(level_size):
                node = q.popleft()
                layer.append(node)
                for neigh in G.neighbors(node):
                    if neigh not in visited:
                        visited.add(neigh)
                        q.append(neigh)
            layers.append(layer)

        pos = {}
        max_width = max(len(layer) for layer in layers) if layers else 1
        y_gap = 1.0 / max(1, len(layers))
        for depth, layer in enumerate(layers):
            x_gap = 1.0 / max(1, len(layer))
            for i, node in enumerate(layer):
                x = (i + 0.5) * x_gap
                y = 1.0 - depth * y_gap
                pos[node] = (x * max_width, y)
        for node in G.nodes():
            if node not in pos:
                pos[node] = (0, 0)
        return pos
