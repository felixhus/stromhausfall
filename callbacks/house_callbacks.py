import base64
import io
import json
import time

import pandas as pd
from dash import Input, Output, State, ctx, html, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.modules as modules
import source.objects as objects
import source.sql_modules as sql_modules


def house_callbacks(app):
    @app.callback(Output('cyto_bathroom', 'elements', allow_duplicate=True),
                  Output('cyto_livingroom', 'elements', allow_duplicate=True),
                  Output('cyto_kitchen', 'elements', allow_duplicate=True),
                  Output('cyto_office', 'elements', allow_duplicate=True),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Input('interval_refresh', 'n_intervals'),
                  State('cyto_bathroom', 'elements'),
                  State('cyto_livingroom', 'elements'),
                  State('cyto_kitchen', 'elements'),
                  State('cyto_office', 'elements'),
                  State('store_device_dict', 'data'),
                  prevent_initial_call=True)
    def initial_room_configuration(interval, cyto_bathroom, cyto_livingroom, cyto_kitchen, cyto_office, device_dict):
        # Bathroom elements
        device_dict['house1']['lamp_bathroom'] = objects.create_LampObject(
            'lamp_bathroom', "Bad")  # Add lamp to device dictionary
        device_dict['rooms']['bathroom'] = {}
        device_dict['rooms']['bathroom']['name'] = 'Bad'  # Create roomname
        device_dict['rooms']['bathroom']['devices'] = [
            'lamp_bathroom']  # Create list of devices in bathroom in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_bathroom'}
        lamp_node = {'data': {'id': 'lamp_bathroom'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_bathroom'}}
        cyto_bathroom.append(socket_node)
        cyto_bathroom.append(lamp_node)
        cyto_bathroom.append(lamp_edge)

        # Livingroom elements
        device_dict['house1']['lamp_livingroom'] = objects.create_LampObject(
            'lamp_livingroom', "Wohnzimmer")  # Add lamp to device dictionary
        device_dict['rooms']['livingroom'] = {}
        device_dict['rooms']['livingroom']['name'] = 'Wohnzimmer'  # Create roomname
        device_dict['rooms']['livingroom']['devices'] = [
            'lamp_livingroom']  # Create list of devices in livingroom in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_livingroom'}
        lamp_node = {'data': {'id': 'lamp_livingroom'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_livingroom'}}
        cyto_livingroom.append(socket_node)
        cyto_livingroom.append(lamp_node)
        cyto_livingroom.append(lamp_edge)

        # Kitchen elements
        device_dict['house1']['lamp_kitchen'] = objects.create_LampObject(
            'lamp_kitchen', "Küche")  # Add lamp to device dictionary
        device_dict['rooms']['kitchen'] = {}
        device_dict['rooms']['kitchen']['name'] = 'Küche'  # Create roomname
        device_dict['rooms']['kitchen']['devices'] = [
            'lamp_kitchen']  # Create list of devices in kitchen in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_kitchen'}
        lamp_node = {'data': {'id': 'lamp_kitchen'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_kitchen'}}
        cyto_kitchen.append(socket_node)
        cyto_kitchen.append(lamp_node)
        cyto_kitchen.append(lamp_edge)

        # Office elements
        device_dict['house1']['lamp_office'] = objects.create_LampObject(
            'lamp_office', "Büro")  # Add lamp to device dictionary
        device_dict['rooms']['office'] = {}
        device_dict['rooms']['office']['name'] = 'Büro'  # Create roomname
        device_dict['rooms']['office']['devices'] = [
            'lamp_' + 'office']  # Create list of devices in office in dictionary
        socket_node = {'data': {'id': 'socket1', 'parent': 'power_strip'}, 'position': {'x': 35, 'y': 175},
                       'classes': 'socket_node_style_on', 'linked_device': 'lamp_office'}
        lamp_node = {'data': {'id': 'lamp_office'}, 'position': {'x': 35, 'y': 25},
                     'classes': 'room_node_style',
                     'style': {'background-image': ['/assets/Icons/icon_bulb.png']}, 'linked_socket': 'socket1'}
        lamp_edge = {'data': {'source': 'socket1', 'target': 'lamp_office'}}
        cyto_office.append(socket_node)
        cyto_office.append(lamp_node)
        cyto_office.append(lamp_edge)

        return cyto_bathroom, cyto_livingroom, cyto_kitchen, cyto_office, device_dict

    @app.callback(Output('store_results_house_power', 'data'),
                  Output('store_results_house_energy', 'data'),
                  Output('graph_power_house', 'figure'),
                  Output('graph_sunburst_house', 'figure'),
                  Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_calculate', 'n_clicks'),
                  State('store_device_dict', 'data'),
                  State('tabs_main', 'value'),
                  State('store_grid_object_dict', 'data'),
                  State('store_custom_house', 'data'),
                  prevent_initial_call=True)
    def start_calculation_house(btn, device_dict, tabs_main, gridObject_dict, house):
        try:
            start_time = time.process_time()
            if tabs_main == 'house1':
                df_power, df_sum, df_energy, graph_power, graph_sunburst = modules.calculate_house(device_dict,
                                                                                                   range(0, 7 * 1440))
                gridObject_dict[house]['power'] = df_sum.loc['house1'].values.flatten().tolist()
                elapsed_time = time.process_time() - start_time
                return df_power.to_json(orient='index'), df_energy.to_json(
                    orient='index'), graph_power, graph_sunburst, gridObject_dict, f"Berechnungszeit: {elapsed_time}"
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('cost_tab', 'children'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('store_results_house_energy', 'data'),
                  State('input_cost_kwh', 'value'),
                  State('store_device_dict', 'data'),
                  prevent_initial_call=True)
    def cost_result(data, cost_kwh, device_dict):
        try:
            data = json.loads(data)  # Get calculated energy per device
            device_costs = []
            for element in data:  # Filter rooms out of data, store device energy with the device id
                if data[element]['type'] == 'device':
                    cost = data[element]['energy'] * cost_kwh * 52
                    name = device_dict['house1'][element]['name']  # Get name of device
                    icon = device_dict['house1'][element]['icon']  # Get icon of device
                    device_costs.append((name, cost, icon))
            device_costs = sorted(device_costs, key=lambda energy: energy[1],
                                  reverse=True)  # Sort devices by their cost
            children = dash_components.add_device_costs(device_costs)  # Get dash components
            return children, no_update
        except PreventUpdate:
            return no_update, no_update
        except Exception as err:
            return no_update, err.args[0]

    @app.callback(Output('card_additional_devices', 'children'),
                  Input('modal_additional_devices', 'opened'),
                  State('radiogroup_room', 'value'))
    def fill_device_modal(modal_open, radio_room):
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
    def add_additional_device(btn, radio_device, radio_room):   # Development
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
        triggered_id = ctx.triggered_id
        if triggered_id == 'tabs_additional_devices':
            if tab == 'own':    # If "own" tab was clicked, check if there are already own devices in the store element, otherwise show elements to load file
                if len(own_device_dict) > 0:
                    devices = list(own_device_dict.values())
                    children = dash_components.add_card_additional_devices(devices, None, True)
                    return no_update, no_update, children, {'display': 'none'}, no_update
            raise PreventUpdate
        elif triggered_id == 'button_load_own_devices':   # Load given file and check if its the right one
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
            if 'own_devices_dict' not in content_dict:
                return no_update, no_update, no_update, no_update, 'notification_wrong_file'
            else:
                devices = list(content_dict['own_devices_dict'].values())
                children = dash_components.add_card_additional_devices(devices, None, True)
            return content_dict['own_devices_dict'], no_update, children, {'display': 'none'}, no_update
        elif triggered_id == 'upload_own_devices':  # Show filename of selected file
            return no_update, filename, no_update, no_update, no_update

    @app.callback(Output('input_new_icon', 'icon'),
                  Input('input_new_icon', 'value'),
                  prevent_initial_callback=True)
    def update_new_icon(icon):
        if icon is None or icon == '':
            raise PreventUpdate
        return DashIconify(icon=icon)

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
        triggered_id = ctx.triggered_id
        if triggered_id == 'button_add_new_device':
            if input_name == '' or input_menu_type is None:
                return no_update, no_update, 'notification_missing_input'
            if input_icon == '':
                input_icon = 'ic:outline-device-unknown'    # if no icon was given, take standard one
            if filename is None:    # If no file was uploaded
                return no_update, no_update, 'notification_no_file_selected'
            elif not filename.endswith('.csv'):  # Check if the file format is .csv
                return no_update, no_update, 'notification_wrong_file_format'
            try:
                content_type, content_string = upload_content.split(",")  # Three lines to get dict from content
                decoded = base64.b64decode(content_string)
                df_csv = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=';')
                df_csv["time"] = pd.to_datetime(df_csv.iloc[:, 0])
                date_start = df_csv["time"][0].date()
                # df_csv["time"] = df_csv["time"].apply(lambda x: x.time())  # Extract time from timestamps
                df_csv.set_index("time", inplace=True)
                # df_csv.fillna(0)   # Replace NaN with 0
                if input_menu_type == 'device_custom':  # If short profile
                    df_final = df_csv.resample('1T').mean()     # resample profile to 1-minute steps and fill missing values with zero
                    for profile in df_final:
                        index_last_value = df_final[profile].last_valid_index()
                        df_final[profile].loc[:index_last_value] = df_final[profile].loc[:index_last_value].fillna(0)
                else:
                    df_resampled = df_csv.resample('1T').mean()     # resample profile to 1-minute steps and fill missing values with zero
                    index = pd.date_range(start=date_start, periods=1440, freq='1T')
                    df_timestamps = pd.DataFrame(index=index)
                    df_final = pd.merge(df_timestamps, df_resampled, how='left', left_index=True, right_index=True)
                    df_final = df_final.fillna(0)
                power_options = {col: {'key': col} for col in df_final.columns}
                power_profiles = df_final.to_dict('list')
            except Exception as err:
                return no_update, no_update, 'notification_error_reading_csv'    # Show Error message
            for profile in power_profiles:
                if len(power_profiles[profile]) > 1440:
                    return no_update, no_update, 'notification_profile_length'
            device = {
                'id': None,
                'name': input_name,
                'type': 'own_device_' + str(len(own_device_dict)),  # generate unique type name
                'menu_type': input_menu_type,
                'icon': input_icon,
                'power_options': power_options,
                'power_profiles': power_profiles
            }
            own_device_dict[device['type']] = device
            return own_device_dict, no_update, 'notification_successful_added'
        elif triggered_id == 'upload_new_device':
            return no_update, filename, no_update
        else:
            raise PreventUpdate

