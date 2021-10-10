# standard libraries:
import itertools

# third parties libraries:
import numpy as np


# given the number of students (n1) and universities (n2), returns gamma, preferences, T, S and capacities 
def create_instance(n1,n2):  
    
    gamma = list(itertools.product(range(n1),range(n2)))
    
    resident_prefs = {
        r: np.random.permutation(n2)
        for r in range(n1)
    }

    hospital_prefs = {
        h: np.random.permutation(n1)
        for h in range(n2)
        }
    
    # given num_residents, num_hospitals,resident_prefs, we want to extract S_ij and T_ij
    S=dict()
    T=dict()
    h=0
    for i in range(n1):
        S[i]=dict()
        for j in range(n2):
            h, *_ = np.where(resident_prefs[i]==j)
            S[i][j]=resident_prefs[i][:h[0]+1]

    for i in range(n1):
        T[i]=dict()
        for j in range(n2):
            h, *_ = np.where(hospital_prefs[j]==i)
            T[i][j]=hospital_prefs[j][:h[0]+1]

    # we define the capacity of each university:
    tot_capacity = n1- n2
    number_of_universities = n2
    capacities = np.ones(n2)+ np.random.multinomial(tot_capacity, np.ones(n2)/n2, size=1)[0]
    dict_capacities = dict()
    for i in range(n2):
        dict_capacities[i] = capacities[i]
        
    return gamma, resident_prefs, hospital_prefs, T, S, capacities, dict_capacities

