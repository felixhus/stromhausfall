from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

import source.dash_components as dash_components
import source.modules as modules
import source.objects as objects


def office_callbacks(app):
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
                  State('menu_parent_tabs', 'children'),
                  State('store_selected_element_house', 'data'),
                  Input('cyto_office', 'tapNode'),
                  Input('edit_save_button', 'n_clicks'),
                  Input('edit_delete_button', 'n_clicks'),
                  Input('button_close_menu_office', 'n_clicks'),
                  Input('active_switch_house', 'checked'),
                  [Input(device[1], 'n_clicks') for device in dash_components.devices['office']],
                  prevent_initial_call='initial_duplicate')
    def manage_devices_office(elements, device_dict, tabs_main, children, selected_element, node, btn_save,
                                btn_delete,
                                btn_close, active_switch, *btn_add):  # Callback to handle office action
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
            elif triggered_id[:10] == 'button_add':  # A button in the menu was clicked
                device_type = triggered_id[11:]  # Get type to add
                last_id = int(device_dict['last_id'])  # Get number of last id
                device_dict['last_id'] = last_id + 1  # Increment the last id
                socket_id = "socket" + str(last_id + 1)
                device_id = "device" + str(last_id + 1)
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
                            'style': {'background-image': ['/assets/Icons/icon_' + triggered_id[11:] + '.png']}}
                new_edge = {'data': {'source': socket_id, 'target': device_id}}  # Connect new device with new socket
                new_device = objects.create_DeviceObject(device_id, device_type)
                elements[1]['position'] = new_position_plus
                elements.append(new_socket)  # Append new nodes and edges to cytoscape elements
                elements.append(new_node)
                elements.append(new_edge)
                device_dict['house1'][device_id] = new_device  # Add new device to device dictionary
                device_dict['rooms'][room]['devices'].append(device_id)  # Add new device to room device list
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
