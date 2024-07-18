import csv
import os
import random
import numpy as np
import gymnasium as gym
import glob
from generator import TrafficGenerator
from stable_baselines3.common.callbacks import BaseCallback

# Creazione environment 
def create_env(num_seconds, route_path):
    return gym.make('sumo-rl-v0',
                    net_file='environment.net.xml',
                    route_file=route_path,
                    use_gui=False,
                    num_seconds=num_seconds)
    
    
# Ogni volta che cambiano secondi o veicoli creo x file route nuovi
def generateAllRoutes(seconds, vehicles, route_number, routes_path, route_type, generation_function, multi_staged):
    trafficGenerator = TrafficGenerator(seconds, vehicles, route_type, routes_path)

    if not os.path.exists(routes_path):
        os.makedirs(routes_path)
        
    seed = [random.randint(0, 100000) for _ in range(route_number)]
    n_seed = 0
    
    for i in range(route_number):
        trafficGenerator.generate_routefile(seed=seed[n_seed], n=i, function=generation_function, multi_staged=multi_staged)
        n_seed = (n_seed + 1)%route_number
    
    
# Output: ["routes/routes.rou0.xml"]
def getRoutes(routes_path):
    routes = glob.glob(routes_path + "*.xml")
    return routes

# Callback personalizzato per raccogliere informazioni durante il training
class CustomCallback(BaseCallback):
    def __init__(self, path):
        super(CustomCallback, self).__init__(path)
        self.mean_reward = None
        self.path = path

    def _on_step(self) -> bool:
        # Registrazione della reward attuale
        reward = self.locals["rewards"]
        self.mean_reward = np.mean(reward)*100
        return True

    def _on_training_end(self) -> None:
        # Verifica se il file esiste già
        file_exists = os.path.isfile(self.path)
        
        # Apri il file in modalità append con il modulo csv
        with open(self.path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Scrivi la media della reward
            writer.writerow([self.mean_reward])