import random
import numpy as np

# Funzione per generare le quattro ipotesi: balanced , EW, NS, e random
def generate_xml(type, car_gen_steps, route_path, stop_time):
    if type == "random":
        type = random.choice(["EW", "NS", "balanced"])

    # stocasticità su direzione
    straight_value = np.random.normal(0.70, 0.1)
    generation_value = np.random.normal(0.75, 0.1)

    coming_from_percentage = generation_value if type == "EW" else 1 - generation_value

    routes_header = """
    <routes>
        
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
        <route id="S_E" edges="S2TL TL2E"/>
        
        
    """

    route_map = {
        'EW': ['W_E', 'E_W', 'W_N', 'W_S', 'E_N', 'E_S'],
        'NS': ['N_S', 'S_N', 'N_W', 'N_E', 'S_W', 'S_E'],
        'balanced': ['W_E', 'E_W', 'N_S', 'S_N', 'W_N', 'W_S', 'E_N', 'E_S', 'S_W', 'N_W', 'N_E', 'S_E']
    }

    def generate_vehicle(car_counter, step, stop, route_id, stop_lane):
        return (f'    <vehicle id="{route_id}_{car_counter}" type="standard_car" route="{route_id}" '
                f'depart="{step}" departLane="random" departSpeed="10" arrivalLane="{random_out_lane}"> '
                f'<stop lane="TL2{route_id.split("_")[1]}_{stop_lane}" startPos="-10" endPos="-10" duration="{stop}"/> '
                '</vehicle>')

    with open(route_path, "w") as routes:
        routes.write(routes_header)
        for car_counter, (step, stop) in enumerate(zip(car_gen_steps, stop_time)):
            random_out_lane = np.random.randint(0, 4)
            stop_lane = random_out_lane
            axis_direction = np.random.uniform()
            straight_or_turn = np.random.uniform()
            route_straight = np.random.randint(1, 3)
            route_turn = np.random.randint(1, 5)

            if type in ['EW', 'NS']:
                if axis_direction < coming_from_percentage:
                    if straight_or_turn < straight_value:
                        route_id = route_map['EW'][route_straight - 1] if type == 'EW' else route_map['NS'][route_straight - 1]
                        routes.write(generate_vehicle(car_counter, step, stop, route_id, stop_lane) + '\n')
                    else:
                        route_id = route_map['EW'][route_turn + 1] if type == 'EW' else route_map['NS'][route_turn + 1]
                        routes.write(generate_vehicle(car_counter, step, stop, route_id, stop_lane) + '\n')
                else:
                    if straight_or_turn < straight_value:
                        route_id = route_map['NS'][route_straight - 1] if type == 'EW' else route_map['EW'][route_straight - 1]
                        routes.write(generate_vehicle(car_counter, step, stop, route_id, stop_lane) + '\n')
                    else:
                        route_id = route_map['NS'][route_turn + 1] if type == 'EW' else route_map['EW'][route_turn + 1]
                        routes.write(generate_vehicle(car_counter, step, stop, route_id, stop_lane) + '\n')
            else:
                if straight_or_turn < straight_value:
                    route_id = route_map['balanced'][np.random.randint(0, 4)]
                else:
                    route_id = route_map['balanced'][np.random.randint(4, 12)]
                routes.write(generate_vehicle(car_counter, step, stop, route_id, stop_lane) + '\n')

        routes.write('</routes>')