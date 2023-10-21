import sys
import rtamt

# Monitor for STL traces


#The Registrers Descriptions are  wrong in the TryHackMe's (Attacking ICS Plant #1)  webpage
# Registers Description: TODO: map out the rest of the registers
# Registry 1: Associated with the bottle sensor. Value is 0 when bottle is under the nozzle. Value is 1 when roller is moving and bottle isn't under the nozzle.

# Registry 2: Associated with the water level sensor. Value is 1 until the bottle is filled. Value is 0 when the bottle is full.

# Registry 3: Associated with the roller actuators. Value 0 when roller is stopped and water is being filled. Value is 1 when roller is moving.

# Registry 4: Associated with the nozzle. Value 1 when the water is being filled and nozzle is open. Value 0 when bottle is fully filled and nozzle is closed.
# Registry 5: ?????
# ......
# Registry 16: Associated with the plant. Value 1 starts the plant. And I got Value 2 after some time.


def spec1(T_int_value,roller_values, nozzle_values):
    spec = rtamt.StlDenseTimeSpecification()
    spec.name = 'Initialization Phase Monitoring'

    spec.declare_var('nozzle', 'float')
    spec.declare_var('roller', 'float')
    spec.declare_const('T', 'float', T_int_value)
    spec.set_var_io_type('nozzle', 'input')
    spec.set_var_io_type('roller', 'input')
    spec.spec = 'always[0:T s]((roller == 1) and (nozzle == 0))'

    try:
        spec.parse()
    except rtamt.RTAMTException as err:
        print('RTAMT Exception: {}'.format(err))
        sys.exit()
    #loop_size=len(nozzle_values)
    #p=[]
    #for i in range(loop_size):
    #    y=[nozzle_values[i]]; z=[roller_values[i]]
    #    rob = spec.evaluate(['roller', z], ['nozzle', y])
    #    p.append(rob[0])
    #print('Robustness of {} : {} '.format(spec.name,p))
    
    rob = spec.evaluate(['roller', roller_values], ['nozzle', nozzle_values])
    print('Robustness of {} : {} '.format(spec.name,rob))

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
    spec.spec = 'always((bottle_sensor == 1) implies response)'

    try:
        spec.parse()
    except rtamt.RTAMTException as err:
        print('RTAMT Exception: {}'.format(err))
        sys.exit()
    #=========FOR GETTING robustness value for each sample to see the transition==========
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



def spec3(water_level_sensor_values,roller_values,nozzle_values):
    spec = rtamt.StlDenseTimeSpecification()
    spec.name = 'Moving Phase Monitoring'
    spec.declare_var('nozzle', 'float')
    spec.declare_var('roller', 'float')
    spec.declare_var('water_level_sensor', 'float')
    spec.declare_var('response', 'float')
    spec.set_var_io_type('water_level_sensor', 'input')
    spec.set_var_io_type('nozzle', 'output')
    spec.set_var_io_type('roller', 'output')

    # TODO: Example STL specification #3 for Filling phase. Adjust based on your needs.
    # You may want to start out with some simpler specs to better understand the robustness
    spec.add_sub_spec('response = ((nozzle == 0) and (roller == 1))')
    spec.spec = 'always((water_level_sensor == 1) implies response)'

    try:
        spec.parse()
    except rtamt.RTAMTException as err:
        print('RTAMT Exception: {}'.format(err))
        sys.exit()

    #loop_size=len(water_level_sensor_values)
    #p=[]
    #for i in range(loop_size):
    #    x=[water_level_sensor_values[i]]; y=[nozzle_values[i]]; z=[roller_values[i]]
    #    rob = spec.evaluate(['water_level_sensor', x], ['nozzle', y], ['roller', z])
     #   p.append(rob[0])
    #print('Robustness of {} : {} '.format(spec.name,p))
    
    
    rob = spec.evaluate(['water_level_sensor', water_level_sensor_values], ['nozzle', nozzle_values], ['roller', roller_values])
    print('Robustness of {} : {} '.format(spec.name,rob))
    
    
    
    

def spec4(plant_status_values,roller_values,nozzle_values):
    spec = rtamt.StlDenseTimeSpecification()
    spec.name = 'Start/Stop Behavior Monitoring'
    spec.declare_var('nozzle', 'float')
    spec.declare_var('roller', 'float')
    spec.declare_var('plant_status', 'float')
    spec.declare_var('response', 'float')
    spec.set_var_io_type('plant_status', 'input')
    spec.set_var_io_type('nozzle', 'output')
    spec.set_var_io_type('roller', 'output')

    # TODO: Example STL specification #4 for Filling phase. Adjust based on your needs.
    # You may want to start out with some simpler specs to better understand the robustness
    spec.add_sub_spec('response = ((nozzle == 0) and (roller == 0))')
    spec.spec = 'always((plant_status == 0) implies response)'

    try:
        spec.parse()
    except rtamt.RTAMTException as err:
        print('RTAMT Exception: {}'.format(err))
        sys.exit()

    #loop_size=len(plant_status_values)
    #p=[]
    #for i in range(loop_size):
    #    x=[plant_status_values[i]]; y=[nozzle_values[i]]; z=[roller_values[i]]
    #    rob = spec.evaluate(['plant_status', x], ['nozzle', y], ['roller', z])
    #    p.append(rob[0])
    #print('Robustness of {} : {} '.format(spec.name,p))
    
    rob = spec.evaluate(['plant_status', plant_status_values], ['nozzle', nozzle_values], ['roller', roller_values])
    print('Robustness of {} : {} '.format(spec.name,rob))

def monitor():
    # Read the traces
    with open('traces.txt', 'r') as file:
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

    T_int_value=timestamps[0]

    #print(bottle_sensor_values)
    #print(nozzle_values)
    #print(roller_values)
    #spec1Test(roller_values,nozzle_values)

    spec1(T_int_value,roller_values,nozzle_values)
    spec2(bottle_sensor_values,roller_values,nozzle_values)
    spec3(water_level_sensor_values,roller_values,nozzle_values)
    spec4(plant_status_values,roller_values,nozzle_values)

if __name__ == '__main__':
    # Process arguments
    monitor()
