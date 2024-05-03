import random
import time
import gymnasium as gym
import os
from stable_baselines3 import DQN
import sumo_rl
import csv

import sys
sys.path.append('/media/sergiovz/Volume/uni_proj/rl-traffic-lights/generator/')

from generator_test import TrafficGenerator



nVehicles = 2500
nTests = 20

csv_file_path = f'output_{nVehicles}/'
tests = {
    f"dqn_{nVehicles}_{i}.csv": [random.randint(1, 100000), nVehicles] for i in range(1, nTests + 1)
    }

NUM_SECONDS = 28000
ITERATIONS = 5400
model_path = "../models/DQN_49ore/best_847800.zip" # Specificare il modello
times_file_path = os.path.join(csv_file_path, 'times.txt')

if not os.path.exists(csv_file_path):
    os.makedirs(csv_file_path)
    
constants_file_path = os.path.join(csv_file_path, 'constants.txt')

with open(constants_file_path, 'a') as constants_file:
    constants_file.write("Costanti inizializzate:\n\n")

    # Salvataggio delle costanti
    constants_file.write("tests:\n")
    for test_name, test_values in tests.items():
        constants_file.write(f"{test_name}: {test_values}\n")

    constants_file.write(f"\nNUM_SECONDS: {NUM_SECONDS}\n")
    constants_file.write(f"ITERATIONS: {ITERATIONS}\n")
    constants_file.write(f"model_path: {model_path}\n")
    constants_file.write(f"csv_file_path: {csv_file_path}\n")
    

for output_file, values in tests.items():
    trafficGenerator = TrafficGenerator(NUM_SECONDS, values[1])
    trafficGenerator.generate_routefile(values[0])

    env = gym.make('sumo-rl-v0',
                   net_file='../routes/environment.net.xml',
                   route_file='../routes/episode_routes_test.rou.xml',
                   use_gui=False,
                   num_seconds=NUM_SECONDS)

    model = DQN.load(model_path, env=env)

    obs, info = env.reset()

    with open(csv_file_path + output_file, 'a', newline='') as csv_file:
        fieldnames = info.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if csv_file.tell() == 0:
            writer.writeheader()

        with open(times_file_path, 'a') as times_file:
            for _ in range(ITERATIONS):
                env.render()
                start_time = time.time()
                action, _ = model.predict(obs)
                obs, reward, done, _, info = env.step(action)
                end_time = time.time()

                writer.writerow(info)
                times_file.write(f"{end_time - start_time}\n")

    env.close()