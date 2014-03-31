#/usr/env python
import sys
import random
from collections import deque
import profile

sys.setrecursionlimit(10**6)

DEGREE = 6
MIN_WEIGHT = 1
MAX_WEIGHT = 50
NUM_VERTEX = 5000

class Node:

  def __init__(self, value):
    self.value = value
    self.rank = 0
    self.parent = self
    self.child = []

  def __repr__(self):
    return "Node {0} {1} P:{2}".format(self.value, self.rank, self.parent.value)

class Graph:

    def __init__(self, n):
        self.matrix = self.array_init(n, 0)
        self.degreeTable = [0 for i in range(n)]
        self.vertex = [i for i in range(n)]
        self.num_vertex = n
        self.color = [] # for DFS

    def __iter__(self):
        self.current = (0,-1)
        return self

    def next(self):
        v = self.current[0]
        u = self.current[1]

        u +=1
        if u >= len(self.matrix[v]):
            u = 0
            v +=1

        if v >= len(self.matrix):
            raise StopIteration
        else:
            edge_id = (v, u)
            edge_weight = self.getWeight(v, u)
            self.current = (v,u)
            return (edge_id, edge_weight)

    def __len__(self):
        """
        return number of edge in this graph
        """
        count = 0
        for row in self.matrix:
            for elm in row:
                if elm > 0:
                    count += 1
        return count

    def amend_gap(self, v1, v2):

        self.DFS(v1)
        prev_v = v1
        counter_added_edge = 0
        for v in self.traverse:
          if prev_v != v and self.getWeight(prev_v, v) == 0:
            self.setWeight(prev_v, v, random.randint(MIN_WEIGHT, MAX_WEIGHT))
            counter_added_edge += 1
            #print "connect:",prev_v, v
          prev_v = v
        print "Edges added:",counter_added_edge

    def setWeight(self, v1, v2, weight = 1):
        if v2 > v1:
            v1, v2 = v2, v1
        self.matrix[v1][v2] = weight

    def getWeight(self, v1, v2):
        if v2 > v1:
            v1, v2 = v2, v1
        return self.matrix[v1][v2]

    def getVertexDegree(self, vertex):
        if vertex in self.degreeTable:
            return self.degreeTable(vertex)
        else:
            return 0

    def getNeighborVertex(self, vertex):
        neighbor = []
        for i in range(vertex):
          if self.getWeight(vertex, i) > 0:
            neighbor.append(i)
        for i in range(vertex, self.num_vertex):
          if self.getWeight(i, vertex) > 0:
            neighbor.append(i)
        return neighbor

    def array_init(self, m, init_value):
        matrix = list()
        for i in range(m):
            row = list()
            for j in range(i+1):
               row.append(init_value)
            matrix.append(row)
        return matrix

    def dump(self):
        counter_row = 0
        for row in self.matrix:
            print counter_row,
            counter_row += 1
            for elm in row:
                print "{0:>02}".format(elm),
            print

    def DFS(self, v):
      if type(v) != int:
        v = v.value

      v_list = range(self.num_vertex)
      for i in v_list:
        self.color.append('white')
      self.traverse = []
      self.DFS_util(v)

      for i in v_list:
        if self.color[i] == 'white':
          self.DFS_util(i)

    def DFS_util(self, v):
      self.color[v] = 'grey'
      self.traverse.append(v)
      for w in self.getNeighborVertex(v):
        if self.color[w] == 'white':
          self.DFS_util(w)
      self.color[v] = 'black'

    def BFS(self, v):
      if type(v) != int:
        v = v.value

      q = deque([])
      v_list = range(self.num_vertex)

      for i in v_list:
        self.color.append('white')
      self.traverse = [v]
      self.color[v] = 'black'

      for i in v_list:
        if self.color[i] == 'white':
          self.traverse.append(i)
          q.extend(self.getNeighborVertex(i))
        while len(q) > 0:
          w = q.popleft()
          if self.color[w] == 'white':
            self.traverse.append(w)
            self.color[w] = 'black'
            q.extend(self.getNeighborVertex(v))

    def traceback(self, s, t):
        v = t
        self.traverse = []
        while v is not s:
            self.traverse.append(v)
            v = self.parent[v]
        self.traverse.append(v)
        self.traverse.reverse()

class Graph_six_degree(Graph):

    def __init__(self, n):
        self.feasibility(n, DEGREE)
        Graph.__init__(self, n)
        self.connect()

    def feasibility(self, n, degree):
        total_edge = (n-1+1) * (n-1)/2
        if total_edge < degree * n/2:
            raise Exception("Too few edges to meet the criteria")

    @profile.timeit
    def connect(self):
        """
        repeat until all vertex meet the DEGREE
        """
        i = 0
        while i < len(self.degreeTable):
            if self.degreeTable[i] != DEGREE:
                i = 0
                self.generate_connection()
            i += 1

    @profile.counted
    def generate_connection(self):
        # reset information
        self.degreeTable = [0 for i in range(self.num_vertex)]
        self.matrix = self.array_init(self.num_vertex, 0)
        candicate = [i for i in range(self.num_vertex)]

        RETRY = self.num_vertex * DEGREE * 10
        retry_counter = 0
        while len(candicate) > 1 and retry_counter < RETRY:
            retry_counter += 1
            v = random.choice(candicate)
            u = random.choice(candicate)

            # skip self connection or already connected
            if v == u or self.getWeight(v,u) > 0:
                continue

            self.setWeight(v, u, random.randint(MIN_WEIGHT, MAX_WEIGHT))
            for elm in [v, u]:
                self.degreeTable[elm] += 1
                if self.degreeTable[elm] >= DEGREE:
                    candicate.remove(elm)

class Graph_random_connect20(Graph):

    def __init__(self, n):
        Graph.__init__(self, n)
        self.connect()

    def connect(self):
        """
        randomly connect to other vertexes by 20%
        """
        for v in range(self.num_vertex):
            for u in range(v):
                if random.random() < 0.2:
                    self.setWeight(v, u, random.randint(MIN_WEIGHT, MAX_WEIGHT))
                    self.degreeTable[v] +=1
                    self.degreeTable[u] +=1

def main():

    g1 = Graph_six_degree(NUM_VERTEX)
    #g1.dump()
    #print g1.degreeTable
    print g1.connect.times
    print g1.generate_connection.called

if __name__ == '__main__':
    main()
