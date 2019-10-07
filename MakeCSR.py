import csv, json

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbours = []

    def addNeighbour(self, neighbour_id):
        for i in range(len(self.neighbours)):
            if self.neighbours[i] > neighbour_id:
                self.neighbours = self.neighbours[:i] + [neighbour_id] + self.neighbours[i:]
                return
        self.neighbours += [neighbour_id]


def extract_nodes_from_json(json_filename):
    json_file = open(json_filename, 'r')
    datas = json.load(json_file)
    keys = []
    for key, _ in datas.items():
        keys += [int(key)]
    json_file.close()
    print("number of nodes: ", len(keys))
    keys.sort()
    nodes = []
    check = 0
    for node_id in keys:
        assert check == node_id
        nodes += [Node(node_id)]
        check += 1
    return nodes


def extract_edges_from_csv(csv_filename):
    csv_file = open(csv_filename, 'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    flag = True
    edges_count = 0
    edges = []
    for row in csv_reader:
        if flag:
            flag = False
        else:
            edges += [(int(row[0]), int(row[1]))]
            edges_count += 1
    csv_file.close()
    print("readed edges count: ", edges_count)
    return edges


def make_csr(json_filename, csv_filename, node_filename, edge_filename):
    nodes = extract_nodes_from_json(json_filename)
    edges = extract_edges_from_csv(csv_filename)
    for edge in edges:
        nodes[edge[0]].addNeighbour(edge[1])
        nodes[edge[1]].addNeighbour(edge[0])
    csr_node_vector = []
    csr_edge_vector = []
    edge_vector_size = 0
    for node in nodes:
        csr_node_vector += [edge_vector_size]
        csr_edge_vector += node.neighbours
        edge_vector_size += len(node.neighbours)
    csr_node_vector += [edge_vector_size]
    
    assert csr_node_vector[-1] == len(csr_edge_vector)

    csr_node_file = open(node_filename, 'w')
    csr_node_file.write(str(len(csr_node_vector)) + '\n')
    for element in csr_node_vector:
        csr_node_file.write(str(element) + '\n')
    csr_node_file.close()

    csr_edge_file = open(edge_filename, 'w')
    csr_edge_file.write(str(len(csr_edge_vector)) + '\n')
    for element in csr_edge_vector:
        csr_edge_file.write(str(element) + '\n')
    csr_edge_file.close()


make_csr("data/gemsec_deezer_dataset/deezer_clean_data/HR_genres.json",  \
            "data/gemsec_deezer_dataset/deezer_clean_data/HR_edges.csv", \
            "result/HR.nodes", "result/HR.edges")


