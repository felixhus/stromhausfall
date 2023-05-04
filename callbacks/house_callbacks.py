"""
house_callbacks.py contains all dash callbacks for house functions of the app.
"""
# TODO: Write all room callbacks in a more efficient form than copying them for each room.

import base64
import io
import json

import pandas as pd
from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.modules as modules
import source.sql_modules as sql_modules


def house_callbacks(app):
    @app.callback(Output('cyto_bathroom', 'elements', allow_duplicate=True),
                  Output('cyto_livingroom', 'elements', allow_duplicate=True),
                  Output('cyto_kitchen', 'elements', allow_duplicate=True),
                  Output('cyto_office', 'elements', allow_duplicate=True),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Input('interval_refresh', 'n_intervals'),
                  State('store_backup', 'data'),
                  State('cyto_bathroom', 'elements'),
                  State('cyto_livingroom', 'elements'),
                  State('cyto_kitchen', 'elements'),
                  State('cyto_office', 'elements'),
                  State('store_device_dict', 'data'),
                  prevent_initial_call=True)
    def initial_room_configuration(interval, backup, cyto_bathroom, cyto_livingroom,
                                   cyto_kitchen, cyto_office, device_dict):
        """
        This callback is executed only on the first load of the app when no backup exists. It creates the basic
        components in each room of the custom house: A socket with a lamp.
        :param interval: [Input] Interval which triggers this callback on refresh
        :param backup: [State] Backup store component to check whether there is a backup
        :param cyto_bathroom: [State] Cytoscape of the bathroom
        :param cyto_livingroom: [State] Cytoscape of the livingroom
        :param cyto_kitchen: [State] Cytoscape of the kitchen
        :param cyto_office: [State] Cytoscape of the office
        :param device_dict: [State] Dictionary containing all devices in the custom house
        :return: [cyto_bathroom>data, cyto_livingroom>data, cyto_kitchen>data, cyto_office>data, store_device_dict>data]
        """

        if backup is not None:
            database = 'source/database_profiles.db'
            image_lamp_src = modules.get_icon_url('mdi:lightbulb-on-outline')
            # Bathroom elements
            device_dict['house1']['lamp_bathroom'] = modules.create_device_object('lamp_bathroom', 'lamp', database)
            device_dict['house1']['lamp_bathroom']['name'] = "Lampe Bad"
            device_dict['rooms']['bathroom'] = {}
            device_dict['rooms']['bathroom']['name'] = 'Bad'  # Create roomname
            device_dict['rooms']['bathroom']['devices'] = [
                'lamp_bathroom']  # Create list of devices in bathroom in dictionary
            socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                           'classes': 'socket_node_style_on', 'linked_device': 'lamp_bathroom'}
            lamp_node = {'data': {'id': 'lamp_bathroom'}, 'position': {'x': 35, 'y': 25},
                         'classes': 'room_node_style',
                         'style': {'background-image': image_lamp_src}, 'linked_socket': 'socket1'}
            lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_bathroom'}}
            cyto_bathroom.append(socket_node)
            cyto_bathroom.append(lamp_node)
            cyto_bathroom.append(lamp_edge)

            # Livingroom elements
            device_dict['house1']['lamp_livingroom'] = modules.create_device_object('lamp_livingroom', 'lamp', database)
            device_dict['house1']['lamp_livingroom']['name'] = "Lampe Wohnzimmer"
            device_dict['rooms']['livingroom'] = {}
            device_dict['rooms']['livingroom']['name'] = 'Wohnzimmer'  # Create roomname
            device_dict['rooms']['livingroom']['devices'] = [
                'lamp_livingroom']  # Create list of devices in livingroom in dictionary
            socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                           'classes': 'socket_node_style_on', 'linked_device': 'lamp_livingroom'}
            lamp_node = {'data': {'id': 'lamp_livingroom'}, 'position': {'x': 35, 'y': 25},
                         'classes': 'room_node_style',
                         'style': {'background-image': image_lamp_src}, 'linked_socket': 'socket1'}
            lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_livingroom'}}
            cyto_livingroom.append(socket_node)
            cyto_livingroom.append(lamp_node)
            cyto_livingroom.append(lamp_edge)

            # Kitchen elements
            device_dict['house1']['lamp_kitchen'] = modules.create_device_object('lamp_kitchen', 'lamp', database)
            device_dict['house1']['lamp_kitchen']['name'] = "Lampe Küche"
            device_dict['rooms']['kitchen'] = {}
            device_dict['rooms']['kitchen']['name'] = 'Küche'  # Create roomname
            device_dict['rooms']['kitchen']['devices'] = [
                'lamp_kitchen']  # Create list of devices in kitchen in dictionary
            socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                           'classes': 'socket_node_style_on', 'linked_device': 'lamp_kitchen'}
            lamp_node = {'data': {'id': 'lamp_kitchen'}, 'position': {'x': 35, 'y': 25},
                         'classes': 'room_node_style',
                         'style': {'background-image': image_lamp_src}, 'linked_socket': 'socket1'}
            lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_kitchen'}}
            cyto_kitchen.append(socket_node)
            cyto_kitchen.append(lamp_node)
            cyto_kitchen.append(lamp_edge)

            # Office elements
            device_dict['house1']['lamp_office'] = modules.create_device_object('lamp_office', 'lamp', database)
            device_dict['house1']['lamp_office']['name'] = "Lampe Büro"
            device_dict['rooms']['office'] = {}
            device_dict['rooms']['office']['name'] = 'Büro'  # Create roomname
            device_dict['rooms']['office']['devices'] = [
                'lamp_' + 'office']  # Create list of devices in office in dictionary
            socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                           'classes': 'socket_node_style_on', 'linked_device': 'lamp_office'}
            lamp_node = {'data': {'id': 'lamp_office'}, 'position': {'x': 35, 'y': 25},
                         'classes': 'room_node_style',
                         'style': {'background-image': image_lamp_src}, 'linked_socket': 'socket1'}
            lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_office'}}
            cyto_office.append(socket_node)
            cyto_office.append(lamp_node)
            cyto_office.append(lamp_edge)

            return cyto_bathroom, cyto_livingroom, cyto_kitchen, cyto_office, device_dict
        else:
            raise PreventUpdate

    @app.callback(Output('store_results_house_power', 'data'),
                  Output('store_results_house_energy', 'data'),
                  Output('graph_power_house', 'figure'),
                  Output('graph_sunburst_house', 'figure'),
                  Output('result_parent_tabs', 'value'),
                  Output('tabs_menu', 'value', allow_duplicate=True),
                  Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_calculate', 'n_clicks'),
                  State('store_device_dict', 'data'),
                  State('tabs_main', 'value'),
                  State('store_grid_object_dict', 'data'),
                  State('store_custom_house', 'data'),
                  prevent_initial_call=True)
    def start_calculation_house(btn, device_dict, tabs_main, gridObject_dict, house):
        """

        :param btn: [Input] Button to start calculation
        :param device_dict: [State] Dictionary containing all devices in the custom house
        :param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param house: [State] Id of custom house
        :return: [store_results_house_power>data, store_results_house_energy>data, graph_power_house>figure,
        graph_sunburst_house>figure, result_parent_tabs>value, tabs_menu>value, store_grid_object_dict>data,
        store_notification>data]
        """

        try:
            if tabs_main == 'house1':   # If calculation button was clicked in house mode
                # Start calculation of house and save all results
                df_power, df_sum, df_energy, graph_power, graph_sunburst = \
                    modules.calculate_house(device_dict, range(0, 7 * 1440))
                # FIXME: Documentation of calculate_house
                # Set calculated power profile as profile of the house in the grid
                gridObject_dict[house]['power'] = df_sum.loc['house1'].values.flatten().tolist()
                return df_power.to_json(orient='index'), df_energy.to_json(orient='index'), \
                       graph_power, graph_sunburst, 'house', 'results', gridObject_dict, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('cost_tab', 'children'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('store_results_house_energy', 'data'),
                  State('input_cost_kwh', 'value'),
                  State('store_device_dict', 'data'),
                  prevent_initial_call=True)
    def cost_result(data, cost_kwh, device_dict):
        """
        Calculates the yearly energy costs for each device, fetches the dash components and displays them
        in the cost tab.
        :param data: [Input] Energy result data of house calculation
        :param cost_kwh: [State] Cost of 1 kWh of electrical energy, from settings
        :param device_dict: [State] Dictionary containing all devices in the custom house
        :return: [cost_tab>children, store_notification>data]
        """

        try:
            data = json.loads(data)  # Get calculated energy per device
            device_costs = []
            for element in data:  # Filter rooms out of data, store device energy with the device id
                if data[element]['type'] == 'device':
                    cost = data[element]['energy'] * cost_kwh * 52  # Calculate yearly energy consumption from monthly
                    name = device_dict['house1'][element]['name']  # Get name of device
                    icon = device_dict['house1'][element]['icon']  # Get icon of device
                    device_costs.append((name, cost, icon))
                    # Sort devices by their cost, highest first
            device_costs = sorted(device_costs, key=lambda energy: energy[1], reverse=True)
            children = dash_components.add_device_costs(device_costs)  # Get dash components
            return children, no_update
        except PreventUpdate:
            return no_update, no_update
        except Exception as err:
            return no_update, err.args[0]

    @app.callback(Output('card_additional_devices', 'children'),
                  Input('modal_additional_devices', 'opened'),
                  State('radiogroup_room', 'value'))
    def fill_additional_device_modal(modal_open, radio_room):
        """
        Load all devices from sql database and show them as additional devices in the additional devices modal.
        :param modal_open: [Input] The opening of the modal_additional_devices triggers this callback
        :param radio_room: [State] Selected room
        :return: [card_additional_devices>children]
        """
        if modal_open:
            devices = sql_modules.get_all_devices('source/database_profiles.db')
            childs_additional = dash_components.add_card_additional_devices(devices, radio_room, False)
            return childs_additional
        else:
            raise PreventUpdate

    @app.callback(Output('modal_additional_devices', 'opened'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_add_additional_device', 'n_clicks'),
                  State('radiogroup_devices', 'value'),
                  State('radiogroup_room', 'value'),
                  prevent_initial_call=True)
    def add_additional_device_check(btn, radio_device, radio_room):   # Development
        """
        Callback to check whether a device and room was selected wenn the "add" button is clicked. If not,
        return corresponding notifications. It also closes the modal after.
        :param btn: [Input] Button to add an additional device
        :param radio_device: [State] Selected device type
        :param radio_room: [State] Selected room
        :return: [modal_additional_devices>opened]
        """

        if btn is not None:
            if radio_device is None:
                return no_update, "notification_no_device_selected"
            elif radio_room is None:
                return no_update, "notification_no_room_selected"
            else:
                return False, no_update
        else:
            raise PreventUpdate

    @app.callback(Output('store_own_device_dict', 'data'),
                  Output('text_filename_load_own', 'children', allow_duplicate=True),
                  Output('card_own_devices_add', 'children'),
                  Output('card_own_devices_load', 'style'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_load_own_devices', 'n_clicks'),
                  Input('tabs_additional_devices', 'value'),
                  Input('upload_own_devices', 'filename'),
                  State('upload_own_devices', 'contents'),
                  State('store_own_device_dict', 'data'),
                  prevent_initial_call=True)
    def load_own_devices(btn_load, tab, filename, upload_content, own_device_dict):
        """
        Callback to upload own devices, show them or to show already uploaded ones.
        :param btn_load: [Input] Button to load the own devices from file
        :param tab: [Input] Tab value of additional devices modal
        :param filename: [Input] Filename of uploaded file
        :param upload_content: [State] Content of uploaded file
        :param own_device_dict: [State] Dictionary to store the own devices
        :return: [store_own_device_dict>data, text_filename_load_own>children, card_own_devices_add>children,
        card_own_devices_load>style, store_notification>data]
        """

        triggered_id = ctx.triggered_id
        if triggered_id == 'tabs_additional_devices':
            # If "own" tab was clicked, check if there are already own devices in the store element,
            # otherwise show elements to load file
            if tab == 'own':
                if len(own_device_dict) > 0:
                    # Get own devices from store component
                    devices = list(own_device_dict.values())
                    # Get radio list of devices
                    children = dash_components.add_card_additional_devices(devices, None, True)
                    return no_update, no_update, children, {'display': 'none'}, no_update
            raise PreventUpdate
        elif triggered_id == 'button_load_own_devices':   # Load given file and check if it's the right one
            if btn_load is None:
                raise PreventUpdate
            if filename is None:
                return no_update, no_update, no_update, no_update, 'notification_no_file_selected'
            if not filename.endswith('.json'):  # Check if the file format is .json
                return no_update, no_update, no_update, no_update, 'notification_wrong_file_format'
            else:
                content_type, content_string = upload_content.split(",")  # Three lines to get dict from content
                decoded = base64.b64decode(content_string)
                content_dict = json.loads(decoded)
            # Check if the file contains own devices dictionary
            if 'own_devices_dict' not in content_dict:
                return no_update, no_update, no_update, no_update, 'notification_wrong_file'
            else:
                devices = list(content_dict['own_devices_dict'].values())
                children = dash_components.add_card_additional_devices(devices, None, True)
            return content_dict['own_devices_dict'], no_update, children, {'display': 'none'}, no_update
        elif triggered_id == 'upload_own_devices':  # Show filename of uploaded file
            return no_update, filename, no_update, no_update, no_update

    @app.callback(Output('store_own_device_dict', 'data', allow_duplicate=True),
                  Output('text_filename_load_new', 'children'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_add_new_device', 'n_clicks'),
                  Input('upload_new_device', 'filename'),
                  State('input_new_name', 'value'),
                  State('input_new_menu_type', 'value'),
                  State('input_new_icon', 'value'),
                  State('store_own_device_dict', 'data'),
                  State('upload_new_device', 'contents'),
                  prevent_initial_call=True)
    def add_new_device(btn_add, filename, input_name, input_menu_type, input_icon, own_device_dict, upload_content):
        """
        Callback to add a new custom device to the app. The user has to input the name, type, icon and a file, which
        contains the power profiles in Watts. There are two possibilities for this file:
        - CSV-File: First column are timestamps. Every following column is read as a separate power profile
        - XLS-File: First column are timestamps. Every following column is read as a separate power profile.
            Also, the file can contain several sheets, which will be read separately. This can be useful if
            the user wants to add several power profiles which don't share the same timestamps.
        In general the profiles can contain several values per minute, they are resampled to 1-min-steps.
        A device dict is created and added to the own-devices-dictionary.
        :param btn_add: [Input] Button to add new device
        :param filename: [Input] Filename of uploaded file
        :param input_name: [State] Name of new device
        :param input_menu_type: [State] Type of new device (preset or custom)
        :param input_icon: [State] Icon of new device (Iconify)
        :param own_device_dict: [State] Dictionary containing all own devices
        :param upload_content: [State] Content of uploaded file
        :return: [store_own_devices_dict>data, text_filename_load_new>children, store_notification>data]
        """

        triggered_id = ctx.triggered_id
        if triggered_id == 'button_add_new_device':
            if input_name == '' or input_menu_type is None:
                return no_update, no_update, 'notification_missing_input'
            if input_icon == '':
                input_icon = 'ic:outline-device-unknown'    # if no icon was given, take standard one
            if filename is None:    # If no file was uploaded
                return no_update, no_update, 'notification_no_file_selected'
            # Check if the file format is .csv or .xls or .xlsx
            elif not filename.endswith('.csv') and not filename.endswith('.xls') and not filename.endswith('.xlsx'):
                return no_update, no_update, 'notification_wrong_file_format'
            try:
                content_type, content_string = upload_content.split(",")  # Get dict from content
                decoded = base64.b64decode(content_string)
                if filename.endswith('.csv'):
                    # Assume that the user uploaded a CSV file
                    data = {'df_csv': pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=';')}
                elif 'xls' in filename:
                    # Assume that the user uploaded an Excel file, creates one dataframe per sheet
                    data = pd.read_excel(io.BytesIO(decoded), sheet_name=None)
                else:
                    raise Exception("Fehler beim Laden")
                date_start = {}     # Dict to store the start date of each sheet
                for df in data:     # Convert time to datetime-format and set it as index
                    data[df]['time'] = pd.to_datetime(data[df].iloc[:, 0])
                    date_start[df] = data[df]["time"][0].date()
                    data[df].set_index('time', inplace=True)
                df_final = {}
                if input_menu_type == 'device_custom':  # If short profile snippet
                    for df in data:     # For every sheet of the input data
                        df_final[df] = data[df].resample('1T').mean()     # resample profiles to 1-minute steps
                        for profile in df_final[df]:                      # Fill nan but only up to end of profiles
                            index_last_value = df_final[df][profile].last_valid_index()
                            df_final[df][profile].loc[:index_last_value] = \
                                df_final[df][profile].loc[:index_last_value].fillna(0)
                else:
                    for df in data:     # For every sheet of the input data
                        df_resampled = data[df].resample('1T').mean()     # resample profile to 1-minute steps
                        index = pd.date_range(start=date_start[df], periods=1440, freq='1T')
                        df_timestamps = pd.DataFrame(index=index)
                        df_final[df] = pd.merge(df_timestamps, df_resampled, how='left',
                                                left_index=True, right_index=True)
                        df_final[df] = df_final[df].fillna(0)   # Fill nans with zeros
                power_profiles = {}
                power_options = {}
                # Create power_profiles and power_options for each profile
                for df in df_final:
                    temp_dict = {col: {'key': col} for col in df_final[df].columns}
                    power_options.update(temp_dict)
                    temp_dict = df_final[df].to_dict('list')
                    power_profiles.update(temp_dict)
            except Exception as err:
                return no_update, no_update, 'notification_error_reading_csv'    # Show Error message
            for profile in power_profiles:
                if len(power_profiles[profile]) > 1440:
                    return no_update, no_update, 'notification_profile_length'
            # Create device with all properties
            device = {
                'id': None,
                'name': input_name,
                'type': 'own_device_' + str(len(own_device_dict)),  # generate unique type name
                'menu_type': input_menu_type,
                'icon': input_icon,
                'power_options': power_options,
                'power_profiles': power_profiles
            }
            # Add device to dictionary
            own_device_dict[device['type']] = device
            return own_device_dict, no_update, 'notification_successful_added'
        elif triggered_id == 'upload_new_device':
            return no_update, filename, no_update
        else:
            raise PreventUpdate

    @app.callback(Output('input_new_icon', 'icon'),
                  Input('input_new_icon', 'value'),
                  prevent_initial_callback=True)
    def update_new_icon(icon):
        """
        Returns a dash iconify icon as the icon of the text input, if the content of the input was changed to another
        icon name.
        :param icon: [Input] Text input with icon name
        :return: [input_new_icon>icon]
        """

        if icon is None or icon == '':
            raise PreventUpdate
        return DashIconify(icon=icon)
