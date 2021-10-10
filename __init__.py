# std libraries
import os
import itertools

# third parties libraries
import numpy as np
import gurobipy as grb

# project libraries
import heuristics as heur
import math_models as mod
import instance as inst
import read as read


# we create an instance of the problem with 100 students, 5 colleges and 2 extra posts
n1 = 100
n2 = 5
fund = 2    
gamma, resident_prefs, hospital_prefs, T, S, capacities, dict_capacities = inst.create_instance(n1,n2)

# we compute the optimal solution through the aggregated linearization
sol = mod.miqp(n1, n2, resident_prefs, hospital_prefs, S, T, capacities, fund, binary = False)
# we print the cost (as the sum of the regrets of the students), the computational time, the status of the model, the matching matrix and the extra posts allocation vector
print(sol)

