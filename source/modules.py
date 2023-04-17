import base64
import copy
import io
import json
import warnings
from datetime import datetime, timedelta
from random import randint

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
from scipy import interpolate

import source.objects as objects
import source.plot as plot
import source.sql_modules as sql_modules

days = {'mo': 0, 'tu': 1, 'wd': 2, 'th': 3, 'fr': 4, 'sa': 5, 'su': 6}


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


def check_power_profiles(graph):
    max_length = 0
    for node in graph.nodes(data=True):     # Get length of longest power profile (most timesteps)
        if node[0][:11] != 'transformer':   # Don't check for transformer helper node
            if len(node[1]['object']['power']) > max_length:
                max_length = len(node[1]['object']['power'])
    for node in graph.nodes(data=True):     # Interpolate all shorter profiles to the length of the longest one
        if node[0][:11] != 'transformer':  # Don't check for transformer helper node
            if len(node[1]['object']['power']) != max_length:
                node[1]['object']['power'] = interpolate_profile(node[1]['object']['power'], max_length, 'nearest')
    return graph


def generate_equations(graph):
    df_power = pd.DataFrame()
    for node in graph.nodes(data=True):     # Get power profile from each node
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


def correct_cyto_edges(elements, graph, flow):
    """
    Function takes the elements of the grid cytoscape and corrects all edges, so the point in the same direction as in the directed graph of the grid.
    Needed for the display of arrows.
    :param elements: Element list of dash cytoscape
    :param graph: Directed Graph of the grid.
    :param flow: Result of the flow calculation.
    :return: Edited Element list of dash cytoscape
    """
    # elements_new = copy.deepcopy(elements)
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
        return 'check_power_profiles', data, False
    elif state == 'check_power_profiles':
        data['grid_graph'] = check_power_profiles(data['grid_graph'])
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
        data['elements'] = correct_cyto_edges(data['elements'], data['grid_graph'], data['df_flow'])
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
    return data['df_flow'], data['labels'], data['elements'], plot_graph(data['grid_graph'])


def calculate_house(device_dict, timesteps):
    df_power = pd.DataFrame(columns=timesteps)
    df_power.insert(0, 'room', None)  # Add column for room of device
    df_sum = pd.DataFrame(columns=timesteps)
    df_energy = pd.DataFrame(columns=['type', 'energy'])
    for room in device_dict['rooms']:
        for dev in device_dict['rooms'][room]:  # Go through each device in the house
            device = device_dict['house1'][dev]  # Get device properties from dict
            if device['active']:  # If device is activated
                df_power.loc[device['id'], df_power.columns != 'room'] = device['power']
                df_power.loc[device['id'], df_power.columns == 'room'] = room
                energy = df_power.loc[device['id'], df_power.columns != 'room'].sum() / 60 / 1000  # Calculate energy in kWh
                df_energy.loc[device['id']] = {'type': 'device', 'energy': energy}
            else:
                df_energy.loc[device['id']] = {'type': 'device', 'energy': 0}
        # Problem hier: Es werden alle geräte aufsummiert
        df_sum.loc[room] = df_power.loc[df_power['room'] == room].sum().transpose()  # Get sum of all devices in room
        energy = df_sum.loc[room].sum() / 60 / 1000  # Calculate energy in kWh
        temp = df_sum.loc[room]
        df_energy.loc[room] = {'type': 'room', 'energy': energy}
    df_sum.loc['house1'] = df_sum.sum().transpose()  # Get sum of all rooms in house
    energy = df_sum.loc['house1'].sum() / 60 / 1000  # Calculate energy in kWh
    df_energy.loc['house1'] = {'type': 'house', 'energy': energy}
    figures = plot.plot_all_devices_room(df_power, df_sum, df_energy, device_dict)
    return df_power, df_sum, figures[0], figures[1]


def interpolate_profile(values, number_steps, interpolation_type):
    # possible kinds: linear, nearest, nearest-up, zero, slinear, quadratic, cubic, previous, next
    if len(values) < 2:
        values = np.append(values, values[0])
    timesteps_values = np.linspace(0, number_steps-1, num=len(values), endpoint=True)
    f_inter = interpolate.interp1d(timesteps_values, values, kind=interpolation_type)
    x_new = np.linspace(0, number_steps, num=number_steps, endpoint=False)
    y_new = f_inter(x_new)
    plt.plot(y_new)
    plt.show()
    return y_new


def save_settings_devices(children, device_dict, selected_element, house, day):
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
        elif child['type'] == 'Group':
            save_settings_devices(child['props']['children'], device_dict, selected_element, house, day)  # Recursive execution for all elements in group
        else:  # Save values of input components to device dictionary
            if child['type'] == 'TextInput':
                if child['props']['id'] == 'name_input':
                    device_dict[house][selected_element]['name'] = child['props']['value']
            elif child['type'] == 'Select':
                if child['props']['id'] == 'load_profile_select':
                    if child['props']['value'] is not None:
                        device_dict[house][selected_element]['selected_power_option'] = child['props']['value']
                        key = device_dict[house][selected_element]['power_options'][child['props']['value']]['key']
                        database = 'source/database_profiles.db'
                        table_name = device_dict[house][selected_element]['menu_type']  # From which SQLite-Table
                        load_profile = sql_modules.get_load_profile(table_name, key,
                                                                    database)  # Get load profile from sqlite database
                        load_profile *= 7   # Extend profile from one day to one week
                        device_dict[house][selected_element][
                            'power'] = load_profile  # Save loaded profile to device dictionary
            elif child['type'] == 'TimeInput':
                if child['props']['value'] is not None:     # There is a time input -> Add to load profile
                    day_ind = days[day]    # Get number of day in week (Monday=0, Tuesday=1, ...)
                    timestamp = child['props']['value']
                    timestamp = timestamp[len(timestamp)-8:]    # Get time from input
                    minutes = int(timestamp[:2]) * 60 + int(timestamp[3:5])     # calculate start in minutes
                    minutes = minutes + day_ind * 24 * 60                           # Add offset due to different days
                    power = pd.Series(device_dict[house][selected_element]['power'])    # Get current power profile
                    new_values = pd.Series([100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100])    # Development
                    index_pos = minutes - 1
                    power[index_pos:index_pos + len(new_values)] = new_values.values
                    device_dict[house][selected_element]['power'] = power.to_list()
    return device_dict


def save_settings_house(children, gridObject_dict, selected_element, year, week, used_profiles, checkbox):
    if checkbox:    # If wanted, load a random household profile from the database
        date_start, date_stop = get_monday_sunday_from_week(week, year)
        profile = randint(1, 74)
        while profile in used_profiles:     # Make sure to load a profile which wasn't used already
            profile = randint(1, 74)
        used_profiles.append(profile)
        power = sql_modules.get_household_profile('source/database_izes.db', profile, date_start, date_stop)
        gridObject_dict[selected_element]['power'] = power
        gridObject_dict[selected_element]['power_profile'] = profile
    gridObject_dict[selected_element]['name'] = children[0]['props']['value']
    return gridObject_dict, used_profiles


def save_settings_pv(children, gridObject_dict, selected_element, year, week):
    # Important: Changes here also have to be done in update_settings module
    postcode = children[2]['props']['value']
    tilt = children[4]['props']['children'][1]['props']['children'][1]['props']['children'][1]['props']['value']
    rated_power = children[4]['props']['children'][1]['props']['children'][0]['props']['children'][1]['props']['value']
    database = 'source/database_pv.db'
    token_rn = '9d539337969f016d51d3c637ddba49bbc9fe6e71'   # Authorization renewables.ninja
    sess = requests.session()
    sess.headers = {'Authorization': 'Token ' + token_rn}
    url = 'https://www.renewables.ninja/api/data/pv'
    if not sql_modules.check_postcode(postcode, database):  # Check if the given postcode exist in database
        return gridObject_dict, 'notification_false_postcode'
    lon, lat, city = sql_modules.get_coordinates(postcode, database)    # Get coordinates from postcode
    if week == 1:   # Problem: Data only exist from 2019, week 1 starts in 2018
        week = 2
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
        return gridObject_dict, 'notification_pv_api_error'
    # Write data to selected element:
    gridObject_dict[selected_element]['power'] = [-i * 1000 for i in data_pd['electricity'].values.tolist()]  # Inverted Power and unit changed to Watts
    gridObject_dict[selected_element]['location'] = [postcode, lat, lon]
    gridObject_dict[selected_element]['name'] = children[0]['props']['value']
    gridObject_dict[selected_element]['rated_power'] = rated_power
    gridObject_dict[selected_element]['tilt'] = tilt
    return gridObject_dict, None


def update_settings(gridObject_dict, selected_element, year, week):
    date_start, date_stop = get_monday_sunday_from_week(week, year)
    if gridObject_dict[selected_element]['object_type'] == 'house':
        profile = gridObject_dict[selected_element]['power_profile']
        power = sql_modules.get_household_profile('source/database_izes.db', profile, date_start, date_stop)
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
    first_day = datetime(year, 1, 1)    # get the date of the first day of the year
    days_to_first_monday = (7 - first_day.weekday()) % 7    # calculate the days to the first Monday of the year
    monday_first_week = first_day + timedelta(days=days_to_first_monday)    # calculate the date of the Monday of the first week
    monday = monday_first_week + timedelta(weeks=week_num-2)    # calculate the date of the Monday of the given week
    sunday = monday + timedelta(days=6)     # calculate the date of the Sunday of the given week
    return monday.date(), sunday.date()


def handle_error(err):
    print("Error: ", err)
