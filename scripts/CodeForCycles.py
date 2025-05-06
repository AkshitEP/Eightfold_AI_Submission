import csv
from collections import defaultdict
import ast

class Graph:
    def __init__(self):
        # Adjacency list representation of the graph
        self.graph = defaultdict(list)

    # Function to add a directed edge to the graph
    def add_edge(self, u, v):
        self.graph[u].append(v)

    def build_graph_from_csv(self, csv_file_path):
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                person_id = row['ID']  # The ID of the person being recommended
                recommenders = ast.literal_eval(row['Recommenders ID'])  # Convert string to list
                
                # Add an edge from each recommender to the person
                for recommender in recommenders:
                    self.add_edge(recommender, person_id)

    # Function to find all cycles that include a specific vertex
    def find_cycles(self, start_vertex):
        all_cycles = []  # to store all found cycles
        path = []  # to store the current path
        visited = set()  # to track visited nodes

        def dfs(v, start):
            visited.add(v)   # Mark the current node as visited
            path.append(v)   # Add the current node to the path

            # Explore all adjacent vertices
            for neighbor in self.graph[v]:
                if neighbor == start:
                    # Cycle found (includes the start vertex)
                    cycle = path + [start]  # Complete the cycle
                    all_cycles.append(cycle)  # Add the cycle to the list
                elif neighbor not in visited:
                    dfs(neighbor, start)  # Continue DFS with unvisited nodes

            # Backtrack
            path.pop()  # Remove the last vertex from the path
            visited.remove(v)  # Unmark the vertex as visited

        # Start DFS from the given vertex to detect cycles
        dfs(start_vertex, start_vertex)

        return all_cycles

# Example usage:
g = Graph()

# Build the graph from a CSV file
g.build_graph_from_csv('/Users/vansh/Desktop/hackathon/Final_Persons_And_Recommenders.csv')

# Specify the vertex to find cycles for
for i in range(1000):

    start_vertex = str(i)  # Replace with an ID you want to check

    # Find and print all cycles involving the start vertex
    cycles = g.find_cycles(start_vertex)
    if cycles == []:
        continue
    print(f"All cycles involving vertex {start_vertex}:")
    for cycle in cycles:
        print(cycle)
