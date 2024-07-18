import math
import random
import numpy as np

def uniform(seconds, n_cars_generated, sorted = True):
  timings = np.random.uniform(0, seconds, n_cars_generated)
  if sorted: timings = np.sort(timings)
  return timings.astype(int)

def weibull(seconds, n_cars_generated, sorted = True):
  # the generation of cars is distributed according to a weibull distribution
  timings = np.random.weibull(2, n_cars_generated)
  if sorted: timings = np.sort(timings)
  
  # reshape the distribution to fit the interval 0:max_steps
  car_gen_steps_raw = []
  min_old = math.floor(timings[1]) 
  max_old = math.ceil(timings[-1])
  min_new = 0
  max_new = seconds 
  for value in timings:
      car_gen_steps_raw = np.append(car_gen_steps_raw, ((max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)

  car_gen_steps_raw = np.rint(car_gen_steps_raw)  # round every value to int -> effective steps when a car will be generated
  
  # genero un offset casuale per spostare la distribuzione
  offset_percentage = random.uniform(0.10, 0.25)
  offset = int(offset_percentage * seconds)
  
  return car_gen_steps_raw + offset

def bimodal(seconds, n_cars_generated, sorted=True):
  def generate_timings(loc, scale, size, min_val, max_val):
        timings = np.random.normal(loc=loc, scale=scale, size=size)
        while np.any(timings < min_val) or np.any(timings > max_val):
            timings = np.where((timings < min_val) | (timings > max_val),
                               np.random.normal(loc=loc, scale=scale, size=timings.shape),
                               timings)
        return timings

  loc1 = seconds / 4 
  loc2 = seconds / 2
  loc3 = loc1 + loc2

  n1 = int(n_cars_generated * 0.35)
  n2 = int(n_cars_generated * 0.15)
  n3 = int(n_cars_generated - n1 - n2)

  timings1 = generate_timings(loc1, seconds / 10, n1, 0, seconds)
  timings2 = generate_timings(loc2, seconds / 10, n2, 0, seconds)
  timings3 = generate_timings(loc3, seconds / 10, n3, 0, seconds)

  timings = np.concatenate([timings1, timings2, timings3])
  if sorted:
      timings = np.sort(timings)

  return timings.astype(int)

  # loc1 = seconds / 4 
  # loc2 = seconds / 2
  # loc3 = loc1 + loc2

  # n1 = int(n_cars_generated * 0.35)
  # n2 = int(n_cars_generated * 0.15)
  # n3 = int(n_cars_generated - n1 - n2)

  # timings1 = np.random.normal(loc=loc1, scale=seconds / 10, size=n1)
  # timings2 = np.random.normal(loc=loc2, scale=seconds / 10, size=n2)
  # timings3 = np.random.normal(loc=loc3, scale=seconds / 10, size=n3)

  # timings = np.concatenate([timings1, timings2, timings3])
  # timings = np.clip(timings, 0, seconds)
  # if sorted: timings = np.sort(timings)

  # return timings.astype(int)


# Stop utils


def uniform_array(n, max_val):
    return np.ceil(np.random.uniform(0.4*max_val, 0.6*max_val, n))

def weibull_array(n, max_value, mu, sigma_sx, sigma_dx):
    x = np.linspace(0, n-1, n)
    
    # Creare due metà della distribuzione gaussiana con sigma diversi
    gauss_sx = np.exp(-((x[x < mu] - mu) ** 2) / (2 * sigma_sx ** 2))
    gauss_dx = np.exp(-((x[x >= mu] - mu) ** 2) / (2 * sigma_dx ** 2))
    
    # Combinare le due metà
    gauss = np.concatenate((gauss_sx, gauss_dx))
    scaled_gauss = gauss / np.max(gauss) * max_value  # scalare la gaussiana per avere max_val al centro
    
    return np.ceil(scaled_gauss)