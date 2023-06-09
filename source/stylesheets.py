"""
stylesheets.py contains the different css stylesheets of the app. They define the appearance of components and are
given as lists of python dictionaries. They are split into Group and Class selectors.
"""

cyto_stylesheet = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
        }
    },
    # Class selectors
    {
        'selector': '.node_style',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'roundrectangle',
            'width': 50,
            'height': 50,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 40,
            'background-height': 40,
        }
    },
    {
        'selector': '.node_style_custom',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'rectangle',
            'width': 50,
            'height': 50,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 40,
            'background-height': 40,
        }
    },
    {
        'selector': '.node_style_selected',
        'style': {
            'background-color': '#blue',
            'shape': 'roundrectangle',
            'width': 50,
            'height': 50,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 40,
            'background-height': 40,
        }
    },
    {
        'selector': '.room_node_style',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'roundrectangle',
            'width': 30,
            'height': 30,
            'background-width': 20,
            'background-height': 20,
        }
    },
    {
        'selector': '.socket_node_style',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'roundrectangle',
            'width': 30,
            'height': 30,
            'background-image': 'https://api.iconify.design/mdi:power-socket-de.svg',
            'background-width': 20,
            'background-height': 20,
        }
    },
    {
        'selector': '.socket_node_style_on',
        'style': {
            'background-color': '#89CFF0',
            'shape': 'roundrectangle',
            'width': 30,
            'height': 30,
            'background-image': 'https://api.iconify.design/mdi:power-socket-de.svg',
            'background-width': 20,
            'background-height': 20,
        }
    },
    {
        'selector': '.socket_node_style_off',
        'style': {
            'background-color': '#FF7F50',
            'shape': 'roundrectangle',
            'width': 30,
            'height': 30,
            'background-image': 'https://api.iconify.design/mdi:power-socket-de.svg',
            'background-width': 20,
            'background-height': 20,
        }
    },
    {
        'selector': '.power_strip_style',
        'style': {
            'shape': 'roundrectangle',
            'width': 10,
            'height': 10,
        }
    },
    {
        'selector': '.line_style_new',
        'style': {
            'width': '2px',
            'curve-style': 'bezier',
        }
    }
]

cyto_stylesheet_calculated = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
    # Class selectors
    {
        'selector': '.node_style',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'roundrectangle',
            'width': 50,
            'height': 50,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 40,
            'background-height': 40,
        }
    },
    {
        'selector': '.node_style_custom',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'rectangle',
            'width': 50,
            'height': 50,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 40,
            'background-height': 40,
        }
    },
    {
        'selector': '.node_style_selected',
        'style': {
            'background-color': '#blue',
            'shape': 'roundrectangle',
            'width': 50,
            'height': 50,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 40,
            'background-height': 40,
        }
    },
    {
        'selector': '.line_style',
        'style': {
            'width': '2px',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'target-arrow-shape': 'triangle',
        }
    },
    {
        'selector': '.line_style_reverse',
        'style': {
            'width': '2px',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'source-arrow-shape': 'triangle',
            # 'line-color': 'red'
        }
    },
    {
        'selector': '.line_style_new',
        'style': {
            'width': '2px',
            'curve-style': 'bezier',
        }
    }
]

button_add_components_style = {
    'width': '60px',
    'height': '60px',
    'icon_width': 40,   # Dash Iconify needs an Integer
    'margin-top': '3px',
    'margin-bottom': '3px',
}
