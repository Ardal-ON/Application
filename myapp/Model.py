import numpy as np
import joblib
from sklearn.naive_bayes import GaussianNB

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

        self._model = joblib.load('E:/USC/AME 505/project/Application/myapp/assets/models/gaussian_naive_bayes_model.joblib')

        self.random_initialization()
        self.predict()

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
    
    def get_parameter_dict(self):
        return self._parameter_dict

        
