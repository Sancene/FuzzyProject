import numpy as np
import skfuzzy as fuzz
import random as rd
from time import sleep
from skfuzzy import control as ctrl
import warnings

warnings.filterwarnings("ignore")

class fuzzyCalculator:
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(fuzzyCalculator, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        ClientSpeed = ctrl.Antecedent(np.arange(0, 1001, 1), 'ClientSpeed') #mb
        ServerResponseTime = ctrl.Antecedent(np.arange(0, 101, 1), 'ServerResponseTime') #ms
        self.TrafficControl = ctrl.Consequent(np.arange(0, 101, 1), 'TrafficControl')
        
        # Auto-membership function population is possible with .automf(3, 5, or 7)
        ClientSpeed.automf(3)
        ServerResponseTime.automf(3, invert=True)
        
        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        self.TrafficControl['Low'] = fuzz.trimf(self.TrafficControl.universe, [0, 0, 50]) #Most important content
        self.TrafficControl['medium'] = fuzz.trimf(self.TrafficControl.universe, [0, 50, 100]) #content of medium importance
        self.TrafficControl['high'] = fuzz.trimf(self.TrafficControl.universe, [50, 100, 100]) #least important content
        
        ClientSpeed.view()
        ServerResponseTime.view()
        self.TrafficControl.view()
        
        rule1 = ctrl.Rule(ClientSpeed['poor'] & ServerResponseTime['poor'], self.TrafficControl['Low'])
        rule2 = ctrl.Rule(ClientSpeed['average'] & ServerResponseTime['poor'], self.TrafficControl['Low'])
        rule3 = ctrl.Rule(ClientSpeed['poor'] & ServerResponseTime['average'], self.TrafficControl['Low'])
        rule4 = ctrl.Rule(ClientSpeed['average'] & ServerResponseTime['average'], self.TrafficControl['medium'])
        rule6 = ctrl.Rule(ClientSpeed['average'] & ServerResponseTime['good'], self.TrafficControl['medium'])
        rule5 = ctrl.Rule(ClientSpeed['good'] & ServerResponseTime['average'], self.TrafficControl['high'])
        rule7 = ctrl.Rule(ClientSpeed['good'] & ServerResponseTime['poor'], self.TrafficControl['Low'])
        rule8 = ctrl.Rule(ClientSpeed['poor'] & ServerResponseTime['good'], self.TrafficControl['Low'])
        rule9 = ctrl.Rule(ClientSpeed['good'] & ServerResponseTime['good'], self.TrafficControl['high'])
        
        tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        
        self.tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
    
    
    def calculate(self, clientSpeed, serverResponse):
        self.tipping.input['ClientSpeed'] = clientSpeed
        self.tipping.input['ServerResponseTime'] = serverResponse
        self.tipping.compute()
        self.TrafficControl.view(sim=self.tipping)
        return round(self.tipping.output['TrafficControl'])
    
calc = fuzzyCalculator()
#print(calc.calculate(1000, 0))
stop = False

#least number = 16.666666
#greatest number = 83.3333
#website with 83 blocks of content, 16 being the minimum number of displayed blocks
while stop == False:    
    userSpeed = rd.randint(0, 1000)
    hostResponse = rd.randint(0, 100)
    print("User connection speed, mb: ", userSpeed)
    print("Server response time, ms: ", hostResponse)
    print("Number of blocks to display:", calc.calculate(userSpeed, hostResponse), '\n')
    sleep(1.5)
