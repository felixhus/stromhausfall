def create_HouseObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'power': [0] * 7 * 24 * 60,
        'voltage': 400,
        'object_type': 'house',
        'name': "Haus",
        'icon': 'bi:house-door',
        'ui_color': '#6a93b0',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "battery", "pv", "smart_meter"],
        'active': True,
        'config_mode': 'preset',
        'power_profile': None
    }


def create_TransformerObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'impedance': None,
        'rating': 250,    # rating in kVA
        'power': [0],
        'object_type': 'transformer',
        'name': "Transformator",
        'icon': 'icon_transformer.png',
        'ui_color': '#9cb6ca',
        'allowed_types_to_connect': ["house", "switch_cabinet", "battery", "pv", "smartmeter", "externalgrid"],
        'active': True
    }


def create_SmartMeterObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'power': None,
        'object_type': 'smartmeter',
        'name': "Smart Meter",
        'icon': 'icon_meter.png',
        'ui_color': '#83a4bd',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "externalgrid", "house", "pv", "battery"],
        'active': True
    }


def create_ExternalGridObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': 20000,
        'power': [0],
        'object_type': 'externalgrid',
        'name': "Externes Netz",
        'icon': 'icon_powerplant.png',
        'ui_color': '#b5c8d7',
        'allowed_types_to_connect': ["transformer", "pv", "smartmeter"],
        'active': True
    }


def create_BatteryObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': 400,
        'power': [0],
        'object_type': 'battery',
        'name': "Batteriespeicher",
        'icon': 'material-symbols:battery-charging-20-outline',
        'ui_color': '#b5c8d7',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "house", "pv", "smartmeter"],
        'active': True
    }


def create_PVObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'power': [0]*(24*7),
        'object_type': 'pv',
        'location': [None, None, None],     # Location consisting of postcode, lat, lon
        'orientation': 0,   # azimuth angle
        'rated_power': 0,
        'tilt': 0,
        'name': "Solaranlage",
        'icon': 'fa6-solid:solar-panel',
        'ui_color': '#b5c8d7',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "battery", "smartmeter"],
        'active': True
    }


def create_SwitchCabinetObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'power': [0],
        'object_type': 'switch_cabinet',
        'name': "Verteilerkasten",
        'icon': 'icon-park-outline:connection-point',
        'ui_color': '#9cb6ca',
        'allowed_types_to_connect': ["transformer", "house", "battery", "pv", "smartmeter", "switch_cabinet"],
        'active': True
    }


def create_TransformerHelperNodeObject():
    return {
        'power': 0,
        'object_type': 'transformer_helper',
    }


def create_LineObject(object_id, edge_id):
    return {
        'id': object_id,
        'linkedEdge': edge_id,
        'voltage': None,
        'object_type': 'line',
        'name': "Leitung",
        'active': True
    }