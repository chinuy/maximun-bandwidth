import graph
import heap
import random
import sys

NUM_VERTEX = 1000

def makeSet(v):
  return graph.Node(v)

def find(v):
  w = v
  s = []

  while w.parent != w:
    s.append(w)
    w = w.parent

  while len(s) > 0:
    u = s.pop()
    u.parent = w

  return w

def union(v1, v2):
  if v1.rank > v2.rank:
    v2.parent = v1
  elif v1.rank < v2.rank:
    v1.parent = v2
  else:
    v2.parent = v1
    v1.rank = v2.rank + 1

class GraphProblem:

    def __init__(self, input_graph):
        self.g = input_graph

    def setSourceSink(self, source, sink):
        self.source = source
        self.sink = sink

class Dijkstra_without_heap(GraphProblem):

    def __init__(self, input_graph):
        GraphProblem.__init__(self, input_graph)

    def solve(self):
        frige = []
        self.g.parent = []
        bandwidth = []
        for i in range(self.g.num_vertex):
            self.g.parent.append(None)
            bandwidth.append(-sys.maxint)

        bandwidth[self.source] = sys.maxint

        for v in self.g.getNeighborVertex(self.source):
            self.g.parent[v] = self.source
            bandwidth[v] = self.g.getWeight(self.source, v)
            frige.append(v)

        while bandwidth[self.sink] <= -sys.maxint and \
                self.sink not in frige:

            _max_b = -sys.maxint
            _max_i = None
            for i in range(len(frige)):
                if _max_b < bandwidth[frige[i]]:
                    _max_b = bandwidth[frige[i]]
                    _max_i= i
            u = frige[_max_i]
            del frige[_max_i]

            for w in self.g.getNeighborVertex(u):
                bandwidth_of_u_w = self.g.getWeight(u, w)
                if bandwidth[w] == -sys.maxint:
                    self.g.parent[w] = u
                    bandwidth[w] = min(bandwidth[u], bandwidth_of_u_w)
                    frige.append(w)
                elif w in frige and bandwidth[w] < min(bandwidth[u],\
                        bandwidth_of_u_w):
                    self.g.parent[w] = u
                    bandwidth[w] = min(bandwidth[u], bandwidth_of_u_w)

        self.g.traceback(self.source, self.sink)
        print self.g.traverse

class Dijkstra_with_heap(GraphProblem):

    def __init__(self, input_graph):
        GraphProblem.__init__(self, input_graph)

    def solve(self):
        frige = heap.MaxHeap()
        self.g.parent = []
        bandwidth = []
        for i in range(self.g.num_vertex):
            self.g.parent.append(None)
            bandwidth.append(-sys.maxint)

        bandwidth[self.source] = sys.maxint

        for v in self.g.getNeighborVertex(self.source):
            self.g.parent[v] = self.source
            bandwidth[v] = self.g.getWeight(self.source, v)
            frige.insert((v,bandwidth[v]))

        while bandwidth[self.sink] <= -sys.maxint and \
                self.sink not in frige:
            u = frige.getMax()[0]
            frige.delete_root()
            for w in self.g.getNeighborVertex(u):
                bandwidth_of_u_w = self.g.getWeight(u, w)
                if bandwidth[w] == -sys.maxint:
                    self.g.parent[w] = u
                    bandwidth[w] = min(bandwidth[u], bandwidth_of_u_w)
                    frige.insert((w, bandwidth[w]))
                elif w in frige and bandwidth[w] < min(bandwidth[u],\
                        bandwidth_of_u_w):
                    self.g.parent[w] = u
                    bandwidth[w] = min(bandwidth[u], bandwidth_of_u_w)

        self.g.traceback(self.source, self.sink)
        print self.g.traverse

class Kruskal_with_heap(GraphProblem):

    def __init__(self, input_graph):
        GraphProblem.__init__(self, input_graph)
        self.h= heap.MaxHeap()

        for e in self.g:
            self.h.insert(e)

    def solve(self):
        t = graph.Graph(self.g.num_vertex)

        v = []
        for i in range(self.g.num_vertex):
          v.append(makeSet(i))

        root = v[0] #temp set the root to the first node
        while len(self.h) > 0:
          e = self.h.getMax()
          ((v1, v2), weight) = e
          self.h.delete_root()
          if weight == 0:
            break
          r1 = find(v[v1])
          r2 = find(v[v2])
          if r1 != r2:
            t.setWeight(v1, v2, weight)
            union(r1, r2)

          if r1.rank > root.rank:
            root = r1
          if r2.rank > root.rank:
            root = r2

        #print root
        #t.DFS(root)
        #print t.traverse

def randomSourceSink(n):
    source = random.randint(0,n-1)
    sink = random.randint(0,n-1)
    if source == sink:
      sink += 1 # simply prevent source and sink are the same
      sink %= n# for boundary condition
    print "S:", source
    print "T:", sink
    return (source, sink)

def main():
    for i in range(5):
        print "-- Run --",i
        problem = Kruskal_with_heap(graph.Graph_random_connect20(NUM_VERTEX))
        problem.setSourceSink(*randomSourceSink(NUM_VERTEX))
        #problem.g.dump()
        problem.solve()
        print "-- End --", i

if __name__ == '__main__':
    main()
