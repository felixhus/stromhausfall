"""
The problem is that the callback functions are nested function in a top level function in each callback file.
This is done to distribute them over several files and make the structure of the project cleaner. The problem in
documenting them is that SPHINX does not recognize nested function docstrings with the "automodule" command. This is
where this script jumps in.
"""
import ast


def get_autofunction_list(file_path, top_level_function_name):
    """
    This function takes a file with a top level function in it, which contains nested functions. For every nested
    function it prints out one line:
    .. autofunction:: top_level_function_name.nested_function_name

    :param file_path: Path of the file to go through
    :type file_path: str
    :param top_level_function_name: Name of the top level function
    :type top_level_function_name: str
    :return: Lines of sphinx autofunction
    """

    # Parse the file with ast
    with open(file_path, 'r') as f:
        source = f.read()
    module = ast.parse(source)

    # Find the top-level function definition
    top_level_function = None
    for node in module.body:
        if isinstance(node, ast.FunctionDef) and node.name == top_level_function_name:
            top_level_function = node
            break
    if top_level_function is None:
        raise ValueError(f"No top-level function found with name '{top_level_function_name}'")

    # Collect all the nested functions within the top-level function
    nested_functions = []
    for node in ast.walk(top_level_function):
        if isinstance(node, ast.FunctionDef):
            nested_functions.append(node.name)

    autofunctions = []

    for name in nested_functions:
        qualified_name = top_level_function_name + '.' + name
        autofunction = '.. autofunction:: {}\n'.format(qualified_name)
        autofunctions.append(autofunction)

    return ''.join(autofunctions)

# file_path = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\callbacks\general_callbacks.py"
# top_level_function = 'general_callbacks'
# print(get_autofunction_list(file_path, top_level_function))

import ast

# Replace with the path to your Python file
filename = r"C:\Users\felix\Documents\HOME\Uni\02_Master\05_Masterthesis\02_Code\05_PowerHouse\callbacks\general_callbacks.py"

# Replace with the name of the function that contains the nested functions
function_name = 'general_callbacks'

with open(filename, 'r') as f:
    tree = ast.parse(f.read())

# for node in tree.body:
#     if isinstance(node, ast.FunctionDef) and node.name == function_name:
#         with open('output_file.py', 'w') as output_file:
#             for inner_node in node.body:
#                 if isinstance(inner_node, ast.FunctionDef):
#                     output_file.write(f'"""{ast.get_docstring(inner_node)}"""\n')
#                     output_file.write(f'def {inner_node.name}():\n    pass\n')

for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name == function_name:
        with open('output_file.py', 'w') as output_file:
            for inner_node in node.body:
                if isinstance(inner_node, ast.FunctionDef):
                    print(f'"""{ast.get_docstring(inner_node)}"""\n')
                    print(f'def {inner_node.name}():\n    pass\n')

