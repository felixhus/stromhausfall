import grid_objects
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def get_last_id(elements):
    last_id = [0, 0]
    for ele in elements:
        if 'source' not in ele['data']:
            last_id[0] = int(ele['data']['id'][4:])
    for ele in elements:
        if 'source' in ele['data']:
            last_id[1] = int(ele['data']['id'][4:])
    return last_id


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
        return grid_objects.HouseObject(node_id=node_id, object_id=object_id)
    elif object_type == "button_transformer":
        return grid_objects.TransformerObject(node_id=node_id, object_id=object_id)
    elif object_type == "button_externalgrid":
        return grid_objects.ExternalGrid(node_id=node_id, object_id=object_id)
    elif object_type == "button_pv":
        return grid_objects.PV(node_id=node_id, object_id=object_id)
    elif object_type == "button_battery":
        return grid_objects.Battery(node_id=node_id, object_id=object_id)
    elif object_type == "button_smartmeter":
        return grid_objects.SmartMeter(node_id=node_id, object_id=object_id)
    elif object_type == "button_switch_cabinet":
        return grid_objects.SwitchCabinet(node_id=node_id, object_id=object_id)
    else:
        return None


def connection_allowed(source, target, object_list):
    target_type = None
    for gridobject in object_list:
        if gridobject.get_id() == target:
            target_type = gridobject.object_type
            break
    for gridobject in object_list:
        grabbed_id = gridobject.get_id()
        if gridobject.get_id() == source:
            if target_type in gridobject.allowed_types_to_connect:
                return True
    return False


def generate_grid_dataframes(elements, grid_objects):
    """
    Generate pandas DataFrames from given cytoscape elements.
    :param elements: Cytoscape element list, nodes and edges
    :param grid_objects: List of all grid objects to link them to the nodes
    :return df_nodes: DataFrame containing all nodes of the grid; df_edges: DataFrame containing all edges of the grid.
    """
    try:
        nodes = []
        edges = []
        for ele in elements:    # Divide elements into nodes and edges
            if 'source' in ele['data']:
                edges.append(ele['data'])   # Extract needed data from edges
            else:
                for go in grid_objects:     # Find grid object with the same id and link it to the node
                    if go.id == ele['data']['id']:
                        ele['data']['linkedObject'] = go
                nodes.append(ele['data'])   # Extract needed data from nodes
        df_nodes = pd.DataFrame(nodes)      # Generate DataFrames from extracted data, which describe the grid
        df_edges = pd.DataFrame(edges)
        return df_nodes, df_edges
    except Exception as err:
        handle_error(err)


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
        for idx in range(len(df_edges.index)):
            if df_edges.loc[idx, 'source'] in graph.nodes \
                    and df_edges.loc[idx, 'target'] in graph.nodes:   # Check if source and target node exist
                graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'], id=df_edges.loc[idx, 'id'])
            else:
                raise Exception("Kante mit nicht existierendem Knoten")
        nx.draw(graph)
        plt.show()
        return graph
    except Exception as err:
        handle_error(err)


def calculate_power_flow(elements, grid_object_list):
    """
    Main function to calculate the power flows in the created and configured grid
    :param grid_object_list: List of objects in grid with id corresponding to node ids of cytoscape
    :param elements: Grid elements in form of cytoscape graph
    :return:
    """
    df_nodes, df_edges = generate_grid_dataframes(elements, grid_object_list)
    grid_graph = generate_grid_graph(df_nodes, df_edges)


def handle_error(err):
    print(err)
