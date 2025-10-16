import heapq
import matplotlib.pyplot as plt
import networkx as nx
import datetime 
from collections import deque

class GraphManager:
    def __init__(self):
        self.graph ={}
        self.original_graph = {}
        self.road_speeds ={}

    def add_route(self,city1,city2,distance):

        d= float(distance)
        for g in (self.graph, self.original_graph):
            if(city1 not in g):
                g[city1]={}
            if(city2 not in g):
                g[city2]={}
            g[city1][city2]=d
            g[city2][city1]=d


        if d < 30:
            speed = 40.0
        elif d< 100:
            speed = 60.0
        else:
            speed = 90.0

        self.road_speeds[(city1),(city2)] =speed
        self.road_speeds[(city2),(city1)] =speed

        def get_all_routes(self):

            routes= []
            seen= set()
            for city in self.graph:
                for neighbor,dist in self.graph[city].items():
                    if(neighbor,city) in seen:
                        continue
                    routes.append((city,neighbor,dist))
                    seen.add((city,neighbor))
            return routes
        
        #Dijkstra

        def dijkstra(self,start,goal):

            if start not in self.graph or goal not in self.graph:
                return None,None

            pq=[(0.0,start,[])]
            visited= set()

            while pq:
                cost, node, path= heapq.heappop(pq)
                if node in visited:
                    continue
                visited.add(node)
                path= path+ [node]

                if node == goal:
                    return path, round(cost,2)
                
                for neigh, w in self.graph[node].items():
                    if neigh not in visited:
                        heapq.heappush(pq, (cost+ w, neigh, path))

                return None,None
            
        
        # A*

        def a_star(self,start,goal):

            if start not in self.graph or goal not in self.graph:
                return None, None
            def heuristic(a,b):
                return abs(len(a) - len(b)) *5
            
            open_heap= [(heuristic(start,goal),start)]
            came_from= {}
            g_score = {start: 0.0}

            while open_heap:
                _, current =heapq.heappop(open_heap)
                if current ==goal:
                    path= [current]
                    while current in came_from:
                        current = came_from[current]
                        path.append(current)
                    return path[::-1],round(g_score[goal],2)
                for neigh, w in self.graph[current].items():
                    tentative_g = g_score[current] +w
                    if neigh not in g_score or tentative_g < g_score[neigh]:
                        came_from[neigh]= current 
                        g_score[neigh]= tentative_g
                        f= tentative_g + heuristic(neigh, goal)
                        heapq.heappush(open_heap, (f, neigh))

                return None, None
            
        
        

