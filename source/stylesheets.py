cyto_stylesheet = [
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
    # {
    #     'selector': '.node_house',
    #     'style': {
    #         'background-color': '#6a93b0',
    #         'shape': 'roundrectangle',
    #         'width': 25,
    #         'height': 25,
    #         'background-image': ['/assets/Icons/icon_house.png'],
    #         'background-width': 25,
    #         'background-height': 25,
    #     }
    # },
    {
        'selector': '.line_style',
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
    # {
    #     'selector': '.node_house',
    #     'style': {
    #         'background-color': '#6a93b0',
    #         'shape': 'roundrectangle',
    #         'width': 25,
    #         'height': 25,
    #         'background-image': ['/assets/Icons/icon_house.png'],
    #         'background-width': 25,
    #         'background-height': 25,
    #     }
    # },
    {
        'selector': '.line_style',
        'style': {
            'width': '2px',
            'curve-style': 'bezier',
            'label': 'data(label)',
            'target-arrow-shape': 'triangle'
        }
    }
]

button_add_components_style = {
    'width': '60px',
    'height': '60px',
    'icon_width': '40px',
    'margin-top': '3px',
    'margin-bottom': '3px',
}
