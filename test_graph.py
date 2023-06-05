import plotly.io as pio
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import tempfile
import os

# Create the three Plotly figures
fig1 = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
fig2 = go.Figure(data=go.Bar(x=[1, 2, 3], y=[4, 5, 6]))
fig3 = go.Figure(data=go.Pie(labels=['A', 'B', 'C'], values=[1, 2, 3]))

# Define the PDF file path
output_file = 'output.pdf'

# Define the titles for each plot
titles = ['Plot 1', 'Plot 2', 'Plot 3']

# Create a temporary directory to store the plot images
temp_dir = tempfile.mkdtemp()

# Export the figures to PDF
for fig, title in zip([fig1, fig2, fig3], titles):
    # Save the figure as an image file
    image_file = os.path.join(temp_dir, f'{title.lower().replace(" ", "_")}.png')
    pio.write_image(fig, image_file)

# Convert the images to a single PDF file
pio.images_to_pdf([os.path.join(temp_dir, f'{title.lower().replace(" ", "_")}.png') for title in titles], output_file)

# Remove the temporary directory
os.rmdir(temp_dir)


# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1('Download PDF'),
    html.A('Download', id='download-link', download='output.pdf', href='', target='_blank')
])

# Define the callback to update the download link
@app.callback(Output('download-link', 'href'), [Input('download-link', 'id')])
def update_download_link(value):
    return '/' + output_file

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
