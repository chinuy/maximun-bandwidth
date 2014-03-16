import graph
import heap

num_vertex = 10
class Dijkstra:
    pass

class Dijkstra_without_heap(Dijkstra):
    pass

class Dijkstra_with_heap(Dijkstra):
    pass

class Kruskal_with_heap:

    def __init__(self):
        self.g = graph.Graph_six_degree(num_vertex)
        self.h= heap.Heap()
        for e in self.g:
            self.h.insert(e)

    def solve(self):
        while(len(self.h)>0):
            print self.h.getMin()
            self.h.delete_root()

def main():
    problem = Kruskal_with_heap()
    problem.solve()

if __name__ == '__main__':
    main()
