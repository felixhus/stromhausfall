import time, json, copy
import source.modules as modules

def measure_time(stopwatch=None):
    """This function measures the time a program takes. It outputs the elapsed wall and cpu time.

    **USAGE:** To start the measurement, call the function without input and store the return value.
    To stop the measurement call the function with the stored value as input.
        stopwatch = measure_time()
        measure_time(stopwatch)

    :param stopwatch: Stores the start time (wall and cpu)
    :return: Returns the start time when called without parameter
    """
    if stopwatch is None:
        stopwatch = [0, 0]
    if stopwatch[0] != 0:
        time_wall_stop = time.time()
        time_cpu_stop = time.process_time()
        elapsed_wall_time = time_wall_stop - stopwatch[0]
        elapsed_process_time = time_cpu_stop - stopwatch[1]
        print("Elapsed wall time: %.2f Milliseconds" % (elapsed_wall_time * 1000))
        print("Elapsed process time: %.2f Milliseconds" % (elapsed_process_time * 1000))
    else:
        stopwatch[0] = time.time()
        stopwatch[1] = time.process_time()
        return stopwatch


with open('test_grid_runtime.json') as file:
    data = json.load(file)
    timesteps = 10080

    calculate_input = copy.deepcopy(data['gridObject_dict'])
    for node in data['gridObject_dict']:
        if calculate_input[node]['object_type'] != 'line':
            calculate_input[node]['power'] = calculate_input[node]['power'][0:timesteps]

    stopwatch = measure_time()

    modules.calculate_power_flow(data['cyto_grid'], calculate_input)

    measure_time(stopwatch)
