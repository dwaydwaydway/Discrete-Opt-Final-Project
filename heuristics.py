# Python standard library: 
import os
import itertools
import time

# third parties libraries:
import numpy as np
from matching import Player
from matching.games import HospitalResident
import gurobipy as grb



def facility_location(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund, binary = False):
    name= 'facility_loc'
    model = grb.Model(f'{name}')
    model.setParam('OutputFlag', True )
    model.setParam('Threads', 1)
    model.setParam("TimeLimit", 3600.0)    
    model.params.Presolve = 0

    gamma = list(itertools.product(range(n1),range(n2)))
    
    # add allocation vars
    x = { key : model.addVar(lb=0, ub=1.0, name=f"x_{key[0]}_{key[1]}", vtype= grb.GRB.CONTINUOUS) for key in gamma }    
    
    # add funding vars
    if binary:
        var_bound = 1
    else:
        var_bound = fund
    if fund >= 0:
        t = { uni : model.addVar(lb = 0, ub = var_bound, name = f"t_{uni}", vtype = grb.GRB.CONTINUOUS) for uni in range(n2) }
    else:
        t = { uni : model.addVar(lb = var_bound, ub = 0, name = f"t_{uni}", vtype = grb.GRB.CONTINUOUS) for uni in range(n2) }
    # set objective
    model.ModelSense = +1 # maximize: -1; minimize: +1
    model.setObjective(
        grb.quicksum([
            x[i,j]*(s_cost[i][j]-1) for i in range(n1) for j in range(n2)
        ])
    )

    # add residents capacity consts
    for i in range(n1):
        model.addLConstr(grb.quicksum(x[i,j] for j in range(n2)) ==  1)
        
    # add hospital capacity consts
    for j in range(n2):
        model.addLConstr(grb.quicksum(x[i,j] for i in range(n1)) - t[j] <=  capacities[j]) 
    # add funding consts 
    if fund >= 0:
        model.addLConstr(grb.quicksum(t[u] for u in range(n2)) <= fund)
    else:
        # add funding consts 
        model.addLConstr(grb.quicksum(t[u] for u in range(n2)) <= fund)
    # solving and recording data
    current_path = os.getcwd()
    if not os.path.exists(current_path+f'\Experiments_n1={n1}'):
        os.makedirs(current_path+f'\Experiments_n1={n1}')
    
    experiment_name = f'{name}_st{n1}un{n2}fund{fund}'
    model.setParam('LogFile', current_path+f'\Experiments_n1={n1}\m.{experiment_name}.gurobi-log.txt')
    model.optimize()
    model.printStats()

    data = [model.ObjVal, model.Runtime, model.Status, np.reshape(model.getAttr(grb.GRB.Attr.X)[:n1*n2],(n1,n2)), 
            np.reshape(model.getAttr(grb.GRB.Attr.X)[n1*n2:n1*n2+n2],(n2)), model.NumIntVars]

    filedata = open(current_path+f'\Experiments_n1={n1}\m.{experiment_name}.gurobi-log.txt', 'a')
    print(f'Runtime: {model.Runtime}',file=filedata)
    filedata.close()
    
    return data[4], data[0], data[5]




def stable_with_extra(n2, capacities, alloc, resident_prefs, hospital_prefs):
    aux_capacities = [capacities[u]+alloc[u] for u in range(n2)]
    aux_game = HospitalResident.create_from_dictionaries(resident_prefs, hospital_prefs, aux_capacities)
    aux_matching = aux_game.solve(optimal="resident")
    return aux_matching, sum([sum([list(resident_prefs[r.name]).index(item1.name) for r in item2]) for item1,item2 in aux_matching.items()])




def LP_based_heuristic(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund):
    
    allocation = facility_location(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund, binary = False)
        
    results = stable_with_extra(n2,capacities, allocation[0], resident_prefs, hospital_prefs)
    obj_value = results[1]
         
    # we return the objective value, the allocation of funding and the matching
    return obj_value, allocation[0], results[0]





def greedy_approach(n2, resident_prefs, hospital_prefs, fund, capacities):
    
    obj_val = -1
    
    allocation = np.zeros(n2)
    
    if fund == 0:
        
        game = HospitalResident.create_from_dictionaries(resident_prefs, hospital_prefs, capacities)
        matching = game.solve()
        chosen_matching = matching
        obj_val = sum([sum([list(resident_prefs[r.name]).index(item1.name) for r in item2]) for item1,item2 in matching.items()])


    else:
    
        for i in range(abs(fund)):
            # initialization
            temp_alloc = np.zeros(n2)
            matchings = dict()
            
            index = -1

            for h in range(n2):
                aux_capacities = np.zeros(n2)
                aux_capacities = [capacities[u]+allocation[u] for u in range(n2)]
                if fund >= 0:
                    aux_capacities[h] += 1
                else:
                    aux_capacities[h] -= 1

                aux_game = HospitalResident.create_from_dictionaries(resident_prefs, hospital_prefs, aux_capacities)
                aux_matching = aux_game.solve(optimal="resident")
                matchings[h] = aux_matching
                temp_alloc[h] = sum([sum([list(resident_prefs[r.name]).index(item1.name) for r in item2]) for item1,item2 in aux_matching.items()])

            index = np.argmin(temp_alloc)
            if fund >= 0:
                allocation[index] += 1
            else:
                allocation[index] -= 1

            if i == abs(fund)-1 :
                obj_val = temp_alloc[index]
                chosen_matching = matchings[index]
            else:
                del matchings
            
    return obj_val, allocation, chosen_matching




def unravel_matching(assignment, gamma):
    sol_match = dict()
    
    for u,s in assignment.items():
        sol_match[u.name] = []
        for r in s:
            sol_match[u.name].append(r.name)
            
    solution = {}
    for st,un in gamma:
        if st in sol_match[un]:
            solution[st, un] = 1
        else:
            solution[st, un] = 0
    
    return solution
    

def add_bound(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund):
    current_path = os.getcwd()
    if not os.path.exists(current_path+f'\Heuristics_sol'):
        os.makedirs(current_path+f'\Heuristics_sol')
        
    start_LP_based = time.time()
    LP_based_sol = LP_based_heuristic(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund)
    end_LP_based = time.time()
    experiment_name = f'LP_based_st{n1}un{n2}fund{fund}'
    filedata = open(current_path+f'\Heuristics_sol\\{experiment_name}.txt', 'a')
    print(f'Runtime: {end_LP_based-start_LP_based}',file=filedata)
    print(f'solution: {LP_based_sol[0]}',file=filedata)
    filedata.close()
    
    start_greedy = time.time()
    greedy_sol = greedy_approach(n2, resident_prefs, hospital_prefs, fund, capacities)
    end_greedy = time.time()
    experiment_name = f'greedy_st{n1}un{n2}fund{fund}'
    filedata = open(current_path+f'\Heuristics_sol\\{experiment_name}.txt', 'a')
    print(f'Runtime: {end_greedy-start_greedy}',file=filedata)
    print(f'solution: {greedy_sol[0]}',file=filedata)
    filedata.close()
    
    if LP_based_sol[0] <= greedy_sol[0]:
        allocation = LP_based_sol[1]
        matching = LP_based_sol[2]
        best_value = LP_based_sol[0]
    else:
        allocation = greedy_sol[1]
        matching = greedy_sol[2]
        best_value = greedy_sol[0]
    
    gamma = list(itertools.product(range(n1),range(n2)))
    x_solution = unravel_matching(matching, gamma)
    
    return x_solution, allocation
        
