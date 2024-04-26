import gymnasium as gym
import os
from stable_baselines3 import DQN
import sumo_rl
import csv

from generator import TrafficGenerator


NUM_SECONDS = 28000
ITERATIONS = 5400 #int(NUM_SECONDS / 5)
model_path = "models/DQN/518400.zip"
csv_file_path = 'outputs/'

env = gym.make('sumo-rl-v0',
                net_file='environment.net.xml',
                route_file='episode_routes.rou.xml',
                use_gui=False,
                num_seconds=NUM_SECONDS)

model = DQN.load(model_path, env=env)

obs, info = env.reset()

with open(csv_file_path + "output_test.csv", 'a', newline='') as csv_file:
    fieldnames = info.keys()
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    if csv_file.tell() == 0:
        writer.writeheader()

    for _ in range(ITERATIONS):
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, _, info = env.step(action)

        writer.writerow(info)
