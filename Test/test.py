import dash
import dash_cytoscape as cyto
import dash_html_components as html

app = dash.Dash(__name__)

elements = [
    {"data": {"id": "A", "label": "Node A"}},
    {"data": {"id": "B", "label": "Node B"}},
    {"data": {"source": "A", "target": "B", "label": "Edge AB"}}
]

stylesheet = [
    {
        'selector': 'edge',
        'style': {
            'mid-source-arrow-color': 'black',
            'mid-source-arrow-shape': 'triangle',
            # 'mid-source-arrow-fill': 'hollow',
            'line-color': 'green',
        }
    }
]

app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-arrows',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=elements,
        stylesheet=stylesheet
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
