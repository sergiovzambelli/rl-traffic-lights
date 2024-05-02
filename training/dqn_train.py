import gymnasium as gym
import os
from stable_baselines3 import DQN
import sumo_rl

from generator_train import TrafficGenerator

model_dir = "models/DQN_2"
logdir = "logs"

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

env = gym.make('sumo-rl-v0',
                net_file='../routes/environment.net.xml',
                route_file='../routes/episode_routes.rou.xml',
                use_gui=False,
                num_seconds=28000) #num_seconds corrisponde al tempo in secondi massimo della simulazione

model = DQN("MlpPolicy", env, verbose=0, tensorboard_log=logdir)


# Singolo episodio da 5400 steps, ossia 5400 azioni
# Quando il numero di steps si azzera la simulazione conclude
TIMESTEPS = 5400
i = 0

# trafficGenerator = TrafficGenerator(TIMESTEPS, 5400)
# trafficGenerator.generate_routefile(723)

while True:
  model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps = False, tb_log_name = "DQN_2")
  model.save(f"{model_dir}/{TIMESTEPS*i}")
  i = i+1

env.close()