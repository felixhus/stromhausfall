# !!! THIS FILE IS ONLY FOR DOCUMENTATION PURPOSES. IT CONTAINS NO CODE!!!
"""
grid_callbacks.py contains all dash callbacks for grid functions of the app.
""" 


def start_calculation_grid(btn, elements, gridObject_dict, tabs_main):
    """
Starts the calculation of the grid and calls all necessary functions.

:param btn: [Input] Button to start calculation
:param elements: [State] Elements of grid cytoscape
:param gridObject_dict: [State] Dictionary containing all grid objects and their properties
:param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
:return: store_flow_data > data
:return: tabs_menu > value
:return: result_parent_tabs > value
:return: cyto_grid > stylesheet
:return: cyto_grid > elements
:return: timestep_slider > max
:return: store_edge_labels > data
:return: store_notification > data
"""
    pass

def update_labels(slider, flow):
    """
If flow was calculated and the slider set to a new timestep, this function generates the cytoscape edge labels
for this timestep from the flow results. It rounds them and get the power, which is taken or given to the
external grid. This is then shown on the alert components in the grid result section.

:param slider: [Input] Timestep set by slider
:param flow: [State] The calculated flow data
:return: alert_externalgrid > children
:return: store_edge_labels > data
:return: store_notification > data
"""
    pass

def edit_grid(btn_add, node, btn_delete, btn_line, button_hv, button_lv, elements, gridObject_dict, btn_line_active, start_of_line, selected_element, node_ids, tabs_main):
    """
This callback manages all the edit action of the grid cytoscape. It adds new nodes and lines and
deletes them if wanted.

:param btn_add: [Input] Id of pressed add object button
:param node: [Input] Pressed node of cyto_grid
:param btn_delete: [Input] Button to delete an object
:param btn_line: [Input] Button to activate line edit mode
:param button_hv: [Input] Button to select the high voltage side of the transformer
:param button_lv: [Input] Button to select the low voltage side of the transformer
:param elements: [State] Elements of grid cytoscape
:param gridObject_dict: [State] Dictionary containing all grid objects and their properties
:param btn_line_active: [State] Status of the line edit mode
:param start_of_line: [State] First clicked node to add a line
:param selected_element: [State] Selected element of the cyto_grid
:param node_ids: [State] Two node ids of nodes to connect, but voltage has to be set
:param tabs_main: [State] Tab value of main tab, whether grid, house or settings mode is shown
:return: cyto_grid > elements
:return: store_grid_object_dict > data
:return: start_of_line > data
:return: store_element_deleted > data,
:return: store_notification > data
:return: store_get_voltage > data
:return: modal_voltage > opened
"""
    pass

def edit_grid_objects(node, edge, element_deleted, control, selected_element, gridObject_dict, btn_line_active, custom_house):
    """
Callback which controls what happens when nodes or edges in the grid are clicked. Also, this callback handles
the selection of the house mode (preset or custom). If an element is deleted, it closes the connected tab.

:param node: [Input] Clicked node of cytoscape
:param edge: [Input] Clicked edge of cytoscape
:param element_deleted: [Input] Id of the element which was deleted
:param control: [Input] Segmented control if house mode is preset or custom
:param selected_element: [State] Selected element of the cyto_grid
:param gridObject_dict: [State] Dictionary containing all grid objects and their properties
:param btn_line_active: [State] Status of the line edit mode
:param custom_house: [State] Id of custom configured house
:return: store_grid_object_dict > data
:return: store_menu_change_tab_grid > data
:return: cyto_grid > tapNodeData,
:return: cyto_grid > tapEdgeData
:return: store_selected_element_grid > data
:return: tabs_main > value
:return: house_fade > is_in,
:return: store_custom_house > data
:return: tab_house > disabled
:return: house_mode > value
:return: store_notification > data
"""
    pass

def edge_labels(labels, elements):
    """
Takes generated edge labels, sets them for each edge, sets the direction of the edge arrow and returns
the updates cytoscape elements.

:param labels: [Input] Generated edge labels
:param elements: [State] Cytoscape grid elements
:return: cyto_grid > elements
"""
    pass

def time_slider(slider, year, week):
    """
If the slider selects a new timestep, this callback displays the weekday, date and time of the step
in the grid result section.

:param slider: [Input] Timestep slider value
:param year: [State] Year from settings
:param week: [State] Week of the year from settings
:return: alert_time > children
"""
    pass

def compass_action(gridObject_dict, selected_element):
    """
If a button of the PV compass was clicked, the corresponding orientation is written to the PV object
and the compass needle is rotated to the clicked orientation.

:param gridObject_dict: [State] Dictionary containing all grid objects and their properties
:param selected_element: [State] Cytoscape element which was clicked in the grid
:param args: [Input] One Input per button of the compass
:return: store_grid_object_grid > data
:return: button_compass > style
"""
    pass

def edit_mode(btn_line, n_events, event, btn_active):
    """
This callback activates or deactivates the line edit mode with the line button and the ESC key.
It also sets the style of the button if it is activated or not.

:param btn_line: [Input] Button to add a line between grid objects
:param n_events: [Input] Key event listener n_events
:param event: [State] Key event listener event
:param btn_active: [State] Status of line edit mode
:return: cyto_grid > autoungrabify
:return: store_line_edit_active > data
:return: button_line > variant
"""
    pass

def custom_house_style(selected_element, elements):
    """
Sets the style of a house which is selected as custom. It changes the shape from a rounded rectangle to a
normal one.

:param selected_element: [Input] Id of house which was selected as custom
:param elements: [State]
:return: cyto_grid > elements
"""
    pass

def button_add_pressed():
    """
Takes the id of a pressed button to add a grid object and passes it to the store element. A change of this
then triggers another callback to add the object.

:param args: [Input] Add grid object buttons
:return: store_add_node > data
"""
    pass
