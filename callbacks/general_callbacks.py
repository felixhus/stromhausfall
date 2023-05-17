"""
general_callbacks.py contains all dash callbacks for general functions of the app.
"""

import base64
import json

import dash_mantine_components as dmc
from dash import Input, Output, State, ctx, no_update, html, dcc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.modules as modules

# root_path = '/home/stromhausfall/mysite/'
root_path = ''


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
                          children, day, gridObject_dict, year, week, used_profiles, checkbox, figure_pv, figure_house):
        """
        Callback to save all properties of a selected element when save-button or enter was pressed.

        :param btn_save: [Input] Button to save properties
        :param key_save: [Input] Event of Enter-click
        :param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
        :param device_dict: [State] Dictionary containing all devices in the custom house
        :param selected_element_house: [State] Cytoscape element which was clicked in the house
        :param selected_element_grid: [State] Cytoscape element which was clicked in the grid
        :param children: [State] Children of the menu_parent_tabs, all Inputs of the component menu
        :param day: [State] Day selected in the pagination of the menu
        :param gridObject_dict: [State] Dictionary containing all grid objects
        :param year: [State] Year selected in settings
        :param week: [State] Week selected in settings
        :param used_profiles: [State] Already used random profiles from IZES
        :param checkbox: [State] Bool if checkbox to load random profile is checked
        :param figure_pv: [State] Figure element of graph_pv
        :param figure_house: [State] Figure element of graph_house
        :return: store_device_dict > data
        :return: store_grid_object_dict > data
        :return: graph_pv > figure
        :return: graph_house > figure
        :return: store_used_profiles > data
        :return: checkbox_random_profile > checked
        :return: store_save_by_enter > data
        :return: store_notification > data
        """

        try:
            if btn_save is None and key_save is None:  # If button wasn't clicked and enter wasn't pressed
                raise PreventUpdate
            if children[2] is None:  # Catch event that enter was pressed without an open menu
                raise PreventUpdate
            else:
                if tabs_main == 'house1':  # If button was clicked in house mode
                    # Save settings of selected element to device_dict
                    device_dict = modules.save_settings_devices(children[2]['props']['children'], device_dict,
                                                                selected_element_house, 'house1', day)
                    return device_dict, no_update, no_update, no_update, no_update, no_update, None, no_update
                elif tabs_main == 'grid':  # If button was clicked in grid mode
                    if gridObject_dict[selected_element_grid]['object_type'] == 'pv':  # If PV is selected
                        # Get updated gridObject_dict and optional notifications for PV
                        gridObject_dict, notif = modules.save_settings_pv(children[2]['props']['children'],
                                                                          gridObject_dict, selected_element_grid,
                                                                          year, week)
                        # Set plot of pv figure, but invert power for plot
                        figure_pv["data"][0]["y"] = [-i for i in gridObject_dict[selected_element_grid]['power']]
                        if notif is not None:
                            return no_update, no_update, no_update, no_update, no_update, no_update, None, notif
                        else:
                            return no_update, gridObject_dict, figure_pv, no_update, \
                                   no_update, no_update, None, no_update
                    elif gridObject_dict[selected_element_grid]['object_type'] == 'house':  # If House is selected
                        gridObject_dict, used_profiles = modules.save_settings_house(children[2]['props']['children'],
                                                                                     gridObject_dict,
                                                                                     selected_element_grid, year, week,
                                                                                     used_profiles, checkbox)
                        figure_house["data"][0]["y"] = gridObject_dict[selected_element_grid]['power']
                        return no_update, gridObject_dict, no_update, figure_house, \
                               used_profiles, False, None, no_update
                    # If a transformer is selected
                    elif gridObject_dict[selected_element_grid]['object_type'] == 'transformer':
                        childs = children[2]['props']['children']
                        gridObject_dict[selected_element_grid]['name'] = childs[0]['props']['value']
                        gridObject_dict[selected_element_grid]['rating'] = childs[2]['props']['value']
                        return no_update, gridObject_dict, no_update, no_update, no_update, no_update, None, no_update
                    # If a switch cabinet is selected
                    elif gridObject_dict[selected_element_grid]['object_type'] == 'switch_cabinet':
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
                  State('menu_parent_tabs', 'children'),
                  State('store_grid_object_dict', 'data'),
                  State('store_device_dict', 'data'),
                  State('store_selected_element_grid', 'data'),
                  State('store_selected_element_house', 'data'),
                  prevent_initial_call=True)
    def manage_menu_tabs(tab_value_house, tab_value_grid, tabs_main, menu_children, gridObject_dict,
                         device_dict, selected_element_grid, selected_element_house):
        """
        Manages the menu tabs, which are shown when a grid object or house device was clicked.
        It removes all tab panels and creates the new one to show.

        :param tab_value_house: [Input] Updated value of the house menu tab
        :param tab_value_grid: [Input] Updated value of the grid menu tab
        :param tabs_main: [Input] Tab value of main tab, whether grid, house or settings mode is shown
        :param menu_children: [State] Existing tab panels of the menu_parent_tab
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param device_dict: [State] Dictionary containing all devices in the custom house
        :param selected_element_grid: [State] Cytoscape element which was clicked in the grid
        :param selected_element_house: [State] Cytoscape element which was clicked in the house
        :return: menu_parent_tabs > children
        :return: menu_parent_tabs > value
        :return: active_switch_grid > style
        :return: active_switch_house > style
        :return: store_notification > data
        """
        # TODO: Change way of creating tab panels, so that already existing ones are used again
        # This should make the application faster. Instead of popping all existing ones and every time create
        # a new one, check if there already is a tab panel for the clicked component and update this one.

        try:
            triggered_id = ctx.triggered_id
            if triggered_id == 'tabs_main':     # If the main tabs were changed, this controls the active switches
                if tabs_main == 'grid':         # It always shows the right one and hides the other one
                    return no_update, 'empty', {'display': 'block'}, {'display': 'none'}, no_update
                elif tabs_main == 'house1':
                    return no_update, 'empty', {'display': 'none'}, {'display': 'block'}, no_update
                else:
                    raise PreventUpdate
                # If a device in the house was clicked, prepare the variables
            elif triggered_id == 'store_menu_change_tab_house':
                if tab_value_house == 'empty':  # If no tab should be shown, show empty one
                    return no_update, 'empty', no_update, no_update, no_update
                tab_value = tab_value_house
                selected_element = selected_element_house
                elements_dict = device_dict['house1']
                # If a device in the grid was clicked, prepare the variables
            elif triggered_id == 'store_menu_change_tab_grid':
                if tab_value_grid == 'empty':   # If no tab should be shown, show empty one
                    return no_update, 'empty', no_update, no_update, no_update
                tab_value = tab_value_grid
                selected_element = selected_element_grid
                elements_dict = gridObject_dict
            else:
                raise PreventUpdate
            while len(menu_children) > 2:  # Remove all tabs except the 'empty' tab and the 'init_ids' tab
                menu_children.pop()
            # Create new tab panel
            new_tab_panel = dash_components.add_menu_tab_panel(tab_value, selected_element, elements_dict)
            menu_children = menu_children + [new_tab_panel]  # Add children of new tab panel
            return menu_children, tab_value, no_update, no_update, no_update
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('modal_readme', 'opened'),
                  Input('button_readme', 'n_clicks'),
                  prevent_initial_call=True)
    def open_readme(btn):
        """
        Opens the readme modal.

        :param btn: [Input] Button Readme input
        :return: True to open readme
        :rtype: bool
        """

        if btn is not None:
            return True
        else:
            raise PreventUpdate

    @app.callback(Output('drawer_notifications', 'opened'),
                  Input('button_notifications', 'n_clicks'))
    def open_drawer_notifications(btn):
        """
        Opens the data drawer when button is clicked.

        :param btn: [Input] Button Notification input
        :return: True to open drawer
        :rtype: bool
        """

        if btn is not None:
            return True
        else:
            raise PreventUpdate

    @app.callback(Output('modal_start', 'opened'),
                  Input('button_start', 'n_clicks'),
                  Input('button_start_load', 'n_clicks'))
    def open_start_card(btn, btn_load):
        """
        Closes the start modal which is shown on loading the app.

        :param btn: [Input] Button to start the app
        :param btn_load: [Input] Button to load a configuration
        :return: False to close the modal
        :rtype: bool
        """

        if btn is not None or btn_load is not None:
            return False
        else:
            raise PreventUpdate

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
        """
        Store the settings to the dcc store object if changed.

        :param week: [Input] Week of the year
        :param year: [Input] Year to get data from
        :param settings_dict: DCC store object to save to
        :return: store_settings > data
        """

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
                  elements_grid, elements_bath, elements_kitchen, elements_livingroom, elements_office,
                  filename, upload_content, settings_dict, custom_house, own_devices):
        """
        Handles all functions of the main menu (burger menu in the navbar). It saves the configuration to a
        download-json file or loads an uploaded one. Also, it is handles the download of created own devices.

        :param btn_save: [Input] Main Menu button to save a configuration
        :param btn_load_menu: [Input] Main menu button to load a configuration
        :param btn_own: [Input] Main menu button to download own devices
        :param btn_load: [Input] Start Modal load button
        :param btn_start_load: [Input] Button to start the upload of a configuration file
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param device_dict: [State] Dictionary containing all house devices and their properties
        :param elements_grid: [State] Elements of grid cytoscape
        :param elements_bath: [State] Elements of bathroom cytoscape
        :param elements_kitchen: [State] Elements of kitchen cytoscape
        :param elements_livingroom: [State] Elements of livingroom cytoscape
        :param elements_office: [State] Elements of office cytoscape
        :param filename: [State] Filename of uploaded file
        :param upload_content: [State] Content of uploaded file
        :param settings_dict: [State] Dictionary containing the settings
        :param custom_house: [State] Id of custom house
        :param own_devices: [State] Dictionary containing all own devices
        :return: download_json > data
        :return: modal_load_configuration > opened
        :return: store_grid_object_dict > data
        :return: store_device_dict > data
        :return: cyto_grid > elements
        :return: cyto_bathroom > elements
        :return: cyto_livingroom > elements
        :return: cyto_kitchen > elements
        :return: cyto_office > elements
        :return: input_week > value
        :return: input_year > value
        :return: store_custom_house > data
        :return: tab_house > disabled
        :return: store_notification > data
        """

        try:
            triggered_id = ctx.triggered_id
            if triggered_id == 'menu_item_save':
                save_dict = {'gridObject_dict': gridObject_dict,    # Collect all important data in one dictionary
                             'device_dict': device_dict,
                             'cyto_grid': elements_grid,
                             'cyto_bathroom': elements_bath,
                             'cyto_kitchen': elements_kitchen,
                             'cyto_livingroom': elements_livingroom,
                             'cyto_office': elements_office,
                             'settings': settings_dict,
                             'custom_house': custom_house}
                # Give collected data to download component
                return dict(content=json.dumps(save_dict), filename="konfiguration.json"), \
                       no_update, no_update, no_update, no_update, no_update, no_update, \
                       no_update, no_update, no_update, no_update, no_update, no_update, no_update
            elif triggered_id == 'menu_item_own_devices':
                save_dict = {'own_devices_dict': own_devices}   # Create dictionary with own devices in it
                # Give collected data to download component
                return dict(content=json.dumps(save_dict), filename="eigene_geraete.json"), \
                       no_update, no_update, no_update, no_update, no_update, no_update, \
                       no_update, no_update, no_update, no_update, no_update, no_update, no_update
            elif triggered_id == 'menu_item_load' or triggered_id == 'button_start_load':
                # If one of the buttons to load a configuration was clicked, open the loading modal
                return no_update, True, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                       no_update, no_update, no_update, no_update, no_update
            elif triggered_id == 'button_load_configuration':
                # If the button in the loading modal to load a configuration was clicked, start the loading procedure
                if filename is None:    # Check if a file was uploaded
                    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                           no_update, no_update, no_update, no_update, no_update, 'notification_no_file_selected'
                if not filename.endswith('.json'):  # Check if the file format is .json
                    return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                           no_update, no_update, no_update, no_update, no_update, 'notification_wrong_file_format'
                else:
                    content_type, content_string = upload_content.split(",")  # Three lines to get dict from content
                    decoded = base64.b64decode(content_string)
                    content_dict = json.loads(decoded)
                    # Check if there is a custom house existing, if so, activate house tab
                    custom_house_disabled = True
                    if content_dict['device_dict']['house1'] is not None:
                        custom_house_disabled = False
                    if not ('gridObject_dict' in content_dict and   # Check if all needed dictionaries are there
                            'device_dict' in content_dict and 'cyto_grid' in content_dict):
                        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                               no_update, no_update, no_update, no_update, no_update, 'notification_wrong_file'
                    # write all read data into the dash components
                    return no_update, False, content_dict['gridObject_dict'], content_dict['device_dict'], \
                           content_dict['cyto_grid'], content_dict['cyto_bathroom'], content_dict['cyto_kitchen'], \
                           content_dict['cyto_livingroom'], content_dict['cyto_office'], \
                           content_dict['settings']['week'], content_dict['settings']['year'], \
                           content_dict['custom_house'], custom_house_disabled, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update, no_update, no_update, no_update, no_update, no_update
        except Exception as err:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, \
                   no_update, no_update, no_update, no_update, no_update, err.args[0]

    @app.callback(Output('text_filename_load', 'children'),
                  Input('upload_configuration', 'filename'),
                  prevent_initial_call=True)
    def filename_upload(filename):
        """
        Shows the filename of an uploaded file below the upload area to show the user that it was uploaded.

        :param filename: [Input] Filename of uploaded file
        :return: text_filename_load > children
        """

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
        """
        Updates all components with the new settings.

        :param btn_update: [Input] Button to update the settings
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param week: [State] Input week of year
        :param year: [State] Input year
        :return: store_device_dict > data
        :return: store_grid_object_dict > data
        :return: store_notification > data
        """
        # TODO: Implement update of settings properly. Also see modules>update_settings
        # Does not work yet, not in use, button_update_settings is disabled

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
        """
        Stores all relevant data in DCC store components, which stays stored for the whole session, even on a reload.
        Is triggered by an intervall (e.g. every 10 seconds).

        :param interval: [Input] Interval to trigger the backup
        :param gridObject_dict: [State] Dictionary containing all grid objects and their properties
        :param device_dict: [State] Dictionary containing all house devices and their properties
        :param elements_grid: [State] Elements of grid cytoscape
        :param elements_bath: [State] Elements of bathroom cytoscape
        :param elements_kitchen: [State] Elements of kitchen cytoscape
        :param elements_livingroom: [State] Elements of livingroom cytoscape
        :param elements_office: [State] Elements of office cytoscape
        :param settings_dict: [State] Dictionary containing the settings
        :param custom_house: [State] Id of custom house
        :return: store_backup > data
        """

        save_dict = {'gridObject_dict': gridObject_dict,    # Collect all relevant data in a dictionary
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
                  Output('cyto_livingroom', 'elements', allow_duplicate=True),
                  Output('cyto_kitchen', 'elements', allow_duplicate=True),
                  Output('cyto_office', 'elements', allow_duplicate=True),
                  Output('input_week', 'value', allow_duplicate=True),
                  Output('input_year', 'value', allow_duplicate=True),
                  Output('store_custom_house', 'data', allow_duplicate=True),
                  Output('tab_house', 'disabled', allow_duplicate=True),
                  Output('modal_start', 'opened', allow_duplicate=True),
                  Input('interval_refresh', 'n_intervals'),
                  State('store_backup', 'data'),
                  prevent_initial_call=True)
    def refresh(interval, backup_dict):
        """
        Loads all backup data on a refresh, if existing. Is triggered once by an interval. Closes the start-modal
        if it is a refresh with backup data.

        :param interval: [Input] Interval which is only triggered once at a refresh
        :param backup_dict: [State] Stored backup data
        :return: store_grid_object_dict > data
        :return: store_device_dict > data
        :return: cyto_grid > elements
        :return: cyto_bathroom > elements
        :return: cyto_livingroom > elements
        :return: cyto_kitchen > elements
        :return: cyto_office > elements
        :return: input_week > value
        :return: input_year > value
        :return: store_custom_house > data
        :return: tab_house > disabled
        :return: modal_start > opened
        """

        if backup_dict is not None:
            backup_dict = json.loads(backup_dict)
            custom_house_disabled = True
            if backup_dict['custom_house'] is not None:
                custom_house_disabled = False
            return backup_dict['gridObject_dict'], backup_dict['device_dict'], \
                   backup_dict['cyto_grid'], backup_dict['cyto_bathroom'], backup_dict['cyto_livingroom'], \
                   backup_dict['cyto_kitchen'], backup_dict['cyto_office'], \
                   backup_dict['settings']['week'], backup_dict['settings']['year'], backup_dict['custom_house'], \
                   custom_house_disabled, False
        else:
            raise PreventUpdate

    @app.callback(Output('store_save_by_enter', 'data'),
                  Input('key_event_listener', 'n_events'),
                  State('key_event_listener', 'event'),
                  prevent_initial_call=True)
    def enter_save(key_n, key_event):
        """
        Listen to Enter events and change store_save_by_enter to trigger save action.

        :param key_n: [Input] Key event listener n_events
        :param key_event: [State] Key event listener event
        :return: store_save_by_enter > data
        """

        if key_event['key'] == 'Enter':
            return 'pressed'
        else:
            raise PreventUpdate

    @app.callback(Output('card_tutorial', 'style'),
                  Output('store_tutorial', 'data'),
                  Output('pagination_tutorial', 'total'),
                  Output('card_tutorial_content', 'children'),
                  Input('button_tutorial', 'n_clicks'),
                  Input('pagination_tutorial', 'page'),
                  State('card_tutorial', 'style'),
                  State('store_tutorial', 'data'),
                  prevent_initial_call=True)
    def control_tutorial(btn, page, style, tutorial_steps):
        """
        Opens or closes the tutorial on button click.

        :param btn: [Input] "Tutorial" button
        :param page: [Input] Pagination selection of tutorial step
        :param style: [State] Opening status stored in the style property
        :param tutorial_steps: [State] List of tutorial steps and help
        :return: card_tutorial > style
        :return: store_tutorial > data
        :return: pagination_tutorial > total
        :return: card_tutorial_content > children
        """

        triggered_id = ctx.triggered_id
        if triggered_id == 'button_tutorial':
            if style['display'] == 'none':
                if tutorial_steps is None:
                    tutorial_steps = modules.extract_tutorial_steps(root_path + 'docs/tutorial.md')
                heading = "Tutorial - " + tutorial_steps[page - 1][0]
                body = tutorial_steps[page - 1][1]
                content = [html.B(heading), html.Div(body)]
                return {'display': 'block'}, tutorial_steps, len(tutorial_steps), content
            else:
                return {'display': 'none'}, no_update, no_update, no_update
        elif triggered_id == 'pagination_tutorial':
            heading = "Tutorial - " + tutorial_steps[page-1][0]
            body = tutorial_steps[page-1][1]
            content = [html.B(heading), html.Div(body)]
            return no_update, no_update, no_update, content
        elif triggered_id == 'help_tutorial':
            raise PreventUpdate
        else:
            raise PreventUpdate

    @app.callback(Output('drawer_help', 'opened'),
                  Output('drawer_help', 'children'),
                  Input('help_tutorial', 'n_clicks'),
                  State('store_tutorial', 'data'),
                  State('pagination_tutorial', 'page'),
                  prevent_initial_call=True)
    def help_tutorial(btn, tutorial_steps, page):
        """
        Opens the help drawer and loads the help of the current tutorial step into it.

        :param btn: [Input] Help button
        :param tutorial_steps: [State] List of tutorial steps and help
        :param page: [State] Selected page/step of the tutorial
        :return:
        """

        if btn is not None:
            return True, dcc.Markdown(tutorial_steps[page-1][2])

    @app.callback(Output('notification_container', 'children'),
                  Output('drawer_notifications', 'children'),
                  Output('badge_notifications', 'children'),
                  Input('store_notification', 'data'),
                  State('drawer_notifications', 'children'))
    def notification(notification_data, notif_list):
        """
        Handles all notifications raised. If it is a predefined notification, the text, icon and color is fetched
        and the notification is found. If not, the notification_data itself is shown in the notification.
        Also, the notification is added to the list in the drawer and the pill showing the number of notifications
        is updated.

        :param notification_data: [Input] Raised notification data
        :param notif_list: [State] List of notifications raised before
        :return: notification_container > children
        :return: drawer_notifications > children
        :return: badge_notifications > children
        """

        duration = 5000     # Duration of notification shown in the right bottom corner of the app
        if notification_data is None:
            raise PreventUpdate
        elif notification_data == 'notification_wrong_file_format':
            notification_message = ["Falsches Dateiformat!",
                                    "Diese Datei kann ich leider nicht laden, sie hat das falsche Format!"]
            icon = DashIconify(icon="mdi:file-remove-outline")
            color = 'yellow'
        elif notification_data == 'notification_no_file_selected':
            notification_message = ["Keine Datei ausgewählt!",
                                    "Bitte lade eine Datei hoch."]
            icon = DashIconify(icon="mdi:file-remove-outline")
            color = 'yellow'
        elif notification_data == 'notification_wrong_file':
            notification_message = ["Falsche Datei!",
                                    "Diese Datei ist beschädigt oder enthält nicht alle Daten, die ich brauche."]
            icon = DashIconify(icon="mdi:file-remove-outline")
            color = 'yellow'
        elif notification_data == 'notification_pv_api_error':
            notification_message = ["Fehler Datenabfrage!",
                                    "Die Daten konnten nicht von renewables.ninja abgefragt werden."]
            icon = DashIconify(icon="fa6-solid:solar-panel")
            color = 'red'
        elif notification_data == 'notification_false_postcode':
            notification_message = ["Zustellung nicht möglich!",
                                    "Diese Postleitzahl kenne ich leider nicht."]
            icon = DashIconify(icon="material-symbols:mail-outline-rounded")
            color = 'yellow'
        elif notification_data == 'notification_false_connection':
            notification_message = ["Kabelsalat!",
                                    "Zwischen diesen beiden Komponenten kannst du keine Leitung ziehen."]
            icon = DashIconify(icon="mdi:connection")
            color = 'yellow'
        elif notification_data == 'notification_isolates':
            notification_message = ["Kein Netz!", "Es gibt Knoten, die nicht mit dem Netz verbunden sind!"]
            icon = DashIconify(icon="material-symbols:group-work-outline")
            color = 'red'
        elif notification_data == 'notification_emptygrid':
            notification_message = ["Blackout!", "Hier muss erst noch ein Netz gebaut werden!"]
            icon = DashIconify(icon="uil:desert")
            color = 'yellow'
        elif notification_data == 'notification_cycles':
            notification_message = ["Achtung (kein) Baum!", "Das Netz beinhaltet parallele Leitungen oder Zyklen, "
                                                            "dies ist leider noch nicht unterstützt."]
            icon = DashIconify(icon="ph:tree")
            color = 'red'
        elif notification_data == 'notification_custom_house':
            notification_message = ["So detailliert kann ich (noch) nicht.",
                                    "Es ist bereits ein Haus im Detail konfiguriert. "
                                    "Wenn du das andere Haus löscht oder dort ein fertiges Profil auswählst, "
                                    "kannst du dieses nach deinen Wünschen konfigurieren."]
            icon = DashIconify(icon="mdi:house-group")
            color = 'yellow'
        elif notification_data == 'notification_no_time_input':
            notification_message = ["Keine Zeit!",
                                    "Bitte eine Uhrzeit eingeben."]
            icon = DashIconify(icon="material-symbols:nest-clock-farsight-analog-outline")
            color = 'yellow'
        elif notification_data == 'notification_no_profile_selected':
            notification_message = ["Kein Gerätetyp ausgewählt!",
                                    "Bitte ein Lastprofil auswählen."]
            icon = DashIconify(icon="mdi:chart-bell-curve")
            color = 'yellow'
        elif notification_data == 'notification_no_device_selected':
            notification_message = ["Kein Gerät ausgewählt!",
                                    "Bitte ein Gerät auswählen."]
            icon = DashIconify(icon="material-symbols:device-unknown-outline-rounded")
            color = 'yellow'
        elif notification_data == 'notification_no_room_selected':
            notification_message = ["Kein Raum ausgewählt!",
                                    "Bitte einen Raum im Haus auswählen."]
            icon = DashIconify(icon="material-symbols:meeting-room-outline-rounded")
            color = 'yellow'
        elif notification_data == 'notification_missing_input':
            notification_message = ["Leerer Raum!",
                                    "Mir fehlt eine Information bei deiner Eingabe."]
            icon = DashIconify(icon="ph:shooting-star")
            color = 'yellow'
        elif notification_data == 'notification_error_reading_csv':
            notification_message = ["Fehler beim Lesen der Datei!",
                                    "Scheinbar ist der Inhalt der csv-Datei nicht richtig formatiert."]
            icon = DashIconify(icon="mdi:file-alert-outline")
            color = 'red'
        elif notification_data == 'notification_profile_length':
            notification_message = ["Lastprofil zu lang!",
                                    "Eins der eingelesenen Lastprofile ist zu lang. Die maximale Länge ist ein Tag "
                                    "(1440 Minuten)."]
            icon = DashIconify(icon="mdi:chart-bell-curve")
            color = 'red'
        elif notification_data == 'notification_successful_added':
            notification_message = ["Neues Gerät erfolgreich hinzugefügt!",
                                    "Du findest es unter dem Reiter \"Eigene\"."]
            icon = DashIconify(icon="material-symbols:check-circle-outline-rounded")
            color = 'blue'
        else:
            notification_message = ["Fehler!", notification_data]
            icon = DashIconify(icon="material-symbols:warning-outline-rounded")
            color = 'red'
        # Append new notification to list of notifications shown in the drawer
        notif_list.append(dmc.Alert(notification_message[1], title=notification_message[0], color=color,
                                    withCloseButton=True))
        return dmc.Notification(title=notification_message[0],
                                message=notification_message[1],
                                action='show', color=color, autoClose=duration,
                                icon=icon, id='notification_data'), \
               notif_list, len(notif_list)
