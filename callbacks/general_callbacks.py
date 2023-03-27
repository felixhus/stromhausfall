import dash_mantine_components as dmc
from dash import Input, Output, State, ctx, no_update
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import source.dash_components as dash_components
import source.modules as modules


def general_callbacks(app):
    @app.callback(Output('store_results_house', 'data'),
                  Output('graph_power_house', 'figure'),
                  Output('graph_sunburst_house', 'figure'),
                  Output('store_notification6', 'data'),
                  Input('button_calculate', 'n_clicks'),
                  State('store_device_dict', 'data'),
                  State('tabs_main', 'value'),
                  prevent_initial_call=True)
    def start_calculation_house(btn, device_dict, tabs_main):
        try:
            if tabs_main == 'house1':
                graph_power, graph_sunburst = modules.calculate_house(device_dict, range(0, 1440))
                return None, graph_power, graph_sunburst, no_update
            else:
                raise PreventUpdate
        except PreventUpdate:
            return no_update, no_update
        except Exception as err:
            return no_update, err.args[0]

    @app.callback(Output('menu_parent_tabs', 'children'),
                  Output('menu_parent_tabs', 'value'),
                  Output('active_switch_grid', 'style'),
                  Output('active_switch_house', 'style'),
                  Output('store_notification5', 'data'),
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
    def manage_menu_containers(tab_value_house, tab_value_grid, tabs_main, switch_state, menu_children, gridObject_dict,
                               device_dict, selected_element_grid, selected_element_house):
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
            while len(menu_children) > 1:  # Remove all tabs except the 'empty' tab
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
                  Output('store_notification7', 'data'),
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

    @app.callback(Output('notification_container', 'children'),
                  Output('drawer_notifications', 'children'),
                  Output('bade_notifications', 'children'),
                  Input('store_notification1', 'data'),
                  Input('store_notification2', 'data'),
                  Input('store_notification3', 'data'),
                  Input('store_notification4', 'data'),
                  Input('store_notification5', 'data'),
                  Input('store_notification6', 'data'),
                  Input('store_notification7', 'data'),
                  Input('store_notification8', 'data'),
                  State('drawer_notifications', 'children'))
    def notification(data1, data2, data3, data4, data5, data6, data7, data8, notif_list):
        triggered_id = ctx.triggered_id
        if triggered_id == 'store_notification1':
            data = data1
        elif triggered_id == 'store_notification2':
            data = data2
        elif triggered_id == 'store_notification3':
            data = data3
        elif triggered_id == 'store_notification4':
            data = data4
        elif triggered_id == 'store_notification5':
            data = data5
        elif triggered_id == 'store_notification6':
            data = data6
        elif triggered_id == 'store_notification7':
            data = data7
        elif triggered_id == 'store_notification8':
            data = data8
        else:
            raise PreventUpdate
        if data is None:
            raise PreventUpdate
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
            notification_message = ["So detailliert kann ich (noch) nicht.", "Es ist bereits ein Hause im Detail konfiguriert. Wenn du das andere Haus löscht oder dort ein fertiges Profil auswählst, kannst du dieses nach deinen Wünschen konfigurieren."]
            icon = DashIconify(icon="mdi:house-group")
            color = 'yellow'
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

    @app.callback(Output('drawer_notifications', 'opened'),
                  Input('button_notifications', 'n_clicks'))
    def open_drawer_notifications(btn):
        if btn is not None:
            return True
        else:
            raise PreventUpdate

    @app.callback(Output('modal_start', 'opened'),
                  Input('button_start', 'n_clicks'))
    def open_menu_card(btn):
        if btn is not None:
            return False
        else:
            raise PreventUpdate

    @app.callback(Output('graph_device', 'figure'),
                  Input('store_device_dict', 'data'),
                  State('store_selected_element_house', 'data'),
                  State('graph_device', 'figure'),
                  prevent_initial_call=True)
    def update_figure(data, selected_element, figure):  # Update the values of the graphs if another profile is chosen
        # patched_fig = Patch()
        # Patch scheint noch nicht zu funktionieren, vielleicht später nochmal probieren
        if selected_element in data['house1']:  # Check if element is still in dict or if it was deleted
            figure["data"][0]["y"] = data['house1'][selected_element]['power']
        else:
            raise PreventUpdate
        return figure

    @app.callback(Output('modal_timeseries', 'opened'),
                  Output('timeseries_table', 'data'),
                  Input('pill_add_profile', 'n_clicks'),
                  Input('button_add_value', 'n_clicks'),
                  Input('button_save_profile', 'n_clicks'),
                  State('timeseries_table', 'data'),
                  State('textinput_profile_name', 'value'),
                  prevent_initial_call=True)
    def modal_timeseries(pill, btn_add, btn_save, rows, name):
        triggered_id = ctx.triggered_id
        if triggered_id == 'pill_add_profile':  # Open modal to add timeseries
            if pill is not None:
                return True, no_update
            else:
                raise PreventUpdate
        elif triggered_id == 'button_add_value':  # Add one empty row to the data table
            rows.append({'time': '', 'power': ''})
            return no_update, rows
        elif triggered_id == 'button_save_profile':
            # Funktionen zum Interpolieren und in Datenbank schreiben existieren in "sql_modules".
            # Problem: Ich kann die neuen Lastprofile eigentlich nicht in die SQL-Datenbank schreiben, da die dann
            # für alle verändert wird.
            return False, no_update
        else:
            raise PreventUpdate
