def create_HouseObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'power': None,
        'voltage': 400,
        'object_type': 'house',
        'name': "Haus",
        'icon': 'icon_house.png',
        'ui_color': '#6a93b0',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "battery", "pv", "smart_meter"],
    }


def create_TransformerObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'impedance': None,
        'power': None,
        'object_type': 'transformer',
        'name': "Transformator",
        'icon': 'icon_transformer.png',
        'ui_color': '#9cb6ca',
        'allowed_types_to_connect': ["house", "switch_cabinet", "battery", "pv", "smartmeter", "externalgrid"],
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
    }


def create_ExternalGridObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': 20000,
        'power': None,
        'object_type': 'externalgrid',
        'name': "Externes Netz",
        'icon': 'icon_powerplant.png',
        'ui_color': '#b5c8d7',
        'allowed_types_to_connect': ["transformer", "pv", "smartmeter"],
    }


def create_BatteryObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': 400,
        'power': None,
        'object_type': 'battery',
        'name': "Batteriespeicher",
        'icon': 'icon_battery.png',
        'ui_color': '#b5c8d7',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "house", "pv", "smartmeter"],
    }


def create_PVObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'power': None,
        'object_type': 'pv',
        'name': "Solaranlage",
        'icon': 'icon_pv.png',
        'ui_color': '#b5c8d7',
        'allowed_types_to_connect': ["transformer", "switch_cabinet", "battery", "smartmeter"],
    }


def create_SwitchCabinetObject(object_id, node_id):
    return {
        'id': object_id,
        'linkedNode': node_id,
        'voltage': None,
        'power': None,
        'object_type': 'switch_cabinet',
        'name': "Verteilerkasten",
        'icon': 'icon_switch_cabinet.png',
        'ui_color': '#9cb6ca',
        'allowed_types_to_connect': ["transformer", "house", "battery", "pv", "smartmeter", "switch_cabinet"],
    }
