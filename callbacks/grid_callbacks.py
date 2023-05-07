"""
grid_callbacks.py contains all dash callbacks for grid functions of the app.
"""

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

root_path = '/home/stromhausfall/mysite/'

# Button Ids and rotations for compass buttons PV
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
                  Output('result_parent_tabs', 'value', allow_duplicate=True),
                  Output('cyto_grid', 'stylesheet'),
                  Output('cyto_grid', 'elements', allow_duplicate=True),
                  Output('timestep_slider', 'max'),
                  Output('store_edge_labels', 'data'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_calculate', 'n_clicks'),
                  State('cyto_grid', 'elements'),
                  State('store_grid_object_dict', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def start_calculation_grid(btn, elements, gridObject_dict, tabs_main):
        """
        Starts the calculation of the grid and calls all necessary functions.
        :param btn: [Input] Button to start calculation
        :param elements: [State] Elements of grid cytoscape
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
        :return: [store_flow_data>data, tabs_menu>value, result_parent_tabs>value, cyto_grid>stylesheet,
        cyto_grid>elements, timestep_slider>max, store_edge_labels>data, store_notification>data]
        """

        try:
            if tabs_main == 'grid':     # If button was clicked in grid mode, start calculation
                df_flow, labels = calculate_power_flow(elements, gridObject_dict)
                # Create labels for cytoscape edges/electrical lines and round numbers for better display
                labels = {k: round(v, 1) for k, v in labels.items()}
                # Convert to json to store in dcc store object
                df_flow_json = df_flow.to_json(orient='index')
                # Return calculation results and show 'result' tab. Activate edge labels by stylesheet
                return df_flow_json, 'results', 'grid', \
                       stylesheets.cyto_stylesheet_calculated, elements, len(df_flow.index), labels, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('alert_externalgrid', 'children'),
                  Output('store_edge_labels', 'data', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('timestep_slider', 'value'),
                  State('store_flow_data', 'data'),
                  prevent_initial_call=True)
    def update_labels(slider, flow):
        """
        If flow was calculated and the slider set to a new timestep, this function generates the cytoscape edge labels
        for this timestep from the flow results. It rounds them and get the power, which is taken or given to the
        external grid. This is then shown on the alert components in the grid result section.
        :param slider: [Input] Timestep set by slider
        :param flow: [State] The calculated flow data
        :return: [alert_externalgrid>children, store_edge_labels>data, store_notification>data]
        """

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
                return text_alert, labels, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, err.args[0]

    @app.callback(Output('cyto_grid', 'elements'),
                  Output('store_grid_object_dict', 'data'),
                  Output('start_of_line', 'data'),
                  Output('store_element_deleted', 'data'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Output('store_get_voltage', 'data'),
                  Output('modal_voltage', 'opened'),
                  Input('store_add_node', 'data'),
                  Input('cyto_grid', 'selectedNodeData'),
                  Input('edit_delete_button', 'n_clicks'),
                  Input('button_line', 'n_clicks'),
                  Input('button_voltage_hv', 'n_clicks'),
                  Input('button_voltage_lv', 'n_clicks'),
                  State('cyto_grid', 'elements'),
                  State('store_grid_object_dict', 'data'),
                  State('store_line_edit_active', 'data'),
                  State('start_of_line', 'data'),
                  State('store_selected_element_grid', 'data'),
                  State('store_get_voltage', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def edit_grid(btn_add, node, btn_delete, btn_line, button_hv, button_lv, elements,
                  gridObject_dict, btn_line_active, start_of_line, selected_element, node_ids, tabs_main):
        """
        This callback manages all the edit action of the grid cytoscape. It adds new nodes and lines and
        deletes them if wanted.
        :param btn_add: [Input] Id of pressed add object button
        :param node: [Input] Pressed node of cyto_grid
        :param btn_delete: [Input] Button to delete an object
        :param btn_line: [Input] Button to activate line edit mode
        :param button_hv: [Input] Button to select the high voltage side of the transformer
        :param button_lv: [Input] Button to select the low voltage side of the transformer
        :param elements: [State] Elements of grid cytoscape
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param btn_line_active: [State] Status of the line edit mode
        :param start_of_line: [State] First clicked node to add a line
        :param selected_element: [State] Selected element of the cyto_grid
        :param node_ids: [State] Two node ids of nodes to connect, but voltage has to be set
        :param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
        :return: [cyto_grid>elements, store_grid_object_dict>data, start_of_line>data, store_element_deleted>data,
        store_notification>data, store_get_voltage>data, modal_voltage>opened]
        """

        triggered_id = ctx.triggered_id
        if triggered_id == 'store_add_node':    # A button to add a grid object was clicked
            last_id = get_last_id(elements)     # Get last used id
            new_gridobject = generate_grid_object(btn_add, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
            if new_gridobject['icon'].endswith('.png'):     # If a png picture is given as the logo
                image_src = app.get_asset_url('Icons/' + new_gridobject['icon'])
            else:   # If a dash iconify icon is given
                image_src = get_icon_url(new_gridobject['icon'])
            # Add new object to grid object dictionary
            gridObject_dict[new_gridobject['id']] = new_gridobject
            # Create new cytoscape node with the necessary content
            new_node = {'data': {'id': 'node' + str(last_id[0] + 1)},
                        'position': {'x': 50 + last_id[0] * 8, 'y': 50 + last_id[0] * 8}, 'classes': 'node_style',
                        'style': {'background-image': image_src, 'background-color': new_gridobject['ui_color']}}
            elements.append(new_node)
            return elements, gridObject_dict, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'button_line':  # Start line edit mode, set 'start_of_line' as None
            return no_update, no_update, None, no_update, no_update, no_update, no_update
        elif triggered_id == 'cyto_grid':  # Node was clicked
            if not node == []:
                if btn_line_active:  # Add-line-mode is on
                    if start_of_line is not None:   # If the start of the line already is set
                        # Check if connection is allowed
                        if connection_allowed(start_of_line[0]['id'], node[0]['id'], gridObject_dict):
                            last_id = get_last_id(elements)     # Get last edge id
                            return_temp = no_update             # Temporary variable
                            modal_boolean = False               # Boolean if voltage modal has to be shown
                            start_object = gridObject_dict[start_of_line[0]['id']]
                            end_object = gridObject_dict[node[0]['id']]
                            # Check if voltage level of connection is defined through one of the components
                            if start_object['voltage'] is None and end_object['voltage'] is None:
                                return_temp = [start_object['id'], end_object['id']]    # Pass ids to voltage modal
                                modal_boolean = True    # Set boolean to show voltage modal
                            elif start_object['voltage'] is None and start_object['object_type'] != 'transformer':
                                start_object['voltage'] = end_object['voltage']
                            elif end_object['voltage'] is None and end_object['object_type'] != 'transformer':
                                end_object['voltage'] = start_object['voltage']
                            # Create new cytoscape edge with necessary content
                            new_edge = {'data': {'source': start_of_line[0]['id'], 'target': node[0]['id'],
                                                 'id': 'edge' + str(last_id[1] + 1), 'label': ''},
                                        'classes': 'line_style_new'}
                            gridObject_dict[new_edge['data']['id']] = objects.create_LineObject(new_edge['data']['id'],
                                                                                                new_edge['data']['id'])
                            elements.append(new_edge)
                            return elements, gridObject_dict, None, no_update, no_update, return_temp, modal_boolean
                        else:
                            # If the connection is not allowed, abort line adding and show notification
                            return elements, no_update, None, no_update, "notification_false_connection", \
                                   no_update, no_update
                    else:
                        # If no start node is selected yet, store the now selected as the start node
                        return elements, no_update, node, no_update, no_update, no_update, no_update
                else:  # Node is clicked in normal mode, do nothing
                    raise PreventUpdate
            else:
                raise PreventUpdate
        elif triggered_id == 'button_voltage_hv':   # The high voltage side was selected in the voltage modal
            for node_id in node_ids:                # Find nodes in gridObject_dict and set the selected voltage
                obj = gridObject_dict[node_id]
                if obj['object_type'] != "transformer":
                    obj['voltage'] = 20000
            return no_update, gridObject_dict, no_update, no_update, no_update, no_update, False
        elif triggered_id == 'button_voltage_lv':   # The low voltage side was selected in the voltage modal
            for node_id in node_ids:                # Find nodes in gridObject_dict and set the selected voltage
                obj = gridObject_dict[node_id]
                if obj['object_type'] != "transformer":
                    obj['voltage'] = 400
            return no_update, gridObject_dict, no_update, no_update, no_update, no_update, False
        elif triggered_id == 'edit_delete_button':  # Delete Object
            if tabs_main == 'grid':  # Check if it was clicked in grid mode
                if btn_delete is not None:
                    index = 0
                    for ele in elements:        # Find element to delete
                        if ele['data']['id'] == selected_element:
                            break
                        index += 1
                    if 'position' in elements[index]:  # Check if it is node
                        # Find connected edges of the node
                        connected_edges = get_connected_edges(elements, elements[index])
                        for edge in connected_edges:    # And delete them as well
                            elements.pop(elements.index(edge))
                    # TODO: Also delete connected edges from the grid object dictionary!
                    elements.pop(index)                    # Delete selected element from cytoscape
                    del gridObject_dict[selected_element]  # Remove element from grid object dict
                    return elements, gridObject_dict, no_update, selected_element, no_update, no_update, no_update
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate  # Button was clicked in other mode than grid, do nothing
        else:
            raise PreventUpdate

    @app.callback(Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_menu_change_tab_grid', 'data'),
                  Output('cyto_grid', 'tapNodeData'),
                  Output('cyto_grid', 'tapEdgeData'),
                  Output('store_selected_element_grid', 'data'),
                  Output('tabs_main', 'value', allow_duplicate=True),
                  Output('house_fade', 'is_in'),
                  Output('store_custom_house', 'data'),
                  Output('tab_house', 'disabled'),
                  Output('house_mode', 'value'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('cyto_grid', 'tapNodeData'),
                  Input('cyto_grid', 'tapEdgeData'),
                  Input('store_element_deleted', 'data'),
                  Input('house_mode', 'value'),
                  State('store_selected_element_grid', 'data'),
                  State('store_grid_object_dict', 'data'),
                  State('store_line_edit_active', 'data'),
                  State('store_custom_house', 'data'),
                  prevent_initial_call=True)
    def edit_grid_objects(node, edge, element_deleted, control, selected_element,
                          gridObject_dict, btn_line_active, custom_house):
        """
        Callback which controls what happens when nodes or edges in the grid are clicked. Also, this callback handles
        the selection of the house mode (preset or custom). If an element is deleted, it closes the connected tab.
        :param node: [Input] Clicked node of cytoscape
        :param edge: [Input] Clicked edge of cytoscape
        :param element_deleted: [Input] Id of the element which was deleted
        :param control: [Input] Segmented control if house mode is preset or custom
        :param selected_element: [State] Selected element of the cyto_grid
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param btn_line_active: [State] Status of the line edit mode
        :param custom_house: [State] Id of custom configured house
        :return: [store_grid_object_dict>data, store_menu_change_tab_grid>data, cyto_grid>tapNodeData,
        cyto_grid>tapEdgeData, store_selected_element_grid>data, tabs_main>value, house_fade>is_in,
        store_custom_house>data, tab_house>disabled, house_mode>value, store_notification>data]
        """

        try:
            triggered_id = ctx.triggered_id
            triggered = ctx.triggered   # Get which property triggered
            if triggered_id == 'cyto_grid':
                if triggered[0]['prop_id'] == 'cyto_grid.tapNodeData':  # Node was clicked
                    if not btn_line_active:     # If button edit mode is not active
                        # Reset tapNodeData and tapEdgeData and return type of node for tab in menu
                        return no_update, gridObject_dict[node['id']]['object_type'], None, None, node['id'], \
                               no_update, no_update, no_update, no_update, no_update, no_update
                    else:
                        raise PreventUpdate
                elif triggered[0]['prop_id'] == 'cyto_grid.tapEdgeData':  # Edge was clicked
                    if not btn_line_active:  # If button edit mode is not active
                        # Reset tapNodeData and tapEdgeData and return type of edge for tab in menu
                        return no_update, gridObject_dict[edge['id']]['object_type'], None, None, edge['id'], \
                               no_update, no_update, no_update, no_update, no_update, no_update
                    else:
                        raise PreventUpdate
                else:
                    raise Exception("Weder Node noch Edge wurde geklickt.")
            elif triggered_id == 'house_mode':  # New mode of house configuration was clicked (segmented control)
                if triggered[0]['value'] is None:   # If value of segmented control is none, do nothing
                    raise PreventUpdate
                if custom_house is None:  # If no house is in custom-mode yet
                    if control == 'preset':
                        # Set config mode, set fade to True (checkbox is visible)
                        gridObject_dict[selected_element]['config_mode'] = 'preset'
                        return gridObject_dict, no_update, no_update, no_update, no_update, no_update, True, \
                               no_update, no_update, no_update, no_update
                    elif control == 'custom':
                        # Set config mode, set fade to False (checkbox is not visible)
                        # Enable house tab and show it
                        gridObject_dict[selected_element]['config_mode'] = 'custom'
                        return gridObject_dict, no_update, no_update, no_update, no_update, 'house1', False, \
                               selected_element, False, no_update, no_update
                    else:
                        raise PreventUpdate
                elif custom_house == selected_element:
                    if control == 'preset':
                        # Set house from custom mode to preset mode, show checkbox and delete store_custom_house
                        gridObject_dict[selected_element]['config_mode'] = 'preset'
                        return gridObject_dict, no_update, no_update, no_update, no_update, no_update, True, \
                               None, True, no_update, no_update
                    else:
                        raise PreventUpdate
                else:
                    # If there already is a custom house, show notification and set control to preset
                    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                           no_update, 'preset', 'notification_custom_house'
            elif triggered_id == 'store_element_deleted':   # If an element was deleted
                # Set menu tab to empty and write None to tapNode/EdgeData so that the next click could be handled
                if element_deleted is not None:
                    return no_update, 'empty', None, None, no_update, no_update, no_update, no_update, no_update, \
                           no_update, no_update
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update, no_update, err.args[0]

    @app.callback(Output('cyto_grid', 'elements', allow_duplicate=True),
                  Input('store_edge_labels', 'data'),
                  State('cyto_grid', 'elements'),
                  prevent_initial_call=True)
    def edge_labels(labels, elements):
        """
        Takes generated edge labels, sets them for each edge, sets the direction of the edge arrow and returns
        the updates cytoscape elements.
        :param labels: [Input] Generated edge labels
        :param elements: [State] Cytoscape grid elements
        :return: [cyto_grid>elements]
        """

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
                  Input('timestep_slider', 'value'),
                  State('input_year', 'value'),
                  State('input_week', 'value'),
                  prevent_initial_call=True)
    def time_slider(slider, year, week):
        """
        If the slider selects a new timestep, this callback displays the weekday, date and time of the step
        in the grid result section.
        :param slider: [Input] Timestep slider value
        :param year: [State] Year from settings
        :param week: [State] Week of the year from settings
        :return: [alert_time>children]
        """

        date_start, date_stop = get_monday_sunday_from_week(week, year)
        time_start = datetime.datetime.combine(date_start, datetime.datetime.min.time())
        slider_time = time_start + datetime.timedelta(minutes=slider)
        text = slider_time.strftime(f"Am {weekdays[slider_time.weekday()]} %d.%m. um %H:%M")
        return text

    @app.callback(Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('button_compass', 'style'),
                  State('store_grid_object_dict', 'data'),
                  State('store_selected_element_grid', 'data'),
                  [Input(button, 'n_clicks') for button in compass_buttons.keys()],
                  prevent_initial_call=True)
    def compass_action(gridObject_dict, selected_element, *args):
        """
        If a button of the PV compass was clicked, the corresponding orientation is written to the PV object
        and the compass needle is rotated to the clicked orientation.
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param selected_element: [State] Cytoscape element which was clicked in the grid
        :param args: [Input] One Input per button of the compass
        :return: [store_grid_object_grid>data, button_compass>style]
        """

        triggered_id = ctx.triggered_id     # Get which button was clicked
        if all(ele is None for ele in args):  # If no button was clicked
            raise PreventUpdate
        gridObject_dict[selected_element]['orientation'] = compass_buttons[triggered_id]
        style = {'transform': f'rotate({compass_buttons[triggered_id] - 45}deg)'}
        return gridObject_dict, style

    @app.callback(Output('cyto_grid', 'autoungrabify'),  # Callback to make Node ungrabbable when adding lines
                  Output('store_line_edit_active', 'data'),
                  Output('button_line', 'variant'),
                  Input('button_line', 'n_clicks'),
                  Input('key_event_listener', 'n_events'),
                  State('key_event_listener', 'event'),
                  State('store_line_edit_active', 'data'),
                  prevent_initial_call=True)
    def edit_mode(btn_line, n_events, event, btn_active):
        """
        This callback activates or deactivates the line edit mode with the line button and the ESC key.
        It also sets the style of the button if it is activated or not.
        :param btn_line: [Input] Button to add a line between grid objects
        :param n_events: [Input] Key event listener n_events
        :param event: [State] Key event listener event
        :param btn_active: [State] Status of line edit mode
        :return: [cyto_grid>autoungrabify, store_line_edit_active>data, button_line>variant]
        """

        triggered_id = ctx.triggered_id
        if triggered_id == 'button_line':
            if not btn_active:      # If line edit mode is inactive
                return True, True, 'light'      # -> Activate it
            else:
                return False, False, 'filled'   # If its active -> Deactivate it
        elif triggered_id == 'key_event_listener':  # If line edit mode is active and "ESC" is pressed
            if event['key'] == 'Escape' and btn_active:
                return False, False, 'filled'       # -> Deactivate it
            else:
                raise PreventUpdate

    @app.callback(Output('cyto_grid', 'elements', allow_duplicate=True),
                  Input('store_custom_house', 'data'),
                  State('cyto_grid', 'elements'),
                  prevent_initial_call=True)
    def custom_house_style(selected_element, elements):
        """
        Sets the style of a house which is selected as custom. It changes the shape from a rounded rectangle to a
        normal one.
        :param selected_element: [Input] Id of house which was selected as custom
        :param elements: [State]
        :return: [cyto_grid>elements]
        """

        if selected_element is not None:
            for ele in elements:    # Find custom house
                if ele['data']['id'] == selected_element:
                    ele['classes'] = 'node_style_custom'    # Set new node style
                    break
            return elements
        raise PreventUpdate

    @app.callback(Output('store_add_node', 'data'),
                  [Input(object_id[0], 'n_clicks') for object_id in menu_objects],
                  prevent_initial_call=True)
    def button_add_pressed(*args):
        """
        Takes the id of a pressed button to add a grid object and passes it to the store element. A change of this
        then triggers another callback to add the object.
        :param args: [Input] Add grid object buttons
        :return: [store_add_node>data]
        """

        triggered_id = ctx.triggered_id
        if triggered_id == 'button_line':
            raise PreventUpdate
        else:
            return triggered_id
