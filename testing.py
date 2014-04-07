import profile
import routing
import graph
from routing import randomSourceSink

def array_init(m, init_value):
    matrix = list()
    for i in range(m):
        row = list()
        for j in range(m):
           row.append(init_value)
        matrix.append(row)
    return matrix

@profile.timeit
def problem_solver(algorithm, problem_graph, problem_source_sink):
    problem = algorithm(problem_graph)
    problem.setSourceSink(*problem_source_sink)
    problem.solve()
    return problem.count

def main():

    num_vertex = 5000
    NUM_ITERATION = 5
    algorithms = [routing.Dijkstra_without_heap, routing.Dijkstra_with_heap, routing.Kruskal_with_heap]

    summary = array_init(3, 0)
    for i in range(NUM_ITERATION):
        problem_graphs = [graph.Graph_six_degree(num_vertex), graph.Graph_random_connect20(num_vertex)]
        for j in range(len(problem_graphs)):
            problem_g = problem_graphs[j]
            problem_source_sink = randomSourceSink(num_vertex)
            problem_g.amend_gap(*problem_source_sink)
            for k in range(len(algorithms)):
                solver = problem_solver(algorithms[k], problem_g, problem_source_sink)
                summary[j][k] += solver
    for j in range(3):
        for k in range(3):
            print summary[j][k]/NUM_ITERATION

if __name__ == '__main__':
    main()
