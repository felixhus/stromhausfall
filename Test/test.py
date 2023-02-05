import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import scipy as sp


def swap_edge_direction(graph_in, edge):
    graph_in.add_edge(edge[1], edge[0], edge[2])


def generate_grid_graph(df_nodes, df_edges):
    """
    Generate a NetworkX graph from the given DataFrames for nodes and edges
    :param df_nodes: DataFrame containing nodes with 'id' and 'linkedObject'
    :param df_edges: DataFrame containing nodes with 'source', 'target' and 'id
    :return: NetworkX graph of the given grid
    """
    try:
        graph = nx.MultiGraph()
        graph.add_nodes_from(df_nodes['id'].tolist())
        nx.set_node_attributes(graph, pd.Series(df_nodes.linkedObject.values, index=df_nodes.id).to_dict(), name="object")
        print(graph.nodes["node1"]["object"])
        for idx in range(len(df_edges.index)):
            if df_edges.loc[idx, 'source'] in graph.nodes \
                    and df_edges.loc[idx, 'target'] in graph.nodes:  # Check if source and target node exist
                graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'], id=df_edges.loc[idx, 'id'])
            else:
                raise Exception("Kante mit nicht existierendem Knoten")
        nx.draw(graph, with_labels=True)
        plt.show()
        # return graph
    except Exception as err:
        # handle_error(err)
        print(err)
    finally:
        return graph


df_edges = pd.read_csv('df_edges.csv')
df_nodes = pd.read_csv('df_nodes.csv')

graph = generate_grid_graph(df_nodes, df_edges)
x = graph.nodes["node1"]["object"]

minimum_spanning_tree = nx.minimum_spanning_tree(graph)

# nx.draw(minimum_spanning_tree, with_labels=True)
# plt.show()

graph_dir = nx.MultiDiGraph()
graph_dir.add_nodes_from(graph)
graph_dir.add_edges_from(graph.edges)

minimum_spanning_arb = nx.minimum_spanning_arborescence(graph_dir)

# nx.draw(minimum_spanning_arb, with_labels=True)
# plt.show()

# graph_final = nx.MultiDiGraph()
# graph_final.add_nodes_from(graph_dir)
# for e in graph_dir.edges:
#     swap_edge_direction(graph_final, e)

# graph_dir = nx.to_directed(graph)
# cycles = nx.find_cycle(graph_dir)

# print(nx.cycle_basis(graph))

# pos = nx.spring_layout(graph_dir)
pos = nx.planar_layout(graph_dir)
nx.draw_networkx_nodes(graph_dir, pos)
nx.draw_networkx_edges(graph_dir, pos, arrowstyle='->')
nx.draw_networkx_labels(graph_dir, pos)
plt.show()

# pos = nx.spring_layout(graph_final)
# nx.draw_networkx_nodes(graph_final, pos)
# nx.draw_networkx_edges(graph_final, pos, arrowstyle='->')
# nx.draw_networkx_labels(graph_final, pos)
# plt.show()

source_node = list(graph_dir)[5]
bfs = list(nx.edge_bfs(graph_dir, source_node, orientation="ignore"))

graph_final = nx.MultiDiGraph()
graph_final.add_nodes_from(graph_dir)
for edge in nx.edge_bfs(graph_dir, source_node, orientation="ignore"):
    print(edge[3])
    if edge[3] == 'reverse':
        graph_final.add_edge(edge[1], edge[0])
    else:
        graph_final.add_edge(edge[0], edge[1])
        # graph_dir.remove_edge(edge[0], edge[1])

pos = nx.planar_layout(graph_final)
nx.draw_networkx_nodes(graph_final, pos)
nx.draw_networkx_edges(graph_final, pos, arrowstyle='->')
nx.draw_networkx_labels(graph_final, pos)
plt.show()

A = nx.incidence_matrix(graph_final, oriented=True).toarray()
B = nx.incidence_matrix(graph_dir, oriented=True).toarray()
# print(nx.incidence_matrix(graph_final))
