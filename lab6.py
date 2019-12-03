# CS3
# Angel Rodriguez II
# Lab 6
# Diego Aguirre
# 12-02-2019
# Purpose: The purpose of this lab is to implement kruskal's algorithm and a topological sort algorithm


import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

list = []

class DisjointSetForest:
    def __init__(self, n):
        self.forest = [-1] * n

    def is_index_valid(self, index):
        return 0 <= index < len(self.forest)

    def find(self, a):
        if not self.is_index_valid(a):
            return -1

        if self.forest[a] < 0:
            return a

        return self.find(self.forest[a])

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)

        if ra != rb:  # Problems 3 and 4
            self.forest[rb] = ra

    def find_contains_loop(self, a, s=None):
        if not self.is_index_valid(a):
            return -1

        if s is None:
            s = set()

        if a in s:
            print("Loop found")
            return -1

        s.add(a)

        if self.forest[a] < 0:
            return a

        return self.find_contains_loop(self.forest[a], s)

class Edge:
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight

class GraphAL:
    # Constructor
    def __init__(self, vertices, weighted=False, directed=False):
        self.al = [[] for i in range(vertices)]
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AL'

    def is_valid_vertex(self, u):
        return 0 <= u < len(self.al)

    def insert_edge(self, weight, source, dest):
        if not self.is_valid_vertex(source) or not self.is_valid_vertex(dest):
            print('Error, vertex number out of range')
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.al[source].append(Edge(dest, weight))
            if not self.directed:
                self.al[dest].append(Edge(source, weight))

    def delete_edge(self, source, dest):
        if source >= len(self.al) or dest >= len(self.al) or source < 0 or dest < 0:
            print('Error, vertex number out of range')
        else:
            deleted = self._delete_edge(source, dest)
            if not self.directed:
                deleted = self._delete_edge(dest, source)
            if not deleted:
                print('Error, edge to delete not found')

    def _delete_edge(self, source, dest):
        i = 0
        for edge in self.al[source]:
            if edge.dest == dest:
                self.al[source].pop(i)
                return True
            i += 1
        return False

    def num_vertices(self):
        return len(self.al)

    def get_highest_cost_edge(self):

        max_key = -float("inf")

        for lst in self.al:
            for edge in lst:
                max_key = max(edge.weight, max_key)

        return max_key

    def num_edges(self):
        count = 0

        for lst in self.al:
            count += len(lst)

        return count

    def edge_weight(self, src, dest):
        if not self.is_valid_vertex(src) or not self.is_valid_vertex(dest):
            return 0  # Design decision

        lst = self.al[src]

        for edge in lst:
            if edge.dest == dest:
                return edge.weight

        return 0

    def contains_cyle(self):  # Asumption: Directed Graph
        dsf = DisjointSetForest(self.num_vertices())

        for i in range(len(self.al)):
            for edge in self.al[i]:
                if dsf.find(i) == dsf.find(edge.dest):
                    return True

                dsf.union(i, edge.dest)

        return False

    def get_list_of_unsorted_edges(self):
        for i in range(len(self.al)):
            for edge in self.al[i]:
                e = (str(edge.weight) + ',' + str(i) +',' + str(edge.dest))
                list.append(e)
        return list

    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(self.al)):
            for edge in self.al[i]:
                d, w = edge.dest, edge.weight
                if self.directed or d > i:
                    x = np.linspace(i * scale, d * scale)
                    x0 = np.linspace(i * scale, d * scale, num=5)
                    diff = np.abs(d - i)
                    if diff == 1:
                        y0 = [0, 0, 0, 0, 0]
                    else:
                        y0 = [0, -6 * diff, -8 * diff, -6 * diff, 0]
                    f = interp1d(x0, y0, kind='cubic')
                    y = f(x)
                    s = np.sign(i - d)
                    ax.plot(x, s * y, linewidth=1, color='k')
                    if self.directed:
                        xd = [x0[2] + 2 * s, x0[2], x0[2] + 2 * s]
                        yd = [y0[2] - 1, y0[2], y0[2] + 1]
                        yd = [y * s for y in yd]
                        ax.plot(xd, yd, linewidth=1, color='k')
                    if self.weighted:
                        xd = [x0[2] + 2 * s, x0[2], x0[2] + 2 * s]
                        yd = [y0[2] - 1, y0[2], y0[2] + 1]
                        yd = [y * s for y in yd]
                        ax.text(xd[2] - s * 2, yd[2] + 3 * s, str(w), size=12, ha="center", va="center")
            ax.plot([i * scale, i * scale], [0, 0], linewidth=1, color='k')
            ax.text(i * scale, 0, str(i), size=20, ha="center", va="center",
                    bbox=dict(facecolor='w', boxstyle="circle"))
        ax.axis('off')
        ax.set_aspect(1.0)
        plt.show()

    def vertices_reachable_from(self, src):
        reachable_vertices = []

        for edge in self.al[src]:
            reachable_vertices.append(edge.dest)

        return reachable_vertices


    def kruskal(self):
        list = self.get_list_of_unsorted_edges()  # gets all the edges and puts them into an list
        num_vert = (self.num_vertices())
        graph2 = GraphAL(num_vert, True, True) # making a new graph with the same number of verticies as the original graph

        # print('----edges BEFORE sorting---')
        # for i in range(len(list)): # prints the list before it's sorted
        #     print(list[i])
        #
        # print('----sorted list----')
        list.sort()
        # for i in range(len(list)): # prints the list after sorting
        #     print(list[i])

        for i in range(len(list)):
            edge = list[i]
            info = edge.split(",")
            weight = int(info[0])
            source = int(info[1])
            dest = int(info[2])
            graph2.insert_edge(weight, source, dest) # inserts edge by edge from the sorted list
            if graph2.contains_cyle(): # if the most recently added edge creates a cycle, enter this if statement
                graph2.delete_edge(source, dest) # deletes the most recently added edge

        self.draw() # figure 1 is the original graph

        graph2.draw() # figure 2 is the graph with kruskals algorithm applied to it

    def topological_sort(self):
        adj_list = []

        for i in range(self.num_vertices()):
            adj_list.append(self.vertices_reachable_from(i))

        all_in_degrees = self.find_in_degree(adj_list, self.num_vertices())

        # for i in range(len(all_in_degrees)):
        #     print(str(i) + ': ' + str(all_in_degrees[i]))

        sort_result = []

        q = []

        for i in range(len(all_in_degrees)):
            if all_in_degrees[i] == 0:
                q.append(i)

        while len(q) != 0:
            u = q.pop()

            sort_result.append(u)

            for adj_vertex in self.vertices_reachable_from(u):
                all_in_degrees[adj_vertex] -= 1

                if all_in_degrees[adj_vertex] == 0:
                    q.append(adj_vertex)

        if len(sort_result) != self.num_vertices():  # cycle found
            return None
        return sort_result

    def find_in_degree(self, adjList, n):  # this method will find the in degrees and return a list
        _in = [0] * n
        out = [0] * n

        for i in range(0, len(adjList)):
            List = adjList[i]
            # Out degree for ith vertex will be the count
            # of direct paths from i to other vertices
            out[i] = len(List)
            for j in range(0, len(List)):
                # Every vertex that has
                # an incoming edge from i
                _in[List[j]] += 1
        return _in