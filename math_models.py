# std libraries
import os
import itertools

# third parties libraries
import numpy as np
import gurobipy as grb

# project libraries
import heuristics as heur

import ipdb


def miqp(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund, binary = False):
    name= 'miqp'    

    model = grb.Model(f'{name}')
    model.setParam('OutputFlag', True )
    model.setParam('Threads', 1)
    model.setParam("TimeLimit", 3600.0)
    
    gamma = list(itertools.product(range(n1),range(n2)))
    
    # retrieve warm-up solution from the best of the two heuristics (LP-based and greedy)
    x_warm, t_warm = heur.add_bound(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund)

    # add allocation vars              
    x = { key: model.addVar(lb=0, ub=1.0, name=f"x_{key[0]}_{key[1]}", vtype=grb.GRB.BINARY) for key in gamma }
    for i,j in gamma:
        x[i,j].start = x_warm[i,j]

    # add funding vars    
    if binary:
        var_type = grb.GRB.BINARY
    else:
        var_type = grb.GRB.INTEGER
    if fund >= 0:
        t = { uni : model.addVar(lb = 0, ub = fund, name = f"t_{uni}", vtype = var_type) for uni in range(n2) }
    else:
        t = { uni : model.addVar(lb = fund, ub = 0, name = f"t_{uni}", vtype = var_type) for uni in range(n2) }

    for i in range(n2):
        t[i].start = t_warm[i]
    # add objective    
    model.ModelSense = +1 # maximize: -1; minimize: +1
    model.setObjective(
        grb.quicksum([
            x[i,j]*(s_cost[i][j]-1) for i in range(n1) for j in range(n2)
        ])
    )

    # add resident capacity consts
    for i in range(n1):
        model.addLConstr(grb.quicksum(x[i,j] for j in range(n2)) ==  1)

    # add hospital capacity consts 
    for j in range(n2):
        model.addLConstr(grb.quicksum(x[i,j] for i in range(n1)) - t[j] <=  capacities[j])
    
    if fund >= 0 :
        # add funding consts
        model.addLConstr(grb.quicksum(t[u] for u in range(n2)) <= fund)
    else:
        model.addLConstr(grb.quicksum(t[u] for u in range(n2)) <= fund)
    
    # add stability quadratic consts 
    for i,j in gamma:
        model.addConstr((capacities[j]+t[j])*(1-grb.quicksum(x[i,h] for h in S[i][j])) - grb.quicksum(x[r,j] for r in T[i][j]) <= 0)

    # solving and recording data
    current_path = os.getcwd()
    if not os.path.exists(current_path+f'\Experiments_n1={n1}'):
        os.makedirs(current_path+f'\Experiments_n1={n1}')
    
    experiment_name = f'{name}_st{n1}un{n2}fund{fund}'
    model.setParam('LogFile', current_path+f'\Experiments_n1={n1}\m.{experiment_name}.gurobi-log.txt')
    model.optimize()
    model.printStats()
    data = [model.ObjVal, model.Runtime, model.Status, np.reshape(model.getAttr(grb.GRB.Attr.X)[:n1*n2],(n1,n2)), 
            np.reshape(model.getAttr(grb.GRB.Attr.X)[n1*n2:n1*n2+n2],(n2)) ]
    
    filedata = open(current_path+f'\Experiments_n1={n1}\m.{experiment_name}.gurobi-log.txt', 'a')
    print(f'Runtime: {model.Runtime}',file=filedata)
    filedata.close()
    
    return data







def McC_agg(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund, binary = False):
    name= 'McC_agg'
    model = grb.Model(f'{name}')
    model.setParam('OutputFlag', True )
    model.setParam('Threads', 1)
    model.setParam("TimeLimit", 3600.0)

    gamma = list(itertools.product(range(n1),range(n2)))
    
    # retrieve warm-up solution from the best of the two heuristics (LP-based and greedy)
    x_warm, t_warm = heur.add_bound(n1, n2, resident_prefs, hospital_prefs, S, s_cost, T, capacities, fund)

    # add allocation vars           
    x = { key: model.addVar(lb=0, ub=1.0, name=f"x_{key[0]}_{key[1]}", vtype=grb.GRB.BINARY)
        for key in gamma }
    for i,j in gamma:
        x[i,j].start = x_warm[i,j]

    # add funding vars   
    if binary:
        var_type = grb.GRB.BINARY
    else:
        var_type = grb.GRB.INTEGER
    t = { uni : model.addVar(lb = 0, ub = fund, name = f"t_{uni}", vtype = var_type) for uni in range(n2) }
    for i in range(n2):
        t[i].start = t_warm[i]
    
    # add McCormick aggredated vars
    w = { key: model.addVar(lb=0, ub=fund, name=f"x_{key[0]}_{key[1]}", vtype=grb.GRB.CONTINUOUS) for key in gamma }
    
    # add objective    
    model.ModelSense = +1 # maximize: -1; minimize: +1
    model.setObjective(
        grb.quicksum([
            x[i,j]*(len(S[i][j])-1) for i in range(n1) for j in range(n2)
        ])
    )

    # add resident capacity consts
    for i in range(n1):
        model.addLConstr(grb.quicksum(x[i,j] for j in range(n2)) ==  1)

    # add hospital capacity consts 
    for j in range(n2):
        model.addLConstr( grb.quicksum(x[i,j] for i in range(n1)) -t[j] <=  capacities[j])

    # add funding consts
    model.addLConstr(grb.quicksum(t[u] for u in range(n2)) <= fund)
    
    # add aggregated linearized McCormick consts 
    for j in range(n2):
        for i in range(n1):
            model.addLConstr(- w[i,j] + t[j] + fund*(grb.quicksum(x[i,q] for q in S[i][j] ))<=  fund )
            model.addLConstr( w[i,j]-t[j] <= 0 )
            model.addLConstr( w[i,j] -fund*(grb.quicksum(x[i,q] for q in S[i][j] ))<= 0 ) 
    
    # add stability aggregated linearized consts
    for i, j in gamma:
        const = model.addLConstr(t[j] - w[i,j] + capacities[j]*(1- grb.quicksum(x[i,q] for q in S[i][j] )) - grb.quicksum(x[p,j] for p in T[i][j])<=0)

    # solving and recording data
    current_path = os.getcwd()
    if not os.path.exists(current_path+f'\Experiments_n1={n1}'):
        os.makedirs(current_path+f'\Experiments_n1={n1}')
    
    experiment_name = f'{name}_st{n1}un{n2}fund{fund}'
    model.setParam('LogFile', current_path+f'\Experiments_n1={n1}\m.{experiment_name}.gurobi-log.txt')
    model.optimize()
    model.printStats()
    print("mdl.getVars(): ")
    print(model.getVars())
    data = [model.ObjVal, model.Runtime, model.Status, np.reshape(model.getAttr(grb.GRB.Attr.X)[:n1*n2],(n1,n2)), 
            np.reshape(model.getAttr(grb.GRB.Attr.X)[n1*n2:n1*n2+n2],(n2)) ]
    
    filedata = open(current_path+f'\Experiments_n1={n1}\m.{experiment_name}.gurobi-log.txt', 'a')
    print(f'Runtime: {model.Runtime}',file=filedata)
    filedata.close()
    
    return data









