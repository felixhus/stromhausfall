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
    elif object_type == "button_transformer":
        return grid_objects.TransformerObject(node_id=node_id, object_id="Dummy")
    elif object_type == "button_externalgrid":
        return grid_objects.ExternalGrid(node_id=node_id, object_id="Dummy")
    elif object_type == "button_pv":
        return grid_objects.PV(node_id=node_id, object_id="Dummy")
    elif object_type == "button_battery":
        return grid_objects.Battery(node_id=node_id, object_id="Dummy")
    elif object_type == "button_smartmeter":
        return grid_objects.SmartMeter(node_id=node_id, object_id="Dummy")
    elif object_type == "button_switch_cabinet":
        return grid_objects.SwitchCabinet(node_id=node_id, object_id="Dummy")
    else:
        return None
