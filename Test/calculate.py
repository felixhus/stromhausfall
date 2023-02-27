import networkx as nx
import numpy as np
import pandas as pd
from ortools.graph.python import min_cost_flow

# R = [0, 1, 0, 0, 0, 1, 0, 0, 2, 1]
#
# a = np.array([[-1, 0, 0, 0, -1, 0, 0, 0, 0, 0],
#               # [1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
#               [0, 1, -1, 1, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 0, 1, -1, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 1, -1, 0, 0, 0],
#               [0, 0, 1, 0, 0, 0, 1, -1, -1, -1],
#               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
#               [0, R[1], 0, 0, 0, -R[5], 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, R[8], -R[9]]])
#
# b = np.array([-14, 0, -2, 0, 0, 0, 6, 10, 0, 0])
#
# x = np.linalg.solve(a, b)
#
# print(x)


#
#
# def main():
#     """MinCostFlow simple interface example."""
#     # Instantiate a SimpleMinCostFlow solver.
#     smcf = min_cost_flow.SimpleMinCostFlow()
#
#     # Define four parallel arrays: sources, destinations, capacities,
#     # and unit costs between each pair. For instance, the arc from node 0
#     # to node 1 has a capacity of 15.
#     start_nodes = np.array([0, 1, 1, 2, 3, 4, 4])
#     end_nodes = np.array([1, 2, 3, 4, 4, 5, 6])
#     capacities = np.array([1, 1, 1, 1, 1, 1, 1])
#     unit_costs = np.array([1, 2, 3, 1, 1, 1, 1])
#
#     # Define an array of supplies at each node.
#     supplies = [12, 0, 0, 0, 0, -4, -8]
#
#     # Add arcs, capacities and costs in bulk using numpy.
#     all_arcs = smcf.add_arcs_with_capacity_and_unit_cost(
#         start_nodes, end_nodes, capacities, unit_costs)
#
#     # Add supply for each nodes.
#     smcf.set_nodes_supply(np.arange(0, len(supplies)), supplies)
#
#     # Find the min cost flow.
#     status = smcf.solve()
#
#     if status != smcf.OPTIMAL:
#         print('There was an issue with the min cost flow input.')
#         print(f'Status: {status}')
#         exit(1)
#     print(f'Minimum cost: {smcf.optimal_cost()}')
#     print('')
#     print(' Arc    Flow / Capacity Cost')
#     solution_flows = smcf.flows(all_arcs)
#     costs = solution_flows * unit_costs
#     for arc, flow, cost in zip(all_arcs, solution_flows, costs):
#         print(
#             f'{smcf.tail(arc):1} -> {smcf.head(arc)}  {flow:3}  / {smcf.capacity(arc):3}       {cost}'
#         )
#
#
# if __name__ == '__main__':
#     main()


# Create the first Series
index1 = pd.date_range('2022-01-01', periods=12, freq='M')
data1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
series1 = pd.Series(data1, index=index1)

# Create the second Series
index2 = pd.date_range('2022-01-01', periods=12, freq='M')
data2 = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0, -10]
series2 = pd.Series(data2, index=index2)

# Create the third Series
index3 = pd.date_range('2022-01-01', periods=12, freq='M')
data3 = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 0, -100]
series3 = pd.Series(data3, index=index3)

# Combine the Series into one dataframe
df = pd.DataFrame({'series1': series1, 'series2': series2, 'series3': series3})
