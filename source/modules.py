import base64
import copy
import io
import warnings

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import objects
import pandas as pd

import source.grid_objects as grid_objects


def get_last_id(elements):
    last_id = [0, 0]
    for ele in elements:
        if 'source' not in ele['data']:
            last_id[0] = int(ele['data']['id'][4:])
    for ele in elements:
        if 'source' in ele['data']:
            last_id[1] = int(ele['data']['id'][4:])
    return last_id


def get_object_from_id(node_id, objects):
    for obj in objects:
        if obj.id == node_id:
            return obj
    return None


def get_connected_edges(elements, selected_element):
    id_element = selected_element['data']['id']
    result = []
    for ele in elements:
        if 'source' in ele['data']:
            if ele['data']['source'] == id_element or ele['data']['target'] == id_element:
                result.append(ele)
    return result


def generate_grid_object(object_type, object_id, node_id):
    if object_type == "button_house":
        return objects.create_HouseObject(object_id, node_id)
    elif object_type == "button_transformer":
        return objects.create_TransformerObject(object_id, node_id)
    elif object_type == "button_externalgrid":
        return objects.create_ExternalGridObject(object_id, node_id)
    elif object_type == "button_pv":
        return objects.create_PVObject(object_id, node_id)
    elif object_type == "button_battery":
        return objects.create_BatteryObject(object_id, node_id)
    elif object_type == "button_smartmeter":
        return objects.create_SmartMeterObject(object_id, node_id)
    elif object_type == "button_switch_cabinet":
        return objects.create_SwitchCabinetObject(object_id, node_id)
    else:
        return None


def connection_allowed(source, target, object_dict):
    """ Check if the connection which is about to be added is allowed. """
    target_type = object_dict[target]['object_type']
    if target_type in object_dict[source]['allowed_types_to_connect']:
        return True
    return False


def generate_grid_dataframes(elements, grid_objects):
    """
    Generate pandas DataFrames from given cytoscape elements.
    :param elements: Cytoscape element list, nodes and edges
    :param grid_objects: Dict of all grid objects to link them to the nodes
    :return df_nodes: DataFrame containing all nodes of the grid; df_edges: DataFrame containing all edges of the grid.
    """
    nodes = []
    edges = []
    for ele in elements:  # Divide elements into nodes and edges
        if 'source' in ele['data']:
            edges.append(ele['data'])  # Extract needed data from edges
        else:
            ele['data']['linkedObject'] = grid_objects[ele['data']['id']]
            # for go in grid_objects:  # Find grid object with the same id and link it to the node
            #     if go.id == ele['data']['id']:
            #         ele['data']['linkedObject'] = go
            nodes.append(ele['data'])  # Extract needed data from nodes
    df_nodes = pd.DataFrame(nodes)  # Generate DataFrames from extracted data, which describe the grid
    for edge in edges:
        source_voltage = df_nodes.loc[df_nodes['id'] == edge['source']]['linkedObject'].values[0]['voltage']
        x = df_nodes.loc[df_nodes['id'] == edge['target']]['linkedObject'].values[0]
        target_voltage = df_nodes.loc[df_nodes['id'] == edge['target']]['linkedObject'].values[0]['voltage']
        if source_voltage is None and target_voltage is None:
            warnings.warn("Keine Spannungsebene für Leitung durch Knoten definiert!")
        if source_voltage is None:
            edge['voltage'] = target_voltage
        elif target_voltage is None:
            edge['voltage'] = source_voltage
        elif source_voltage == target_voltage:
            edge['voltage'] = target_voltage
        else:
            raise Exception("Die Knoten dieser Leitung haben unterschiedliche Spannungsebenen!")
    df_edges = pd.DataFrame(edges)
    return df_nodes, df_edges


def generate_grid_graph(df_nodes, df_edges):
    """
    Generate a NetworkX graph from the given DataFrames for nodes and edges
    :param df_nodes: DataFrame containing nodes with 'id' and 'linkedObject'
    :param df_edges: DataFrame containing nodes with 'source', 'target' and 'id
    :return: NetworkX graph of the given grid
    """
    graph = nx.MultiGraph()
    graph.add_nodes_from(df_nodes['id'].tolist())
    nx.set_node_attributes(graph, pd.Series(df_nodes.linkedObject.values, index=df_nodes.id).to_dict(),
                           name="object")
    nodes = copy.deepcopy(graph.nodes(data=True))
    for node in nodes:
        if node[1]['object']['object_type'] == 'transformer':
            node_id = "transformer_" + node[0]
            node_object = objects.create_TransformerHelperNodeObject()
            graph.add_node(node_id, object=node_object)
            graph.add_edge(node[0], node_id, impedance=12, id='transformer_edge_' + node_id[16:])
    for idx in range(len(df_edges.index)):
        if df_edges.loc[idx, 'source'] in graph.nodes \
                and df_edges.loc[idx, 'target'] in graph.nodes:  # Check if source and target node exist
            if graph.nodes(data=True)[df_edges.loc[idx, 'source']]['object']['object_type'] == 'transformer':
                if df_edges.loc[idx, 'voltage'] == 400:
                    graph.add_edge("transformer_" + df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
                else:
                    graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
            elif graph.nodes(data=True)[df_edges.loc[idx, 'target']]['object']['object_type'] == 'transformer':
                if df_edges.loc[idx, 'voltage'] == 400:
                    graph.add_edge(df_edges.loc[idx, 'source'], "transformer_" + df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
                else:
                    graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
            else:
                graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'], id=df_edges.loc[idx, 'id'])
                edge_id = graph.edges[(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'], 0)]
        else:
            raise Exception("Kante mit nicht existierendem Knoten")
    return graph


def generate_directed_graph(graph):
    number_of_ext_grids = 0
    graph_dir = nx.MultiDiGraph()
    nodes_and_attributes = [(n, d) for n, d in graph.nodes(data=True)]
    graph_dir.add_nodes_from(nodes_and_attributes)
    for node in graph.nodes(data=True):
        if node[1]['object']['object_type'] == "externalgrid":
            number_of_ext_grids += 1
            source_node = node[0]
    if number_of_ext_grids > 1:
        raise Exception("Es sind mehr als ein externes Netz vorhanden.")
    elif number_of_ext_grids < 1:
        raise Exception("Es ist kein externes Netz vorhanden.")
    bfs = nx.edge_bfs(graph, source_node, orientation="ignore")
    for edge in nx.edge_bfs(graph, source_node, orientation="ignore"):
        edge_id = 'edge'
        for edge_undir in graph.edges:
            if (edge[0] == edge_undir[0] and edge[1] == edge_undir[1] and edge[2] == edge_undir[2]) or \
                    (edge[0] == edge_undir[1] and edge[1] == edge_undir[0] and edge[2] == edge_undir[2]):
                edge_id = graph.edges[edge_undir]['id']
                break
        if edge[3] == 'reverse':
            graph_dir.add_edge(edge[1], edge[0], id=edge_id)
        else:
            graph_dir.add_edge(edge[0], edge[1], id=edge_id)
    return graph_dir


def generate_equations(graph):
    df_power = pd.DataFrame()
    for node in graph.nodes(data=True):
        df_power[node[0]] = node[1]['object']['power']
    inc = nx.incidence_matrix(graph, oriented=True).toarray()
    idx = 0
    for node in graph.nodes(data=True):
        if node[1]['object']['object_type'] == 'externalgrid':
            idx_ext = idx
        idx += 1
    # b = s + t
    new_column = np.array([np.zeros(np.shape(inc)[0])])
    new_column[0][idx_ext] = -1
    inc = np.append(inc, np.transpose(new_column), axis=1)
    return inc, df_power


def solve_flow(A, b):
    if np.shape(A)[0] != np.shape(A)[1]:
        raise Exception("Inzidenzmatrix ist nicht quadratisch!")
    flow = np.linalg.solve(A, b)
    return flow


def plot_graph(graph):
    edge_labels = {}
    for edge in graph.edges:
        edge_labels[edge[0:2]] = graph.edges[edge]['id']

    pos = nx.planar_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, arrowstyle='->')
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    fig = plt.figure(plt.get_fignums()[0])

    # Convert Matplotlib figure to PNG image
    png_output = io.BytesIO()
    fig.savefig(png_output, format='png')
    png_output.seek(0)

    # Encode PNG image to base64 string
    base64_encoded = base64.b64encode(png_output.getvalue()).decode('utf-8')

    plt.show()
    return base64_encoded


def power_flow_statemachine(state, data):
    if state == 'init':
        if len(data['elements']) == 0:  # Check if there are any elements in the grid
            raise Exception('notification_emptygrid')
        return 'gen_dataframes', data, False
    elif state == 'gen_dataframes':
        data['df_nodes'], data['df_edges'] = generate_grid_dataframes(data['elements'],
                                                                      data['grid_objects'])  # Generate DataFrames
        return 'gen_grid_graph', data, False
    elif state == 'gen_grid_graph':
        data['grid_graph'] = generate_grid_graph(data['df_nodes'], data['df_edges'])  # Generate NetworkX Graph
        return 'check_isolates', data, False
    elif state == 'check_isolates':
        if nx.number_of_isolates(data['grid_graph']) > 0:  # Check if there are isolated (not connected) nodes
            raise Exception('notification_isolates')
        return 'check_tree', data, False
    elif state == 'check_tree':
        min_spanning_tree = nx.minimum_spanning_tree(data['grid_graph'])
        if data['grid_graph'].number_of_edges() != min_spanning_tree.number_of_edges():
            raise Exception('notification_cycles')
        return 'gen_directed_graph', data, False
    elif state == 'gen_directed_graph':
        data['grid_graph'] = generate_directed_graph(
            data['grid_graph'])  # Give graph edges directions, starting at external grid
        return 'gen_equations', data, False
    elif state == 'gen_equations':
        data['A'], data['df_power'] = generate_equations(data['grid_graph'])
        return 'calc_flow', data, False
    elif state == 'calc_flow':
        column_names = []
        for edge in data['grid_graph'].edges:
            column_names.append(data['grid_graph'].edges[edge]['id'])
        column_names.append("external_grid")
        df_flow = pd.DataFrame(columns=column_names)
        for step, row in data['df_power'].iterrows():
            df_flow.loc[step] = solve_flow(data['A'], row)
        data['df_flow'] = df_flow
        return 'set_edge_labels', data, False
    elif state == 'set_edge_labels':
        data['labels'] = data['df_flow'].loc[0].to_dict()
        return None, data, True


def calculate_power_flow(elements, grid_object_dict):
    """
    Main function to calculate the power flows in the created and configured grid. Built as a state-machine
    :param grid_object_dict: List of objects in grid with id corresponding to node ids of cytoscape
    :param elements: Grid elements in form of cytoscape graph
    :return:
    """
    state = 'init'
    ready = False
    data = {'elements': elements, 'grid_objects': grid_object_dict}
    while not ready:
        print(state)
        state, data, ready = power_flow_statemachine(state, data)
        print("Done")
    return data['df_flow'], data['labels'], plot_graph(data['grid_graph'])


def handle_error(err):
    print("Error: ", err)
