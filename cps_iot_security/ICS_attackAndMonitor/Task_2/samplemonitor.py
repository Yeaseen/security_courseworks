import sys
import rtamt

# Monitor for STL traces
# Registers Description: TODO: map out the rest of the registers
# Registry 1: Associated with the bottle sensor. Value is 1 if the bottle is under the nozzle.
# Registry 2: ?????
# Registry 3: ?????
# Registry 4: Associated with the nozzle. Value 1 opens the nozzle.
# Registry 5: ?????
# ......
# Registry N: ?????

def monitor():
    # Read the traces
    with open('traces.txt', 'r') as file:
        traces = [list(map(float, line.strip().split(','))) for line in file]

    # Split the traces into timestamps and register values
    timestamps = [trace[0] for trace in traces]
    register_values = [trace[1:] for trace in traces]

    # TODO: update the below variables replacing "r1" and "r2" as necessary, possibly creating more registers depending on the spec
    r1_values = [[timestamps[i], register_values[i][0]] for i in range(len(timestamps))]
    r3_values = [[timestamps[i], register_values[i][2]] for i in range(len(timestamps))]
    r4_values = [[timestamps[i], register_values[i][3]] for i in range(len(timestamps))]

    spec = rtamt.StlDenseTimeSpecification()
    spec.name = 'Plant Monitoring'
    spec.declare_var('r1', 'float')
    spec.declare_var('r3', 'float')
    spec.declare_var('r4', 'float')
    spec.set_var_io_type('r1', 'input')
    spec.set_var_io_type('r3', 'output')
    spec.set_var_io_type('r4', 'output')


    # TODO: Example STL specification #2 for Filling phase. Adjust based on your needs.
    # You may want to start out with some simpler specs to better understand the robustness
    spec.spec = 'always((r1 ==1) implies ((r4 ==1) and (r3 == 0)))'

    try:
        spec.parse()
    except rtamt.RTAMTException as err:
        print('RTAMT Exception: {}'.format(err))
        sys.exit()

    rob = spec.evaluate(['r1', r1_values], ['r4', r4_values], ['r3', r3_values])

    print('Robustness: {}'.format(rob))

if __name__ == '__main__':
    # Process arguments
    monitor()
