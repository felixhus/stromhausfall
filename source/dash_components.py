import dash_bootstrap_components as dbc
import source.stylesheets as stylesheets
from dash import dcc, html


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
    return dbc.Button(id=object_id, children=children, style=stylesheets.button_add_components_style)


# def readme_content():
#     with open('readme.md', encoding='UTF-8') as file:
#         content = file.read()
#     return dcc.Markdown(content)
