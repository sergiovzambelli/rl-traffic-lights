import gymnasium as gym
import os
from stable_baselines3 import DQN
import sumo_rl
import csv

from generator import TrafficGenerator

tests = {
    "output_dqn_600_3.csv": [103, 600],
    "output_dqn_600_4.csv": [49039, 600],
    "output_dqn_4000_1.csv": [5, 4000],
    "output_dqn_4000_2.csv": [11237, 4000],
    "output_dqn_2300_1.csv": [99, 2300],
    "output_dqn_2300_2.csv": [1847, 2300],
}

NUM_SECONDS = 28000
ITERATIONS = 5400 #int(NUM_SECONDS / 5)
model_path = "models/DQN/518400.zip"
csv_file_path = 'outputs/'

for output_file, values in tests.items():
    trafficGenerator = TrafficGenerator(NUM_SECONDS, values[1])
    trafficGenerator.generate_routefile(values[0])

    env = gym.make('sumo-rl-v0',
                   net_file='environment.net.xml',
                   route_file='episode_routes_test.rou.xml',
                   use_gui=False,
                   num_seconds=NUM_SECONDS)

    model = DQN.load(model_path, env=env)

    obs, info = env.reset()

    with open(csv_file_path + output_file, 'a', newline='') as csv_file:
        fieldnames = info.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        if csv_file.tell() == 0:
            writer.writeheader()

        for _ in range(ITERATIONS):
            env.render()
            action, _ = model.predict(obs)
            obs, reward, done, _, info = env.step(action)

            writer.writerow(info)

    env.close()
