import random
import numpy as np

def generate_xml_multi_stage(car_gen_steps, route_path, stop_time):
    
    def generate_vehicle(car_counter, step, stop, route_id, stop_lane, routes):
        print(f'    <vehicle id="{route_id}_{car_counter}" type="standard_car" route="{route_id}" depart="{step}" departLane="random" departSpeed="10" arrivalLane="random" > <stop lane="{stop_lane}" startPos="-10" endPos="-10" duration="{stop}"/> </vehicle>', file=routes)
    
    def get_route(route_type, car_counter, step, stop, straight_value, routes):
        random_out_lane = np.random.randint(0,4)
        stop_lane = random_out_lane
        axis_direction = np.random.uniform()
        straight_or_turn = np.random.uniform()
        route_straight = np.random.randint(1, 3)
        route_turn = np.random.randint(1, 5)
        
        if route_type == 'EW':
            if axis_direction < 0.75:
                if straight_or_turn < straight_value:
                    route_id = 'W_E' if route_straight == 1 else 'E_W'
                else:
                    route_id = ['W_N', 'W_S', 'E_N', 'E_S'][route_turn - 1]
            else:
                if straight_or_turn < straight_value:
                    route_id = 'N_S' if route_straight == 1 else 'S_N'
                else:
                    route_id = ['N_W', 'N_E', 'S_W', 'S_E'][route_turn - 1]
        elif route_type == 'NS':
            if axis_direction < 0.75:
                if straight_or_turn < straight_value:
                    route_id = 'N_S' if route_straight == 1 else 'S_N'
                else:
                    route_id = ['N_W', 'N_E', 'S_W', 'S_E'][route_turn - 1]
            else:
                if straight_or_turn < straight_value:
                    route_id = 'W_E' if route_straight == 1 else 'E_W'
                else:
                    route_id = ['W_N', 'W_S', 'E_N', 'E_S'][route_turn - 1]
        else:
            if straight_or_turn < straight_value:
                route_straight = np.random.randint(1, 5)
                route_id = ['W_E', 'E_W', 'N_S', 'S_N'][route_straight - 1]
            else:
                route_turn = np.random.randint(1, 9)
                route_id = ['W_N', 'W_S', 'N_W', 'N_E', 'E_N', 'E_S', 'S_W', 'S_E'][route_turn - 1]
        
        stop_lane = f"TL2{route_id.split('_')[1]}_{stop_lane}"
        generate_vehicle(car_counter, step, stop, route_id, stop_lane, routes)

    straight_value = 0.70 + np.random.uniform(-0.05, 0.05)
    
    num_vehicles = len(car_gen_steps)
    quarter = num_vehicles // 4
    
    route_types = ['balanced', 'NS', 'EW']
    route_type_quarters = [random.choice(route_types) for _ in range(4)]

    
    with open(route_path, "w") as routes:
        print("""<routes>
        <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="25" sigma="0.5" />
        <route id="W_N" edges="W2TL TL2N"/>
        <route id="W_E" edges="W2TL TL2E"/>
        <route id="W_S" edges="W2TL TL2S"/>
        <route id="N_W" edges="N2TL TL2W"/>
        <route id="N_E" edges="N2TL TL2E"/>
        <route id="N_S" edges="N2TL TL2S"/>
        <route id="E_W" edges="E2TL TL2W"/>
        <route id="E_N" edges="E2TL TL2N"/>
        <route id="E_S" edges="E2TL TL2S"/>
        <route id="S_W" edges="S2TL TL2W"/>
        <route id="S_N" edges="S2TL TL2N"/>
        <route id="S_E" edges="S2TL TL2E"/>""", file=routes)

        for car_counter, (step, stop) in enumerate(zip(car_gen_steps, stop_time)):
            if car_counter < quarter:
                route_type = route_type_quarters[0]
            elif car_counter < 2 * quarter:
                route_type = route_type_quarters[1]
            elif car_counter < 3 * quarter:
                route_type = route_type_quarters[2]
            else:
                route_type = 'random'
            
            get_route(route_type, car_counter, step, stop, straight_value, routes)
        
        print('</routes>', file=routes)
