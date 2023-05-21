import networkx as nx

# Create an example power grid tree graph
power_grid = nx.DiGraph()
power_grid.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7)])
# power_grid.nodes[1]['type'] = 'generator'
# power_grid.nodes[2]['type'] = 'load'
# power_grid.nodes[3]['type'] = 'load'
# power_grid.nodes[4]['type'] = 'load'
# power_grid.nodes[5]['type'] = 'load'
# power_grid.nodes[6]['type'] = 'load'
power_grid.nodes[1]['power'] = 0  # Load power value
power_grid.nodes[2]['power'] = 10  # Load power value
power_grid.nodes[3]['power'] = 15  # Load power value
power_grid.nodes[4]['power'] = 8   # Load power value
power_grid.nodes[5]['power'] = 12  # Load power value
power_grid.nodes[6]['power'] = 6   # Load power value
power_grid.nodes[7]['power'] = 3   # Load power value

# Function to calculate and assign flowing power on edges
def calculate_flowing_power(graph, node):
    successors = list(graph.successors(node))
    total_power = 0
    if not successors:
        return graph.nodes[node]['power']
    for successor in successors:
        edge_data = graph.get_edge_data(node, successor)
        power = calculate_flowing_power(graph, successor)
        edge_data['flowing_power'] = power
        total_power += power
    total_power += graph.nodes[node]['power']
    return total_power

# Add loads and calculate flowing power
calculate_flowing_power(power_grid, 1)

# Print edge data with flowing power
for edge in power_grid.edges:
    edge_data = power_grid.get_edge_data(*edge)
    print(f"Edge {edge}: Flowing Power = {edge_data['flowing_power']}")
