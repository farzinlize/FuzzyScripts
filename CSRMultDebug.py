class graph:
    def __init__(self):
        self.node_vector = []
        self.edge_vector = []
        self.size = 0

    def read_graph_from_file(self, node_filename, edge_filename):
        self.node_vector = read_list_from_file(node_filename)
        self.edge_vector = read_list_from_file(edge_filename)
        self.size = len(self.node_vector)-1

    def set_arrays(self, node_vector, edge_vector):
        self.node_vector = node_vector
        self.edge_vector = edge_vector
        self.size = len(node_vector)-1

def read_list_from_file(filename):
    f = open(filename, "r")
    len_list = int(f.readline())
    result = []
    for _ in range(len_list):
        result = result + [int(f.readline())]
    f.close()
    return result


def one_mult(g, multiplier):
    result = [0 for _ in range(g.size)]
    for node_id in range(g.size):
        offset = g.node_vector[node_id]
        degree = g.node_vector[node_id+1] - offset
        for neighbour_index in range(degree):
            neighbour = g.edge_vector[offset + neighbour_index]
            result[node_id] += multiplier[neighbour]
    return result


def read_mult_result(filename):
    f = open(filename, "r")
    result = []
    for _ in range(10):
        print(f.readline())
        line = f.readline()[1:-1].split()
        result = result + [[int(element) for element in line]]
    f.close()
    return result


def main_2(source):
    print("[MAIN] starting")

    g = graph()
    g.read_graph_from_file("data/test1.nodes", "data/test1.edges")

    print("[MAIN] graph readed")

    multiplier = [0 for _ in range(g.size)]
    multiplier[source] = 1
    py_mult = []

    for i in range(10):
        print("index = ", i)
        multiplier = one_mult(g, multiplier)
        py_mult = py_mult + [multiplier]

    print("[MAIN] py_mult calculated")

    cuda_mult = read_mult_result("data/mult_report.out")

    print("[MAIN] cuda_mult readed")

    errors_count = 0
    for index in range(10):
        for mult_index in range(g.size):
            if py_mult[index][mult_index] != cuda_mult[index][mult_index]:
                print("error at mult iteration number: ", index, " at ", mult_index, " position")
                errors_count += 1

    print("errors_count = ", errors_count)


def main_1(source):
    g = graph()
    node_vector = [0, 1, 2, 5, 7, 9, 12, 15, 17, 18]
    edge_vector = [2, 2, 0, 1, 3, 2, 4, 3, 5, 4, 6, 7, 5, 7, 8, 5, 6, 6]
    g.set_arrays(node_vector, edge_vector)

    multiplier = [0 for _ in range(g.size)]
    multiplier[source] = 1
    print("pre mult")
    print(multiplier)

    for i in range(10):
        print("index = ", i)
        multiplier = one_mult(g, multiplier)
        print(multiplier)


main_2(0)
# main(0)
# test_main()