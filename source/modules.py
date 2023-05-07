"""
modules.py contains all kinds of functions used by other modules in the project.
"""

import base64
import copy
import io
import json
import random
import warnings
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
from scipy import interpolate

import source.objects as objects
import source.plot as plot
import source.sql_modules as sql_modules

root_path = '/home/stromhausfall/mysite/'

# Dict to get the number of the day from the string-id of the day
days = {'mo': 0, 'tu': 1, 'wd': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}
# The ids of the selected power profiles for househould from the izes-database
profile_selection = [46, 4, 7, 9, 14, 15, 16, 17, 18, 19, 20, 22, 23, 27, 28, 32, 33, 39, 41, 73, 42, 45, 47, 58, 61, 62, 65]


def get_last_id(elements):
    """
    Returns the last used id in a list of elements. It returns two ids, one for the nodes, one for the edges
    :param elements: List of elements with ids
    :type elements: list
    :return: Last used ids of [nodes, edges]
    :rtype: list[int]
    """

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
    """
    Find edges which are connected to a cytoscape node
    :param elements: Cytoscape elements
    :type elements: list
    :param selected_element: Node to search for
    :type selected_element: dict
    :return: List of connected edges
    :rtype: list
    """

    id_element = selected_element['data']['id']
    result = []
    for ele in elements:
        if 'source' in ele['data']:
            if ele['data']['source'] == id_element or ele['data']['target'] == id_element:
                result.append(ele)
    return result


def generate_grid_object(object_type, object_id, node_id):
    """
    Creates a grid object from the function in objects.py.
    :param object_type: Type of object that should be created
    :type object_type: str
    :param object_id: Id of the object
    :type object_id: str
    :param node_id: Id of the cytoscape node which it is linked to
    :type node_id: str
    :return: Grid object
    """
    # TODO: Get grid objects from a sql database, not hard coded from objects.py. See how it is solved for house devices

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
    """
    Check if the connection which is about to be added is allowed.
    :param source: Id of source node
    :type source: str
    :param target: Id of target node
    :type target: str
    :param object_dict: Dictionary containing all grid objects and their properties
    :type object_dict: dict
    :return: The result of the check, True if allowed
    :rtype: bool
    """

    target_type = object_dict[target]['object_type']
    if target_type in object_dict[source]['allowed_types_to_connect']:
        return True
    return False


def create_device_object(device_id, device_type, database, own=False, own_devices=None):
    """
    Creates a dictionary containing all properties of a device. Chooses source of the data
    regarding own or standard devices.
    :param device_id: Id to set to device
    :type device_id: str
    :param device_type: Type of device to create
    :type device_type: str
    :param database: SQL database to fetch device properties from
    :type database: str
    :param own: Boolean if the device to create is an own device
    :type own: bool
    :param own_devices: Dictionary of existing own devices
    :type own_devices: dict
    :return: Device as a dictionary
    :rtype: dict
    """

    if not own:     # If it is not an own device -> It is a device from the database
        device = sql_modules.get_device(database, device_type)      # Get device properties from the database
        device = device[0]  # Get dict from result
        json_data = device['power_options'].decode('utf-8-sig')     # Decode string with power options from database
        json_data = json_data.replace("'", "\"")
        device['power_options'] = json.loads(json_data)   # Decode dictionary from bytes
    else:
        device = own_devices[device_type]       # If it is an own device -> Get from dictionary
    device['active'] = True                     # Set all other properties
    device['selected_power_option'] = None
    device['power'] = [0] * 24 * 60 * 7
    device['id'] = device_id
    return device


def add_device(elements, device_dict, room, device_type, own, own_devices=None):
    """
    This function adds a device of the given type to the cytoscape (including the socket and repositioning of
    the plus-node) and attaches it to the device dictionary.
    :param elements: Elements of the room cytoscape
    :type elements: list
    :param device_dict: Dictionary containing all devices in the custom house
    :type device_dict: dict
    :param room: Room to add device to
    :type room: str
    :param device_type: Type of device to add
    :type device_type: str
    :param own: Boolean if the device to add is an own device
    :type own: bool
    :param own_devices: Dictionary of existing own devices
    :type own_devices: dict
    :return: elements: Updated element list of cytoscape; device_dict: Updated dictionary of devices
    """

    database = root_path + 'source/database_profiles.db'
    last_id = int(device_dict['last_id'])  # Get number of last id
    device_dict['last_id'] = last_id + 1  # Increment the last id
    socket_id = "socket" + str(last_id + 1)
    device_id = "device" + str(last_id + 1)
    new_device = create_device_object(device_id, device_type, database, own, own_devices)
    image_src = get_icon_url(new_device['icon'])
    position = elements[1]['position']  # Get Position of plus-node
    new_position_plus = {'x': position['x'] + 40, 'y': position['y']}  # Calculate new position of plus-node
    new_socket = {'data': {'id': socket_id, 'parent': 'power_strip'}, 'position': position,
                  'classes': 'socket_node_style_on',  # Generate new socket
                  'linked_device': device_id}  # and link the connected device
    if len(elements) % 6 - 2 > 0:
        position_node = {'x': position['x'], 'y': position['y'] - 80}  # Get position of new device
    else:
        position_node = {'x': position['x'], 'y': position['y'] - 120}
    new_node = {'data': {'id': device_id}, 'classes': 'room_node_style', 'position': position_node,
                'linked_socket': socket_id,  # Generate new device
                'style': {'background-image': image_src}}
    new_edge = {'data': {'source': socket_id, 'target': device_id}}  # Connect new device with new socket

    elements[1]['position'] = new_position_plus
    elements.append(new_socket)  # Append new nodes and edges to cytoscape elements
    elements.append(new_node)
    elements.append(new_edge)
    device_dict['house1'][device_id] = new_device  # Add new device to device dictionary
    device_dict['rooms'][room]['devices'].append(device_id)  # Add new device to room device list
    return elements, device_dict


def generate_grid_dataframes(elements, grid_objects):
    """
    Generate pandas DataFrames from given cytoscape elements.
    :param elements: Cytoscape element list, nodes and edges
    :type elements: list
    :param grid_objects: Dict of all grid objects to link them to the nodes
    :type grid_objects: dict
    :return df_nodes: DataFrame containing all nodes of the grid; df_edges: DataFrame containing all edges of the grid.
    """

    nodes = []
    edges = []
    for ele in elements:  # Divide elements into nodes and edges
        if 'source' in ele['data']:
            edges.append(ele['data'])  # Extract needed data from edges
        else:
            ele['data']['linkedObject'] = grid_objects[ele['data']['id']]
            nodes.append(ele['data'])  # Extract needed data from nodes
    df_nodes = pd.DataFrame(nodes)  # Generate DataFrames from extracted data, which describe the grid
    for edge in edges:
        # Get voltages of source and target node of edge
        source_voltage = df_nodes.loc[df_nodes['id'] == edge['source']]['linkedObject'].values[0]['voltage']
        target_voltage = df_nodes.loc[df_nodes['id'] == edge['target']]['linkedObject'].values[0]['voltage']
        # Check if a voltage for the node is defined and write voltage of line/edge
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
    Generate a NetworkX graph from the given DataFrames for nodes and edges.
    :param df_nodes: DataFrame containing nodes with 'id' and 'linkedObject'
    :type df_nodes: dataframe
    :param df_edges: DataFrame containing nodes with 'source', 'target' and 'id
    :type df_edges: dataframe
    :return: NetworkX graph of the given grid
    """

    graph = nx.MultiGraph()
    graph.add_nodes_from(df_nodes['id'].tolist())
    nx.set_node_attributes(graph, pd.Series(df_nodes.linkedObject.values, index=df_nodes.id).to_dict(), name="object")
    nodes = copy.deepcopy(graph.nodes(data=True))
    # Search for transformer nodes and add a transformer helper node for each transformer node.
    # For more details see thesis.
    for node in nodes:
        if node[1]['object']['object_type'] == 'transformer':
            node_id = "transformer_" + node[0]
            node_object = objects.create_TransformerHelperNodeObject()
            graph.add_node(node_id, object=node_object)
            graph.add_edge(node[0], node_id, impedance=12, id='transformer_edge_' + node_id[16:])
    # Reconnect the edged which are connected to the transformer
    for idx in range(len(df_edges.index)):
        # Check if source and target node exist
        if df_edges.loc[idx, 'source'] in graph.nodes and df_edges.loc[idx, 'target'] in graph.nodes:
            # Search for edges with source transformer
            if graph.nodes(data=True)[df_edges.loc[idx, 'source']]['object']['object_type'] == 'transformer':
                # If edge is 400V -> Reconnect to transformer_helper_node (low voltage side of transformer)
                # else -> Connect to transformer node (high voltage side of transformer)
                if df_edges.loc[idx, 'voltage'] == 400:
                    graph.add_edge("transformer_" + df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
                else:
                    graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
            # Search for edges with target transformer
            elif graph.nodes(data=True)[df_edges.loc[idx, 'target']]['object']['object_type'] == 'transformer':
                # If edge is 400V -> Reconnect to transformer_helper_node (low voltage side of transformer)
                # else -> Connect to transformer node (high voltage side of transformer)
                if df_edges.loc[idx, 'voltage'] == 400:
                    graph.add_edge(df_edges.loc[idx, 'source'], "transformer_" + df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
                else:
                    graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'],
                                   id=df_edges.loc[idx, 'id'])
            else:
                # If edge wasn't connected to a transformer, just add it to the graph as it is.
                graph.add_edge(df_edges.loc[idx, 'source'], df_edges.loc[idx, 'target'], id=df_edges.loc[idx, 'id'])
        else:
            raise Exception("Kante mit nicht existierendem Knoten")
    return graph


def generate_directed_graph(graph):
    """
    Generates a directed graph out of the undirected one. Performs a bfs for this and takes the external grid as
    the starting point. Checks if there are more ore less than one external grids.
    :param graph: Undirected graph
    :type graph: NetworkX graph
    :return: Directed NetworkX graph
    """

    number_of_ext_grids = 0
    graph_dir = nx.MultiDiGraph()
    nodes_and_attributes = [(n, d) for n, d in graph.nodes(data=True)]
    graph_dir.add_nodes_from(nodes_and_attributes)
    for node in graph.nodes(data=True):     # Find all external grids
        if node[1]['object']['object_type'] == "externalgrid":
            number_of_ext_grids += 1
            source_node = node[0]   # Set external grid as source node
    if number_of_ext_grids > 1:
        raise Exception("Es sind mehr als ein externes Netz vorhanden.")
    elif number_of_ext_grids < 1:
        raise Exception("Es ist kein externes Netz vorhanden.")
    # Perform a directed, breadth-first-search of edges to go through all edges, starting at external grid
    for edge in nx.edge_bfs(graph, source_node, orientation="ignore"):
        edge_id = 'edge'
        for edge_undir in graph.edges:
            # Find id of corresponding undirected edge
            if (edge[0] == edge_undir[0] and edge[1] == edge_undir[1] and edge[2] == edge_undir[2]) or \
                    (edge[0] == edge_undir[1] and edge[1] == edge_undir[0] and edge[2] == edge_undir[2]):
                edge_id = graph.edges[edge_undir]['id']
                break
        if edge[3] == 'reverse':
            graph_dir.add_edge(edge[1], edge[0], id=edge_id)    # Add edge to directed graph in direction as undirected
        else:
            graph_dir.add_edge(edge[0], edge[1], id=edge_id)    # Add edge to directed graph in direction as undirected
    return graph_dir


def check_power_profiles(graph):
    """
    Finds the power profile with the most timesteps and interpolate all other profiles to this length.
    :param graph: Directed NetworkX graph
    :type graph: NetworkX graph
    :return: Updated NetworkX graph
    """

    max_length = 0
    for node in graph.nodes(data=True):     # Get length of the longest power profile (most timesteps)
        if node[0][:11] != 'transformer':   # Don't check for transformer helper node
            if len(node[1]['object']['power']) > max_length:
                max_length = len(node[1]['object']['power'])
    for node in graph.nodes(data=True):     # Interpolate all shorter profiles to the length of the longest one
        if node[0][:11] != 'transformer':  # Don't check for transformer helper node
            if len(node[1]['object']['power']) != max_length:
                node[1]['object']['power'] = interpolate_profile(node[1]['object']['power'], max_length, 'nearest')
    return graph


def generate_equations(graph):
    """
    Generates the incidence matrix of the directed graph and adds a column to make it quadratic
    Also returns a dataframe with each power profile in it.
    :param graph: Directed NetworkX graph
    :return: inc: Incidence matrix; df_power: Dataframe with all power profiles
    """

    df_power = pd.DataFrame()
    for node in graph.nodes(data=True):     # Get power profile from each node
        df_power[node[0]] = node[1]['object']['power']
    inc = nx.incidence_matrix(graph, oriented=True).toarray()   # Generate incidence matrix
    idx, idx_ext = 0, 0
    for node in graph.nodes(data=True):     # Find position of external grid node
        if node[1]['object']['object_type'] == 'externalgrid':
            idx_ext = idx
        idx += 1
    # Create new column for external grid to make incidence matrix quadratical
    new_column = np.array([np.zeros(np.shape(inc)[0])])
    new_column[0][idx_ext] = -1
    inc = np.append(inc, np.transpose(new_column), axis=1)
    return inc, df_power


def solve_flow(A, b):
    """
    Solves the load flow with a given incidence matrix and result vector. Checks if the matrix is quadratic.
    :param A: Incidence Matrix = equations to solve
    :param b: Result vector
    :return: Flow vector
    :rtype: ndarray
    """

    if np.shape(A)[0] != np.shape(A)[1]:
        raise Exception("Inzidenzmatrix ist nicht quadratisch!")
    flow = np.linalg.solve(A, b)
    return flow


def plot_graph(graph):
    """
    Plots the NetworkX graph which is created from the grid cytoscape.
    :param graph: NetworkX graph
    :return: base64 string of png picture
    """

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

    # plt.show()
    return base64_encoded


def correct_cyto_edges(elements, graph):
    """
    Function takes the elements of the grid cytoscape and corrects all edges, so the point in the same direction as in
    the directed graph of the grid.
    Needed for the display of arrows.
    :param elements: Element list of dash cytoscape
    :param graph: Directed Graph of the grid.
    :return: Edited Element list of dash cytoscape
    :rtype: list
    """

    for idx, ele in enumerate(elements):
        if 'source' in ele['data']:     # If element is edge
            start_node = None
            target_node = None
            edge_id = ele['data']['id']
            for graph_edge in graph.edges(data=True):  # Search for corresponding edge in graph
                if graph_edge[2]['id'] == edge_id:
                    start_node = graph_edge[0]
                    target_node = graph_edge[1]
                    break
            if start_node is None or target_node is None:
                raise Exception('Fehler bei Richtungszuweisung Leitungen.')
            if start_node[:11] == 'transformer':    # Problem with transformer node: doesn't exist in cytoscape
                if target_node == ele['data']['target']:    # If target of both edges are the same
                    start_node = ele['data']['source']      # Get source node from cytoscape and set start_node
                else:                                       # In this case the desired node is target of cyto edge
                    start_node = ele['data']['target']      # Get target node from cytoscape and set start_node
            if target_node[:11] == 'transformer':  # Same for target node
                if start_node == ele['data']['source']:
                    target_node = ele['data']['target']
                else:
                    target_node = ele['data']['source']
            if ele['data']['source'] != start_node:     # If the orientation of cyto edge and graph edge are different
                elements[idx]['data']['source'] = start_node
                elements[idx]['data']['target'] = target_node
    return elements


def power_flow_statemachine(state, data):
    """
    State machine of grid calculation. Executes all checks and steps necessary.
    :param state: Statemachine state to execute in this step
    :type state: str
    :param data: All needed data for the calculation
    :type data: dict
    :return: Next statemachine state; updated data dict; flag if calculation is done (bool)
    """

    if state == 'init':
        if len(data['elements']) == 0:  # Check if there are any elements in the grid
            raise Exception('notification_emptygrid')
        return 'gen_dataframes', data, False
    elif state == 'gen_dataframes':
        # Generate dataframes of the nodes and edges for the calculation
        data['df_nodes'], data['df_edges'] = generate_grid_dataframes(data['elements'], data['grid_objects'])
        return 'gen_grid_graph', data, False
    elif state == 'gen_grid_graph':
        # Generate NetworkX graph of the grid
        data['grid_graph'] = generate_grid_graph(data['df_nodes'], data['df_edges'])
        return 'check_isolates', data, False
    elif state == 'check_isolates':
        # Check if there are isolated (not connected) nodes
        if nx.number_of_isolates(data['grid_graph']) > 0:
            raise Exception('notification_isolates')
        return 'check_tree', data, False
    elif state == 'check_tree':
        # Check if the graph/grid structure is a tree. If not, there are cycles in the grid.
        # TODO: IMPLEMENT FUNCTIONS TO HANDLE CYCLES AND PARALLEL GRID STRUCTURES. See thesis for more information.
        # Check by generating minimum spanning tree and compare number of edges
        min_spanning_tree = nx.minimum_spanning_tree(data['grid_graph'])
        if data['grid_graph'].number_of_edges() != min_spanning_tree.number_of_edges():
            raise Exception('notification_cycles')
        return 'gen_directed_graph', data, False
    elif state == 'gen_directed_graph':
        # Generate directed graph from undirected graph to handle power flow directions. Starting at external grid.
        data['grid_graph'] = generate_directed_graph(data['grid_graph'])
        return 'check_power_profiles', data, False
    elif state == 'check_power_profiles':
        # Check length of power profiles and adjust them all to the longest length.
        data['grid_graph'] = check_power_profiles(data['grid_graph'])
        return 'gen_equations', data, False
    elif state == 'gen_equations':
        # Generate the equations to solve for the power flow
        data['A'], data['df_power'] = generate_equations(data['grid_graph'])
        return 'calc_flow', data, False
    elif state == 'calc_flow':
        # Calculate the powerflow for every timestep
        column_names = []
        for edge in data['grid_graph'].edges:   # Get column names, one column name for each edge
            column_names.append(data['grid_graph'].edges[edge]['id'])
        column_names.append("external_grid")    # Add column name for external grid
        df_flow = pd.DataFrame(columns=column_names)    # Create dataframe for flow results with column names
        for step, row in data['df_power'].iterrows():   # Solve power flow for each timestep (=row) in df_power
            df_flow.loc[step] = solve_flow(data['A'], row)
        data['df_flow'] = df_flow
        return 'set_edge_labels', data, False
    elif state == 'set_edge_labels':
        # Set the direction of cytoscape edges to point in the right direction and set labels with power in timestep
        data['elements'] = correct_cyto_edges(data['elements'], data['grid_graph'])
        data['labels'] = data['df_flow'].loc[0].to_dict()
        return None, data, True


def calculate_power_flow(elements, grid_object_dict):
    """
    Main function to calculate the power flows in the created and configured grid. Built as a state-machine.
    :param grid_object_dict: Dictionary of objects in grid with id corresponding to node ids of cytoscape
    :type grid_object_dict: dict
    :param elements: Grid elements in form of cytoscape graph
    :type elements: list
    :return: Dataframe Flow, edge labels
    """

    state = 'init'
    ready = False
    data = {'elements': elements, 'grid_objects': grid_object_dict}
    while not ready:
        # print(state)
        state, data, ready = power_flow_statemachine(state, data)
        # print("Done")
    return data['df_flow'], data['labels']


def calculate_house(device_dict, timesteps):
    """
    Takes all devices and calculates: The sum of all devices per room and house; The energy used by devices,
    rooms and house.
    :param device_dict: Dictionary containing all devices in the custom house
    :type device_dict: dict
    :param timesteps: Number of timesteps
    :type timesteps: range
    :return: df_power: Dataframe with power of each device in each timestep;
    df_sum: Dataframe with sum power of all rooms and house per timestep;
    df_energy: Dataframe with overall energy per room and house;
    figure[0]: Scatter plot of results; figure[1]: Sunburst plot of energys
    """

    df_power = pd.DataFrame(columns=timesteps)  # Prepare dataframe with one column per timestep
    df_power.insert(0, 'room', '')  # Add column for room of device
    df_sum = pd.DataFrame(columns=timesteps)    # Prepare dataframe with one column per timestep
    df_energy = pd.DataFrame(columns=['type', 'energy'])    # Prepare dataframe
    for room in device_dict['rooms']:   # Iterate through each room
        for dev in device_dict['rooms'][room]['devices']:  # Go through each device in the house
            device = device_dict['house1'][dev]  # Get device properties from dict
            if device['active']:  # If device is activated
                # Get device power profile as row
                df_power.loc[device['id'], df_power.columns != 'room'] = device['power']
                # Get room of device to room column
                df_power.loc[device['id'], df_power.columns == 'room'] = room
                # Calculate energy in kWh
                energy = df_power.loc[device['id'], df_power.columns != 'room'].sum() / 60 / 1000
                df_energy.loc[device['id']] = {'type': 'device', 'energy': energy}
            else:   # If device is deactivated
                df_energy.loc[device['id']] = {'type': 'device', 'energy': 0}
        # Get sum of all devices in room
        df_sum.loc[room] = df_power.loc[df_power['room'] == room].sum().transpose()
        energy = df_sum.loc[room].sum() / 60 / 1000  # Calculate energy in kWh for room
        df_energy.loc[room] = {'type': 'room', 'energy': energy}
    df_sum.loc['house1'] = df_sum.sum().transpose()  # Get sum of all rooms in house
    energy = df_sum.loc['house1'].sum() / 60 / 1000  # Calculate energy in kWh for house
    df_energy.loc['house1'] = {'type': 'house', 'energy': energy}
    # Plot the results
    figures = plot.plot_all_devices_room(df_power, df_sum, df_energy, device_dict)
    return df_power, df_sum, df_energy, figures[0], figures[1]


def interpolate_profile(values, number_steps, interpolation_type):
    """
    Interpolates a given profile to a given number of timesteps. The interpolation method can be defined.
    Possible kinds of interpolation: linear, nearest, nearest-up, zero, slinear, quadratic, cubic, previous, next
    :param values: Original values of profile
    :type values: list
    :param number_steps: Number of steps of final profile
    :type number_steps: int
    :param interpolation_type: Type of interpolation
    :type interpolation_type:str
    :return: Final interpolated profile
    :rtype: list
    """

    if len(values) == 1:     # If profile consists of only one value, add the same to make interpolation possible
        values = np.append(values, values[0])
    timesteps_values = np.linspace(0, number_steps-1, num=len(values), endpoint=True)
    f_inter = interpolate.interp1d(timesteps_values, values, kind=interpolation_type)
    x_new = np.linspace(0, number_steps, num=number_steps, endpoint=False)
    y_new = f_inter(x_new)
    return y_new


def save_settings_devices(children, device_dict, selected_element, house, day):
    """
    Save all settings of the selected device. This is done by looping over all children of the menu tab.
    After checking their type, it is selected what to do and how to save the input.
    :param children: Children of the menu tab, all inputs of the selected device
    :param device_dict: Dictionary containing all devices in the custom house
    :param selected_element: Cytoscape element which was clicked in the house
    :param house: house-id of house in which a device should be saved, 'house1'
    :param day: Day selected in the pagination of the menu
    :return: device_dict: Dictionary containing all devices in the custom house
    """

    for child in children:  # Go through all components of the settings menu
        if child['type'] == 'Text':  # Do nothing on things like text or vertical spaces
            pass
        elif child['type'] == 'Space':
            pass
        elif child['type'] == 'Button':
            pass
        elif child['type'] == 'Graph':
            pass
        elif child['type'] == 'SegmentedControl':
            pass
        elif child['type'] == 'Group':  # Recursive execution for all elements in group
            save_settings_devices(child['props']['children'], device_dict, selected_element, house, day)
        else:  # Save values of input components to device dictionary
            if child['type'] == 'TextInput':
                if child['props']['id'] == 'name_input':
                    device_dict[house][selected_element]['name'] = child['props']['value']
            elif child['type'] == 'Select':
                if child['props']['id'] == 'load_profile_select_preset':    # Only do this if it is a preset profile
                    if child['props']['value'] is not None:
                        device_dict[house][selected_element]['selected_power_option'] = child['props']['value']
                        # Get key of the database entry from the power options of the device
                        key = device_dict[house][selected_element]['power_options'][child['props']['value']]['key']
                        database = root_path + 'source/database_profiles.db'
                        table_name = device_dict[house][selected_element]['menu_type']  # From which SQLite-Table
                        # Check if it is an own device -> profiles are stored in dict
                        if 'power_profiles' in device_dict[house][selected_element]:
                            load_profile = device_dict[house][selected_element]['power_profiles'][key]
                        else:  # If it is predefined device -> Get load profile from sql database
                            load_profile = sql_modules.get_load_profile(table_name, key, database)
                        load_profile *= 7   # Extend profile from one day to one week
                        # Save generated profile to device dictionary
                        device_dict[house][selected_element]['power'] = load_profile
                    else:
                        # Raise Exception that no profile is selected -> Notification is shown
                        raise Exception("notification_no_profile_selected")
                elif child['props']['id'] == 'load_profile_select_custom':
                    # If it's a custom profile, just set the selected power option, the profile is generated later on
                    device_dict[house][selected_element]['selected_power_option'] = child['props']['value']
            elif child['type'] == 'TimeInput':
                if 'value' in child['props']:     # There is a time input -> Add to load profile
                    if device_dict[house][selected_element]['selected_power_option'] is not None:
                        day_ind = days[day]    # Get number of day in week (Monday=0, Tuesday=1, ...)
                        timestamp = child['props']['value']
                        timestamp = timestamp[len(timestamp)-8:]                    # Get time from input
                        minutes = int(timestamp[:2]) * 60 + int(timestamp[3:5])     # calculate start in minutes
                        minutes = minutes + day_ind * 24 * 60                       # Add offset due to different days
                        table_name = device_dict[house][selected_element]['menu_type']  # From which SQLite-Table
                        selected_power_option = device_dict[house][selected_element]['selected_power_option']
                        # Get key of the database entry from the power options of the device
                        key = device_dict[house][selected_element]['power_options'][selected_power_option]['key']
                        database = root_path + 'source/database_profiles.db'
                        # Check if it is an own device -> profiles are stored in dict
                        if 'power_profiles' in device_dict[house][selected_element]:
                            load_profile = device_dict[house][selected_element]['power_profiles'][key]
                        else:   # If it is predefined device -> Get load profile from database
                            # Get load profile snippet from sql database
                            load_profile = sql_modules.get_load_profile(table_name, key, database)
                        standby_power = load_profile[0]     # Get standby power (first element of loaded profile)
                        load_profile = pd.Series(load_profile[1:])     # Delete first element (standby power)
                        load_profile = load_profile.fillna(0)          # If there are nan values, fill them with zero
                        power = pd.Series(device_dict[house][selected_element]['power'])    # Get current power profile
                        index_pos = minutes - 1
                        # Add loaded profile to power profile of the device and save
                        power[index_pos:index_pos + len(load_profile)] = load_profile.values
                        device_dict[house][selected_element]['power'] = power.to_list()
                    else:
                        # Raise Exception that no profile is selected -> Notification is shown
                        raise Exception("notification_no_profile_selected")
                else:
                    # Raise Exception that no time is selected -> Notification is shown
                    raise Exception("notification_no_time_input")
    return device_dict


def save_settings_house(children, gridObject_dict, selected_element, year, week, used_profiles, checkbox):
    """
    Save all settings of a selected house. Load random profile if wanted.
    :param children: Children of the menu tab, all inputs of the selected object
    :param gridObject_dict: Dictionary containing all grid objects and their properties
    :param selected_element: Cytoscape element which was clicked in the grid
    :param year: Year set in the settings tab
    :param week: Week of year set in the settings tab
    :param used_profiles: Already used random profiles from IZES
    :param checkbox: Bool if checkbox to load random profile is checked
    :return: Updated gridObject_dict, updated used_profiles
    """

    if checkbox:    # If wanted, load a random household profile from the database
        date_start, date_stop = get_monday_sunday_from_week(week, year)
        profile = random.choice(profile_selection)  # Randomly choose one of the profiles provided
        while profile in used_profiles:     # Make sure to load a profile which wasn't used already
            profile = random.choice(profile_selection)
        used_profiles.append(profile)   # Update list of used profiles
        power = sql_modules.get_household_profile(root_path + 'source/database_izes_reduced.db',
                                                  profile, date_start, date_stop)
        gridObject_dict[selected_element]['power'] = power
        gridObject_dict[selected_element]['power_profile'] = profile
    gridObject_dict[selected_element]['name'] = children[0]['props']['value']
    return gridObject_dict, used_profiles


def save_settings_pv(children, gridObject_dict, selected_element, year, week):
    """
    Saves the settings of a PV-module. After all data was checked and prepared, it loads the solar data from
    renewables.ninja.
    :param children: Children of the menu tab, all inputs of the selected object
    :param gridObject_dict: Dictionary containing all grid objects and their properties
    :param selected_element: Cytoscape element which was clicked in the grid
    :param year: Year set in the settings tab
    :param week: Week of year set in the settings tab
    :return: Updated gridObject_dict, Notification
    """
    # TODO: Changes here also have to be done in update_settings module

    # TODO: FETCHING SOLAR DATA IS LIMITED TO 50/hour. CHANGE TO FETCH FROM OWN DATABASE
    # The modules from renewables.ninja to calculate electrical power from solar power can be used.

    postcode = children[2]['props']['value']
    tilt = children[4]['props']['children'][1]['props']['children'][1]['props']['children'][1]['props']['value']
    rated_power = children[4]['props']['children'][1]['props']['children'][0]['props']['children'][1]['props']['value']
    database = root_path + 'source/database_pv.db'
    token_rn = '9d539337969f016d51d3c637ddba49bbc9fe6e71'   # Authorization renewables.ninja
    sess = requests.session()
    sess.headers = {'Authorization': 'Token ' + token_rn}
    url = 'https://www.renewables.ninja/api/data/pv'
    if not sql_modules.check_postcode(postcode, database):  # Check if the given postcode exist in database
        return gridObject_dict, 'notification_false_postcode'   # If not, show error notification
    lon, lat, city = sql_modules.get_coordinates(postcode, database)    # Get coordinates from postcode
    if week == 1:   # Problem: Data only exist from 2019, week 1 starts in 2018
        week = 2    # Solution: use week 2 instead of week one TODO Solve week 1 problem properly
    date_start, date_stop = get_monday_sunday_from_week(week, year)
    azimuth = gridObject_dict[selected_element]['orientation']
    query_params = {
        'lat': lat,  # latitude of the location
        'lon': lon,  # longitude of the location
        'date_from': str(date_start),  # starting date of the data
        'date_to': str(date_stop),  # ending date of the data
        'dataset': 'sarah',  # dataset to use for the simulation
        'capacity': rated_power,  # capacity of the PV system in kW
        'system_loss': 0.1,  # system loss
        'tracking': 0,  # tracking mode, 0 = fixed, 1 = 1-axis tracking, 2 = 2-axis tracking
        'tilt': tilt,  # tilt angle of the PV system in degrees
        'azim': azimuth,  # azimuth angle of the PV system in degrees
        'format': 'json'  # format of the data, csv or json
    }
    response = sess.get(url, params=query_params)   # Send the GET request and get the response
    if response.status_code == 200:     # Check if the request was successful
        data_pd = pd.read_json(json.dumps(response.json()['data']), orient='index', typ='frame')
    else:
        return gridObject_dict, 'notification_pv_api_error'     # Show an error notification
    # Write data to selected element (Inverted Power and unit changed to Watts):
    gridObject_dict[selected_element]['power'] = [-i * 1000 for i in data_pd['electricity'].values.tolist()]
    gridObject_dict[selected_element]['location'] = [postcode, lat, lon]
    gridObject_dict[selected_element]['name'] = children[0]['props']['value']
    gridObject_dict[selected_element]['rated_power'] = rated_power
    gridObject_dict[selected_element]['tilt'] = tilt
    return gridObject_dict, None


def update_settings(gridObject_dict, selected_element, year, week):
    """
    Updates the selected element with the stored settings year and week.
    :param gridObject_dict: Dictionary containing all grid objects and their properties
    :type gridObject_dict: dict
    :param selected_element: Element to update
    :type selected_element: str
    :param year: Year to fetch data from
    :type year: int
    :param week: Week of the year
    :type week: int
    :return: Updated gridObject_dict
    :rtype: dict
    """
    # TODO: Implement update of settings properly.
    # Does not work yet, not in use, button_update_settings is disabled

    date_start, date_stop = get_monday_sunday_from_week(week, year)
    if gridObject_dict[selected_element]['object_type'] == 'house':
        profile = gridObject_dict[selected_element]['power_profile']
        power = sql_modules.get_household_profile(root_path + 'source/database_izes_reduced.db',
                                                  profile, date_start, date_stop)
        gridObject_dict[selected_element]['power'] = power
    elif gridObject_dict[selected_element]['object_type'] == 'pv':
        lat = gridObject_dict[selected_element]['location'][1]
        lon = gridObject_dict[selected_element]['location'][2]
        token_rn = '9d539337969f016d51d3c637ddba49bbc9fe6e71'  # Authorization renewables.ninja
        sess = requests.session()
        sess.headers = {'Authorization': 'Token ' + token_rn}
        url = 'https://www.renewables.ninja/api/data/pv'
        if week == 1:  # Problem: Data only exist from 2019, week 1 starts in 2018
            week = 2
        date_start, date_stop = get_monday_sunday_from_week(week, year)
        azimuth = gridObject_dict[selected_element]['orientation']
        query_params = {
            'lat': lat,  # latitude of the location
            'lon': lon,  # longitude of the location
            'date_from': str(date_start),  # starting date of the data
            'date_to': str(date_stop),  # ending date of the data
            'dataset': 'sarah',  # dataset to use for the simulation
            'capacity': 1,  # capacity of the PV system in kW
            'system_loss': 0.1,  # system loss in %
            'tracking': 0,  # tracking mode, 0 = fixed, 1 = 1-axis tracking, 2 = 2-axis tracking
            'tilt': 35,  # tilt angle of the PV system in degrees
            'azim': azimuth,  # azimuth angle of the PV system in degrees
            'format': 'json'  # format of the data, csv or json
        }
        response = sess.get(url, params=query_params)  # Send the GET request and get the response
        if response.status_code == 200:  # Check if the request was successful
            data_pd = pd.read_json(json.dumps(response.json()['data']), orient='index', typ='frame')
        else:
            raise Exception('Fehler bei der PV-Datenabfrage!')
        # Write data to selected element:
        gridObject_dict[selected_element]['power'] = [-i * 1000 for i in
                                                      data_pd['electricity'].values.tolist()]  # Inverted Power and unit changed to Watts
    return gridObject_dict


def get_monday_sunday_from_week(week_num, year):
    """
    Get the dates of monday and sunday of a given week in a given year.
    :param week_num:
    :type week_num: int
    :param year:
    :type year: int
    :return: Dates of monday and sunday
    :rtype: date
    """

    first_day = datetime(year, 1, 1)    # get the date of the first day of the year
    days_to_first_monday = (7 - first_day.weekday()) % 7    # calculate the days to the first Monday of the year
    # calculate the date of the Monday of the first week
    monday_first_week = first_day + timedelta(days=days_to_first_monday)
    monday = monday_first_week + timedelta(weeks=week_num-2)    # calculate the date of the Monday of the given week
    sunday = monday + timedelta(days=6)     # calculate the date of the Sunday of the given week
    return monday.date(), sunday.date()


def get_button_dict():
    """
    Get a dictionary of all the buttons of the rooms in the custom house. The dictionary is split into each room
    and contains the menu-objects for each device. They consist of:
    name, dash button-id, icon
    Only the devices are considered, which have a standard room named in the database.
    :return: dictionary of buttons for the room menus
    :rtype: dict
    """

    devices = sql_modules.get_button_dict(root_path + 'source/database_profiles.db')  # Get the dict from the database
    button_dict = {}
    for device in devices:
        if device[1] not in button_dict:  # If room doesn't already exist in dict, create list for it
            button_dict[device[1]] = []
        button_dict[device[1]].append([
            device[2], "button_add_" + device[0], device[4]
        ])
    return button_dict


def get_icon_url(icon_name: str):
    """
    Takes an icon name in the format "mdi:icon-name" and returns the Iconify URL for the icon.
    :param icon_name: iconify name of icon
    :type icon_name: str
    :return: url of icon
    :rtype: str
    """

    base_url = "https://api.iconify.design"
    icon_url = f"{base_url}/{icon_name}.svg"
    response = requests.get(icon_url)
    return response.url
