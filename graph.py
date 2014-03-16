#/usr/env python
import sys
import random

DEGREE = 6
MIN_WEIGHT = 1
MAX_WEIGHT = 50
num_vertex = 1000

class Graph:

    def feasibility(self, n, degree):
        total_edge = (n-1+1) * (n-1)/2
        if total_edge < degree * n/2:
            raise Exception("Too few edges to meet the criteria")

    def __init__(self, n):
        self.feasibility(n, DEGREE)
        self.matrix = self.array_init(n, n, 0)
        self.degreeTable = [0 for i in range(n)]
        self.vertex = [i for i in range(n)]

    def __iter__(self):
        self.current = (0,0)
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
        count = 0
        for row in self.matrix:
            for elm in row:
                if elm > 0:
                    count += 1
        return count

    def setEdge(self, v1, v2, weight = 1):
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

    def array_init(self, m, n, init_value):
        matrix = list()
        for i in range(m):
            row = list()
            for j in range(i+1):
               row.append(init_value)
            matrix.append(row)
        return matrix

    def dump(self):
        for row in self.matrix:
            for elm in row:
                print "{0:>02}".format(elm),
            print

class Graph_six_degree(Graph):

    def __init__(self, n):
        Graph.__init__(self, n)
        self.num_vertex = n
        self.connect()
        
    def connect(self):
        """
        randomly connect to other vertexes
        """
        for d in range(DEGREE):
            candicate = [i for i in range(self.num_vertex)]
            while len(candicate) > 1:
                v = random.choice(candicate)
                u = random.choice(candicate)

                # skip self connection or already connected
                if v == u or self.getWeight(v,u) > 0:
                    continue

                self.setEdge(v, u, random.randint(MIN_WEIGHT, MAX_WEIGHT))
                for elm in [v, u]:
                    self.degreeTable[elm] += 1
                    if self.degreeTable[elm] >= d:
                        candicate.remove(elm)
                #print candicate, v,u
        for d in self.degreeTable:
            if d != DEGREE:
                print self.degreeTable
                raise Exception("Fail to generate the map of six degree")

class Graph_random_connect20(Graph):

    def __init__(self, n):
        Graph.__init__(self, n)
        self.num_vertex = n
        self.connect()
        
    def connect(self):
        """
        randomly connect to other vertexes by 20%
        """
        for v in range(num_vertex):
            for u in range(v):
                if random.random() < 0.2:
                    self.setEdge(v, u, random.randint(MIN_WEIGHT, MAX_WEIGHT))
                    self.degreeTable[v] +=1
                    self.degreeTable[u] +=1

def main():

    print "STEP1: Generate graphs"
    g1 = Graph_six_degree(num_vertex)
    g2 = Graph_random_connect20(num_vertex)

if __name__ == '__main__':
    main()
