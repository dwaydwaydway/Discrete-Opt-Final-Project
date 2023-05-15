# standard libraries:
import itertools
import ipdb
# third parties libraries:
import numpy as np
np.random.seed(0)

def remove_nan(pref, schoolHashes):
    schools2remove = set()
    for hash_ in schoolHashes:
        if len(pref[hash_]) == 0:
            schools2remove.add(hash_)
    print(f"schools2remove: {schools2remove}")
    return [school for school in schoolHashes if school not in schools2remove], schools2remove

def clean_student_rank(pref, studentHashes, schools2remove):
    clean_count = 0
    for student in studentHashes:
        for i in pref[student]:
            if pref[student][i] in schools2remove:
                pref[student].remove(i)
                clean_count += 1
    print(f"Clean_count: {clean_count}")
    return studentHashes

# given the number of students (n1) and universities (n2), returns gamma, preferences, T, S and capacities 
def create_instance(cap, pref):  
    studentHashes, schoolHashes = [key for key in pref if key not in cap], [key for key in cap]
    schoolHashes, schools2remove = remove_nan(pref, schoolHashes)
    studentHashes = clean_student_rank(pref, studentHashes, schools2remove)
    n1, n2 = len(studentHashes), len(schoolHashes)
    idx2student, idx2school = {i:s_hash for i, s_hash in enumerate(studentHashes)}, {i:s_hash for i, s_hash in enumerate(schoolHashes)}
    student2idx, school2idx = {idx2student[k]:k for k in idx2student}, {idx2school[k]:k for k in idx2school}

    gamma = list(itertools.product(range(n1),range(n2)))
    
    resident_prefs = {
        r: np.array([school2idx[pref[idx2student[r]][rank]] for rank in pref[idx2student[r]]])
        for r in range(n1)
    }
    hospital_prefs = {
        h: np.array([student2idx[pref[idx2school[h]][rank]] for rank in pref[idx2school[h]]])
        for h in range(n2)
        }
    #ipdb.set_trace()
    # given num_residents, num_hospitals,resident_prefs, we want to extract S_ij and T_ij
    S=dict()
    s_cost = dict()
    T=dict()
    h=0
    for i in range(n1):
        S[i]=dict()
        s_cost[i]=dict()
        for j in range(n2):
            h, *_ = np.where(resident_prefs[i]==j)
            if len(h) == 0:
                S[i][j]=np.arange(n2)
                s_cost[i][j]=len(resident_prefs[i])+1
            else:
                S[i][j]=resident_prefs[i][:h[0]+1]
                s_cost[i][j]=len(S[i][j])


    for i in range(n1):
        T[i]=dict()
        for j in range(n2):
            h, *_ = np.where(hospital_prefs[j]==i)
            if len(h) == 0:
                T[i][j]=np.arange(n1) # if not ranked
            else:
                T[i][j]=hospital_prefs[j][:h[0]]

    # we define the capacity of each university:
    tot_capacity = n1- n2
    number_of_universities = n2
    #capacities = (n2)*np.ones(n2)+ np.random.multinomial(tot_capacity, np.ones(n2)/n2, size=1)[0]
    capacities = np.array([cap[idx2school[i]] for i in range(n2)])
    dict_capacities = dict()
    for i in range(n2):
        dict_capacities[i] = capacities[i]
        
    return gamma, resident_prefs, hospital_prefs, T, S, s_cost, capacities, dict_capacities, n1, n2

