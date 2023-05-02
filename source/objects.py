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


def create_DeviceObject(device_id, device_type):
    if device_type == 'hairdryer':
        return {
            'id': device_id,
            'name': 'Föhn',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'icon-park-outline:hair-dryer',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Lange Haare': {'key': 'hairdryer_long', 'icon': None},
                'Kurze Haare': {'key': 'hairdryer_short', 'icon': None},
            }
        }
    elif device_type == 'iron':
        return {
            'id': device_id,
            'name': 'Bügeleisen',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'tabler:ironing-1',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Klasse A': {'key': 'iron_class_A', 'icon': None},
                'Klasse B': {'key': 'iron_class_B', 'icon': None},
                'Klasse C': {'key': 'iron_class_C', 'icon': None},
            }
        }
    elif device_type == 'toothbrush':
        return {
            'id': device_id,
            'name': 'Elektrische Zahnbürste',
            'type': device_type,
            'menu_type': 'device_preset',
            'icon': 'mdi:toothbrush-electric',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                '3 Minuten Putzen': {'key': 'toothbrush_3_min', 'icon': None},
                '5 Minuten Putzen': {'key': 'toothbrush_5_min', 'icon': None},
                'Mit der Hand putzen': {'key': 'toothbrush_hand', 'icon': None},
            }
        }
    elif device_type == 'refrigerator':
        return {
            'id': device_id,
            'name': 'Kühlschrank',
            'type': device_type,
            'menu_type': 'device_preset',   # Development
            'icon': 'mdi:fridge-outline',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Großer Kühlschrank': {'key': 'Refrigerator_Big', 'icon': None},
                'Kleiner Kühlschrank Alt': {'key': 'Refrigerator_Small_Old', 'icon': None},
                'Kleiner Kühlschrank Neu': {'key': 'Refrigerator_Small_New', 'icon': None},
            }
        }
    elif device_type == 'dishwasher':
        return {
            'id': device_id,
            'name': 'Spülmaschine',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'fluent:dishwasher-20-regular',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Geschirr spülen': {'key': 'dishwasher', 'icon': None},
            }
        }
    elif device_type == 'kettle':
        return {
            'id': device_id,
            'name': 'Wasserkocher',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'material-symbols:kettle-outline',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                '2000 W': {'key': 'kettle_2000W', 'icon': None},
                '2500 W': {'key': 'kettle_2500W', 'icon': None}
            }
        }
    elif device_type == 'boiler':
        return {
            'id': device_id,
            'name': 'Boiler',
            'type': device_type,
            'menu_type': 'device_preset',
            'icon': 'mdi:water-boiler',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': 'Boiler',
            'power_options': {
                'Boiler': {'key': 'water_boiler', 'icon': None}
            }
        }
    elif device_type == 'washing_machine':
        return {
            'id': device_id,
            'name': 'Waschmaschine',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'icon-park-outline:washing-machine-one',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': 'Waschgang',
            'power_options': {
                'Waschgang': {'key': 'washing_machine', 'icon': None}
            }
        }
    elif device_type == 'oven':
        return {
            'id': device_id,
            'name': 'Ofen',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon':  'material-symbols:oven-gen-outline',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Lampe': {'key': 'lamp_basic', 'icon': None},
                'VDEW': {'key': 'vdew_test_cubic', 'icon': None}
            }
        }
    elif device_type == 'coffee':
        return {
            'id': device_id,
            'name': 'Kaffeemaschine',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'ic:outline-coffee',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Lampe': {'key': 'lamp_basic', 'icon': None},
                'VDEW': {'key': 'vdew_test_cubic', 'icon': None}
            }
        }
    elif device_type == 'desktop_pc':
        return {
            'id': device_id,
            'name': 'Desktop PC',
            'type': device_type,
            'menu_type': 'device_preset',
            'icon': 'ph:desktop-tower',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Arbeiten 4 Stunden': {'key': 'desktop_pc_4h', 'icon': None},
                'Arbeiten 8 Stunden': {'key': 'desktop_pc_8h', 'icon': None},
                'Arbeiten 12 Stunden': {'key': 'desktop_pc_12h', 'icon': None}
            }
        }
    elif device_type == 'tv_lcd':
        return {
            'id': device_id,
            'name': 'Fernseher',
            'type': device_type,
            'menu_type': 'device_custom',
            'icon': 'mdi:tv-classic',
            'power': [0] * 24*60*7,
            'active': True,
            'selected_power_option': None,
            'power_options': {
                '2 Stunden fernsehen': {'key': 'tv_lcd_2h', 'icon': None},
                '8 Stunden fernsehen': {'key': 'tv_lcd_8h', 'icon': None}
            }
        }
    else:
        return {
            'id': device_id,
            'name': 'Gerät',
            'type': 'device',
            'menu_type': 'device_preset',
            'icon': None,
            'power': [0] * 24*60,
            # 'power': [270.0, 980.0, 753.0, 65.0, 874.0, 945.0, 665.0, 384.0, 116.0, 930.0, 563.0, 500.0, 56.0, 850.0, 452.0, 228.0, 411.0, 813.0, 335.0, 172.0, 216.0, 983.0, 17.0, 873.0, 676.0, 780.0, 439.0, 206.0, 881.0, 872.0, 798.0, 768.0, 941.0, 75.0, 854.0, 611.0, 945.0, 976.0, 633.0, 788.0, 410.0, 724.0, 406.0, 234.0, 649.0, 629.0, 465.0, 667.0, 298.0, 370.0, 993.0, 528.0, 178.0, 897.0, 621.0, 480.0, 734.0, 225.0, 27.0, 54.0, 601.0, 608.0, 957.0, 404.0, 114.0, 796.0, 96.0, 82.0, 465.0, 725.0, 57.0, 902.0, 969.0, 82.0, 338.0, 846.0, 836.0, 664.0, 971.0, 272.0, 929.0, 711.0, 207.0, 80.0, 846.0, 367.0, 903.0, 80.0, 638.0, 906.0, 419.0, 917.0, 112.0, 491.0, 768.0, 34.0, 683.0, 662.0, 755.0, 374.0, 348.0, 173.0, 891.0, 242.0, 915.0, 913.0, 228.0, 717.0, 95.0, 729.0, 842.0, 285.0, 716.0, 347.0, 121.0, 167.0, 675.0, 803.0, 405.0, 605.0, 156.0, 199.0, 731.0, 389.0, 408.0, 149.0, 673.0, 686.0, 428.0, 695.0, 916.0, 272.0, 82.0, 287.0, 825.0, 406.0, 467.0, 378.0, 531.0, 707.0, 199.0, 220.0, 312.0, 627.0, 193.0, 434.0, 756.0, 420.0, 760.0, 234.0, 760.0, 798.0, 551.0, 545.0, 896.0, 1.0, 250.0, 363.0, 792.0, 240.0, 518.0, 597.0, 590.0, 141.0, 814.0, 162.0, 635.0, 425.0, 940.0, 286.0, 182.0, 114.0, 371.0, 80.0, 989.0, 759.0, 863.0, 296.0, 643.0, 475.0, 273.0, 490.0, 293.0, 562.0, 142.0, 565.0, 148.0, 640.0, 534.0, 485.0, 518.0, 997.0, 317.0, 215.0, 710.0, 650.0, 324.0, 958.0, 863.0, 603.0, 729.0, 5.0, 347.0, 337.0, 926.0, 277.0, 371.0, 486.0, 221.0, 73.0, 925.0, 89.0, 377.0, 363.0, 887.0, 355.0, 489.0, 827.0, 36.0, 145.0, 820.0, 894.0, 607.0, 196.0, 755.0, 848.0, 442.0, 739.0, 942.0, 731.0, 785.0, 525.0, 114.0, 243.0, 813.0, 844.0, 650.0, 511.0, 683.0, 429.0, 491.0, 342.0, 818.0, 933.0, 217.0, 47.0, 749.0, 997.0, 770.0, 915.0, 647.0, 875.0, 625.0, 567.0, 601.0, 488.0, 788.0, 174.0, 193.0, 517.0, 654.0, 953.0, 922.0, 441.0, 493.0, 451.0, 555.0, 545.0, 151.0, 828.0, 657.0, 780.0, 471.0, 701.0, 537.0, 895.0, 790.0, 253.0, 415.0, 745.0, 731.0, 196.0, 204.0, 622.0, 934.0, 947.0, 243.0, 692.0, 561.0, 481.0, 499.0, 488.0, 320.0, 832.0, 91.0, 250.0, 871.0, 828.0, 175.0, 574.0, 786.0, 532.0, 362.0, 289.0, 846.0, 397.0, 633.0, 858.0, 249.0, 858.0, 74.0, 388.0, 141.0, 444.0, 281.0, 322.0, 684.0, 166.0, 988.0, 462.0, 242.0, 141.0, 359.0, 527.0, 355.0, 875.0, 709.0, 272.0, 362.0, 247.0, 592.0, 455.0, 31.0, 672.0, 45.0, 662.0, 705.0, 547.0, 143.0, 918.0, 918.0, 741.0, 755.0, 66.0, 338.0, 725.0, 0.0, 3.0, 544.0, 966.0, 406.0, 404.0, 913.0, 83.0, 490.0, 551.0, 241.0, 871.0, 978.0, 311.0, 63.0, 346.0, 590.0, 861.0, 545.0, 963.0, 47.0, 701.0, 937.0, 897.0, 859.0, 870.0, 631.0, 107.0, 951.0, 564.0, 811.0, 758.0, 634.0, 951.0, 718.0, 393.0, 794.0, 453.0, 786.0, 661.0, 596.0, 398.0, 403.0, 712.0, 226.0, 790.0, 529.0, 187.0, 402.0, 118.0, 720.0, 862.0, 587.0, 355.0, 84.0, 270.0, 314.0, 917.0, 394.0, 900.0, 739.0, 727.0, 917.0, 622.0, 770.0, 620.0, 586.0, 765.0, 676.0, 400.0, 999.0, 235.0, 688.0, 531.0, 521.0, 829.0, 439.0, 537.0, 815.0, 834.0, 616.0, 610.0, 901.0, 109.0, 909.0, 876.0, 779.0, 400.0, 346.0, 657.0, 594.0, 540.0, 685.0, 713.0, 861.0, 488.0, 244.0, 786.0, 765.0, 349.0, 122.0, 137.0, 738.0, 688.0, 145.0, 819.0, 528.0, 567.0, 634.0, 497.0, 72.0, 968.0, 192.0, 453.0, 824.0, 891.0, 452.0, 553.0, 486.0, 856.0, 700.0, 477.0, 643.0, 878.0, 127.0, 879.0, 972.0, 261.0, 189.0, 226.0, 912.0, 38.0, 647.0, 250.0, 858.0, 236.0, 567.0, 125.0, 33.0, 106.0, 132.0, 467.0, 234.0, 939.0, 909.0, 568.0, 465.0, 534.0, 28.0, 184.0, 132.0, 720.0, 328.0, 809.0, 369.0, 970.0, 507.0, 181.0, 914.0, 299.0, 960.0, 4.0, 465.0, 383.0, 604.0, 807.0, 451.0, 339.0, 333.0, 429.0, 757.0, 110.0, 251.0, 854.0, 404.0, 673.0, 241.0, 183.0, 705.0, 72.0, 908.0, 220.0, 115.0, 366.0, 788.0, 532.0, 578.0, 421.0, 470.0, 719.0, 893.0, 655.0, 250.0, 585.0, 344.0, 225.0, 445.0, 430.0, 345.0, 141.0, 95.0, 557.0, 351.0, 895.0, 623.0, 9.0, 603.0, 177.0, 159.0, 188.0, 954.0, 228.0, 76.0, 574.0, 153.0, 919.0, 485.0, 247.0, 608.0, 487.0, 820.0, 727.0, 671.0, 284.0, 118.0, 480.0, 363.0, 516.0, 580.0, 157.0, 8.0, 334.0, 38.0, 805.0, 916.0, 849.0, 993.0, 982.0, 365.0, 333.0, 316.0, 796.0, 871.0, 197.0, 528.0, 985.0, 975.0, 578.0, 946.0, 218.0, 645.0, 874.0, 457.0, 93.0, 64.0, 614.0, 957.0, 68.0, 604.0, 553.0, 926.0, 439.0, 605.0, 934.0, 939.0, 652.0, 217.0, 858.0, 101.0, 192.0, 813.0, 694.0, 113.0, 246.0, 600.0, 38.0, 422.0, 193.0, 650.0, 771.0, 683.0, 702.0, 967.0, 630.0, 587.0, 509.0, 658.0, 913.0, 327.0, 741.0, 460.0, 606.0, 146.0, 557.0, 269.0, 662.0, 611.0, 113.0, 510.0, 216.0, 922.0, 210.0, 681.0, 973.0, 545.0, 370.0, 33.0, 600.0, 651.0, 328.0, 205.0, 681.0, 810.0, 881.0, 397.0, 963.0, 110.0, 969.0, 16.0, 77.0, 264.0, 29.0, 977.0, 90.0, 867.0, 789.0, 268.0, 792.0, 219.0, 153.0, 28.0, 387.0, 127.0, 859.0, 900.0, 160.0, 820.0, 868.0, 16.0, 596.0, 974.0, 525.0, 437.0, 688.0, 108.0, 446.0, 101.0, 596.0, 962.0, 39.0, 902.0, 356.0, 671.0, 492.0, 121.0, 632.0, 963.0, 611.0, 508.0, 728.0, 656.0, 499.0, 254.0, 744.0, 912.0, 579.0, 837.0, 286.0, 715.0, 20.0, 664.0, 90.0, 207.0, 325.0, 190.0, 128.0, 395.0, 781.0, 551.0, 811.0, 742.0, 702.0, 322.0, 687.0, 377.0, 361.0, 831.0, 491.0, 444.0, 478.0, 600.0, 41.0, 616.0, 918.0, 714.0, 854.0, 477.0, 702.0, 912.0, 235.0, 96.0, 443.0, 402.0, 40.0, 174.0, 895.0, 940.0, 464.0, 436.0, 74.0, 409.0, 886.0, 139.0, 878.0, 625.0, 301.0, 944.0, 939.0, 458.0, 327.0, 304.0, 424.0, 852.0, 193.0, 78.0, 506.0, 987.0, 178.0, 646.0, 992.0, 431.0, 25.0, 140.0, 229.0, 83.0, 56.0, 169.0, 290.0, 750.0, 924.0, 815.0, 166.0, 15.0, 74.0, 503.0, 950.0, 783.0, 291.0, 227.0, 998.0, 524.0, 638.0, 952.0, 935.0, 684.0, 123.0, 889.0, 774.0, 729.0, 354.0, 363.0, 766.0, 373.0, 783.0, 430.0, 188.0, 865.0, 868.0, 962.0, 220.0, 959.0, 60.0, 634.0, 124.0, 681.0, 302.0, 167.0, 765.0, 374.0, 398.0, 728.0, 535.0, 871.0, 169.0, 849.0, 426.0, 808.0, 127.0, 20.0, 452.0, 938.0, 607.0, 162.0, 66.0, 667.0, 387.0, 692.0, 634.0, 623.0, 936.0, 723.0, 354.0, 105.0, 104.0, 528.0, 40.0, 789.0, 944.0, 875.0, 826.0, 577.0, 946.0, 790.0, 762.0, 831.0, 546.0, 595.0, 753.0, 940.0, 968.0, 17.0, 671.0, 1.0, 662.0, 56.0, 391.0, 602.0, 237.0, 716.0, 228.0, 123.0, 267.0, 816.0, 137.0, 973.0, 531.0, 175.0, 515.0, 804.0, 186.0, 441.0, 493.0, 478.0, 102.0, 10.0, 96.0, 465.0, 915.0, 709.0, 527.0, 559.0, 7.0, 801.0, 14.0, 584.0, 949.0, 597.0, 439.0, 532.0, 792.0, 466.0, 671.0, 514.0, 907.0, 559.0, 270.0, 247.0, 983.0, 41.0, 612.0, 541.0, 165.0, 555.0, 626.0, 840.0, 181.0, 38.0, 826.0, 580.0, 867.0, 136.0, 541.0, 363.0, 536.0, 31.0, 663.0, 205.0, 602.0, 816.0, 624.0, 697.0, 317.0, 186.0, 235.0, 755.0, 466.0, 332.0, 518.0, 587.0, 92.0, 528.0, 480.0, 213.0, 783.0, 417.0, 717.0, 654.0, 939.0, 351.0, 712.0, 364.0, 62.0, 944.0, 203.0, 209.0, 260.0, 331.0, 566.0, 583.0, 608.0, 118.0, 685.0, 18.0, 370.0, 575.0, 430.0, 128.0, 187.0, 596.0, 307.0, 119.0, 275.0, 343.0, 367.0, 431.0, 342.0, 853.0, 441.0, 758.0, 522.0, 637.0, 546.0, 309.0, 193.0, 753.0, 526.0, 609.0, 976.0, 46.0, 831.0, 639.0, 41.0, 890.0, 779.0, 106.0, 846.0, 190.0, 17.0, 773.0, 928.0, 627.0, 826.0, 647.0, 47.0, 2.0, 610.0, 659.0, 8.0, 670.0, 470.0, 264.0, 230.0, 824.0, 309.0, 796.0, 750.0, 240.0, 679.0, 341.0, 218.0, 662.0, 423.0, 144.0, 279.0, 156.0, 525.0, 514.0, 730.0, 799.0, 815.0, 427.0, 668.0, 75.0, 338.0, 912.0, 336.0, 441.0, 873.0, 565.0, 458.0, 611.0, 371.0, 222.0, 361.0, 192.0, 112.0, 606.0, 459.0, 953.0, 258.0, 744.0, 737.0, 160.0, 16.0, 400.0, 137.0, 661.0, 41.0, 363.0, 5.0, 825.0, 616.0, 372.0, 93.0, 520.0, 108.0, 559.0, 407.0, 402.0, 265.0, 386.0, 161.0, 925.0, 579.0, 859.0, 536.0, 575.0, 739.0, 954.0, 40.0, 419.0, 676.0, 866.0, 654.0, 220.0, 709.0, 25.0, 767.0, 567.0, 492.0, 542.0, 67.0, 510.0, 917.0, 35.0, 63.0, 575.0, 245.0, 761.0, 263.0, 688.0, 788.0, 323.0, 594.0, 219.0, 236.0, 888.0, 862.0, 567.0, 459.0, 600.0, 336.0, 654.0, 36.0, 363.0, 971.0, 981.0, 552.0, 994.0, 353.0, 553.0, 503.0, 364.0, 124.0, 538.0, 151.0, 787.0, 339.0, 584.0, 210.0, 486.0, 570.0, 889.0, 304.0, 354.0, 266.0, 825.0, 585.0, 243.0, 928.0, 235.0, 130.0, 90.0, 33.0, 634.0, 848.0, 293.0, 817.0, 286.0, 4.0, 679.0, 71.0, 154.0, 58.0, 127.0, 495.0, 311.0, 147.0, 774.0, 525.0, 598.0, 853.0, 422.0, 354.0, 296.0, 42.0, 884.0, 427.0, 425.0, 941.0, 560.0, 521.0, 680.0, 838.0, 872.0, 264.0, 813.0, 302.0, 779.0, 240.0, 44.0, 559.0, 825.0, 152.0, 61.0, 353.0, 611.0, 581.0, 951.0, 526.0, 306.0, 604.0, 288.0, 62.0, 180.0, 464.0, 353.0, 789.0, 727.0, 680.0, 754.0, 440.0, 139.0, 206.0, 406.0, 114.0, 258.0, 12.0, 729.0, 66.0, 824.0, 530.0, 289.0, 581.0, 955.0, 851.0, 457.0, 24.0, 829.0, 790.0, 329.0, 66.0, 954.0, 82.0, 765.0, 116.0, 841.0, 140.0, 756.0, 761.0, 763.0, 648.0, 482.0, 855.0, 349.0, 604.0, 910.0, 308.0, 491.0, 537.0, 865.0, 854.0, 976.0, 139.0, 414.0, 417.0, 235.0, 229.0, 566.0, 263.0, 959.0, 550.0, 701.0, 659.0, 832.0, 395.0, 161.0, 647.0, 931.0, 520.0, 879.0, 421.0, 184.0, 248.0, 220.0, 624.0, 42.0, 104.0, 506.0, 70.0, 359.0, 541.0, 144.0, 713.0, 235.0, 954.0, 268.0, 386.0, 399.0, 712.0, 474.0, 843.0, 13.0, 291.0, 293.0, 259.0, 224.0, 560.0, 29.0, 678.0, 882.0, 899.0, 184.0, 673.0, 649.0, 220.0, 411.0, 204.0, 967.0, 935.0, 597.0, 908.0, 957.0, 505.0, 551.0, 806.0, 68.0, 287.0, 652.0, 488.0, 1.0, 717.0, 398.0, 701.0, 630.0, 411.0, 401.0, 714.0, 790.0, 777.0, 427.0, 856.0, 250.0, 341.0, 609.0, 564.0, 523.0, 887.0, 446.0, 485.0, 309.0, 775.0, 654.0, 463.0, 255.0, 251.0, 326.0, 33.0, 846.0, 621.0, 240.0, 549.0, 494.0, 929.0, 499.0, 872.0, 952.0, 289.0, 919.0, 872.0, 77.0, 15.0, 270.0, 485.0, 70.0, 155.0, 93.0, 188.0, 406.0, 957.0, 486.0, 687.0, 197.0, 459.0, 174.0, 255.0, 263.0, 993.0, 150.0, 358.0, 243.0, 139.0, 911.0, 852.0, 336.0, 796.0, 784.0, 941.0, 56.0, 921.0, 493.0, 961.0, 15.0, 602.0, 71.0, 885.0, 637.0, 978.0, 750.0, 455.0, 302.0, 794.0, 637.0, 899.0, 189.0, 624.0, 62.0, 12.0, 826.0, 805.0, 404.0, 996.0, 817.0, 415.0, 14.0, 983.0, 587.0, 435.0, 477.0, 448.0, 913.0, 607.0, 886.0, 838.0, 601.0, 598.0, 47.0, 915.0, 334.0, 278.0, 402.0, 385.0, 1000.0, 3.0, 186.0, 883.0, 813.0, 152.0, 895.0, 916.0, 525.0, 894.0, 490.0, 521.0],
            'active': True,
            'selected_power_option': None,
            'power_options': {
                'Klasse A': {'key': 'day_device_A', 'icon': 'tabler:hexagon-letter-a'},
                'Klasse B': {'key': 'day_device_B', 'icon': 'tabler:hexagon-letter-b'},
                'Klasse C': {'key': 'day_device_C', 'icon': 'tabler:hexagon-letter-c'},
            }
    }


def create_LampObject(device_id, room):
    return {
        'id': device_id,
        'name': 'Lampe ' + room,
        'type': 'lamp',
        'menu_type': 'device_preset',
        'icon': 'mdi:lightbulb-on-outline',
        'power': [0] * 24*60*7,
        'active': True,
        'selected_power_option': None,
        'power_options': {
            'Lampe Profil 1': {'key': 'lamp_01', 'icon': None},
            'Lampe Profil 2': {'key': 'lamp_02', 'icon': None},
            'Lampe Profil 3': {'key': 'lamp_03', 'icon': None},
            'Lampe Profil 4': {'key': 'lamp_04', 'icon': None},
        }
    }
