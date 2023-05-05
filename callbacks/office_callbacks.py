"""
office_callbacks.py contains all dash callbacks for office functions of the app.
"""

from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

import source.modules as modules


def office_callbacks(app, button_dict):
    @app.callback(Output('menu_devices_office', 'opened', allow_duplicate=True),
                  Output('modal_additional_devices', 'opened', allow_duplicate=True),
                  Output('radiogroup_room', 'value', allow_duplicate=True),
                  Input('button_additional_office', 'n_clicks'),
                  prevent_initial_call=True)
    def menu_show(btn_additional):
        """
        Opens the additional devices modal, closes the room menu and passes the room as a preset to the room radio
        :param btn_additional: [Input] Button to open the additional device menu
        :return: [menu_devices_office>opened, modal_additional_devices>opened, radiogroup_room>value]
        """

        return False, True, 'office'  # Show modal and close menu when button "Weitere" was clicked.

    @app.callback(Output('cyto_office', 'elements'),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Output('menu_devices_office', 'style'),
                  Output('menu_devices_office', 'opened'),
                  Output('store_menu_change_tab_house', 'data', allow_duplicate=True),
                  Output('store_selected_element_house', 'data', allow_duplicate=True),
                  Output('active_switch_house', 'checked', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  State('cyto_office', 'elements'),
                  State('store_device_dict', 'data'),
                  State('tabs_main', 'value'),
                  State('store_selected_element_house', 'data'),
                  State('radiogroup_room', 'value'),
                  State('radiogroup_devices', 'value'),
                  State('store_own_device_dict', 'data'),
                  Input('cyto_office', 'tapNode'),
                  Input('edit_save_button', 'n_clicks'),
                  Input('edit_delete_button', 'n_clicks'),
                  Input('button_close_menu_office', 'n_clicks'),
                  Input('active_switch_house', 'checked'),
                  Input('button_add_additional_device', 'n_clicks'),
                  Input('button_add_own_device', 'n_clicks'),
                  [Input(device[1], 'n_clicks') for device in button_dict['office']],
                  prevent_initial_call='initial_duplicate')
    def manage_devices_bathroom(elements, device_dict, tabs_main, selected_element, radio_room, radio_devices,
                                own_device_dict, node, btn_save, btn_delete,
                                btn_close, active_switch, btn_additional, btn_own, *btn_add):
        try:
            room = 'office'
            triggered_id = ctx.triggered_id
            if triggered_id is None:  # Initial call
                raise PreventUpdate
            if triggered_id == 'cyto_office':
                if node['data']['id'] == 'plus':  # Open Menu with Devices to add
                    position = elements[1]['position']
                    return no_update, no_update, {"position": "relative", "top": position['y'], "left": position['x']}, \
                           True, no_update, no_update, no_update, no_update
                elif node['data']['id'] == 'power_strip':
                    return no_update, no_update, no_update, no_update, 'power_strip', no_update, no_update, no_update
                elif node['data']['id'][:6] == "socket":  # A socket was clicked, switch this one on/off
                    linked_device = None
                    for ele in elements:
                        if ele['data']['id'] == node['data']['id']:
                            linked_device = ele['linked_device']
                            if ele['classes'] == 'socket_node_style_on':
                                ele['classes'] = 'socket_node_style_off'
                                device_dict['house1'][ele['linked_device']][
                                    'active'] = False  # Store new mode in device_dict
                            else:
                                ele['classes'] = 'socket_node_style_on'
                                device_dict['house1'][ele['linked_device']]['active'] = True
                            break
                    if linked_device is not None and linked_device == selected_element:  # If the socket of the selected element was clicked
                        switch_state = device_dict['house1'][linked_device]['active']  # Update the switch state
                    else:
                        switch_state = no_update  # Otherwise don't update
                    return elements, device_dict, no_update, no_update, no_update, no_update, switch_state, no_update
                else:  # A device was clicked
                    switch_state = device_dict['house1'][node['data']['id']]['active']      # Return, which menu should be opened
                    if node['data']['id'][:6] == "device":
                        menu_type = device_dict['house1'][node['data']['id']]['menu_type']
                        return no_update, no_update, no_update, no_update, menu_type, node['data'][
                            'id'], switch_state, no_update
                    elif node['data']['id'][:4] == "lamp":
                        return no_update, no_update, no_update, no_update, 'lamp', node['data'][
                            'id'], switch_state, no_update
                    else:
                        raise PreventUpdate
            elif triggered_id == 'active_switch_house':
                for ele in elements:
                    if 'linked_device' in ele:
                        if ele['linked_device'] == selected_element:  # search for socket connected to device
                            if active_switch:
                                ele['classes'] = 'socket_node_style_on'
                                device_dict['house1'][ele['linked_device']]['active'] = True
                            else:
                                ele['classes'] = 'socket_node_style_off'
                                device_dict['house1'][ele['linked_device']]['active'] = False
                            break
                return elements, device_dict, no_update, no_update, no_update, no_update, no_update, no_update
            elif triggered_id[:10] == 'button_add':  # A button to add a device was clicked. This could be either a menu button, the button_add_additional device or button_add_own_device
                own = False
                if triggered_id == 'button_add_additional_device':  # If this room was selected in the radio menu
                    if btn_additional is None:
                        raise PreventUpdate
                    if radio_room == room and radio_devices is not None:
                        device_type = radio_devices  # Get type to add
                    else:
                        raise PreventUpdate
                elif triggered_id == 'button_add_own_device':  # The button to add an own device in the additional modal was clicked
                    if btn_own is None:
                        raise PreventUpdate
                    if radio_room == room and radio_devices is not None:
                        device_type = radio_devices  # Get type to add
                        own = True
                    else:
                        raise PreventUpdate
                else:
                    device_type = triggered_id[11:]  # Get type to add
                elements, device_dict = modules.create_new_device(elements, device_dict, room, device_type, own,
                                                                  own_devices=own_device_dict)
                return elements, device_dict, no_update, False, ['empty',
                                                                 None], no_update, no_update, no_update  # Return elements and close menu
            elif triggered_id == 'edit_save_button':
                raise PreventUpdate
            elif triggered_id == 'edit_delete_button':
                if tabs_main != 'house1' or btn_delete is None:  # If button was clicked in grid mode or is None do nothing
                    raise PreventUpdate
                if selected_element not in device_dict['rooms'][room]['devices']:  # If delete button was clicked on device in another room
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
                device_dict['rooms'][room]['devices'].remove(selected_element)     # remove device from room list
                return elements, device_dict, no_update, no_update, ['empty', None], no_update, no_update, no_update
            elif triggered_id == 'button_close_menu_office':  # The button "close" of the menu was clicked, close the menu
                return no_update, no_update, no_update, False, no_update, no_update, no_update, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]
