import grid_objects

def get_last_id(elements):
    last_id = [0, 0]
    for ele in elements:
        if 'source' not in ele['data']:
            last_id[0] = int(ele['data']['id'][4:])
    for ele in elements:
        if 'source' in ele['data']:
            last_id[1] = int(ele['data']['id'][4:])
    return last_id


def get_connected_edges(elements, selected_element):
    id_element = selected_element['data']['id']
    result = []
    for ele in elements:
        if 'source' in ele['data']:
            if ele['data']['source'] == id_element or ele['data']['target'] == id_element:
                result.append(ele)
    return result


def generate_grid_object(object_type, object_id, node_id):
    if object_type == "button_house":
        return grid_objects.HouseObject(node_id=node_id, object_id="Dummy")
    else:
        return None
