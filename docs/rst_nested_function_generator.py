"""
The problem is that the callback functions are nested function in a top level function in each callback file.
This is done to distribute them over several files and make the structure of the project cleaner. The problem in
documenting them is that SPHINX does not recognize nested function docstrings with the "automodule" command. This is
where this script jumps in.
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


# Replace with the path to your Python file
filename = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\callbacks\general_callbacks.py"
# Replace with the name of the function that contains the nested functions
function_name = 'general_callbacks'
output_file = 'general_callbacks.py'

get_nested_function_docstrings(filename, output_file, function_name)
