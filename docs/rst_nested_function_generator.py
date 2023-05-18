"""
The problem is that the callback functions are nested function in a top level function in each callback file.
This is done to distribute them over several files and make the structure of the project cleaner. The problem in
documenting them is that SPHINX does not recognize nested function docstrings with the "automodule" command. This is
where these scripts jump in. They create a new python file in the /docs folder, which contain all the functions and
docstrings without code at top level.
"""

import ast


def get_nested_function_docstrings(filename, output_file_name, function_name):
    """
    This function takes a file with a top level function in it, which contains nested functions. It creates a new
    python file with all nested function and their docstrings in it. This file then can be read by Sphinx.

    :param filename: Name of file including the nested functions
    :type filename: str
    :param output_file_name: Name of output file
    :type output_file_name: str
    :param function_name: Name of top level function containing nested functions
    :type function_name: str
    :return: Nothing
    """

    with open(filename, 'r') as f:
        tree = ast.parse(f.read())

    with open(output_file_name, 'w') as output_file:
        output_file.write(f'# !!! THIS FILE IS ONLY FOR DOCUMENTATION PURPOSES. IT CONTAINS NO CODE!!!\n')
        output_file.write(f'"""\n{ast.get_docstring(tree)}\n""" \n\n')
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                for inner_node in node.body:
                    if isinstance(inner_node, ast.FunctionDef):
                        args = ', '.join(arg.arg for arg in inner_node.args.args)
                        output_file.write(f'\ndef {inner_node.name}({args}):\n    """'
                                          f'\n{ast.get_docstring(inner_node)}\n"""\n    pass\n')



def get_nested_function_docstrings_room(filename, output_file_name, function_names):
    """
    Only for room_callbacks file! This function takes a file with multiple top level functions in it,
    which contains nested functions. They are specified in the "function_names" input. It creates a new
    python file with all nested function and their docstrings in it. It also adds the docstring of the room_callback
    function. This file then can be read by Sphinx.

    :param filename: Name of file including the nested functions
    :type filename: str
    :param output_file_name: Name of output file
    :type output_file_name: str
    :param function_names: Names of top level function containing nested functions
    :type function_names: list[str]
    :return: Nothing
    """

    with open(filename, 'r') as f:
        tree = ast.parse(f.read())

    with open(output_file_name, 'w') as output_file:
        output_file.write(f'# !!! THIS FILE IS ONLY FOR DOCUMENTATION PURPOSES. IT CONTAINS NO CODE!!!\n')
        output_file.write(f'"""\n{ast.get_docstring(tree)}\n""" \n\n')
        for node in tree.body:
            # Handle main function of room callbacks and the docstring
            if isinstance(node, ast.FunctionDef) and ast.get_docstring(node) is not None:
                args = ', '.join(arg.arg for arg in node.args.args)
                output_file.write(f'\ndef {node.name}({args}):\n    """'
                                  f'\n{ast.get_docstring(node)}\n"""\n    pass\n')
            elif isinstance(node, ast.FunctionDef) and node.name in function_names:
                for inner_node in node.body:
                    if isinstance(inner_node, ast.FunctionDef):
                        args = ', '.join(arg.arg for arg in inner_node.args.args)
                        output_file.write(f'\ndef {inner_node.name}({args}):\n    """'
                                          f'\n{ast.get_docstring(inner_node)}\n"""\n    pass\n')


# Replace with the path to your source Python file
filename = "../callbacks/grid_callbacks.py"
# Replace with the name of the function that contains the nested functions
function_name = 'grid_callbacks'
function_names_room = ['create_menu_show_callbacks', 'create_manage_devices_callback']
output_file = 'grid_callbacks.py'

get_nested_function_docstrings(filename, output_file, function_name)
# get_nested_function_docstrings_room(filename, output_file, function_names_room)
