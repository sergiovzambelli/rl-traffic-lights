from matplotlib import pyplot as plt
import numpy as np
from generation_functions import *
from ipotesi import generate_xml
from ipotesi_multi_stage import generate_xml_multi_stage

class TrafficGenerator:
    def __init__(self, seconds, n_cars_generated, type, route_path):
        self._n_cars_generated = n_cars_generated  
        self._seconds = seconds
        self._type = type
        self._route_path = route_path

    def generate_routefile(self, seed, n, function, multi_staged = False):
        """
        Generation of the route of every car for one episode
        """
        np.random.seed(seed) 
        max_stop = 20

        if function == "uniform":
            car_gen_steps = uniform(self._seconds, self._n_cars_generated)
            stop_time = uniform_array(self._n_cars_generated, max_stop)
            
        elif function == "weibull":
            car_gen_steps = weibull(self._seconds, self._n_cars_generated)
            stop_time = weibull_array(self._n_cars_generated, max_stop, 100, 0.03*self._n_cars_generated, 0.12*self._n_cars_generated)
            
        elif function == "bimodal":
            car_gen_steps = bimodal(self._seconds, self._n_cars_generated)
            stop_time = bimodal(max_stop, self._n_cars_generated, sorted=False)
        
        if multi_staged: generate_xml_multi_stage(car_gen_steps, self._route_path + "routes.rou" + str(n) + ".xml", stop_time)
        else: generate_xml(self._type, car_gen_steps, self._route_path + "routes.rou" + str(n) + ".xml", stop_time)