class GridObject:
    """ The structure to store information of a grid object """

    def __init__(self, node_id, object_id, voltage=None):
        self.voltage = voltage
        self.linkedNode = node_id
        self.parents = [None]
        self.children = [None]
        self.name = None
        self.connected_node = node_id
        self.id = object_id

    def get_id(self):
        return self.id


class HouseObject(GridObject):
    """ A residential house as a node in the power grid """
    object_type = "house"
    name = "Haus"
    icon = "icon_house.png"
    ui_color = '#6a93b0'
    allowed_types_to_connect = ["transformer", "switch_cabinet", "battery", "pv", "smart_meter"]

    def dummy(self):
        pass


class TransformerObject(GridObject):
    """ A transformer, voltage 20kV to 0.4kV"""
    object_type = "transformer"
    icon = "icon_transformer.png"
    ui_color = '#9cb6ca'
    allowed_types_to_connect = ["house", "switch_cabinet", "battery", "pv", "smartmeter", "externalgrid"]

    def __init__(self, impedance=1, *args, **kwargs):
        super(TransformerObject, self).__init__(*args, **kwargs)
        self.impedance = impedance


class LineObject(GridObject):
    """ An electrical line to connect Grid Objects """
    object_type = "line"
    name = "Leitung"
    ui_color = '#cddae4'

    def __init__(self, *args, **kwargs):
        super(LineObject, self).__init__(*args, **kwargs)
        if self.voltageLevel == 0.4:
            self.icon = "icon_line_lv.png"
        else:
            self.icon = "icon_line_hv.png"


class SmartMeter(GridObject):
    """ Object to show results of connected node """
    object_type = "smartmeter"
    name = "Smart Meter"
    icon = "icon_meter.png"
    ui_color = '#83a4bd'
    allowed_types_to_connect = ["transformer", "switch_cabinet", "externalgrid", "house", "pv", "battery"]


class ExternalGrid(GridObject):
    """ External Grid to give and take energy """
    object_type = "externalgrid"
    name = "Ext. Netz"
    icon = "icon_powerplant.png"
    ui_color = '#b5c8d7'
    allowed_types_to_connect = ["transformer", "externalgrid", "smartmeter"]


class Battery(GridObject):
    """ Battery which can store electrical energy """
    object_type = "battery"
    name = "Battery"
    icon = "icon_battery.png"
    ui_color = '#b5c8d7'
    allowed_types_to_connect = ["transformer", "switch_cabinet", "house", "pv", "smartmeter"]


class PV(GridObject):
    """ Battery which can store electrical energy """
    object_type = "PV"
    name = "PV"
    icon = "icon_pv.png"
    ui_color = '#b5c8d7'
    allowed_types_to_connect = ["transformer", "switch_cabinet", "battery", "pv", "smartmeter"]


class SwitchCabinet(GridObject):
    """ Battery which can store electrical energy """
    object_type = "switch_cabinet"
    name = "Switch Cabinet"
    icon = "icon_switch_cabinet.png"
    ui_color = '#9cb6ca'
    allowed_types_to_connect = ["transformer", "house", "battery", "pv", "smartmeter"]


class TransformerHelperNode:
    object_type = "transformer_helper"
