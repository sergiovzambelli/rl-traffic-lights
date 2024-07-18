import math
import numpy as np
import pandas as pd

threshold = 10

scale_factor = 500

def isFinished(monitor_path):
    data = pd.read_csv(monitor_path, delimiter=",", header=None)
    r_values = data[0]
    total_data_points = len(r_values)
    
    if total_data_points < 5:
        return False
    
    y = np.exp(np.linspace(0, 200, 300) /  scale_factor)
    y_normalized = y / np.max(y)
    
    # Calcola gamma
    gamma = 1 - y_normalized[total_data_points-1]

    if gamma > 0:
        last_gamma_values = r_values[-math.ceil(gamma*total_data_points):]
        mean_last_gamma = np.mean(last_gamma_values)
        mean_last_gamma_modded = mean_last_gamma * gamma
        print(mean_last_gamma_modded)
        if math.ceil(mean_last_gamma_modded) == 0:
            return True
    
    return False

def reachedTimeout(monitor_path, seconds_threshold):
    data = pd.read_csv(monitor_path, delimiter=",", header=None)
    third_column_values = data[2]
    total_time = third_column_values.sum()
    
    if total_time > seconds_threshold:
        return True
    else:
        return False