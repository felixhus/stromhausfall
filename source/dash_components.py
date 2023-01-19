import dash_bootstrap_components as dbc
import source.stylesheets as stylesheets
from dash import dcc, html
import dash_cytoscape as cyto
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def add_storage_variables():
    return html.Div([dcc.Store(id='start_of_line'), dcc.Store(id='store_add_node'),
                     dcc.Store(id='line_edit_active'), dcc.Store(id='selected_element'),
                     dcc.Store(id='element_deleted')])


def add_grid_object_button(object_id, name=None, linked_object=None, icon=None):
    """
    Methode erzeugt einen Button für das Menü, um Grid-Objekte hinzuzufügen.
    :param object_id: Id des Buttons
    :param linked_object: Node, der beim Klicken zum Grid hinzugefügt wird.
    :param name: Name des Buttons
    :param icon: Pfad zum anzuzeigenden Icon
    :return: DBC Button
    """
    # children = html.Img(src=icon, width=stylesheets.button_add_components_style['width'])
    if icon is not None:
        children = html.Img(src=icon, height=str(stylesheets.button_add_components_style['icon_width']))
    else:
        children = name
    return dmc.Button(id=object_id, children=children, style=stylesheets.button_add_components_style)


def add_cytoscape_grid(nodes, edges):
    cytoscape = cyto.Cytoscape(
        id='cyto1',
        layout={'name': 'preset'},
        autoRefreshLayout=False,
        style={'width': '800px', 'height': '100%', 'background': '#e6ecf2', 'frame': 'blue'},
        elements=edges + nodes,
        stylesheet=stylesheets.cyto_stylesheet
    )
    return cytoscape


def add_modal_readme():
    with open('README.md', encoding='UTF-8') as file:
        content_readme = file.read()
    return dmc.Modal(
        title="Readme",
        id="modal_readme",
        children=dcc.Markdown(content_readme),
        opened=False
        # dbc.ModalHeader(dbc.ModalTitle("Readme")),
        # dbc.ModalBody(dcc.Markdown(content_readme), id="modal_readme_body")
    )


def add_modal_edit():
    return dmc.Modal(
        title="Edit",
        id='modal_edit',
        children=[
            dmc.Text("", id='modal_text'),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button("Löschen", color='red', variant='outline', id='modal_edit_delete_button',
                           leftIcon=DashIconify(icon="material-symbols:delete-outline")),
                dmc.Button("Schließen", variant='outline', id='modal_edit_close_button')
            ], position='right')
        ]
    )
    # return dbc.Modal([
    #     dbc.ModalHeader(dbc.ModalTitle("Header")),
    #     dbc.ModalBody("Edit grid element here", id="modal_body"),
    #     dbc.ModalFooter(
    #         dbc.Button(
    #             "Close", id="close_modal", className="ms-auto", n_clicks=0
    #         )
    #     ),
    # ],
    #     id="modal",
    #     is_open=False,
    # )


# def readme_content():
#     with open('readme.md', encoding='UTF-8') as file:
#         content = file.read()
#     return dcc.Markdown(content)
