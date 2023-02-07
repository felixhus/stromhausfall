from source.modules import (generate_grid_object, get_last_id,
                            get_object_from_id)


def simple_grid(app):
    elements = []
    gridObject_list = []
    nodes_to_add = ['button_externalgrid', 'button_transformer', 'button_switch_cabinet', 'button_house', 'button_house',
              'button_house', 'button_pv']
    lines_to_add = [['node1', 'node2'], ['node2', 'node3'], ['node3', 'node5'], ['node3', 'node6'], ['node2', 'node4'], ['node2', 'node7']]
    power_list = [0, 0, 0, 1, 3, 4, -1]
    for element in nodes_to_add:
        last_id = get_last_id(elements)
        new_gridobject = generate_grid_object(element, 'node' + str(last_id[0] + 1), 'node' + str(last_id[0] + 1))
        image_src = app.get_asset_url('Icons/' + new_gridobject.icon)
        gridObject_list.append(new_gridobject)
        new_element = {'data': {'id': 'node' + str(last_id[0] + 1)},
                       'position': {'x': 50, 'y': 50}, 'classes': 'node_style',
                       'style': {'background-image': image_src, 'background-color': new_gridobject.ui_color}}
        elements.append(new_element)
        # -------------------
    for line in lines_to_add:
        last_id = get_last_id(elements)
        start_object = get_object_from_id(line[0], gridObject_list)
        end_object = get_object_from_id(line[1], gridObject_list)
        new_edge = {'data': {'source': line[0], 'target': line[1],
                             'id': 'edge' + str(last_id[1] + 1)}, 'classes': 'line_style'}
        elements.append(new_edge)
    get_object_from_id('node7', gridObject_list).voltage = 400
    return elements, gridObject_list
