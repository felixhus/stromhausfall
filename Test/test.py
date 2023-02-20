import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div('Right-click here', id='target-element', style={'position': 'relative'}),
    html.Ul([
        html.Li('Menu item 1'),
        html.Li('Menu item 2'),
        html.Li('Menu item 3'),
    ], id='context-menu', style={'position': 'absolute', 'display': 'none'})
])

app.clientside_callback(
    """
    function toggleContextMenu(display, x, y) {
        const menu = document.getElementById('context-menu');
        menu.style.display = display;
        menu.style.left = x + 'px';
        menu.style.top = y + 'px';
    }
    """,
    dash.dependencies.Output('context-menu', 'style'),
    dash.dependencies.Input('target-element', 'n_clicks'),
    dash.dependencies.State('target-element', 'n_clicks_timestamp'),
    dash.dependencies.State('target-element', 'clientHeight'),
    dash.dependencies.State('target-element', 'clientWidth'),
    dash.dependencies.State('context-menu', 'style')
)

app.clientside_callback(
    """
    function hideContextMenu() {
        const menu = document.getElementById('context-menu');
        menu.style.display = 'none';
    }
    """,
    dash.dependencies.Output('context-menu', 'style'),
    dash.dependencies.Input('context-menu', 'n_clicks')
)

app.clientside_callback(
    """
    function handleRightClick(n_clicks, timestamp, targetHeight, targetWidth) {
        if (n_clicks === 0) {
            return;
        }

        const menu = document.getElementById('context-menu');
        const display = menu.style.display === 'none' ? 'block' : 'none';

        const x = Math.min(timestamp, targetWidth - menu.offsetWidth);
        const y = Math.min(targetHeight, window.innerHeight - menu.offsetHeight);

        return [display, x, y];
    }
    """,
    dash.dependencies.Output('context-menu', 'style'),
    dash.dependencies.Output('context-menu', 'n_clicks'),
    dash.dependencies.Input('target-element', 'n_clicks'),
    dash.dependencies.State('target-element', 'n_clicks_timestamp'),
    dash.dependencies.State('target-element', 'clientHeight'),
    dash.dependencies.State('target-element', 'clientWidth'),
    prevent_initial_call=True
)

if __name__ == '__main__':
    app.run_server(debug=True)
