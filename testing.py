import profile
import routing
import graph
from routing import randomSourceSink

@profile.timeit
def problem_solver(algorithm, problem_graph, problem_source_sink):
    problem = algorithm(problem_graph)
    problem.setSourceSink(*problem_source_sink)
    problem.solve()

def main():

    num_vertex = 5000
    algorithms = [routing.Dijkstra_without_heap, routing.Dijkstra_with_heap, routing.Kruskal_with_heap]

    for i in range(5):
        problem_graphs = [graph.Graph_six_degree(num_vertex), graph.Graph_random_connect20(num_vertex)]
        for problem_g in problem_graphs:
            problem_source_sink = randomSourceSink(num_vertex)
            problem_g.amend_gap(*problem_source_sink)
            for algo in algorithms:
                solver = problem_solver(algo, problem_g, problem_source_sink)
                print problem_solver.times

if __name__ == '__main__':
    main()
