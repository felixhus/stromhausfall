# !!! THIS FILE IS ONLY FOR DOCUMENTATION PURPOSES. IT CONTAINS NO CODE!!!
"""
house_callbacks.py contains all dash callbacks for house functions of the app.
""" 


def initial_room_configuration(interval, backup, cyto_bathroom, cyto_livingroom, cyto_kitchen, cyto_office, device_dict):
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
:return: cyto_bathroom > data
:return: cyto_livingroom > data
:return: cyto_kitchen > data
:return: cyto_office > data
:return: store_device_dict > data
"""
    pass

def start_calculation_house(btn, device_dict, tabs_main, gridObject_dict, house):
    """
Start the calculation of the powers and energys in the rooms of the house.

:param btn: [Input] Button to start calculation
:param device_dict: [State] Dictionary containing all devices in the custom house
:param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
:param gridObject_dict: [State] Dictionary containing all grid objects and their properties
:param house: [State] Id of custom house
:return: store_results_house_power > data
:return: store_results_house_energy > data
:return: graph_power_house > figure
:return: graph_sunburst_house > figure
:return: result_parent_tabs > value
:return: tabs_menu > value
:return: store_grid_object_dict > data
:return: store_notification > data
"""
    pass

def cost_result(data, cost_kwh, device_dict):
    """
Calculates the yearly energy costs for each device, fetches the dash components and displays them
in the cost tab.

:param data: [Input] Energy result data of house calculation
:param cost_kwh: [State] Cost of 1 kWh of electrical energy, from settings
:param device_dict: [State] Dictionary containing all devices in the custom house
:return: cost_tab > children
:return: store_notification > data
"""
    pass

def fill_additional_device_modal(modal_open, radio_room):
    """
Load all devices from sql database and show them as additional devices in the additional devices modal.

:param modal_open: [Input] The opening of the modal_additional_devices triggers this callback
:param radio_room: [State] Selected room by radiogroup
:return: card_additional_devices > children
"""
    pass

def add_additional_device_check(btn, radio_device, radio_room):
    """
Callback to check whether a device and room was selected wenn the "add" button is clicked. If not,
return corresponding notifications. It also closes the modal after.

:param btn: [Input] Button to add an additional device
:param radio_device: [State] Selected device type
:param radio_room: [State] Selected room
:return: modal_additional_devices > opened
"""
    pass

def load_own_devices(btn_load, tab, filename, upload_content, own_device_dict):
    """
Callback to upload own devices, show them or to show already uploaded ones.

:param btn_load: [Input] Button to load the own devices from file
:param tab: [Input] Tab value of additional devices modal
:param filename: [Input] Filename of uploaded file
:param upload_content: [State] Content of uploaded file
:param own_device_dict: [State] Dictionary to store the own devices
:return: store_own_device_dict > data
:return: text_filename_load_own > children
:return: card_own_devices_add > children
:return: card_own_devices_load > style
:return: store_notification > data
"""
    pass

def add_new_device(btn_add, filename, input_name, input_menu_type, input_icon, own_device_dict, upload_content):
    """
Callback to add a new custom device to the app. The user has to input the name, type, icon and a file, which
contains the power profiles in Watts. There are two possibilities for this file:

* CSV-File: First column are timestamps. Every following column is read as a separate power profile
* XLS-File: First column are timestamps. Every following column is read as a separate power profile.

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
:return: store_own_devices_dict > data
:return: text_filename_load_new > children
:return: store_notification > data
"""
    pass

def update_figure_house(data, day_control, selected_element, figure, day):
    """
Update the values of the device graph if another day is chosen to be shown or the device dict is changed.

:param data: [Input] Dictionary containing all house devices and their properties
:param day_control: [Input] Day from pagination below device power profile
:param selected_element: [State] Cytoscape element which was clicked in the house
:param figure: [State] Figure of graph which shows power profile of device
:param day: [State] Day from pagination below device power profile
:return: graph_device > figure
"""
    pass

def update_figure_devices(day, figure):
    """
Update the values of the result graphs if another day is chosen to be shown.
Also opens the modal with the full screen graph if the total timeframe is selected.

:param day: [Input] Selected day of the pagination below a figure
:param figure: [State] Figure to update
:return: graph_power_house > figure
:return: graph_modal > figure
:return: modal_graph > opened
"""
    pass

def show_legend(checkbox, figure):
    """
Controls the visibility of the legend of the graph_power_house figure.

:param checkbox: [Input] Input if legend should be visible
:param figure: [State] Figure which the legend belongs to
:return: Boolean if the legend should be visible
:rtype: bool
"""
    pass

def update_new_icon(icon):
    """
Returns a dash iconify icon as the icon of the text input, if the content of the input was changed to another
icon name.

:param icon: [Input] Text input with icon name
:return: input_new_icon > icon
"""
    pass
