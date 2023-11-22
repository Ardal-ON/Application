import numpy as np
import joblib
from sklearn.naive_bayes import GaussianNB
import statistics
class Model:
    def __init__(self):
        self._parameter_dict = {
            'engine_rpm' : None,
            'lub_oil_pressure' : None,
            'fuel_pressure' : None,
            'coolant_pressure' : None,
            'lub_oil_temp' : None,
            'coolant_temp' : None,
            'engine_condition' : None
        }
        
        self._parameter_bounds_dict = {
            'engine_rpm' : [80,1450],
            'lub_oil_pressure' : [0.2,6.4],
            'fuel_pressure' : [0.6,12.0],
            'coolant_pressure' : [0.0,4.8],
            'lub_oil_temp' : [72.2,81.6],
            'coolant_temp' : [61.6,95.9],
            'engine_condition' : [0.0,1.0]
        }

        self._Maintenance_dict = {
            'engine_rpm' : None,
            'lub_oil_pressure' : None,
            'fuel_pressure' : None,
            'coolant_pressure' : None,
            'lub_oil_temp' : None,
            'coolant_temp' : None,
            'engine_condition' : None
        }

        self._parameter_mean_std_dict = {
            'engine_rpm' : [772,239.37],
            'lub_oil_pressure' : [3.3,1.0],
            'fuel_pressure' : [6.2,2.05],
            'coolant_pressure' : [2.2,0.8],
            'lub_oil_temp' : [76.6,1.6],
            'coolant_temp' : [78.4,6.1],
            'engine_condition' : [0.63,0.48]
        }

        self._model = joblib.load('E:/USC/AME 505/project/Application/myapp/assets/models/gaussian_naive_bayes_model.joblib')

        self.random_initialization()
        #self.predict()

    def random_initialization(self):
        for parameter in self._parameter_dict:
            if parameter == 'engine_condition':
                continue
            min = self._parameter_bounds_dict[parameter][0]
            max = self._parameter_bounds_dict[parameter][-1]
            self._parameter_dict[parameter] = \
                np.round(np.random.uniform(min,max),decimals=6)

    def predict(self):
        parameter_list = []

        for parameter in self._parameter_dict:
            if parameter == 'engine_condition':
                continue
            parameter_list.append(self._parameter_dict[parameter])

        self._parameter_dict['engine_condition'] = self._model.predict([parameter_list])[0]

        self.maintenance_decider()
    
    def maintenance_decider(self):
        overall =  self._parameter_dict['engine_condition']
        self._Maintenance_dict['engine_condition'] = self._parameter_dict['engine_condition']
        
        for parameter in self._parameter_dict:
            if parameter == 'engine_condition':
                continue
            mean = self._parameter_mean_std_dict[parameter][0]
            std = self._parameter_mean_std_dict[parameter][1]
            value = self._parameter_dict[parameter]
            zscore = statistics.NormalDist(mu=mean, sigma=std).zscore(value)
            if overall == 1:
                if abs(zscore) <= 3:
                    self._Maintenance_dict[parameter] = 1
                elif abs(zscore) > 3:
                    self._Maintenance_dict[parameter] = 0
            elif overall == 0:
                if abs(zscore) <= 1:
                    self._Maintenance_dict[parameter] = 1
                elif abs(zscore) <= 2:
                    self._Maintenance_dict[parameter] = 0.5
                elif abs(zscore) > 2 :
                    self._Maintenance_dict[parameter] = 0
                    

    
    def get_parameter_dict(self):
        return self._parameter_dict
    
    def set_parameter_dict(self,parameter,value):
        self._parameter_dict[parameter] = value

    def get_parameter_bounds_dict(self):
        return self._parameter_bounds_dict
    
    def get_Maintenance_dict(self):
        return self._Maintenance_dict
        
