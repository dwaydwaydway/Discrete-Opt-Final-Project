# std libraries
import os
import itertools

# third parties libraries
import numpy as np
import gurobipy as grb

# project libraries
from . import heuristics as heur
from . import math_models as mod
from . import instance
from . import read

# in this file we read the dataset and produce the relevant information to display in a LaTex table 

init_n1 = [1000, 2000]

init_n2 = [5, 8, 10, 15]

funding = [1,2,5,10,20,30]

for n1 in init_n1:
    
    current_path = os.getcwd()
    folder_path = current_path + "\Complete_final_experiments"+f'\Experiments_n1={n1}'
    folder_path_heuristics = current_path + "\Complete_final_experiments"+'\Heuristics_sol'
    
    for n2 in init_n2:
        
        for f in funding:
            
            IP_file = open(folder_path+"\m.miqp_st{}un{}fund{}.gurobi-log.txt".format(n1,n2,f),"r")
            IP_results = read.read(IP_file)
            IP_file.close()

            MC_agg_file = open(folder_path+"\m.McC_agg_st{}un{}fund{}.gurobi-log.txt".format(n1,n2,f),"r")
            MC_agg_results = read.read(MC_agg_file)
            MC_agg_file.close()
            
            LP_based_file = open(folder_path_heuristics+"\\Alf_st{}un{}fund{}.txt".format(n1,n2,f),"r")
            LP_based_results = read.read_heur(LP_based_file)
            LP_based_file.close()
            
            Greedy_file = open(folder_path_heuristics+"\\greedy_st{}un{}fund{}.txt".format(n1,n2,f),"r")
            Greedy_results = read.read_heur(Greedy_file)
            Greedy_file.close()
            
            solution = np.minimum(IP_results[7], MC_agg_results[7])
            mean_solution = np.round(np.mean( solution),1)
            
            IP_root_gap = read.compute_root_gap(IP_results[3], solution, IP_results[12])
            Agg_root_gap = read.compute_root_gap(MC_agg_results[3], solution, MC_agg_results[12])
            
            LP_based_gap = abs(np.round( (( LP_based_results[0] - mean_solution)/mean_solution )*100 , 1))
            Greedy_based_gap = abs(np.round( (( Greedy_results[0] - mean_solution)/mean_solution )*100 , 1))
            
            print(f' {f} & {n1} & {n2} & '\
                  f' {LP_based_gap} & {LP_based_results[1]} & {Greedy_based_gap} & {Greedy_results[1]} & '\
                  f' {IP_results[0]} & {IP_results[1]} & {IP_results[2]} & '\
                  f'{IP_root_gap} & {IP_results[4]} & {IP_results[5]} & '\
                  f' {IP_results[6]} & {IP_results[13]} & {IP_results[8]} & '\
                  f' {MC_agg_results[0]} & {MC_agg_results[1]} & {MC_agg_results[2]} & '\
                  f'{Agg_root_gap} & {MC_agg_results[4]} & {MC_agg_results[5]} & '\
                  f' {MC_agg_results[6]} & {MC_agg_results[13]} & {MC_agg_results[8]} \\\\ \n \hline \n') # & '\
                  
            
            

