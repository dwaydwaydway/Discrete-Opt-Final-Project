# std libraries
import os
import warnings

# third parties libraries
import numpy as np
import matplotlib.pyplot as plt


# libraries from this project

import read as rd




# PERFORMANCE PROFILE PLOT
init_n1 = [1000,2000]
init_n2 = [5, 8, 10, 15]
funding = [1,2,5,10,20,30]

IP_time = []
AGG_time = []
for n1 in init_n1:
    
    current_path = os.getcwd()
    folder_path = current_path +f'\Data\Experiments_n1={n1}'
    folder_path_heuristics = current_path +'\Data\Heuristics_sol'
    for n2 in init_n2:
        for f in funding:
            
            warnings.filterwarnings("ignore")
            IP_file = open(folder_path+"\m.miqp_st{}un{}fund{}.gurobi-log.txt".format(n1,n2,f),"r")
            IP_results=rd.read(IP_file)
            IP_file.close()

            MC_agg_file = open(folder_path+"\m.McC_agg_st{}un{}fund{}.gurobi-log.txt".format(n1,n2,f),"r")
            MC_agg_results = rd.read(MC_agg_file)
            MC_agg_file.close()
            
            LP_based_file = open(folder_path_heuristics+"\\LP_based_st{}un{}fund{}.txt".format(n1,n2,f),"r")
            LP_based_results = rd.read_heur(LP_based_file)
            LP_based_file.close()
            
            Greedy_file = open(folder_path_heuristics+"\\greedy_st{}un{}fund{}.txt".format(n1,n2,f),"r")
            Greedy_results = rd.read_heur(Greedy_file)
            Greedy_file.close()
            
            IP_time = np.hstack((IP_time, IP_results[14]))
            AGG_time = np.hstack((AGG_time,MC_agg_results[14]))


IP_data = np.sort(IP_time)
AGG_data = np.sort(AGG_time)

def create_x_array(array):
    # we create the array with the unique times less than 3600 seconds
    no_copies_array = np.unique(array)
    x_axis = [t for t in no_copies_array if t<3600]
    # original lenght of the array to compute the percentage
    length = size(array)
    y_axis = dict()
    first_point = array[0]
    for point in array:
        if point in y_axis:
            y_axis[point] += 1

        elif point<3600:
            y_axis[point] = 1

    # now we compute the cumulated value for every point
    for point in x_axis:
        if point == first_point:
            old_point = point
        else:
            y_axis[point] = y_axis[point] + y_axis[old_point]
            old_point = point
    percentage_dict = {key: np.round((y_axis[key]/length)*100,1)
                        for key in y_axis.keys() if key<3600}
    
    return percentage_dict, x_axis

IP_dict, IP_x = create_x_array(IP_data)

IP_x = np.int_(IP_x).reshape(-1)
IP_y = np.float_(list(IP_dict.values())).reshape(-1) #(d => d.Value).ToList()

AGG_dict, AGG_x = create_x_array(AGG_data)
AGG_x = np.int_(AGG_x).reshape(-1)
AGG_y = np.float_(list(AGG_dict.values())).reshape(-1) #(d => d.Value).ToList()


plt.plot(IP_x, IP_y, label='IQP', color='blue')
plt.plot(AGG_x, AGG_y, label='Agg-Lin', color='red')
plt.xlabel('seconds')
plt.ylabel('% of solved instances')
plt.legend(loc='center right', fontsize='x-large')
plt.title('Performance profile')
plt.savefig('performance_profile.pdf')
plt.show()



# PLOT PERFORMANCE OF THE HEURISTICS

init_n2 = [5, 8, 10, 15]
funding = [1,2,5,10,20,30]

n1 = 2000

LP_dict = dict()
GR_dict = dict()
    
current_path = os.getcwd()
folder_path = current_path +f'\Data\Experiments_n1={n1}'
folder_path_heuristics = current_path +'\Data\Heuristics_sol'

for n2 in init_n2:
    
    LP_dict[n2] = []
    GR_dict[n2] = []
    
    for f in funding:

        warnings.filterwarnings("ignore")
        IP_file = open(folder_path+"\m.miqp_st{}un{}fund{}.gurobi-log.txt".format(n1,n2,f),"r")
        IP_results=rd.read(IP_file)
        IP_file.close()

        MC_agg_file = open(folder_path+"\m.McC_agg_st{}un{}fund{}.gurobi-log.txt".format(n1,n2,f),"r")
        MC_agg_results = rd.read(MC_agg_file)
        MC_agg_file.close()

        LP_based_file = open(folder_path_heuristics+"\\LP_based_st{}un{}fund{}.txt".format(n1,n2,f),"r")
        LP_based_results = rd.read_heur(LP_based_file)
        LP_based_file.close()

        Greedy_file = open(folder_path_heuristics+"\\greedy_st{}un{}fund{}.txt".format(n1,n2,f),"r")
        Greedy_results = rd.read_heur(Greedy_file)
        Greedy_file.close()

        solution = np.minimum(IP_results[7], MC_agg_results[7] )
        mean_solution = np.round(np.mean( solution),1)

        LP_based_gap = abs(np.round( (( LP_based_results[0] - mean_solution)/mean_solution )*100 , 1))
        Greedy_based_gap = abs(np.round( (( Greedy_results[0] - mean_solution)/mean_solution )*100 , 1))

        LP_dict[n2] = np.append(LP_dict[n2], LP_based_gap)
        GR_dict[n2] = np.append(GR_dict[n2], Greedy_based_gap)


x = [1,2,5,10,20,30]

plt.subplot(2, 2, 1)
plt.plot(x, LP_dict[5],   'ko-', label='LPH', color='green')
plt.plot(x, GR_dict[5],  'ko-', label='Grdy', color='orange')
plt.title('5 colleges')
plt.xlabel('$B$')
plt.ylabel('gap')
plt.legend(loc='upper left', fontsize='x-small')

plt.subplot(2, 2, 2)
plt.plot(x, LP_dict[8],  'ko-', label='LPH', color='green')
plt.plot(x, GR_dict[8],  'ko-', label='Grdy', color='orange')
plt.title('8 colleges')
plt.xlabel('$B$')
plt.ylabel('gap')
plt.legend(loc='upper left', fontsize='x-small')

plt.subplot(2, 2, 3)
plt.plot(x, LP_dict[10],  'ko-', label='LPH', color='green')
plt.plot(x, GR_dict[10],  'ko-', label='Grdy', color='orange')
plt.title('10 colleges')
plt.xlabel('$B$')
plt.ylabel('gap')
plt.legend(loc='upper left', fontsize='x-small')

plt.subplot(2, 2, 4)
plt.plot(x, LP_dict[15],  'ko-', label='LPH', color='green')
plt.plot(x, GR_dict[15],  'ko-', label='Grdy', color='orange')
plt.title('15 colleges')
plt.xlabel('$B$')
plt.ylabel('gap')
plt.legend(loc='upper left', fontsize='x-small')

plt.tight_layout()
plt.savefig('Heuristics.pdf')
plt.show()



# CODE FOR PLOTTING THE HISTOGRAM


def enum_ranks( n1, n2, resident_prefs, allocation):
    ranking = dict()
    ranking = dict.fromkeys(range(n2),0)
    #print(ranking1)
    for i in range(n1):
        univ = np.where(np.round(allocation[i,:]) == 1)[0][0]
        rank = np.where(resident_prefs[i] == univ)[0][0]
        ranking[rank] += 1 

    return ranking

for i in range(instances):
    
    gamma, resident_prefs, hospital_prefs, T, S, capacities, dict_capacities = create_instance(n1,n2)
    
    # FUNDING 
    fund = 0
    sol1 = miqp(n1, n2, resident_prefs, hospital_prefs, S, T, capacities, fund,  binary = False)
    _, model1 = sol1
    allocation1 = np.reshape(model1.getAttr(grb.GRB.Attr.X)[:n1*n2],(n1,n2))
    ranking1 = enum_ranks( n1, n2, resident_prefs, allocation1)
    print(ranking1)
    filedata = open(current_path+f'\Plot_bars_fund={fund}.txt', 'a')
    print(f'{i} average of positions: {ranking1}',file=filedata)
    filedata.close()
    
    # FUNDING 
    fund = 1
    sol2 = miqp(n1, n2, resident_prefs, hospital_prefs, S, T, capacities, fund,  binary = False)
    _, model2 = sol2
    allocation2 = np.reshape(model2.getAttr(grb.GRB.Attr.X)[:n1*n2],(n1,n2))
    ranking2 = enum_ranks( n1, n2, resident_prefs, allocation2)
    print(ranking2)
    filedata = open(current_path+f'\Plot_bars_fund={fund}.txt', 'a')
    print(f'{i} average of positions: {ranking2}',file=filedata)
    filedata.close()
    
    # FUNDING 
    fund = 30
    sol3 = miqp(n1, n2, resident_prefs, hospital_prefs, S, T, capacities, fund,  binary = False)
    _, model3 = sol3
    allocation3 = np.reshape(model3.getAttr(grb.GRB.Attr.X)[:n1*n2],(n1,n2))
    ranking3 = enum_ranks( n1, n2, resident_prefs, allocation3)
    print(ranking3)
    filedata = open(current_path+f'\Plot_bars_fund={fund}.txt', 'a')
    print(f'{i} average of positions: {ranking3}',file=filedata)
    filedata.close()
    
    
    if i == 0:
        solution1  = ranking1
        solution2  = ranking2
        solution3  = ranking3
    else:
        solution1 = np.vstack((solution1,ranking1))
        solution2 = np.vstack((solution2,ranking2))
        solution3 = np.vstack((solution3,ranking3))
    
sol_dict1 = dict()
sol_dict2 = dict()
sol_dict3 = dict()

for i in range(n2):
    frequence1 = 0 
    frequence2 = 0
    frequence3 = 0
    
    for j in range(instances):
        frequence1 += solution1[j][0][i]
        frequence2 += solution2[j][0][i]
        frequence3 += solution3[j][0][i]
        
    sol_dict1[i] = round(frequence1/instances)
    sol_dict2[i] = round(frequence2/instances)
    sol_dict3[i] = round(frequence3/instances)
    

filedata = open(current_path+f'\Plot_bars_fund=0.txt', 'a')
print(f'Final average of positions: {sol_dict1}',file=filedata)
filedata.close()

filedata = open(current_path+f'\Plot_bars_fund=1.txt', 'a')
print(f'Final average of positions: {sol_dict2}',file=filedata)
filedata.close()

filedata = open(current_path+f'\Plot_bars_fund=30.txt', 'a')
print(f'Final average of positions: {sol_dict3}',file=filedata)
filedata.close()



n1 = 1000
n2 = 15

ranking0 = {0: 783, 1: 170, 2: 36, 3: 9, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
ranking1 = {0: 793, 1: 164, 2: 34, 3: 8, 4: 2, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}
ranking2 = {0: 938, 1: 58, 2: 3, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

min_r0 = list(ranking0.values())
min_r0_rev = [ele for ele in reversed(min_r0)]
not0_r0 = n2 - next((i for i, x in enumerate(min_r0_rev) if x), None)

min_r1 = list(ranking1.values())
min_r1_rev = [ele for ele in reversed(min_r1)]
not0_r1 = n2 - next((i for i, x in enumerate(min_r1_rev) if x), None)


min_r2 = list(ranking2.values())
min_r2_rev = [ele for ele in reversed(min_r2)]
not0_r2 = n2 - next((i for i, x in enumerate(min_r2_rev) if x), None)

limit = max(not0_r0, not0_r1, not0_r2) 

x = np.arange(1,limit+1)

frequencies_0 = [a/n1 for a in min_r0[:limit]]
frequencies_1 = [a/n1 for a in min_r1[:limit]]
frequencies_2 = [a/n1 for a in min_r2[:limit]]

ax = plt.subplot(111)
plt.bar( x-0.3, frequencies_0,  width=0.3, color='b', label='$B$ = 0')
plt.bar( x, frequencies_1,  width=0.3, color='gold', label='$B$ = 1')
plt.bar( x+0.3, frequencies_2,  width=0.3, color='r', label='$B$ = 30')
plt.legend()
plt.xlabel('rankings')
plt.ylabel('frequencies of the number of students')

plt.title(f"{n1} students and {n2} colleges")
plt.savefig(f'Hystogram.pdf')


plt.show()