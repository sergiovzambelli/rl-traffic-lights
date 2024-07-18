import time
import os
from stable_baselines3.common.monitor import Monitor
from generator import TrafficGenerator
import random
from threshold import isFinished, reachedTimeout
from utils import CustomCallback, create_env, generateAllRoutes, getRoutes
from stable_baselines3.common.evaluation import evaluate_policy


routes_number = 32

def train_model(seconds, vehicles, step_name, ipotesys, model, generation_function, global_path, multi_staged = False):
  
  # Path dei file salvati
  current_path = global_path + "/" + step_name + "/" + ipotesys + "/"
  
  if not os.path.exists(current_path):
    os.makedirs(current_path)
    
  # Generazione di tutti i route
  generateAllRoutes(seconds=seconds, vehicles=vehicles, route_number=routes_number, routes_path=current_path + "routes/", route_type=ipotesys, generation_function=generation_function, multi_staged=multi_staged)

  routes = getRoutes(current_path + "routes/")
  routes_index = 0
  
  env = create_env(seconds, routes[routes_index])
  env = Monitor(env, current_path, override_existing=False)
  model.set_env(env)  
  
  callback = CustomCallback(current_path + "monitor_2.csv")

  actions = seconds/5
  repeat = True
  start_time = time.time()
        
  try:
    while repeat:
      model.learn(total_timesteps=actions, reset_num_timesteps = False, callback = callback)
      repeat = not isFinished(current_path + "monitor.csv") and not reachedTimeout(current_path + "monitor.csv", 12900)
      if repeat:
        routes_index = (routes_index + 1) % routes_number
        env = create_env(seconds, routes[routes_index])
        env = Monitor(env, current_path, override_existing=False)
        model.set_env(env)
  except Exception as e:
    print(e)
      
  end_time = time.time()
  duration_minutes = (end_time - start_time) / 60

  with open(current_path + "info.txt", "a") as f:
    f.write(f"Execution time: {duration_minutes:.2f} min\n")
    