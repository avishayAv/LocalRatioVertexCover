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
    print("Edges format is <Vertex>, <Vertex>, <Weight>. once done, please type done.")
    edges_input = input("Enter edge : ")
    edges = []
    while edges_input != skip_redundant_spaces_in_str('done'):
        edge_formatted = skip_redundant_spaces_in_list(edges_input.split(','))
        if len(edge_formatted) != 3:
            print("Edges format is <Vertex>, <Vertex>, <Weight>. Please try again.")
        elif edge_formatted[0] not in nodes or edge_formatted[1] not in nodes:
            print("No such vertexes. Please try again.")
        else:
            edges.append(edge_formatted)
        edges_input = input("Enter edge : ")
    return edges


def get_nodes():
    nodes_input = input("Enter desired nodes divided by comma : ")
    return skip_redundant_spaces_in_list(nodes_input.split(','))


def print_edges(graph):
    for u, v, w in graph.edges.data('weight'):
        print(f'({u},{v}) --> {w}')


def print_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True)
    edge_labels = {(u, v): d for u, v, d in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()


def main():
    graph = nx.MultiGraph()

    # nodes = get_nodes()
    # graph.add_nodes_from(nodes)
    # graph.add_edges_from(get_edges(nodes))
    # mock
    graph.add_nodes_from(['a','b','c'])
    graph.add_edges_from([('a','b',2), ('a','c',3)])

    print(graph.nodes)
    print_edges(graph)

    print_graph(graph)


if __name__ == '__main__':
    main()