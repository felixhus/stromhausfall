import os
import random
import time

import dash_bootstrap_components as dbc
import dash_extensions as dex
import dash_mantine_components as dmc
import grid_objects
# import objects
import pandas as pd
import plotly.express as px
# from dash_extensions import EventListener
from dash import Dash, Input, Output, State, ctx, dcc, html, no_update
from dash.exceptions import PreventUpdate
# from dash_extensions.enrich import DashProxy
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.example_grids as example_grids
import source.objects as objects
import source.stylesheets as stylesheets
from source.modules import (calculate_power_flow, connection_allowed,
                            generate_grid_object, get_connected_edges,
                            get_last_id)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])
server = app.server
df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length')

menu_objects = [
    ['button_house', 'icon_house2.png'],
    ['button_transformer', 'icon_transformer.png'],
    ['button_externalgrid', 'icon_powerplant.png'],
    ['button_pv', 'icon_pv.png'],
    ['button_battery', 'icon_battery.png'],
    ['button_smartmeter', 'icon_meter.png'],
    ['button_switch_cabinet', 'icon_switch_cabinet.png'],
    ['button_line', 'icon_line_lv.png'],
]

house_objects = [
    ['button_dryer', "Föhn"],
    ['button_fridge', "Kühlschrank"],
    ['button_lamp', "Lampe"],
    ['button_stove', "Herd"],
    ['button_tv', "TV"],
]

nodes = []
edges = []
# gridObject_dict = []
bathroom = grid_objects.BathroomObject()

app.layout = dmc.NotificationsProvider(dbc.Container([
    dbc.Col([
        dbc.Row(
            dash_components.dash_navbar(),
        ),
        dbc.Row([
            dbc.Col([
                dmc.Card([
                    dbc.Row(dash_components.add_grid_object_button(object_id=menu_objects[i][0],
                                                                   icon=app.get_asset_url(
                                                                       'Icons/' + menu_objects[i][1])))
                    for i in range(len(menu_objects))
                ], id='grid_buttons', style={'display': 'block'}, withBorder=True, shadow="sm", radius="md"),
                html.Div([
                    dbc.Row(dash_components.add_grid_object_button(object_id=house_objects[i][0],
                                                                   name=house_objects[i][1]))
                    for i in range(len(house_objects))
                ], id='house_buttons', style={'display': 'none'}),
            ], width=1),
            dbc.Col([dash_components.add_cytoscape_layout()], width=7),
            dbc.Col([dash_components.card_start(), dash_components.card_menu()], width=True)
        ]),
        dash_components.add_modal_edit(),
        dash_components.add_modal_readme(),
        dash_components.add_drawer_notifications(),
        dash_components.add_modal_voltage_level(),
        dash_components.add_storage_variables(),
        dex.EventListener(id='key_event_listener', events=[{'event': 'keydown', 'props': ["key"]}]),
        html.P(id='init')], width=True),
    html.Div(id='notification_container')
], id='main_container'))


@app.callback(Output('cyto1', 'autoungrabify'),  # Callback to make Node ungrabbable when adding lines
              Output('store_line_edit_active', 'data'),
              Output('button_line', 'variant'),
              Input('button_line', 'n_clicks'),
              Input('key_event_listener', 'n_events'),
              State('key_event_listener', 'event'),
              State('store_line_edit_active', 'data'),
              prevent_initial_call=True)
def edit_mode(btn_line, n_events, event, btn_active):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        if not btn_active:
            return True, True, 'light'
        else:
            return False, False, 'filled'
    elif triggered_id == 'key_event_listener':
        if event['key'] == 'Escape' and btn_active:
            return False, False, 'filled'
        else:
            raise PreventUpdate


@app.callback(Output('cyto1', 'elements'),  # Callback to change elements of cyto
              Output('store_grid_object_dict', 'data'),
              Output('start_of_line', 'data'),
              Output('store_element_deleted', 'data'),
              Output('store_notification1', 'data'),
              Output('store_get_voltage', 'data'),
              Output('modal_voltage', 'opened'),
              Input('store_add_node', 'data'),
              Input('cyto1', 'selectedNodeData'),
              Input('edit_delete_button', 'n_clicks'),
              Input('button_line', 'n_clicks'),
              Input('example_button', 'n_clicks'),
              Input('store_edge_labels', 'data'),
              Input('button_voltage_hv', 'n_clicks'),
              Input('button_voltage_lv', 'n_clicks'),
              State('cyto1', 'elements'),
              State('store_grid_object_dict', 'data'),
              State('store_line_edit_active', 'data'),
              State('start_of_line', 'data'),
              State('store_selected_element_grid', 'data'),
              State('store_get_voltage', 'data'),
              prevent_initial_call=True)
def edit_grid(btn_add, node, btn_delete, btn_line, btn_example, labels, button_hv, button_lv, elements,
              gridObject_dict, btn_line_active, start_of_line, selected_element, node_ids):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':  # Start line edit mode, set 'start_of_line' as None
        return no_update, no_update, None, no_update, no_update, no_update, no_update
    elif triggered_id == 'store_add_node':
        last_id = get_last_id(elements)
        new_gridobject = generate_grid_object(btn_add, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
        image_src = app.get_asset_url('Icons/' + new_gridobject['icon'])
        gridObject_dict[new_gridobject['id']] = new_gridobject
        new_element = {'data': {'id': 'node' + str(last_id[0] + 1)},
                       'position': {'x': 50, 'y': 50}, 'classes': 'node_style',
                       'style': {'background-image': image_src, 'background-color': new_gridobject['ui_color']}}
        elements.append(new_element)
        return elements, gridObject_dict, no_update, no_update, no_update, no_update, no_update
    elif triggered_id == 'cyto1':  # # Node was clicked
        if not node == []:
            if btn_line_active:  # Add-line-mode is on
                if start_of_line is not None:
                    if connection_allowed(start_of_line[0]['id'], node[0]['id'], gridObject_dict):
                        last_id = get_last_id(elements)
                        return_temp = no_update
                        modal_boolean = False
                        start_object = gridObject_dict[start_of_line[0]['id']]
                        end_object = gridObject_dict[node[0]['id']]
                        if start_object['voltage'] is None and end_object[
                            'voltage'] is None:  # Check if voltage level of connection is defined through one of the components
                            return_temp = [start_object['id'], end_object['id']]
                            modal_boolean = True
                        new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'],
                                             'id': 'edge' + str(last_id[1] + 1), 'label': 'x'},
                                    'classes': 'line_style'}
                        gridObject_dict[new_edge['data']['id']] = objects.create_LineObject(new_edge['data']['id'], new_edge['data']['id'])
                        elements.append(new_edge)
                        return elements, gridObject_dict, None, no_update, no_update, return_temp, modal_boolean
                    else:
                        return elements, no_update, None, no_update, "notification_false_connection", no_update, no_update
                else:
                    return elements, no_update, node, no_update, no_update, no_update, no_update
            else:  # Node is clicked in normal mode
                raise PreventUpdate
        else:
            raise PreventUpdate
    elif triggered_id == 'edit_delete_button':  # Delete Object
        if btn_delete is not None:
            index = 0
            for ele in elements:
                if ele['data']['id'] == selected_element:
                    break
                index += 1
            if 'position' in elements[index]:  # Check if it is node
                connected_edges = get_connected_edges(elements, elements[index])
                for edge in connected_edges:
                    elements.pop(elements.index(edge))
            elements.pop(index)
            del gridObject_dict[selected_element]  # Remove element from grid object dict
            return elements, gridObject_dict, no_update, selected_element, no_update, no_update, no_update
        else:
            raise PreventUpdate
    elif triggered_id == 'example_button':
        ele, gridObject_dict = example_grids.simple_grid_timeseries_day(app, 96)
        return ele, gridObject_dict, no_update, no_update, no_update, no_update, no_update
    elif triggered_id == 'store_edge_labels':  # Set labels of edges with power values
        for edge, label in labels.items():
            for ele in elements:
                if edge == ele['data']['id']:
                    ele['data']['label'] = str(label)
                    break
        return elements, no_update, no_update, no_update, no_update, no_update, no_update
    elif triggered_id == 'button_voltage_hv':
        for node_id in node_ids:
            obj = gridObject_dict[node_id]
            if obj['object_type'] != "transformer":
                obj['voltage'] = 20000
        return no_update, gridObject_dict, no_update, no_update, no_update, no_update, False
    elif triggered_id == 'button_voltage_lv':
        for node_id in node_ids:
            obj = gridObject_dict[node_id]
            if obj['object_type'] != "transformer":
                obj['voltage'] = 400
        return no_update, gridObject_dict, no_update, no_update, no_update, no_update, False
    else:
        raise PreventUpdate


@app.callback(Output('store_menu_change_tab_grid', 'data'),
              Output('cyto1', 'tapNodeData'),
              Output('cyto1', 'tapEdgeData'),
              Output('store_selected_element_grid', 'data'),
              Output('store_notification3', 'data'),
              Input('cyto1', 'tapNodeData'),
              Input('cyto1', 'tapEdgeData'),
              # Input('edit_delete_button', 'n_clicks'),
              Input('edit_save_button', 'n_clicks'),
              Input('store_element_deleted', 'data'),
              State('store_grid_object_dict', 'data'),
              State('store_line_edit_active', 'data'))
def edit_grid_objects(node, edge, btn_save, element_deleted, gridObject_dict, btn_line_active):
    try:
        triggered_id = ctx.triggered_id
        triggered = ctx.triggered
        if triggered_id == 'cyto1':
            if triggered[0]['prop_id'] == 'cyto1.tapNodeData':   # Node was clicked
                if not btn_line_active:
                    return gridObject_dict[node['id']]['object_type'], None, None, node['id'], no_update   # Reset tapNodeData and tapEdgeData and return type of node for tab in menu
                else:
                    raise PreventUpdate
            elif triggered[0]['prop_id'] == 'cyto1.tapEdgeData':     # Edge was clicked
                return gridObject_dict[edge['id']]['object_type'], None, None, edge['id'], no_update   # Reset tapNodeData and tapEdgeData and return type of edge for tab in menu
            else:
                raise Exception("Weder Node noch Edge wurde geklickt.")
        elif triggered_id == 'edit_save_button':    # Save button was clicked in the menu
            raise PreventUpdate
        # elif triggered_id == 'edit_delete_button':  # Delete button was clicked in the menu
        #     raise PreventUpdate
        elif triggered_id == 'store_element_deleted':
            if element_deleted is not None:
                return 'empty', None, None, no_update, no_update
            else:
                return PreventUpdate
        else:
            raise PreventUpdate
    except PreventUpdate:
        return no_update, no_update, no_update, no_update, no_update
    except Exception as err:
        return no_update, no_update, no_update, no_update, err.args[0]


# @app.callback(Output('modal_edit', 'opened'),
#               Output('modal_text', 'children'),
#               Output('store_selected_element', 'data'),
#               Output('cyto1', 'tapNodeData'),
#               Output('cyto1', 'tapEdgeData'),
#               Output('power_input', 'value'),
#               Output('chips_type', 'value'),
#               Input('cyto1', 'tapNodeData'),
#               Input('cyto1', 'tapEdgeData'),
#               Input('modal_edit_close_button', 'n_clicks'),
#               Input('modal_edit_save_button', 'n_clicks'),
#               Input('element_deleted', 'data'),
#               State('store_selected_element', 'data'),
#               State('store_line_edit_active', 'data'),
#               State('cyto1', 'elements'),
#               State('chips_type', 'value'),
#               State('power_input', 'value'),
#               State('store_grid_object_dict', 'data'))
# def edit_grid_element(node, edge, btn_close, btn_save, element_deleted, selected_element,
#                       btn_line_active, elements, set_type, power_in, gridObject_dict):
#     triggered_id = ctx.triggered_id
#     if triggered_id == 'element_deleted':
#         if element_deleted:
#             return False, None, None, None, None, no_update, no_update
#         else:
#             raise PreventUpdate
#     elif triggered_id == 'cyto1':
#         if node is not None and edge is None:
#             if not btn_line_active:
#                 body_text = "Edit settings of " + node['id'] + " here."
#                 power = gridObject_dict[node['id']]['power']
#                 # power = get_object_from_id(node['id'], gridObject_list).power
#                 value = abs(power)
#                 if power < 0:
#                     chip = 'Einspeisung'
#                 else:
#                     chip = 'Last'
#                 return True, body_text, node['id'], None, None, value, chip
#             else:
#                 raise PreventUpdate
#         elif node is None and edge is not None:
#             if not btn_line_active:
#                 body_text = "Edit settings of " + edge['id'] + " here."
#                 return True, body_text, edge['id'], None, None, no_update, no_update
#             else:
#                 raise PreventUpdate
#         else:
#             return False, None, None, None, None, no_update, no_update
#     elif triggered_id == 'modal_edit_save_button':
#         if selected_element[:4] == "node":
#             if set_type == "Last":
#                 direction = 1
#             else:
#                 direction = -1
#             obj = get_object_from_id(selected_element, gridObject_list)
#             obj.power = direction * power_in
#             return False, no_update, None, no_update, no_update, no_update, no_update
#         elif selected_element[:4] == "edge":
#             raise PreventUpdate
#         else:
#             raise PreventUpdate
#     elif triggered_id == 'modal_edit_close_button':
#         return False, no_update, no_update, no_update, no_update, no_update, no_update
#     else:
#         raise PreventUpdate


@app.callback(Output('store_add_node', 'data'),
              [Input(object_id[0], 'n_clicks') for object_id in menu_objects],
              prevent_initial_call=True)
def button_add_pressed(*args):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        raise PreventUpdate
    else:
        return triggered_id


@app.callback(Output('store_flow_data', 'data'),
              Output('graph_image', 'style'),
              Output('graph_image', 'src'),
              Output('alert_externalgrid', 'children'),
              Output('alert_externalgrid', 'hide'),
              Output('tabs', 'value'),
              Output('cyto1', 'stylesheet'),
              Output('timestep_slider', 'max'),
              Output('store_edge_labels', 'data'),
              Output('store_notification2', 'data'),
              Input('button_calculate', 'n_clicks'),
              Input('timestep_slider', 'value'),
              State('store_flow_data', 'data'),
              State('cyto1', 'elements'),
              State('store_grid_object_dict', 'data'),
              prevent_initial_call=True)
def start_calculation(btn, slider, flow, elements, gridObject_dict):
    try:
        triggered_id = ctx.triggered_id
        if triggered_id == 'button_calculate':
            df_flow, labels, format_img_src = calculate_power_flow(elements, gridObject_dict)
            df_flow_json = df_flow.to_json(orient='index')
            img_src = 'data:image/png;base64,{}'.format(format_img_src)
            return df_flow_json, {'display': 'block'}, img_src, no_update, no_update, 'results', \
                   stylesheets.cyto_stylesheet_calculated, len(df_flow.index), labels, no_update
        elif triggered_id == 'timestep_slider':
            df_flow = pd.read_json(flow, orient='index')
            labels = df_flow.loc[slider - 1].to_dict()
            if df_flow.loc[slider - 1, 'external_grid'].item() > 0:
                text_alert = "Es werden " + str(
                    abs(df_flow.loc[slider - 1, 'external_grid'].item())) + " kW an das Netz abgegeben."
            else:
                text_alert = "Es werden " + str(
                    abs(df_flow.loc[slider - 1, 'external_grid'].item())) + " kW aus dem Netz bezogen."
            return no_update, no_update, no_update, text_alert, False, no_update, no_update, no_update, labels, no_update
        else:
            raise PreventUpdate
    except PreventUpdate:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
               no_update
    except Exception as err:
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
               err.args[0]


@app.callback(Output('modal_readme', 'opened'),
              Input('button_readme', 'n_clicks'),
              prevent_initial_call=True)
def open_readme(btn):
    return True


@app.callback(Output('notification_container', 'children'),
              Output('drawer_notifications', 'children'),
              Output('bade_notifications', 'children'),
              Input('store_notification1', 'data'),
              Input('store_notification2', 'data'),
              Input('store_notification3', 'data'),
              State('drawer_notifications', 'children'))
def notification(data1, data2, data3, notif_list):
    triggered_id = ctx.triggered_id
    if triggered_id == 'store_notification1':
        data = data1
    elif triggered_id == 'store_notification2':
        data = data2
    elif triggered_id == 'store_notification3':
        data = data3
    else:
        raise PreventUpdate
    if data is None:
        raise PreventUpdate
    elif data == 'notification_false_connection':
        notification_message = ["Kabelsalat!",
                                "Zwischen diesen beiden Komponenten kannst du keine Leitung ziehen."]
        icon = DashIconify(icon="mdi:connection")
        color = 'yellow'
    elif data == 'notification_isolates':
        notification_message = ["Kein Netz!", "Es gibt Knoten, die nicht mit dem Netz verbunden sind!"]
        icon = DashIconify(icon="material-symbols:group-work-outline")
        color = 'red'
    elif data == 'notification_emptygrid':
        notification_message = ["Blackout!", "Hier muss erst noch ein Netz gebaut werden!"]
        icon = DashIconify(icon="uil:desert")
        color = 'yellow'
    elif data == 'notification_cycles':
        notification_message = ["Achtung (kein) Baum!", "Das Netz beinhaltet parallele Leitungen oder Zyklen, "
                                                        "dies ist leider noch nicht unterstützt."]
        icon = DashIconify(icon="ph:tree")
        color = 'red'
    else:
        notification_message = ["Fehler!", data]
        icon = DashIconify(icon="material-symbols:warning-outline-rounded")
        color = 'red'
    notif_list.append(dmc.Alert(notification_message[1], title=notification_message[0], color=color,
                                withCloseButton=True))
    return dmc.Notification(title=notification_message[0],
                            message=notification_message[1],
                            action='show', color=color, autoClose=5000,
                            icon=icon, id='notification'), notif_list, len(notif_list)


@app.callback(Output('cyto_bathroom', 'elements'),
              Output('store_device_dict', 'data'),
              Output('menu_devices', 'style'),
              Output('menu_devices', 'opened'),
              Output('store_menu_change_tab_house', 'data'),
              Output('store_selected_element_house', 'data'),
              State('cyto_bathroom', 'elements'),
              State('store_device_dict', 'data'),
              Input('cyto_bathroom', 'tapNode'),
              Input('button_close_menu', 'n_clicks'),
              [Input(device[1], 'n_clicks') for device in dash_components.devices['bathroom']],
              prevent_initial_call=True)
def manage_devices_bathroom(elements, device_dict, node, btn_close, *btn_add):  # Callback to handle Bathroom action
    triggered_id = ctx.triggered_id
    if triggered_id == 'cyto_bathroom':
        if node['data']['id'] == 'plus':  # Open Menu with Devices to add
            position = elements[1]['position']
            return no_update, no_update, {"position": "relative", "top": position['y'], "left": position['x']}, True, no_update, no_update
        elif node['data']['id'][:6] == "socket":  # A socket was clicked, switch this one on/off
            for ele in elements:
                if ele['data']['id'] == node['data']['id']:
                    if ele['classes'] == 'socket_node_style_on':
                        ele['classes'] = 'socket_node_style_off'
                    else:
                        ele['classes'] = 'socket_node_style_on'
                    break
            return elements, no_update, no_update, no_update, no_update, node['data']['id']
        elif node['data']['id'][:6] == "device":
            return no_update, no_update, no_update, no_update, 'device_bathroom', node['data']['id']
        elif node['data']['id'][:4] == "lamp":
            return no_update, no_update, no_update, no_update, 'lamp', node['data']['id']
        else:
            raise PreventUpdate
    elif triggered_id[:10] == 'button_add':  # A button in the menu was clicked
        socket_id = "socket" + str((len(elements) - 2) / 3 + 1)[:1]  # Get ids of new elements
        device_id = "device" + str((len(elements) - 2) / 3 + 1)[:1]
        position = elements[1]['position']  # Get Position of plus-node
        new_position_plus = {'x': position['x'] + 40, 'y': position['y']}  # Calculate new position of plus-node
        new_socket = {'data': {'id': socket_id, 'parent': 'power_strip'}, 'position': position,  # Generate new socket
                      'classes': 'socket_node_style'}
        if len(elements) % 6 - 2 > 0:
            position_node = {'x': position['x'], 'y': position['y'] - 80}  # Get position of new device
        else:
            position_node = {'x': position['x'], 'y': position['y'] - 120}
        new_node = {'data': {'id': device_id}, 'classes': 'room_node_style', 'position': position_node,
                    # Generate new device
                    'style': {'background-image': ['/assets/Icons/icon_' + triggered_id[11:] + '.png']}}
        new_edge = {'data': {'source': socket_id, 'target': device_id}}  # Connect new device with new socket
        new_device = objects.create_DeviceObject(device_id)
        elements[1]['position'] = new_position_plus
        elements.append(new_socket)  # Append new nodes and edges to cytoscape elements
        elements.append(new_node)
        elements.append(new_edge)
        device_dict['house1'][device_id] = new_device
        return elements, device_dict, no_update, False, no_update, no_update  # Return elements and close menu
    elif triggered_id == 'button_close_menu':  # The button "close" of the menu was clicked, close the menu
        return no_update, no_update, False, no_update, no_update
    else:
        raise PreventUpdate


@app.callback(Output('menu_parent_tabs', 'children'),
              Output('menu_parent_tabs', 'value'),
              Input('store_menu_change_tab_house', 'data'),
              Input('store_menu_change_tab_grid', 'data'),
              Input('tabs_main', 'value'),
              State('menu_parent_tabs', 'children'),
              State('store_grid_object_dict', 'data'),
              State('store_device_dict', 'data'),
              State('store_selected_element_grid', 'data'),
              State('store_selected_element_house', 'data'),
              prevent_initial_call=True)
def manage_menu_containers(tab_value_house, tab_value_grid, tabs_main, menu_children, gridObject_dict, device_dict,
                           selected_element_grid, selected_element_house):
    triggered_id = ctx.triggered_id
    if triggered_id == 'tabs_main':
        return no_update, 'empty'
    elif triggered_id == 'store_menu_change_tab_house':   # If a device in the house was clicked, prepare the variables
        tab_value = tab_value_house
        selected_element = selected_element_house
        elements_dict = device_dict['house1']
    elif triggered_id == 'store_menu_change_tab_grid':  # If a device in the grid was clicked, prepare the variables
        tab_value = tab_value_grid
        selected_element = selected_element_grid
        elements_dict = gridObject_dict
    else:
        raise PreventUpdate
    while len(menu_children) > 1:
        menu_children.pop()
    new_tab_panel = dash_components.add_menu_tab_panel(tab_value, selected_element, elements_dict)
    return menu_children + [new_tab_panel], tab_value


@app.callback(Output("power_input", "icon"),
              Input("chips_type", "value"),
              prevent_initial_call=True)
def chips_type(value):
    if value == "Last":
        return DashIconify(icon="material-symbols:download")
    elif value == "Einspeisung":
        return DashIconify(icon="material-symbols:upload")
    else:
        raise PreventUpdate


@app.callback(Output('cyto1', 'layout'),
              Output('example_button', 'disabled'),
              Input('example_button', 'n_clicks'),
              prevent_initial_call=True)
def activate_example(btn):
    time.sleep(0.25)
    return {'name': 'cose'}, True


@app.callback(Output('drawer_notifications', 'opened'),
              Input('button_notifications', 'n_clicks'))
def open_drawer_notifications(btn):
    if btn is not None:
        return True
    else:
        raise PreventUpdate


@app.callback(Output('card_start', 'style'),
              Output('card_menu', 'style'),
              Input('button_start', 'n_clicks'))
def open_menu_card(btn):
    if btn is not None:
        return {'display': 'none'}, {'display': 'block'}
    else:
        raise PreventUpdate


# @app.callback(Output('store_menu_change_tab', 'data'),
#               Input('debug_button', 'n_clicks'),
#               State('menu_parent_tabs', 'children'),
#               prevent_initial_call=True)
# def debug(btn, children):
#     tab_id = str(random.randrange(1000))
#     return 'tab1'


if __name__ == '__main__':
    app.run_server(debug=True)
