import random
import gymnasium as gym
import os
from stable_baselines3 import DQN
import sumo_rl
import csv
import argparse

from generator import TrafficGenerator

def main(models_path, csv_file_path, sound_file):
    NUM_SECONDS = 86400
    ITERATIONS = int(NUM_SECONDS / 5)

    if not os.path.exists(csv_file_path):
        os.makedirs(csv_file_path)

    trafficGenerator = TrafficGenerator(NUM_SECONDS, 20000, "test", "")
    trafficGenerator.generate_routefile(random.randint(0, 100000), 0, "bimodal", False)

    env = gym.make('sumo-rl-v0',
                   net_file='environment.net.xml',
                   route_file='test.rou.xml',
                   use_gui=False,
                   num_seconds=NUM_SECONDS)

    for model_path in models_path:
        # Load model
        model = DQN.load(model_path, env=env)

        obs, info = env.reset()

        # Remove the '.zip' extension from the model_path to use as the CSV file name
        model_name = os.path.splitext(model_path)[0]

        with open(os.path.join(csv_file_path, f"{model_name}.csv"), 'a', newline='') as csv_file:
            fieldnames = info.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if csv_file.tell() == 0:
                writer.writeheader()

            for _ in range(ITERATIONS):
                env.render()
                action, _ = model.predict(obs)
                obs, reward, done, _, info = env.step(action)

                writer.writerow(info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run traffic signal control with RL models.")
    parser.add_argument('--models', nargs='+', required=True, help="List of model paths")
    parser.add_argument('--output_dir', type=str, required=True, help="Directory for output CSV files")
    args = parser.parse_args()

    main(args.models, args.output_dir, args.sound)
