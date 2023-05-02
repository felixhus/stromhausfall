import datetime

import pandas as pd
from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

import source.objects as objects
import source.stylesheets as stylesheets
from source.layout import menu_objects
from source.modules import (calculate_power_flow, connection_allowed,
                            generate_grid_object, get_connected_edges,
                            get_icon_url, get_last_id,
                            get_monday_sunday_from_week)

# Button Ids, azimuth angles, Icons and rotations for Compass buttons PV
compass_buttons = {'button_north': 0,
                   'button_north_east': 45,
                   'button_east': 90,
                   'button_south_east': 135,
                   'button_south': 180,
                   'button_south_west': 225,
                   'button_west': 270,
                   'button_north_west': 315}

weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def grid_callbacks(app):
    @app.callback(Output('store_flow_data', 'data'),
                  Output('tabs_menu', 'value'),
                  Output('cyto1', 'stylesheet'),
                  Output('cyto1', 'elements', allow_duplicate=True),
                  Output('timestep_slider', 'max'),
                  Output('store_edge_labels', 'data'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_calculate', 'n_clicks'),
                  State('store_flow_data', 'data'),
                  State('cyto1', 'elements'),
                  State('store_grid_object_dict', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def start_calculation_grid(btn, flow, elements, gridObject_dict, tabs_main):
        try:
            if tabs_main == 'grid':
                df_flow, labels, elements = calculate_power_flow(elements, gridObject_dict)
                labels = {k: round(v, 1) for k, v in labels.items()}  # Round numbers for better display
                df_flow_json = df_flow.to_json(orient='index')
                return df_flow_json, 'results', \
                       stylesheets.cyto_stylesheet_calculated, elements, len(df_flow.index), labels, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('alert_externalgrid', 'children'),
                  Output('alert_externalgrid', 'hide'),
                  Output('store_edge_labels', 'data', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('timestep_slider', 'value'),
                  State('store_flow_data', 'data'),
                  prevent_initial_call=True)
    def update_labels(slider, flow):
        try:
            if flow is not None:
                df_flow = pd.read_json(flow, orient='index')
                labels = df_flow.loc[slider - 1].to_dict()
                labels = {k: round(v, 1) for k, v in labels.items()}  # Round numbers for better display
                external_grid_value = df_flow.loc[slider - 1, 'external_grid'].item()
                external_grid_value = round(external_grid_value, 1)
                if external_grid_value > 0:
                    text_alert = "Es werden " + str(abs(external_grid_value)) + " W an das Netz abgegeben."
                else:
                    text_alert = "Es werden " + str(abs(external_grid_value)) + " W aus dem Netz bezogen."
                return text_alert, False, labels, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, err.args[0]

    @app.callback(Output('cyto1', 'elements'),  # Callback to change elements of cyto
                  Output('store_grid_object_dict', 'data'),
                  Output('start_of_line', 'data'),
                  Output('store_element_deleted', 'data'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Output('store_get_voltage', 'data'),
                  Output('modal_voltage', 'opened'),
                  Input('store_add_node', 'data'),
                  Input('cyto1', 'selectedNodeData'),
                  Input('edit_delete_button', 'n_clicks'),
                  Input('button_line', 'n_clicks'),
                  Input('button_voltage_hv', 'n_clicks'),
                  Input('button_voltage_lv', 'n_clicks'),
                  State('cyto1', 'elements'),
                  State('store_grid_object_dict', 'data'),
                  State('store_line_edit_active', 'data'),
                  State('start_of_line', 'data'),
                  State('store_selected_element_grid', 'data'),
                  State('store_get_voltage', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def edit_grid(btn_add, node, btn_delete, btn_line, button_hv, button_lv, elements,
                  gridObject_dict, btn_line_active, start_of_line, selected_element, node_ids, tabs_main):
        triggered_id = ctx.triggered_id
        if triggered_id == 'button_line':  # Start line edit mode, set 'start_of_line' as None
            return no_update, no_update, None, no_update, no_update, no_update, no_update
        elif triggered_id == 'store_add_node':
            last_id = get_last_id(elements)
            new_gridobject = generate_grid_object(btn_add, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
            if new_gridobject['icon'].endswith('.png'):     # If a png picture is given as the logo
                image_src = app.get_asset_url('Icons/' + new_gridobject['icon'])
            else:   # If a dash iconify icon is given
                image_src = get_icon_url(new_gridobject['icon'])
            gridObject_dict[new_gridobject['id']] = new_gridobject
            new_element = {'data': {'id': 'node' + str(last_id[0] + 1)},
                           'position': {'x': 50 + last_id[0] * 8, 'y': 50 + last_id[0] * 8}, 'classes': 'node_style',
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
                                                 'id': 'edge' + str(last_id[1] + 1), 'label': ''},
                                        'classes': 'line_style_new'}
                            gridObject_dict[new_edge['data']['id']] = objects.create_LineObject(new_edge['data']['id'],
                                                                                                new_edge['data']['id'])
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
            if tabs_main == 'grid':  # Check if it was clicked in grid mode
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
            else:
                raise PreventUpdate  # Button was clicked in other mode than grid
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

    @app.callback(Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_menu_change_tab_grid', 'data'),
                  Output('cyto1', 'tapNodeData'),
                  Output('cyto1', 'tapEdgeData'),
                  Output('store_selected_element_grid', 'data'),
                  Output('tabs_main', 'value', allow_duplicate=True),
                  Output('house_fade', 'is_in'),
                  Output('store_custom_house', 'data'),
                  Output('tab_house', 'disabled'),
                  Output('house_mode', 'value'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('cyto1', 'tapNodeData'),
                  Input('cyto1', 'tapEdgeData'),
                  Input('edit_save_button', 'n_clicks'),
                  Input('store_element_deleted', 'data'),
                  Input('house_mode', 'value'),
                  State('store_selected_element_grid', 'data'),
                  State('store_grid_object_dict', 'data'),
                  State('store_line_edit_active', 'data'),
                  State('tabs_main', 'value'),
                  State('store_custom_house', 'data'),
                  prevent_initial_call=True)
    def edit_grid_objects(node, edge, btn_save, element_deleted, control, selected_element,
                          gridObject_dict, btn_line_active, tabs_main, custom_house):
        try:
            triggered_id = ctx.triggered_id
            triggered = ctx.triggered
            if triggered_id == 'cyto1':
                if triggered[0]['prop_id'] == 'cyto1.tapNodeData':  # Node was clicked
                    if not btn_line_active:
                        return no_update, gridObject_dict[node['id']]['object_type'], None, None, node['id'], \
                               no_update, no_update, no_update, no_update, no_update, no_update  # Reset tapNodeData and tapEdgeData and return type of node for tab in menu
                    else:
                        raise PreventUpdate
                elif triggered[0]['prop_id'] == 'cyto1.tapEdgeData':  # Edge was clicked
                    return no_update, gridObject_dict[edge['id']]['object_type'], None, None, edge['id'], \
                           no_update, no_update, no_update, no_update, no_update, no_update  # Reset tapNodeData and tapEdgeData and return type of edge for tab in menu
                else:
                    raise Exception("Weder Node noch Edge wurde geklickt.")
            elif triggered_id == 'house_mode':  # New mode of house configuration was clicked (segmented control)
                if custom_house is None:  # If no house is in custom-mode yet
                    if control == 'preset':
                        gridObject_dict[selected_element]['config_mode'] = 'preset'
                        return gridObject_dict, no_update, no_update, no_update, no_update, no_update, True, no_update, no_update, no_update, no_update
                    elif control == 'custom':
                        gridObject_dict[selected_element]['config_mode'] = 'custom'
                        return gridObject_dict, no_update, no_update, no_update, no_update, 'house1', False, selected_element, False, no_update, no_update
                    else:
                        raise PreventUpdate
                elif custom_house == selected_element:
                    if control == 'preset':
                        gridObject_dict[selected_element]['config_mode'] = 'preset'
                        return gridObject_dict, no_update, no_update, no_update, no_update, no_update, True, None, True, no_update, no_update
                    else:
                        raise PreventUpdate
                else:
                    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                           no_update, 'preset', 'notification_custom_house'
            elif triggered_id == 'edit_save_button':  # Save button was clicked in the menu
                if tabs_main != 'grid' or btn_save is None:  # If it was clicked in house mode or is None do nothing
                    raise PreventUpdate
                raise PreventUpdate
            elif triggered_id == 'store_element_deleted':
                if element_deleted is not None:
                    return no_update, 'empty', None, None, no_update, no_update, no_update, no_update, no_update, no_update, no_update
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   err.args[0]

    @app.callback(Output('cyto1', 'elements', allow_duplicate=True),
                  Input('store_edge_labels', 'data'),
                  State('cyto1', 'elements'),
                  prevent_initial_call=True)
    def edge_labels(labels, elements):
        for edge, label in labels.items():  # Set labels of edges with power values
            reverse = label < 0  # If power over edge is negative -> Reverse
            for ele in elements:
                if edge == ele['data']['id']:
                    ele['data']['label'] = str(abs(label))  # Set absolute value of power as label
                    if reverse:
                        ele['classes'] = 'line_style_reverse'
                    else:
                        ele['classes'] = 'line_style'
                    break
        return elements

    @app.callback(Output('alert_time', 'children'),
                  Output('alert_time', 'hide'),
                  Input('timestep_slider', 'value'),
                  State('input_year', 'value'),
                  State('input_week', 'value'),
                  prevent_initial_call=True)
    def time_slider(slider, year, week):
        date_start, date_stop = get_monday_sunday_from_week(week, year)
        time_start = datetime.datetime.combine(date_start, datetime.datetime.min.time())
        slider_time = time_start + datetime.timedelta(minutes=slider)
        text = slider_time.strftime(f"Am {weekdays[slider_time.weekday()]} %d.%m. um %H:%M")
        return text, False

    @app.callback(Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('button_compass', 'style'),
                  State('store_grid_object_dict', 'data'),
                  State('store_selected_element_grid', 'data'),
                  [Input(button, 'n_clicks') for button in compass_buttons.keys()],
                  prevent_initial_call=True)
    def compass_action(gridObject_dict, selected_element, *args):
        triggered_id = ctx.triggered_id
        if all(ele is None for ele in args):  # If no button was clicked
            raise PreventUpdate
        gridObject_dict[selected_element]['orientation'] = compass_buttons[triggered_id]
        style = {'transform': f'rotate({compass_buttons[triggered_id] - 45}deg)'}
        # icon = DashIconify(icon=compass_buttons[triggered_id][1], width=20, rotate=compass_buttons[triggered_id][2])
        return gridObject_dict, style

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

    @app.callback(Output('cyto1', 'elements', allow_duplicate=True),
                  Input('store_custom_house', 'data'),
                  State('cyto1', 'elements'),
                  prevent_initial_call=True)
    def custom_house_style(selected_element, elements):
        if selected_element is not None:
            for ele in elements:
                if ele['data']['id'] == selected_element:
                    ele['classes'] = 'node_style_custom'
                    break
            return elements
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
