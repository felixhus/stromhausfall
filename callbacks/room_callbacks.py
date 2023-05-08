"""
room_callbacks.py creates all dash callbacks for room functions of the app.
"""

from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

import source.modules as modules


def room_callbacks(app, button_dict, rooms):
    """
    Functions creates room callbacks for the rooms of the house. For each room, the same callbacks with different
    Inputs and outputs are created. It is important that the room name has to match the room identifying string in
    the dash component ids (for example cyto_{room} creates cyto_bathroom, cyto_kitchen and so forth).

    :param app: Dash Application to add callbacks to
    :type app: Dash App
    :param button_dict: Dictionary with buttons to create grid objects
    :type button_dict: dict
    :param rooms: Names of rooms in the house
    :type rooms: list[str]
    :return: Nothing
    """

    for room in rooms:
        create_menu_show_callbacks(room, app)
        create_manage_devices_callback(app, button_dict, room)


def create_menu_show_callbacks(room, app):
    @app.callback(Output(f'menu_devices_{room}', 'opened', allow_duplicate=True),
                  Output('modal_additional_devices', 'opened', allow_duplicate=True),
                  Output('radiogroup_room', 'value', allow_duplicate=True),
                  Input(f'button_additional_{room}', 'n_clicks'),
                  prevent_initial_call=True)
    def menu_show(btn_additional):
        """
        Opens the additional devices modal, closes the room menu and passes the room as a preset to the room radio

        :param btn_additional: [Input] Button to open the additional device menu
        :return: menu_devices_{room} > opened
        :return: modal_additional_devices > opened
        :return: radiogroup_room > value
        """

        return False, True, room  # Show modal and close menu when button "Weitere" was clicked.


def create_manage_devices_callback(app, button_dict, room):
    @app.callback(Output(f'cyto_{room}', 'elements'),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Output(f'menu_devices_{room}', 'style'),
                  Output(f'menu_devices_{room}', 'opened'),
                  Output('store_menu_change_tab_house', 'data', allow_duplicate=True),
                  Output('store_selected_element_house', 'data', allow_duplicate=True),
                  Output('active_switch_house', 'checked', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  State(f'cyto_{room}', 'elements'),
                  State('store_device_dict', 'data'),
                  State('tabs_main', 'value'),
                  State('store_selected_element_house', 'data'),
                  State('radiogroup_room', 'value'),
                  State('radiogroup_devices', 'value'),
                  State('store_own_device_dict', 'data'),
                  Input(f'cyto_{room}', 'tapNode'),
                  Input('edit_delete_button', 'n_clicks'),
                  Input(f'button_close_menu_{room}', 'n_clicks'),
                  Input('active_switch_house', 'checked'),
                  Input('button_add_additional_device', 'n_clicks'),
                  Input('button_add_own_device', 'n_clicks'),
                  [Input(device[1], 'n_clicks') for device in button_dict[room]],
                  prevent_initial_call='initial_duplicate')
    def manage_devices_room(elements, device_dict, tabs_main, selected_element, radio_room, radio_devices,
                            own_device_dict, node, btn_delete,
                            btn_close, active_switch, btn_additional, btn_own, *btn_add):
        """
        Manages all functions of a device in a room. If a node of the cytoscape was clicked, it either opens the
        corresponding menu tab or the add device menu. It updates and synchronizes the active state of a device
        with the socket state and the slider in the menu. It adds devices to the room and deletes them with their
        socket and connection.

        :param elements: [State] Elements of the room cytoscape
        :param device_dict: [State] Dictionary containing all devices in the custom house
        :param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
        :param selected_element: [State] Cytoscape element which was clicked in the house
        :param radio_room: [State] Selected room by radiogroup
        :param radio_devices: [State] Selected device by radiogroup
        :param own_device_dict: [State] Dictionary to store the own devices
        :param node: [Input] Node that was clicked in a room cytoscape
        :param btn_delete: [Input] Button to delete device
        :param btn_close: [Input] Button to close the menu in a room
        :param active_switch: [Input] Slider to activate or deactivate a device
        :param btn_additional: [Input] Button to add an additional devices modal
        :param btn_own: [Input] Button to add an own device
        :param btn_add: [Inputs] Button to add a device from a room menu
        :return: cyto{room} > elements
        :return: store_device_dict > data
        :return: menu_devices{room} > style
        :return: menu_devices{room} > opened
        :return: store_menu_change_tab_house > data
        :return: store_selected_element_house > data
        :return: active_switch_house > checked,
        :return: store_notification > data
        """

        try:
            triggered_id = ctx.triggered_id
            if triggered_id is None:  # Initial call
                raise PreventUpdate
            if triggered_id == f'cyto_{room}':    # If a node in the room cytoscape was clicked
                if node['data']['id'] == 'plus':  # Open Menu with Devices to add if plus was clicked
                    position = elements[1]['position']  # Set position of menu
                    return no_update, no_update, {"position": "relative", "top": position['y'],
                                                  "left": position['x']}, \
                           True, no_update, no_update, no_update, no_update
                elif node['data']['id'] == 'power_strip':   # If power strip was clicked, open power strip menu
                    return no_update, no_update, no_update, no_update, 'power_strip', no_update, no_update, no_update
                elif node['data']['id'][:6] == "socket":  # A socket was clicked, switch this one on/off
                    linked_device = None
                    for ele in elements:    # Find linked device
                        if ele['data']['id'] == node['data']['id']:
                            linked_device = ele['linked_device']
                            if ele['classes'] == 'socket_node_style_on':    # If socket is on, turn off
                                ele['classes'] = 'socket_node_style_off'
                                # Store new mode in device_dict
                                device_dict['house1'][ele['linked_device']]['active'] = False
                            else:
                                ele['classes'] = 'socket_node_style_on'     # If socket is off, turn on
                                device_dict['house1'][ele['linked_device']]['active'] = True
                            break
                    # If the socket of the selected element was clicked
                    if linked_device is not None and linked_device == selected_element:
                        switch_state = device_dict['house1'][linked_device]['active']  # Update the switch state
                    else:
                        switch_state = no_update  # Otherwise don't update
                    return elements, device_dict, no_update, no_update, no_update, no_update, switch_state, no_update
                else:  # A device was clicked
                    # Return, which menu should be opened
                    switch_state = device_dict['house1'][node['data']['id']]['active']
                    if node['data']['id'][:6] == "device":
                        menu_type = device_dict['house1'][node['data']['id']]['menu_type']  # Get menu type of device
                        return no_update, no_update, no_update, no_update, menu_type, \
                               node['data']['id'], switch_state, no_update
                    elif node['data']['id'][:4] == "lamp":
                        return no_update, no_update, no_update, no_update, 'lamp', \
                               node['data']['id'], switch_state, no_update
                    else:
                        raise PreventUpdate
            elif triggered_id == 'active_switch_house':     # If the slider was changed
                for ele in elements:
                    if 'linked_device' in ele:  # Find socket connected to selected device
                        if ele['linked_device'] == selected_element:
                            if active_switch:   # If switch was turned on
                                ele['classes'] = 'socket_node_style_on'
                                device_dict['house1'][ele['linked_device']]['active'] = True
                            else:               # If switch was turned off
                                ele['classes'] = 'socket_node_style_off'
                                device_dict['house1'][ele['linked_device']]['active'] = False
                            break
                return elements, device_dict, no_update, no_update, no_update, no_update, no_update, no_update
            # A button to add a device was clicked. This could be either a menu button,
            # the button_add_additional device or button_add_own_device
            elif triggered_id[:10] == 'button_add':
                own = False
                if triggered_id == 'button_add_additional_device':
                    if btn_additional is None:
                        raise PreventUpdate
                    # If this room was selected in the radio menu
                    if radio_room == room and radio_devices is not None:
                        device_type = radio_devices  # Get type to add
                    else:
                        raise PreventUpdate
                # The button to add an own device in the additional modal was clicked
                elif triggered_id == 'button_add_own_device':
                    if btn_own is None:
                        raise PreventUpdate
                    # If this room was selected in the radio menu
                    if radio_room == room and radio_devices is not None:
                        device_type = radio_devices  # Get type to add
                        own = True
                    else:
                        raise PreventUpdate
                else:
                    device_type = triggered_id[11:]  # Get type to add
                elements, device_dict = modules.add_device(elements, device_dict, room, device_type, own,
                                                           own_devices=own_device_dict)
                # Return elements and close menu
                return elements, device_dict, no_update, False, ['empty', None], no_update, no_update, no_update
            elif triggered_id == 'edit_delete_button':  # Button to delete a device was clicked
                # If button was clicked in grid mode or is None do nothing
                if tabs_main != 'house1' or btn_delete is None:
                    raise PreventUpdate
                # If delete button was clicked on device in another room, do nothing
                if selected_element not in device_dict['rooms'][room]['devices']:
                    raise PreventUpdate
                index_device, index_socket, index_edge = 0, 0, 0
                for ele in elements:
                    if ele['data']['id'] == selected_element:  # Find index of device in elements list
                        break
                    index_device += 1
                if index_device >= len(elements):  # If device node was not found
                    raise Exception("Zu löschende Objekte nicht gefunden.")
                linked_socket = elements[index_device]['linked_socket']
                elements.pop(index_device)  # Remove device node from elements list
                for ele in elements:
                    if ele['data']['id'] == linked_socket:  # Find index of connected socket
                        break
                    index_socket += 1
                if index_socket >= len(elements):  # If socket node was not found
                    raise Exception("Zu löschende Objekte nicht gefunden.")
                elements.pop(index_socket)  # Remove socket node from elements list
                for ele in elements:
                    if 'target' in ele['data']:  # Find index of edge connected to device and socket
                        if ele['data']['target'] == selected_element:
                            break
                    index_edge += 1
                if index_edge >= len(elements):  # If edge was not found
                    raise Exception("Zu löschende Objekte nicht gefunden.")
                elements.pop(index_edge)  # Remove edge from elements list
                del device_dict['house1'][selected_element]  # Delete device from device dictionary
                # Change positions of all sockets and devices right of the deleted ones:
                elements[1]['position']['x'] = elements[1]['position']['x'] - 40  # Change position of plus node
                for i in range(index_device - 1, len(elements)):
                    if 'position' in elements[i]:  # Check if it is a node
                        elements[i]['position']['x'] = elements[i]['position']['x'] - 40  # shift node to the left
                device_dict['rooms'][room]['devices'].remove(selected_element)  # remove device from room list
                return elements, device_dict, no_update, no_update, ['empty', None], no_update, no_update, no_update
            # The button "close" of the menu was clicked, close the menu
            elif triggered_id == f'button_close_menu_{room}':
                return no_update, no_update, no_update, False, no_update, no_update, no_update, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]
