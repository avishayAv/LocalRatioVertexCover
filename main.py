import networkx as nx
import matplotlib.pyplot as plt


UNMARKED_VERTEX = '#FAEBD7'
MARKED_VERTEX = 'red'
WEIGHT = 'weight'
VERTEX_COVER = '#00FF00'
MARKED_EDGE = 'white'
UNMARKED_EDGE = 'black'


class Graph:
    def __init__(self, graph, node_color_map, edge_color_map):
        self.graph = graph
        self.node_color_map = node_color_map
        self.edge_color_map = edge_color_map


def skip_redundant_spaces_in_str(str):
    return str.strip()


def skip_redundant_spaces_in_list(items_list):
    items_list_no_spaces = []
    for item in items_list:
        items_list_no_spaces.append(item.strip())
    return items_list_no_spaces


def get_edges(nodes):
    print("Edges format is <Vertex>, <Vertex>. once done, please type done.")
    edges_input = input("Enter edge : ")
    edges = []
    while edges_input != skip_redundant_spaces_in_str('done'):
        edge_formatted = skip_redundant_spaces_in_list(edges_input.split(','))
        if len(edge_formatted) != 2:
            print("Edges format is <Vertex>, <Vertex>. Please try again.")
        elif edge_formatted[0] not in nodes or edge_formatted[1] not in nodes:
            print("No such vertexes. Please try again.")
        else:
            edges.append(edge_formatted)
        edges_input = input("Enter edge : ")
    return edges


def get_nodes():
    nodes_input = input("Enter desired nodes <node>:<weight>, <node>:<weight>, ... : ")
    nodes_seperated = skip_redundant_spaces_in_list(nodes_input.split(','))
    weighted_nodes = {}
    for node in nodes_seperated:
        split_node = node.split(':')
        weighted_nodes[skip_redundant_spaces_in_str(split_node[0])] = int(skip_redundant_spaces_in_str(split_node[1]))
    return weighted_nodes


def print_graph(Graphs, difficulty):
    difficulty_to_seconds = {'slow': 3, 'medium': 2, 'fast': 1}
    plt.figure(1)
    for index, graph in enumerate(Graphs):
        pos = nx.circular_layout(graph.graph)
        nx.draw(graph.graph, pos)
        vertex_weight = {u: f'{u}:{w[WEIGHT]}' for u, w in graph.graph.nodes.data()}
        nx.draw_networkx_nodes(graph.graph, pos, node_color=graph.node_color_map)
        nx.draw_networkx_edges(graph.graph, pos, edge_color=graph.edge_color_map)
        nx.draw_networkx_labels(graph.graph, pos, labels=vertex_weight)
        if index != len(Graphs)-1:
            plt.pause(difficulty_to_seconds[difficulty])
            plt.clf()
    plt.show()


def color_vertex_participate_in_edge(nodes, u, v):
    color_map = []
    for node in nodes:
        if node != u and node != v:
            color_map.append(UNMARKED_VERTEX)
        else:
            color_map.append(MARKED_VERTEX)
    return color_map


def color_vertex_in_cover(nodes):
    color_map = []
    for u, w in nodes.data():
        if w[WEIGHT] == 0:
            color_map.append(VERTEX_COVER)
        else:
            color_map.append(UNMARKED_VERTEX)
    return color_map


def remove_edges_from_taken_vertex(graph, u, v):
    color_map = []
    for a,b in graph.edges:
        if graph.nodes.data()[a][WEIGHT] == 0 or graph.nodes.data()[b][WEIGHT] == 0:
            color_map.append(MARKED_EDGE)
        else:
            color_map.append(UNMARKED_EDGE)
    return color_map


def local_ratio_vertex_cover(Graphs, graph):
    # before
    Graphs.append(Graph(graph, [UNMARKED_VERTEX for node in graph.nodes], [UNMARKED_EDGE for edge in graph.edges]))
    # iterate
    for u, v in graph.edges:
        Graphs.append(Graph(graph, color_vertex_participate_in_edge(graph.nodes, u, v), remove_edges_from_taken_vertex(graph, u, v)))
        curr_graph = graph.copy()
        epsilon = min(curr_graph.nodes[u][WEIGHT], curr_graph.nodes[v][WEIGHT])
        curr_graph.nodes[u][WEIGHT] -= epsilon
        curr_graph.nodes[v][WEIGHT] -= epsilon
        Graphs.append(Graph(curr_graph, color_vertex_participate_in_edge(curr_graph.nodes, u, v), remove_edges_from_taken_vertex(graph, u, v)))
        Graphs.append(Graph(curr_graph, [UNMARKED_VERTEX for node in graph.nodes], remove_edges_from_taken_vertex(graph, u, v)))
        graph = curr_graph
    # result
    Graphs.append(Graph(graph, [UNMARKED_VERTEX for node in graph.nodes], remove_edges_from_taken_vertex(graph, u, v)))
    Graphs.append(Graph(graph, color_vertex_in_cover(graph.nodes), remove_edges_from_taken_vertex(graph, u, v)))


def main():
    graph = nx.Graph()
    Graphs = []

    # nodes = get_nodes()
    # for name, weight in nodes.items():
    #     graph.add_node(name, weight=weight)
    # graph.add_edges_from(get_edges(nodes))
    # difficulty = input("Enter desired difficulty (slow/medium/fast):")
    # mock
    nodes = {'a':2, 'b':3, 'c':5, 'd':1, 'e':2, 'f':3}
    for name, weight in nodes.items():
        graph.add_node(name, weight=weight)
    graph.add_edges_from([('a','b'), ('a','c'), ('a','d'), ('b','d'), ('d','e'), ('e','f')])
    difficulty = 'fast'

    local_ratio_vertex_cover(Graphs, graph)

    print_graph(Graphs, difficulty)


if __name__ == '__main__':
    main()