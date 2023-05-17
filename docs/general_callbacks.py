# !!! THIS FILE IS ONLY FOR DOCUMENTATION PURPOSES. IT CONTAINS NO CODE!!!
"""
general_callbacks.py contains all dash callbacks for general functions of the app.
""" 


def save_props_action(btn_save, key_save, tabs_main, device_dict, selected_element_house, selected_element_grid, children, day, gridObject_dict, year, week, used_profiles, checkbox, figure_pv, figure_house):
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
    pass

def manage_menu_tabs(tab_value_house, tab_value_grid, tabs_main, menu_children, gridObject_dict, device_dict, selected_element_grid, selected_element_house):
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
    pass

def open_readme(btn):
    """
Opens the readme modal.

:param btn: [Input] Button Readme input
:return: True to open readme
:rtype: bool
"""
    pass

def open_drawer_notifications(btn):
    """
Opens the data drawer when button is clicked.

:param btn: [Input] Button Notification input
:return: True to open drawer
:rtype: bool
"""
    pass

def open_start_card(btn, btn_load):
    """
Closes the start modal which is shown on loading the app.

:param btn: [Input] Button to start the app
:param btn_load: [Input] Button to load a configuration
:return: False to close the modal
:rtype: bool
"""
    pass

def settings(week, year, settings_dict):
    """
Store the settings to the dcc store object if changed.

:param week: [Input] Week of the year
:param year: [Input] Year to get data from
:param settings_dict: DCC store object to save to
:return: store_settings > data
"""
    pass

def main_menu(btn_save, btn_load_menu, btn_own, btn_load, btn_start_load, gridObject_dict, device_dict, elements_grid, elements_bath, elements_kitchen, elements_livingroom, elements_office, filename, upload_content, settings_dict, custom_house, own_devices):
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
    pass

def filename_upload(filename):
    """
Shows the filename of an uploaded file below the upload area to show the user that it was uploaded.

:param filename: [Input] Filename of uploaded file
:return: text_filename_load > children
"""
    pass

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
    pass

def backup(interval, gridObject_dict, device_dict, elements_grid, elements_bath, elements_kitchen, elements_livingroom, elements_office, settings_dict, custom_house):
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
    pass

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
    pass

def enter_save(key_n, key_event):
    """
Listen to Enter events and change store_save_by_enter to trigger save action.

:param key_n: [Input] Key event listener n_events
:param key_event: [State] Key event listener event
:return: store_save_by_enter > data
"""
    pass

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
    pass

def help_tutorial(btn, tutorial_steps, page):
    """
Opens the help drawer and loads the help of the current tutorial step into it.

:param btn: [Input] Help button
:param tutorial_steps: [State] List of tutorial steps and help
:param page: [State] Selected page/step of the tutorial
:return:
"""
    pass

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
    pass
