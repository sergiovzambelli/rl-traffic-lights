from datetime import datetime
import time
from matplotlib import pyplot as plt
import numpy as np
import gymnasium as gym
import os
from stable_baselines3 import DQN
from stable_baselines3 import A2C
from stable_baselines3 import PPO
from stable_baselines3.common.logger import configure
import sumo_rl
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import CheckpointCallback
from generator import TrafficGenerator
import pandas as pd
import random
from train import train_model
from utils import create_env
import sys

def seconds(hours):
    return hours * 3600

options = ["balanced", "EW", "NS"]

# Dummy env
env = gym.make('sumo-rl-v0',
            net_file='environment.net.xml',
            route_file="routes.rou.xml",
            use_gui=False,
            num_seconds=2000)

if len(sys.argv) < 2: 
    print("Usage: python3 curriculum_learning.py <name of directory>")
    sys.exit(1)
    
global_path = sys.argv[1]
model_path = global_path + "/models"

if not os.path.exists(model_path):
    os.makedirs(model_path)
    

model = DQN(
    policy="MlpPolicy",
    env=env,
    verbose=0)

start_time = time.time()


try:
    
    for option in options:
        train_model(seconds=seconds(1), vehicles=400, step_name="step1", ipotesys=option, model=model, generation_function="uniform", global_path=global_path)
    
    model.save(model_path + "/step1")
    
    train_model(seconds=seconds(1), vehicles=1500, step_name="step2", ipotesys="multi_staged", model=model, generation_function="uniform", global_path=global_path, multi_staged=True)
    
    model.save(model_path + "/step2")
    
    train_model(seconds=seconds(1), vehicles=2250, step_name="step3", ipotesys="multi_staged", model=model, generation_function="weibull", global_path=global_path, multi_staged=True)

    model.save(model_path + "/step3")
    
    train_model(seconds=seconds(3), vehicles=6000, step_name="step4", ipotesys="multi_staged", model=model, generation_function="weibull", global_path=global_path, multi_staged=True)
    model.save(model_path + "/step4")
    
    train_model(seconds=seconds(5), vehicles=8000, step_name="step5", ipotesys="multi_staged", model=model, generation_function="weibull", global_path=global_path, multi_staged=True)

    model.save(model_path + "/step5")
    
    train_model(seconds=seconds(7), vehicles=10000, step_name="step6", ipotesys="multi_staged", model=model, generation_function="weibull", global_path=global_path, multi_staged=True)

    model.save(model_path + "/step6")
    
    end_time = time.time()
    duration_hours = (end_time - start_time) / 3600
    
    with open(model_path + "/riepilogo_all_info.txt", "a") as f:
        f.write(f"Execution time: {duration_hours:.2f} h")
    
except Exception as e:
    print(e)