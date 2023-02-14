import os
import time

import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import dash_daq as daq
import dash_mantine_components as dmc
import example_grids
# import modules
import plotly.express as px
from dash import Dash, Input, Output, State, ctx, dcc, html, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.example_grids
import source.stylesheets as stylesheets
from source.modules import (calculate_power_flow, connection_allowed,
                            generate_grid_object, get_connected_edges,
                            get_last_id, get_object_from_id)

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
gridObject_list = []

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
            dbc.Col([
                dash_components.add_cytoscape_grid(nodes, edges),
            ], width=7),
            dbc.Col([dash_components.card_start(), dash_components.card_menu()], width=True)
        ]),
        dash_components.add_modal_edit(),
        dash_components.add_modal_readme(),
        dash_components.add_drawer_notifications(),
        dash_components.add_modal_voltage_level(),
        dash_components.add_storage_variables(),
        html.P(id='dummy')], width=True),
    html.Div(id='notification_container')
], id='main_container'))


@app.callback(Output('cyto1', 'autoungrabify'),  # Callback to make Node ungrabbable when adding lines
              Output('line_edit_active', 'data'),
              Output('button_line', 'variant'),
              Input('button_line', 'n_clicks'),
              State('line_edit_active', 'data'),
              prevent_initial_call=True)
def edit_mode(btn_line, btn_active):
    if not btn_active:
        return True, True, 'light'
    else:
        return False, False, 'filled'


@app.callback(Output('cyto1', 'elements'),  # Callback to change elements of cyto
              Output('start_of_line', 'data'),
              Output('element_deleted', 'data'),
              Output('store_notification1', 'data'),
              Output('store_get_voltage', 'data'),
              Input('store_add_node', 'data'),
              Input('cyto1', 'selectedNodeData'),
              Input('modal_edit_delete_button', 'n_clicks'),
              Input('button_line', 'n_clicks'),
              Input('example_button', 'n_clicks'),
              Input('store_edge_labels', 'data'),
              State('cyto1', 'elements'),
              State('line_edit_active', 'data'),
              State('start_of_line', 'data'),
              State('selected_element', 'data'))
def edit_grid(btn_add, node, btn_delete, btn_line, btn_example, elements,
              btn_line_active, start_of_line, selected_element, labels):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        return elements, None, False, None, no_update
    elif triggered_id == 'store_add_node':
        last_id = get_last_id(elements)
        new_gridobject = generate_grid_object(btn_add, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
        image_src = app.get_asset_url('Icons/' + new_gridobject.icon)
        gridObject_list.append(new_gridobject)
        new_element = {'data': {'id': 'node' + str(last_id[0] + 1)},
                       'position': {'x': 50, 'y': 50}, 'classes': 'node_style',
                       'style': {'background-image': image_src, 'background-color': new_gridobject.ui_color}}
        elements.append(new_element)
        return elements, None, False, None, no_update
    elif triggered_id == 'cyto1':  # # Node was clicked
        if not node == []:
            if btn_line_active:  # Add-line-mode is on
                if start_of_line is not None:
                    if connection_allowed(start_of_line[0]['id'], node[0]['id'], gridObject_list):
                        last_id = get_last_id(elements)
                        return_temp = no_update
                        start_object = get_object_from_id(start_of_line[0]['id'], gridObject_list)
                        end_object = get_object_from_id(node[0]['id'], gridObject_list)
                        if start_object.voltage is None and end_object.voltage is None:  # Check if voltage level of connection is defined through one of the components
                            return_temp = [start_object.id, end_object.id]
                        new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'],
                                             'id': 'edge' + str(last_id[1] + 1), 'label': '42'}, 'classes': 'line_style'}
                        elements.append(new_edge)
                        return elements, None, False, None, return_temp
                    else:
                        return elements, None, False, "notification_false_connection", no_update
                else:
                    return elements, node, False, None, no_update
            else:  # Node is clicked in normal mode
                raise PreventUpdate
        else:
            raise PreventUpdate
    elif triggered_id == 'modal_edit_delete_button':  # Delete Object
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
        index = 0
        for obj in gridObject_list:  # Remove element from grid object list
            if obj.id == selected_element:
                break
            index += 1
        gridObject_list.pop(index)
        return elements, None, True, None, no_update
    elif triggered_id == 'example_button':
        ele, temp = example_grids.simple_grid(app)
        for element in temp:
            gridObject_list.append(element)
        return ele, no_update, no_update, no_update, no_update
    elif triggered_id == 'store_add_labels':    # Set labels of edges with power values
        return no_update, no_update, no_update, no_update, no_update
    else:
        raise PreventUpdate


@app.callback(Output('modal_edit', 'opened'),
              Output('modal_text', 'children'),
              Output('selected_element', 'data'),
              Output('cyto1', 'tapNodeData'),
              Output('cyto1', 'tapEdgeData'),
              Output('power_input', 'value'),
              Output('chips_type', 'value'),
              Input('cyto1', 'tapNodeData'),
              Input('cyto1', 'tapEdgeData'),
              Input('modal_edit_close_button', 'n_clicks'),
              Input('modal_edit_save_button', 'n_clicks'),
              Input('element_deleted', 'data'),
              State('selected_element', 'data'),
              State('line_edit_active', 'data'),
              State('cyto1', 'elements'),
              State('chips_type', 'value'),
              State('power_input', 'value'))
def edit_grid_element(node, edge, btn_close, btn_save, element_deleted, selected_element,
                      btn_line_active, elements, set_type, power_in):
    triggered_id = ctx.triggered_id
    if triggered_id == 'element_deleted':
        if element_deleted:
            return False, None, None, None, None, no_update, no_update
        else:
            raise PreventUpdate
    elif triggered_id == 'cyto1':
        if node is not None and edge is None:
            if not btn_line_active:
                body_text = "Edit settings of " + node['id'] + " here."
                power = get_object_from_id(node['id'], gridObject_list).power
                value = abs(power)
                if power < 0:
                    chip = 'Einspeisung'
                else:
                    chip = 'Last'
                return True, body_text, node['id'], None, None, value, chip
            else:
                raise PreventUpdate
        elif node is None and edge is not None:
            if not btn_line_active:
                body_text = "Edit settings of " + edge['id'] + " here."
                return True, body_text, edge['id'], None, None, no_update, no_update
            else:
                raise PreventUpdate
        else:
            return False, None, None, None, None, no_update, no_update
    elif triggered_id == 'modal_edit_save_button':
        if selected_element[:4] == "node":
            if set_type == "Last":
                direction = 1
            else:
                direction = -1
            obj = get_object_from_id(selected_element, gridObject_list)
            obj.power = direction * power_in
            return False, no_update, None, no_update, no_update, no_update, no_update
        elif selected_element[:4] == "edge":
            raise PreventUpdate
        else:
            raise PreventUpdate
    elif triggered_id == 'modal_edit_close_button':
        return False, no_update, no_update, no_update, no_update, no_update, no_update
    else:
        raise PreventUpdate


@app.callback(Output('store_add_node', 'data'),
              [Input(object_id[0], 'n_clicks') for object_id in menu_objects],
              prevent_initial_call=True)
def button_add_pressed(*args):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_line':
        raise PreventUpdate
    else:
        return triggered_id


@app.callback(Output('graph_image', 'style'),
              Output('graph_image', 'src'),
              Output('alert_externalgrid', 'children'),
              Output('alert_externalgrid', 'hide'),
              Output('tabs', 'value'),
              Output('cyto1', 'stylesheet'),
              Output('store_notification2', 'data'),
              Input('button_calculate', 'n_clicks'),
              State('cyto1', 'elements'),
              prevent_initial_call=True)
def start_calculation(btn, elements):
    try:
        if btn is not None:
            flow, format_img_src = calculate_power_flow(elements, gridObject_list)
            time.sleep(4)
            img_src = 'data:image/png;base64,{}'.format(format_img_src)
            if flow.loc['step1', 'external_grid'].item() > 0:
                text_alert = "Es werden " + str(abs(flow.loc['step1', 'external_grid'].item())) + " kW an das Netz abgegeben."
            else:
                text_alert = "Es werden " + str(abs(flow.loc['step1', 'external_grid'].item())) + " kW aus dem Netz bezogen."
            return {'display': 'block'}, img_src, text_alert, False, 'results', stylesheets.cyto_stylesheet_calculated, no_update
        else:
            raise PreventUpdate
    except Exception as err:
        return no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]


@app.callback(Output('modal_readme', 'opened'),
              Input('button_readme', 'n_clicks'),
              prevent_initial_call=True)
def open_readme(btn):
    return True


@app.callback(Output('modal_voltage', 'opened'),
              Input('store_get_voltage', 'data'),
              Input('button_voltage_hv', 'n_clicks'),
              Input('button_voltage_lv', 'n_clicks'),
              State('cyto1', 'elements'),
              prevent_initial_call=True
              )
def modal_voltage(node_ids, button_hv, button_lv, elements):
    triggered_id = ctx.triggered_id
    if triggered_id == 'store_get_voltage':
        if node_ids is None:
            raise PreventUpdate
        return True
    elif triggered_id == 'button_voltage_hv':
        print("Oberspannung")
        for node_id in node_ids:
            obj = get_object_from_id(node_id, gridObject_list)
            if obj.object_type != "transformer":
                obj.voltage = 20000
        return False
    elif triggered_id == 'button_voltage_lv':
        print("Unterspannung")
        for node_id in node_ids:
            obj = get_object_from_id(node_id, gridObject_list)
            if obj.object_type != "transformer":
                obj.voltage = 400
        return False
    else:
        raise PreventUpdate


@app.callback(Output('notification_container', 'children'),
              Output('drawer_notifications', 'children'),
              Output('bade_notifications', 'children'),
              Input('store_notification1', 'data'),
              Input('store_notification2', 'data'),
              State('drawer_notifications', 'children'))
def notification(data1, data2, notif_list):
    triggered_id = ctx.triggered_id
    if triggered_id == 'store_notification1':
        data = data1
    elif triggered_id == 'store_notification2':
        data = data2
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
    time.sleep(0.1)
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
def open_drawer_notifications(btn):
    if btn is not None:
        return {'display': 'none'}, {'display': 'block'}
    else:
        raise PreventUpdate


@app.callback(Output('dummy', 'children'),
              Input('debug_button', 'n_clicks'),
              State('cyto1', 'elements'),
              State('start_of_line', 'data'),
              prevent_initial_call=True)
def debug(btn, elements, start_of_line):
    calculate_power_flow(elements, gridObject_list)
    return None


if __name__ == '__main__':
    app.run_server(debug=True)
