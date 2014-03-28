import graph
import heap
import random

NUM_VERTEX = 100

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


class Dijkstra:
    pass

class Dijkstra_without_heap(Dijkstra):
    pass

class Dijkstra_with_heap(Dijkstra):
    pass

class Kruskal_with_heap():

    def __init__(self, n):
        self.g = graph.Graph_six_degree(n)

        self.source = random.randint(0,n-1)
        self.sink = random.randint(0,n-1)
        if self.source == self.sink:
          self.sink += 1 # simply prevent source and sink are the same
        print "S:", self.source
        print "T:", self.sink

        self.amend_gap(self.source, self.sink)

        self.h= heap.Heap()
        for e in self.g:
            self.h.insert(e)

    def amend_gap(self, v1, v2):

        self.g.DFS(v1)
        prev_v = v1
        counter_added_edge = 0
        for v in self.g.traverse:
          if prev_v != v and self.g.getWeight(prev_v, v) == 0:
            self.g.setWeight(prev_v, v, random.randint(graph.MIN_WEIGHT,\
              graph.MAX_WEIGHT))
            counter_added_edge += 1
            #print "connect:",prev_v, v
          prev_v = v
        print "Edges added:",counter_added_edge

    def solve(self):
        num_vertex = NUM_VERTEX
        t = graph.Graph(num_vertex)

        v = []
        for i in range(num_vertex):
          v.append(makeSet(i))

        root = v[0] #temp set the root to the first node
        while len(self.h) > 0:
          e = self.h.getMin()
          ((v1, v2), weight) = e
          self.h.delete_root()
          if weight == 0:
            continue
          r1 = find(v[v1])
          r2 = find(v[v2])
          if r1 != r2:
            t.setWeight(v1, v2, weight)
            union(r1, r2)

          if r1.rank > root.rank:
            root = r1
          if r2.rank > root.rank:
            root = r2

        print root
        t.DFS(root)
        print t.traverse

def main():
    problem = Kruskal_with_heap(NUM_VERTEX)
    problem.solve()

if __name__ == '__main__':
    main()
