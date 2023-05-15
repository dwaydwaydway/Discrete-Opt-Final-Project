# std libraries
import os
import itertools

# third parties libraries
import numpy as np
import pandas as pd
import gurobipy as grb
import pickle

# project libraries
import heuristics as heur
import math_models as mod
import instance as inst
import read as read
import ipdb

import matplotlib.pyplot as plt

# we create an instance of the problem with 100 students, 5 colleges and 2 extra posts
#n1 = 100
#n2 = 7
fund = 0

cap = pd.read_pickle(r'cap.pck')
pref = pd.read_pickle(r'pref.pck')
gamma, resident_prefs, hospital_prefs, T, S, s_cost, capacities, dict_capacities, n1, n2 = inst.create_instance(cap, pref)
# we compute the optimal solution through the aggregated linearization
#ipdb.set_trace()
percentages, res, n_binding = [], [], []
percentage_cut = 0.11
capa = (capacities * (1 - percentage_cut)).round()
while capa.sum() >= n1:
    sol = mod.miqp(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capa, fund, binary = False)
    # (cost (objective function), computational time, status of the model, matching matrix, extra posts allocation vector)
    with open(f'exp/percentage_cut_{percentage_cut:.2f}.pkl','wb') as f:
        pickle.dump(sol, f)

    if sol[2] != 2:
        Exception("Did not get the optimal solution")

    n_student_each_school = sol[-2].sum(axis=0)    
    print(f"Capacity: {capa}")
    print(f"# students: {n_student_each_school}")
    print(f"loss: {sol[0]}")
    percentages.append(percentage_cut)
    res.append(sol[0])
    n_binding.append(sum([c==s for s, c in zip(n_student_each_school, capa)]))
    
    percentage_cut += 0.01
    capa = (capacities * (1 - percentage_cut)).round()

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('% cut')
    ax1.set_ylabel('Cost(the objective function)', color=color)
    ax1.plot(percentages, res, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('# of Binding Schools', color=color)  # we already handled the x-label with ax1
    ax2.plot(percentages, n_binding, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig("percentage_cutVSloss.png")



