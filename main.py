import networkx as nx
import matplotlib.pyplot as plt


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


def print_edges(graph):
    for u, v in graph.edges:
        print(f'({u} -- {v})')


def print_graph(Graphs):
    fig, axes = plt.subplots(nrows=int(len(Graphs) / 2) + 1, ncols=2)
    ax = axes.flatten()
    for index, graph in enumerate(Graphs):
        pos = nx.bipartite_layout(graph, [node for ind, node in enumerate(graph.nodes) if ind < len(graph.nodes) / 2])
        nx.draw(graph, pos, ax=ax[index])
        vertex_weight = {u: f'{u}:{w["weight"]}' for u, w in graph.nodes.data()}
        nx.draw_networkx_labels(graph, pos, labels=vertex_weight, ax=ax[index])
        ax[index].set_axis_off()
    plt.show()


def print_graph2(Graphs):
    # fig, axes = plt.subplots(nrows=int(len(Graphs) / 2) + 1, ncols=2)
    # ax = axes.flatten()
    for index, graph in enumerate(Graphs):
        plt.figure(index + 1)
        pos = nx.bipartite_layout(graph, [node for ind, node in enumerate(graph.nodes) if ind < len(graph.nodes) / 2])
        nx.draw(graph, pos)
        vertex_weight = {u: f'{u}:{w["weight"]}' for u, w in graph.nodes.data()}
        nx.draw_networkx_labels(graph, pos, labels=vertex_weight)
    plt.show()


def local_ratio_vertex_cover(Graphs, graph):
    # before
    Graphs.append(graph)
    # iterate
    for u, v in graph.edges:
        curr_graph = graph.copy()
        epsilon = min(curr_graph.nodes[u]['weight'], curr_graph.nodes[v]['weight'])
        curr_graph.nodes[u]['weight'] -= epsilon
        curr_graph.nodes[v]['weight'] -= epsilon
        # print_graph(graph)
        Graphs.append(curr_graph)
        graph = curr_graph
    # result
    Graphs.append(graph)


def main():
    graph = nx.Graph()
    Graphs = []

    # nodes = get_nodes()
    # for name, weight in nodes.items():
    #     graph.add_node(name, weight=weight)
    # graph.add_edges_from(get_edges(nodes))
    # mock
    nodes = {'a':2, 'b':3, 'c':5, 'd':1, 'e':2, 'f':3}
    for name, weight in nodes.items():
        graph.add_node(name, weight=weight)
    graph.add_edges_from([('a','b'), ('a','c'), ('a','d'), ('b','c'), ('b','d'), ('d','e'), ('e','f')])

    # debug
    # print(graph.nodes)
    # print_edges(graph)

    local_ratio_vertex_cover(Graphs, graph)

    print_graph2(Graphs)


if __name__ == '__main__':
    main()