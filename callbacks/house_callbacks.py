import json
import time

from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate

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

    # @app.callback(Output('store_menu_elements_house', 'data'),
    #               Input('interval_refresh', 'n_intervals'),
    #               State('store_menu_elements_house', 'data'),
    #               prevent_initial_call=True)
    # def generate_menu_buttons_house(interval, button_dict):
    #     if button_dict is None:
    #         devices = sql_modules.get_button_dict('source/database_profiles.db')     # Get the dict from the database
    #         button_dict = {}
    #         for device in devices:
    #             if device[1] not in button_dict:  # If room doesn't already exist in dict, create list for it
    #                 button_dict[device[1]] = []
    #             button_dict[device[1]].append([
    #                 device[2], "button_add_" + device[0], device[4]
    #             ])
    #         return button_dict
    #     else:
    #         raise PreventUpdate     # If it was already created, skip
