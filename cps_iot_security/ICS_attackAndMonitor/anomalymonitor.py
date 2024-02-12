import sys
import rtamt


#The Registrers Descriptions are  wrong in the TryHackMe's (Attacking ICS Plant #1)  webpage
# Registers Description: TODO: map out the rest of the registers
# Registry 1: Associated with the bottle sensor. Value is 0 when bottle is under the nozzle. Value is 1 when roller is moving and bottle isn't under the nozzle.

# Registry 2: Associated with the water level sensor. Value is 1 until the bottle is filled. Value is 0 when the bottle is full.

# Registry 3: Associated with the roller actuators. Value 0 when roller is stopped and water is being filled. Value is 1 when roller is moving.

# Registry 4: Associated with the nozzle. Value 1 when the water is being filled and nozzle is open. Value 0 when bottle is fully filled and nozzle is closed.
# Registry 5: ?????
# ......
# Registry 16: Associated with the plant. Value 1 starts the plant. And I got Value 2 after some time.


def spec2(bottle_sensor_values,roller_values, nozzle_values):
    spec = rtamt.StlDenseTimeSpecification()
    spec.name = 'Filling Phase Monitoring'
    spec.declare_var('nozzle', 'float')
    spec.declare_var('roller', 'float')
    spec.declare_var('bottle_sensor', 'float')
    spec.declare_var('response', 'float')
    spec.set_var_io_type('bottle_sensor', 'input')
    spec.set_var_io_type('nozzle', 'output')
    spec.set_var_io_type('roller', 'output')

    # TODO: Example STL specification #2 for Filling phase. Adjust based on your needs.
    # You may want to start out with some simpler specs to better understand the robustness
    spec.add_sub_spec('response = ((nozzle == 1) and (roller == 0))')
    spec.spec = 'always((bottle_sensor == 0) implies response)'

    try:
        spec.parse()
    except rtamt.RTAMTException as err:
        print('RTAMT Exception: {}'.format(err))
        sys.exit()
    
    #print(len(bottle_sensor_values))
    #loop_size=len(bottle_sensor_values)
    #p=[]
    #for i in range(loop_size):
    #    x=[bottle_sensor_values[i]]; y=[nozzle_values[i]]; z=[roller_values[i]]
    #    rob = spec.evaluate(['bottle_sensor', x], ['nozzle', y], ['roller', z])
    #    p.append(rob[0])
    #print('Robustness of {} : {} '.format(spec.name,p))
    
    rob = spec.evaluate(['bottle_sensor', bottle_sensor_values], ['nozzle', nozzle_values], ['roller', roller_values])
    print('Robustness of {} : {} '.format(spec.name,rob))



def monitor():
    # Read the traces
    with open('traces_attack_shutdown2.txt', 'r') as file:
        traces = [list(map(float, line.strip().split(','))) for line in file]

    # Split the traces into timestamps and register values
    timestamps = [trace[0] for trace in traces]
    register_values = [trace[1:] for trace in traces]

    # TODO: update the below variables replacing "r1" and "r2" as necessary, possibly creating more registers depending on the spec
    bottle_sensor_values = [[timestamps[i], register_values[i][0]] for i in range(len(timestamps))]
    water_level_sensor_values = [[timestamps[i], register_values[i][1]] for i in range(len(timestamps))]
    roller_values = [[timestamps[i], register_values[i][2]] for i in range(len(timestamps))]
    nozzle_values = [[timestamps[i], register_values[i][3]] for i in range(len(timestamps))]
    plant_status_values = [[timestamps[i], register_values[i][15]] for i in range(len(timestamps))]


    #print(bottle_sensor_values)
    #print(nozzle_values)
    #print(roller_values)

    spec2(bottle_sensor_values,roller_values,nozzle_values)

if __name__ == '__main__':
    # Process arguments
    monitor()
