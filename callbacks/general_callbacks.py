import base64
import copy
import json
import time

import dash
import dash_mantine_components as dmc
from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.modules as modules
from source.modules import days


def general_callbacks(app):
    @app.callback(Output('store_device_dict', 'data', allow_duplicate=True),
                  Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('graph_pv', 'figure'),
                  Output('graph_house', 'figure'),
                  Output('store_used_profiles', 'data'),
                  Output('checkbox_random_profile', 'checked'),
                  Output('store_save_by_enter', 'data', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('edit_save_button', 'n_clicks'),
                  Input('store_save_by_enter', 'data'),
                  State('tabs_main', 'value'),
                  State('store_device_dict', 'data'),
                  State('store_selected_element_house', 'data'),
                  State('store_selected_element_grid', 'data'),
                  State('menu_parent_tabs', 'children'),
                  State('pagination_days_menu', 'value'),
                  State('store_grid_object_dict', 'data'),
                  State('input_year', 'value'),
                  State('input_week', 'value'),
                  State('store_used_profiles', 'data'),
                  State('checkbox_random_profile', 'checked'),
                  State('graph_pv', 'figure'),
                  State('graph_house', 'figure'),
                  prevent_initial_call=True)
    def save_props_action(btn_save, key_save, tabs_main, device_dict, selected_element_house, selected_element_grid,
                          children,
                          day, gridObject_dict, year, week, used_profiles, checkbox, figure_pv, figure_house):
        try:
            triggered_id = ctx.triggered_id
            if btn_save is None and key_save is None:
                raise PreventUpdate
            if children[2] is None:  # Catch event that enter was pressed without an open menu
                raise PreventUpdate
            else:
                if tabs_main == 'house1':  # If button was clicked in house mode
                    device_dict = modules.save_settings_devices(children[2]['props']['children'], device_dict,
                                                                selected_element_house, 'house1', day)
                    return device_dict, no_update, no_update, no_update, no_update, no_update, no_update, no_update
                elif tabs_main == 'grid':  # If button was clicked in grid mode
                    if gridObject_dict[selected_element_grid]['object_type'] == 'pv':  # If PV is selected
                        gridObject_dict, notif = modules.save_settings_pv(children[2]['props']['children'],
                                                                          gridObject_dict, selected_element_grid,
                                                                          year, week)
                        figure_pv["data"][0]["y"] = [-i for i in gridObject_dict[selected_element_grid][
                            'power']]  # Invert power for plot
                        if notif is not None:
                            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, notif
                        else:
                            return no_update, gridObject_dict, figure_pv, no_update, no_update, no_update, None, no_update
                    elif gridObject_dict[selected_element_grid]['object_type'] == 'house':  # If House is selected
                        gridObject_dict, used_profiles = modules.save_settings_house(children[2]['props']['children'],
                                                                                     gridObject_dict,
                                                                                     selected_element_grid, year, week,
                                                                                     used_profiles, checkbox)
                        figure_house["data"][0]["y"] = gridObject_dict[selected_element_grid]['power']
                        return no_update, gridObject_dict, no_update, figure_house, used_profiles, False, None, no_update
                    elif gridObject_dict[selected_element_grid][
                        'object_type'] == 'transformer':  # If Transformer is selected
                        childs = children[2]['props']['children']
                        gridObject_dict[selected_element_grid]['name'] = childs[0]['props']['value']
                        gridObject_dict[selected_element_grid]['rating'] = childs[2]['props']['value']
                        return no_update, gridObject_dict, no_update, no_update, no_update, no_update, None, no_update
                    elif gridObject_dict[selected_element_grid][
                        'object_type'] == 'switch_cabinet':  # If switch cabinet is selected
                        childs = children[2]['props']['children']
                        gridObject_dict[selected_element_grid]['name'] = childs[0]['props']['value']
                        return no_update, gridObject_dict, no_update, no_update, no_update, no_update, None, no_update
                else:
                    raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('menu_parent_tabs', 'children'),
                  Output('menu_parent_tabs', 'value'),
                  Output('active_switch_grid', 'style'),
                  Output('active_switch_house', 'style'),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('store_menu_change_tab_house', 'data'),
                  Input('store_menu_change_tab_grid', 'data'),
                  Input('tabs_main', 'value'),
                  Input('store_update_switch', 'data'),
                  State('menu_parent_tabs', 'children'),
                  State('store_grid_object_dict', 'data'),
                  State('store_device_dict', 'data'),
                  State('store_selected_element_grid', 'data'),
                  State('store_selected_element_house', 'data'),
                  prevent_initial_call=True)
    def manage_menu_tabs(tab_value_house, tab_value_grid, tabs_main, switch_state, menu_children, gridObject_dict,
                         device_dict, selected_element_grid, selected_element_house):
        # TODO: !!!!!!!!!!!!!!!!!!
        try:
            triggered_id = ctx.triggered_id
            if triggered_id == 'tabs_main':
                if tabs_main == 'grid':
                    return no_update, 'empty', {'display': 'block'}, {'display': 'none'}, no_update
                elif tabs_main == 'house1':
                    return no_update, 'empty', {'display': 'none'}, {'display': 'block'}, no_update
                else:
                    raise PreventUpdate
            elif triggered_id == 'store_menu_change_tab_house':  # If a device in the house was clicked, prepare the variables
                if tab_value_house == 'empty':
                    return no_update, 'empty', no_update, no_update, no_update
                tab_value = tab_value_house
                selected_element = selected_element_house
                elements_dict = device_dict['house1']
            elif triggered_id == 'store_menu_change_tab_grid':  # If a device in the grid was clicked, prepare the variables
                if tab_value_grid == 'empty':
                    return no_update, 'empty', no_update, no_update, no_update
                tab_value = tab_value_grid
                selected_element = selected_element_grid
                elements_dict = gridObject_dict
            else:
                raise PreventUpdate
            while len(menu_children) > 2:  # Remove all tabs except the 'empty' tab and the 'init_ids' tab
                menu_children.pop()
            new_tab_panel = dash_components.add_menu_tab_panel(tab_value, selected_element,
                                                               elements_dict)  # Get new tab panel
            menu_children = menu_children + [new_tab_panel]  # Add children of new tab panel
            return menu_children, tab_value, no_update, no_update, no_update
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('result_parent_tabs', 'value'),
                  Output('tabs_menu', 'value', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('graph_power_house', 'figure'),
                  State('tabs_main', 'data'),
                  prevent_initial_call=True)
    def manage_result_containers(figure, tabs_main):
        try:
            triggered_id = ctx.triggered_id
            if triggered_id == 'graph_power_house':
                return 'house', 'results', no_update
        except PreventUpdate:
            return no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, err.args[0]

    @app.callback(Output('modal_readme', 'opened'),
                  Input('button_readme', 'n_clicks'),
                  prevent_initial_call=True)
    def open_readme(btn):
        return True

    @app.callback(Output('drawer_notifications', 'opened'),
                  Input('button_notifications', 'n_clicks'))
    def open_drawer_notifications(btn):
        if btn is not None:
            return True
        else:
            raise PreventUpdate

    @app.callback(Output('modal_start', 'opened'),
                  Input('button_start', 'n_clicks'),
                  Input('button_start_load', 'n_clicks'))
    def open_menu_card(btn, btn_load):
        if btn is not None or btn_load is not None:
            return False
        else:
            raise PreventUpdate

    @app.callback(Output('graph_device', 'figure'),
                  Input('store_device_dict', 'data'),
                  Input('pagination_days_menu', 'value'),
                  State('store_selected_element_house', 'data'),
                  State('graph_device', 'figure'),
                  State('pagination_days_menu', 'value'),
                  prevent_initial_call=True)
    def update_figure_house(data, day_control, selected_element, figure,
                            day):  # Update the values of the graphs if another profile is chosen
        # patched_fig = Patch()
        # Patch scheint noch nicht zu funktionieren, vielleicht später nochmal probieren
        day_ind = days[day]
        index_start = day_ind * 24 * 60
        index_stop = index_start + 24 * 60
        if selected_element in data['house1']:  # Check if element is still in dict or if it was deleted
            figure["data"][0]["y"] = data['house1'][selected_element]['power'][index_start:index_stop]
        else:
            raise PreventUpdate
        return figure

    @app.callback(Output('graph_power_house', 'figure', allow_duplicate=True),
                  Output('graph_modal', 'figure'),
                  Output('modal_graph', 'opened'),
                  Input('pagination_days_results', 'value'),
                  State('graph_power_house', 'figure'),
                  prevent_initial_call=True)
    def update_figure_devices(day, figure):  # Update the values of the graphs if another profile is chosen
        # patched_fig = Patch()
        # Patch scheint noch nicht zu funktionieren, vielleicht später nochmal probieren
        if day == 'tot':  # Set total range
            index_start = 0
            index_stop = 7 * 24 * 60
            figure['layout']['xaxis']['range'] = [index_start, index_stop]
            figure_big = copy.deepcopy(figure)  # Get copy of small figure for the big modal
            figure_big['layout']['height'] = None  # Set size of big figure to full size
            figure_big['layout']['width'] = None
            return figure, figure_big, True
        else:  # Set range for one day
            day_ind = days[day]
            index_start = day_ind * 24 * 60
            index_stop = index_start + 24 * 60
            figure['layout']['xaxis']['range'] = [index_start, index_stop]
            return figure, no_update, no_update

    @app.callback(Output('graph_power_house', 'figure', allow_duplicate=True),
                  Input('checkbox_show_legend', 'checked'),
                  State('graph_power_house', 'figure'),
                  prevent_initial_call=True)
    def show_legend(checkbox, figure):
        if checkbox:
            figure['layout']['showlegend'] = True
        else:
            figure['layout']['showlegend'] = False
        return figure

    # @app.callback(Output('modal_timeseries', 'opened'),   # Not in use
    #               Output('timeseries_table', 'data'),
    #               Input('pill_add_profile', 'n_clicks'),
    #               Input('button_add_value', 'n_clicks'),
    #               Input('button_save_profile', 'n_clicks'),
    #               State('timeseries_table', 'data'),
    #               State('textinput_profile_name', 'value'),
    #               prevent_initial_call=True)
    # def modal_timeseries(pill, btn_add, btn_save, rows, name):
    #     triggered_id = ctx.triggered_id
    #     if triggered_id == 'pill_add_profile':  # Open modal to add timeseries
    #         if pill is not None:
    #             return True, no_update
    #         else:
    #             raise PreventUpdate
    #     elif triggered_id == 'button_add_value':  # Add one empty row to the data table
    #         rows.append({'time': '', 'power': ''})
    #         return no_update, rows
    #     elif triggered_id == 'button_save_profile':
    #         # Funktionen zum Interpolieren und in Datenbank schreiben existieren in "sql_modules".
    #         # Problem: Ich kann die neuen Lastprofile eigentlich nicht in die SQL-Datenbank schreiben, da die dann
    #         # für alle verändert wird.
    #         return False, no_update
    #     else:
    #         raise PreventUpdate

    @app.callback(Output('store_settings', 'data'),
                  Input('input_week', 'value'),
                  Input('input_year', 'value'),
                  State('store_settings', 'data'))
    def settings(week, year, settings_dict):
        settings_dict['week'] = week
        settings_dict['year'] = year
        return settings_dict

    @app.callback(Output('download_json', 'data'),
                  Output('modal_load_configuration', 'opened'),
                  Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Output('cyto_grid', 'elements', allow_duplicate=True),
                  Output('cyto_bathroom', 'elements', allow_duplicate=True),
                  Output('cyto_kitchen', 'elements', allow_duplicate=True),
                  Output('cyto_livingroom', 'elements', allow_duplicate=True),
                  Output('cyto_office', 'elements', allow_duplicate=True),
                  Output('input_week', 'value'),
                  Output('input_year', 'value'),
                  Output('store_custom_house', 'data', allow_duplicate=True),
                  Output('tab_house', 'disabled', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('menu_item_save', 'n_clicks'),
                  Input('menu_item_load', 'n_clicks'),
                  Input('menu_item_own_devices', 'n_clicks'),
                  Input('button_start_load', 'n_clicks'),
                  Input('button_load_configuration', 'n_clicks'),
                  State('store_grid_object_dict', 'data'),
                  State('store_device_dict', 'data'),
                  State('cyto_grid', 'elements'),
                  State('cyto_bathroom', 'elements'),
                  State('cyto_kitchen', 'elements'),
                  State('cyto_livingroom', 'elements'),
                  State('cyto_office', 'elements'),
                  State('upload_configuration', 'filename'),
                  State('upload_configuration', 'contents'),
                  State('store_settings', 'data'),
                  State('store_custom_house', 'data'),
                  State('store_own_device_dict', 'data'),
                  prevent_initial_call=True)
    def main_menu(btn_save, btn_load_menu, btn_own, btn_load, btn_start_load, gridObject_dict, device_dict,
                  elements_grid,
                  elements_bath, elements_kitchen, elements_livingroom, elements_office, filename, upload_content,
                  settings_dict, custom_house, own_devices):
        triggered_id = ctx.triggered_id
        if triggered_id == 'menu_item_save':
            save_dict = {'gridObject_dict': gridObject_dict,
                         'device_dict': device_dict,
                         'cyto_grid': elements_grid,
                         'cyto_bathroom': elements_bath,
                         'cyto_kitchen': elements_kitchen,
                         'cyto_livingroom': elements_livingroom,
                         'cyto_office': elements_office,
                         'settings': settings_dict,
                         'custom_house': custom_house}
            return dict(content=json.dumps(save_dict), filename="konfiguration.json"), no_update, no_update, no_update, \
                   no_update, no_update, no_update, \
                   no_update, no_update, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'menu_item_own_devices':
            save_dict = {'own_devices_dict': own_devices}
            return dict(content=json.dumps(save_dict), filename="eigene_geraete.json"), no_update, no_update, no_update, \
                   no_update, no_update, no_update, \
                   no_update, no_update, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'menu_item_load' or triggered_id == 'button_start_load':
            return no_update, True, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update
        elif triggered_id == 'button_load_configuration':
            if filename is None:
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, 'notification_no_file_selected'
            if not filename.endswith('.json'):  # Check if the file format is .json
                return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, 'notification_wrong_file_format'
            else:
                content_type, content_string = upload_content.split(",")  # Three lines to get dict from content
                decoded = base64.b64decode(content_string)
                content_dict = json.loads(decoded)
                custom_house_disabled = True  # Look up if there is a house configured to activate house tab
                if content_dict['device_dict']['house1'] is not None:
                    custom_house_disabled = False
                if not (
                        'gridObject_dict' in content_dict and 'device_dict' in content_dict and 'cyto_grid' in content_dict):  # Check if all dictionaries are there
                    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, 'notification_wrong_file'
                return no_update, False, content_dict['gridObject_dict'], content_dict['device_dict'], \
                       content_dict['cyto_grid'], content_dict['cyto_bathroom'], content_dict['cyto_kitchen'], \
                       content_dict['cyto_livingroom'], content_dict['cyto_office'], \
                       content_dict['settings']['week'], content_dict['settings'][
                           'year'], content_dict['custom_house'], custom_house_disabled, no_update
        else:
            raise PreventUpdate

    @app.callback(Output('text_filename_load', 'children'),
                  Input('upload_configuration', 'filename'),
                  prevent_initial_call=True)
    def filename_upload(filename):
        return filename

    @app.callback(Output('store_device_dict', 'data', allow_duplicate=True),
                  Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_notification', 'data', allow_duplicate=True),
                  Input('button_update_settings', 'n_clicks'),
                  State('store_grid_object_dict', 'data'),
                  State('input_week', 'value'),
                  State('input_year', 'value'),
                  prevent_initial_call=True)
    def update_settings(btn_update, gridObject_dict, week, year):
        try:
            dict_temp = gridObject_dict
            for obj in gridObject_dict:
                modules.update_settings(dict_temp, obj, year, week)
            return no_update, dict_temp, no_update
        except Exception as err:
            return no_update, no_update, err.args[0]

    @app.callback(Output('store_backup', 'data'),
                  Input('interval_backup', 'n_intervals'),
                  State('store_grid_object_dict', 'data'),
                  State('store_device_dict', 'data'),
                  State('cyto_grid', 'elements'),
                  State('cyto_bathroom', 'elements'),
                  State('cyto_kitchen', 'elements'),
                  State('cyto_livingroom', 'elements'),
                  State('cyto_office', 'elements'),
                  State('store_settings', 'data'),
                  State('store_custom_house', 'data'),
                  prevent_initial_call=True)
    def backup(interval, gridObject_dict, device_dict, elements_grid, elements_bath, elements_kitchen,
               elements_livingroom, elements_office, settings_dict, custom_house):
        save_dict = {'gridObject_dict': gridObject_dict,
                     'device_dict': device_dict,
                     'cyto_grid': elements_grid,
                     'cyto_bathroom': elements_bath,
                     'cyto_kitchen': elements_kitchen,
                     'cyto_livingroom': elements_livingroom,
                     'cyto_office': elements_office,
                     'settings': settings_dict,
                     'custom_house': custom_house}
        return json.dumps(save_dict)

    @app.callback(Output('store_grid_object_dict', 'data', allow_duplicate=True),
                  Output('store_device_dict', 'data', allow_duplicate=True),
                  Output('cyto_grid', 'elements', allow_duplicate=True),
                  Output('cyto_bathroom', 'elements', allow_duplicate=True),
                  Output('cyto_kitchen', 'elements', allow_duplicate=True),
                  Output('cyto_livingroom', 'elements', allow_duplicate=True),
                  Output('cyto_office', 'elements', allow_duplicate=True),
                  Output('input_week', 'value', allow_duplicate=True),
                  Output('input_year', 'value', allow_duplicate=True),
                  Output('store_custom_house', 'data', allow_duplicate=True),
                  Output('tab_house', 'disabled', allow_duplicate=True),
                  Output('modal_start', 'opened', allow_duplicate=True),
                  Input('interval_refresh', 'n_intervals'),
                  State('store_backup', 'data'),
                  State('store_custom_house', 'data'),
                  prevent_initial_call=True)
    def refresh(interval, backup_dict, custom_house):
        custom_house_disabled = True
        if custom_house is not None:
            custom_house_disabled = False
        if backup_dict is not None:
            backup_dict = json.loads(backup_dict)
            return backup_dict['gridObject_dict'], backup_dict['device_dict'], \
                   backup_dict['cyto_grid'], backup_dict['cyto_bathroom'], backup_dict['cyto_kitchen'], \
                   backup_dict['cyto_livingroom'], backup_dict['cyto_office'], \
                   backup_dict['settings']['week'], backup_dict['settings']['year'], backup_dict['custom_house'], \
                   custom_house_disabled, False
        else:
            raise PreventUpdate

    @app.callback(Output('store_save_by_enter', 'data'),
                  Input('key_event_listener', 'n_events'),
                  State('key_event_listener', 'event'),
                  State('edit_save_button', 'n_clicks'),
                  prevent_initial_call=True)
    def enter_save(key_n, key_event, n):
        if key_event['key'] == 'Enter':
            # if n is None:
            #     return 0
            # return n + 1
            return 'pressed'
        else:
            raise PreventUpdate

    @app.callback(Output('notification_container', 'children'),
                  Output('drawer_notifications', 'children'),
                  Output('bade_notifications', 'children'),
                  Input('store_notification', 'data'),
                  State('drawer_notifications', 'children'))
    def notification(data, notif_list):
        if data is None:
            raise PreventUpdate
        elif data == 'notification_wrong_file_format':
            notification_message = ["Falsches Dateiformat!",
                                    "Diese Datei kann ich leider nicht laden, sie hat das falsche Format!"]
            icon = DashIconify(icon="mdi:file-remove-outline")
            color = 'yellow'
        elif data == 'notification_no_file_selected':
            notification_message = ["Keine Datei ausgewählt!",
                                    "Bitte lade eine Datei hoch."]
            icon = DashIconify(icon="mdi:file-remove-outline")
            color = 'yellow'
        elif data == 'notification_wrong_file':
            notification_message = ["Falsche Datei!",
                                    "Diese Datei ist beschädigt oder enthält nicht alle Daten, die ich brauche."]
            icon = DashIconify(icon="mdi:file-remove-outline")
            color = 'yellow'
        elif data == 'notification_pv_api_error':
            notification_message = ["Fehler Datenabfrage!",
                                    "Die Daten konnten nicht von renewables.ninja abgefragt werden."]
            icon = DashIconify(icon="fa6-solid:solar-panel")
            color = 'red'
        elif data == 'notification_false_postcode':
            notification_message = ["Zustellung nicht möglich!",
                                    "Diese Postleitzahl kenne ich leider nicht."]
            icon = DashIconify(icon="material-symbols:mail-outline-rounded")
            color = 'yellow'
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
        elif data == 'notification_custom_house':
            notification_message = ["So detailliert kann ich (noch) nicht.",
                                    "Es ist bereits ein Haus im Detail konfiguriert. Wenn du das andere Haus löscht oder dort ein fertiges Profil auswählst, kannst du dieses nach deinen Wünschen konfigurieren."]
            icon = DashIconify(icon="mdi:house-group")
            color = 'yellow'
        elif data == 'notification_no_time_input':
            notification_message = ["Keine Zeit!",
                                    "Bitte eine Uhrzeit eingeben."]
            icon = DashIconify(icon="material-symbols:nest-clock-farsight-analog-outline")
            color = 'yellow'
        elif data == 'notification_no_profile_selected':
            notification_message = ["Kein Gerätetyp ausgewählt!",
                                    "Bitte ein Lastprofil auswählen."]
            icon = DashIconify(icon="mdi:chart-bell-curve")
            color = 'yellow'
        elif data == 'notification_no_device_selected':
            notification_message = ["Kein Gerät ausgewählt!",
                                    "Bitte ein Gerät auswählen."]
            icon = DashIconify(icon="material-symbols:device-unknown-outline-rounded")
            color = 'yellow'
        elif data == 'notification_no_room_selected':
            notification_message = ["Kein Raum ausgewählt!",
                                    "Bitte einen Raum im Haus auswählen."]
            icon = DashIconify(icon="material-symbols:meeting-room-outline-rounded")
            color = 'yellow'
        elif data == 'notification_missing_input':
            notification_message = ["Leerer Raum!",
                                    "Mir fehlt eine Information bei deiner Eingabe."]
            icon = DashIconify(icon="ph:shooting-star")
            color = 'yellow'
        elif data == 'notification_error_reading_csv':
            notification_message = ["Fehler beim Lesen der Datei!",
                                    "Scheinbar ist der Inhalt der csv-Datei nicht richtig formatiert."]
            icon = DashIconify(icon="mdi:file-alert-outline")
            color = 'red'
        elif data == 'notification_profile_length':
            notification_message = ["Lastprofil zu lang!",
                                    "Eins der eingelesenen Lastprofile ist zu lang. Die maximale Länge ist ein Tag "
                                    "(1440 Minuten)."]
            icon = DashIconify(icon="mdi:chart-bell-curve")
            color = 'red'
        elif data == 'notification_successful_added':
            notification_message = ["Neues Gerät erfolgreich hinzugefügt!",
                                    "Du findest es unter dem Reiter \"Eigene\"."]
            icon = DashIconify(icon="material-symbols:check-circle-outline-rounded")
            color = 'blue'
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
