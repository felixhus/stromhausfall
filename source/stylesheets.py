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
        'selector': '.node_house',
        'style': {
            'background-color': '#6a93b0',
            'shape': 'roundrectangle',
            'width': 25,
            'height': 25,
            'background-image': ['/assets/Icons/icon_house.png'],
            'background-width': 25,
            'background-height': 25,
        }
    },
    {
        'selector': '.line_style',
        'style': {
            'width': '2px'
        }
    }
]

button_add_components_style = {
    'width': '80px',
    'height': '80px',
    'icon_width': '60px',
    # 'background': 'red',
    # 'border': 'red',
    'margin-top': '5px',
    'margin-bottom': '5px',
}
