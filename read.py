# std libraries
import os

# third parties libraries
import numpy as np


# we use this function to extract certain information in the file f that stores the log of the specified mathematical model
def read(f):
    lines = f.readlines()
    
    start=dict()
    finish=dict()
    
    data_names = [ 'init_row', 'init_column', 'init_nonzero', 'init_varcont', 'init_varint', 'init_varbin', 
                 'pre_time', 'pre_lazy', 'root_obj', 'root_computed', 'root_time', 'nodes', 'nodes_time', 'n_warnings',
                 'lp_solution', 'lp_time', 'total_time', 'solution', 'best_bound', 'gap', 'warm_up'     ]
    
    for name in data_names:
        start[name] = 0
        finish[name] = 0
    
    heuristic_result = np.array([])
    heuristic_time = np.array([])
    init_row = np.array([])
    init_column = np.array([])
    init_nonzero = np.array([])
    init_varcont=np.array([])
    init_varint=np.array([])
    init_varbin=np.array([])
    pre_time = np.array([])
    pre_lazy=np.array([]) 
    root_obj = np.array([])
    root_computed = np.array([]) # this records when the root obj has been computed or not
    root_time = np.array([])
    clique = np.array([])
    cover = np.array([])
    flow_cover = np.array([])
    gomory = np.array([])
    gub_cover = np.array([])
    implied_bound = np.array([])
    lazy_constraints = np.array([])
    mir    = np.array([])
    mod_K = np.array([])
    rlt = np.array([])
    strongCG = np.array([])
    zero_half = np.array([])
    nodes=np.array([])
    nodes_time=np.array([])
    n_warnings = np.array([])   
    lp_solution=np.array([])  
    lp_time=np.array([])
    total_time = np.array([])    
    solution=np.array([])
    best_bound = np.array([])
    gap = np.array([])
    warm_up = np.array([])    

    cut_dict = dict()
    cuts_names = ['clique', 'cover','flow_cover','gomory','gub_cover',
                       'implied_bound','lazy_constraints','mir','mod_K','rlt','strongCG', 'zero_half']
    for cutt in cuts_names:
        cut_dict[cutt] = np.array([])
        start[cutt] = 0
        finish[cutt] = 0
        locals()[cutt] = np.array([])
        
    general_list = []
    
    n_init_row = -1000000
    n_pre_row = -1000000
    n_init_column = -1000000
    n_pre_column = -1000000
    
    gurobi_9_Big_preprocess_flag = 0
    root_relax_flag = 0
    
    for line in lines:
        
        if line[0:8] == 'Gurobi 9':
            
            gurobi_9_Big_preprocess_flag = 0
            root_relax_flag = 0
            
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            
            n_init_row = -100000
            n_pre_row = -100000
            n_init_column = -100000
            n_pre_column = -100000
            
        # We record the initial data (rows, columns, nonzeros, variables)
        if line[0:10] == 'Optimize a':      
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            
            for i,j in enumerate(line):
                if j=='h' and line[i+1]==' ':
                    start['init_row']=i+2
                if i>start['init_row'] and j==' ' and finish['init_row']==0 and start['init_row']!=0:
                    finish['init_row']=i
                if i>finish['init_row'] and j==' ' and start['init_column']==0 and finish['init_row']!=0:
                    start['init_column']=i+1
                if i>start['init_column'] and j==' ' and finish['init_column']==0 and start['init_column']!=0:
                    finish['init_column']=i
                if i>finish['init_column'] and j=='d' and start['init_nonzero']==0 and finish['init_column']!=0:
                    start['init_nonzero']=i+2
                if i>start['init_nonzero'] and j==' ' and finish['init_nonzero']==0 and start['init_nonzero']!=0:
                    finish['init_nonzero']=i
            
            n_init_row = int(line[start['init_row']:finish['init_row']])
            n_init_column = int(line[start['init_column']:finish['init_column']])
            init_row=np.append(init_row, n_init_row)
            init_column=np.append(init_column, n_init_column)
            init_nonzero=np.append(init_nonzero,int(line[start['init_nonzero']:finish['init_nonzero']]))
            
        if line[0:10] == 'Variable t' and oldline[0:5] == 'Model':
            for i,j in enumerate(line):
                if j==':' and line[i+1]==' ':
                    start['init_varcont']=i+2
                if i>start['init_varcont'] and j==' ' and finish['init_varcont']==0 and start['init_varcont']!=0:
                    finish['init_varcont']=i
                if i>finish['init_varcont'] and j==',' and start['init_varint']==0 and finish['init_varcont']!=0:
                    start['init_varint']=i+2
                if i>start['init_varint'] and j==' ' and finish['init_varint']==0 and start['init_varint']!=0:
                    finish['init_varint']=i
                if i>finish['init_varint'] and j=='(' and start['init_varbin']==0 and finish['init_varint']!=0:
                    start['init_varbin']=i+1
                if i>start['init_varbin'] and j==' ' and finish['init_varbin']==0 and start['init_varbin']!=0:
                    finish['init_varbin']=i
                    
            init_varcont=np.append(init_varcont,int(line[start['init_varcont']:finish['init_varcont']]))
            init_varint=np.append(init_varint,int(line[start['init_varint']:finish['init_varint']]))
            init_varbin=np.append(init_varbin,int(line[start['init_varbin']:finish['init_varbin']]))
        
        # We store the data of the Presolve method (rows, columns, nonzeros,time, and maybe variables)
        if line[0:10] == 'Presolve t':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if j==':' and line[i+1]==' ':
                    start['pre_time']=i+2
                if i>start['pre_time'] and j=='s' and finish['pre_time']==0 and start['pre_time']!=0:
                    finish['pre_time']=i
                    
            pre_time=np.append(pre_time,float(line[start['pre_time']:finish['pre_time']]))
            
        # If some lazy constraints are extracted, we record it
        if line[0:9] == 'Extracted':
            for i,j in enumerate(line):
                if j=='d' and line[i+1]==' ' and line[i-2]=='t':
                    start['pre_lazy']=i+2
                if i>start['pre_lazy'] and (j==' ') and finish['pre_lazy']==0 and start['pre_lazy']!=0: # or j=='e'
                    finish['pre_lazy']=i
        
            pre_lazy=np.append(pre_lazy,int(line[start['pre_lazy']:finish['pre_lazy']]))
        
        # If there is some root relaxation, we record it 
        if line[0:10] == 'Root relax':
            root_relax_flag = 1
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if j=='e' and line[i+1]==' ' and line[i-1]=='v':
                    start['root_obj']=i+2
                if i>start['root_obj'] and (j==',') and finish['root_obj']==0 and start['root_obj']!=0: # or j=='e'
                    finish['root_obj']=i
                elif j=='f' and line[i+1]==',' and line[i-1]=='f': # if instead of a number a "cutoff" is printed, adapt
                    start['root_obj']=i
                    finish['root_obj']=i
                elif j=='e' and line[i+1]==',' and line[i-1]=='l': # if instead of a number an "infeasible" is printed, adapt
                    start['root_obj']=i
                    finish['root_obj']=i
                if i>finish['root_obj'] and start['root_obj']!=finish['root_obj'] and j==',' and start['root_time']==0 and finish['root_obj']!=0 and line[i-4:i]=='ions':
                    start['root_time']=i+2
                if i>start['root_time'] and j==' ' and finish['root_time']==0 and start['root_time']!=0:
                    finish['root_time']=i

            if start['root_obj']==finish['root_obj']:
                root_relax_flag = 0
            else:
                root_obj = np.append(root_obj,float(line[start['root_obj']:finish['root_obj']]))
                root_time = np.append(root_time,float(line[start['root_time']:finish['root_time']]))
        
        # We read the cuts: 
        cuts = ['  Clique:','  Cover:','  Flow cover:','  Gomory:','  GUB cover:','  Implied bound:',
                '  Lazy constraints:','  MIR:','  Mod-K:','  RLT:','  StrongCG:','  Zero half:']
        short_names = ['clique', 'cover','flow_cover','gomory','gub_cover',
                       'implied_bound','lazy_constraints','mir','mod_K','rlt','strongCG', 'zero_half']
        for cut, name in zip(cuts,short_names):
            # we read each specific kind of cutting plane
            if line[0:len(cut)] == cut: 
                start = dict.fromkeys(start, 0)
                finish = dict.fromkeys(finish, 0)
                for i,j in enumerate(line):
                    if j==':' and line[i+1]==' ':
                        start[name]=i+2
                
                cut_dict[name] = np.append(cut_dict[name], float(line[start[name]:]) )
        
        # we read the number of explored nodes
        if line[0:8] == 'Explored':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if j=='d' and line[i+1]==' ':
                    start['nodes']=i+2
                if i>start['nodes'] and j==' ' and finish['nodes']==0 and start['nodes']!=0:
                    finish['nodes']=i
                if i>finish['nodes'] and line[i-1]=='i' and j=='n' and start['nodes_time']==0 and finish['nodes']!=0:
                    start['nodes_time']=i+2
                if i>start['nodes_time']  and j==' ' and finish['nodes_time']==0 and start['nodes_time']!=0:
                    finish['nodes_time']=i

            nodes=np.append(nodes,int(line[start['nodes']:finish['nodes']]))
            nodes_time=np.append(nodes_time, float(line[start['nodes_time']:finish['nodes_time']]) )
            
        # We retireve the warm-up solution value
        if line[0:15] == 'Loaded user MIP':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if line[i-2]=='i' and line[i-1]=='v' and j=='e': 
                    start['warm_up']=i+2
            
            warm_up = np.append(warm_up,float(line[start['warm_up']:]))
        
        
        # we read the time and the solution if the problem is an LP        
        if line[0:9] == 'Solved in':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if j=='n' and line[i+1]=='d' and line[i+2]==' ' and line[i-1]=='a':
                    start['lp_time']=i+3
                if i>start['lp_time'] and j==' ' and finish['lp_time']==0 and start['lp_time']!=0:
                    finish['lp_time']=i
            
            lp_time=np.append(lp_time,float(line[start['lp_time']:finish['lp_time']]))
            
        if line[0:10] == 'Optimal ob':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if j=='e' and line[i+1]==' ' and line[i+2]==' ' and line[i-1]=='v':
                    start['lp_solution']=i+3
            
            lp_solution=np.append(lp_solution,float(line[start['lp_solution']:]))
            
        
        # RUNTIME
        if line[0:8] == 'Runtime:':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            for i,j in enumerate(line):
                if j==':' and line[i+1]==' ' and line[i-1]=='e':
                    start['total_time']=i+2
            
            total_time = np.append(total_time,float(line[start['total_time']:]))
        
        
        # Warnings
        if line[0:8] == 'Warning:':
            #print(line)
            
            n_warnings = np.append(n_warnings,1)
            
        
        # best objective, best bound and gap
        if line[0:14] == 'Best objective':
            start = dict.fromkeys(start, 0)
            finish = dict.fromkeys(finish, 0)
            flag=0
            for i,j in enumerate(line):
                if j=='v' and line[i+1]=='e' and line[i+2]==' ':
                    start['solution'] = i+3
                if i>start['solution'] and j==',' and finish['solution']==0 and start['solution']!=0:
                    finish['solution'] = i
                if i>finish['solution'] and line[i-1]=='n' and j=='d' and start['best_bound']==0 and finish['solution']!=0:
                    start['best_bound'] = i+2
                if i>start['best_bound']  and j==',' and finish['best_bound']==0 and start['best_bound']!=0:
                    finish['best_bound'] = i
                if i>finish['best_bound'] and line[i-1]=='a' and j=='p' and start['gap']==0 and finish['best_bound']!=0:
                    start['gap'] = i+2
                if i>start['gap'] and j=='%' and finish['gap']==0 and start['gap']!=0:
                    finish['gap'] = i
                      
            solution = np.append(solution,float(line[start['solution']:finish['solution']]))
            best_bound = np.append(best_bound,float(line[start['best_bound']:finish['best_bound']]))
            gap = np.append(gap,float(line[start['gap']:finish['gap']]))
            root_computed = np.append(root_computed, root_relax_flag  ) #  we append root_relax_flag
            if root_relax_flag==0:
                root_obj=np.append(root_obj,0)
                
        oldline=line
        oldpresolveline=line
        
    f.close()
    
    return  [int(np.mean(init_row)), int(np.mean(init_column)), 
             format(np.round(np.mean(pre_time),2), '.2f') , 
            np.round(root_obj,2), format(np.round(np.mean(root_time),2), '.2f'),
            np.round(np.mean(nodes),1), size(np.nonzero(np.round(gap,2))),
            solution, format(np.round(np.mean(total_time),2), '.2f'),
             [np.round(np.mean(cut_dict[name]),1) for name in short_names], 
              np.round(lp_solution,2), format(np.round(np.mean(lp_time),2), '.2f'),
            root_computed, np.round(np.mean(gap),1)   ]


# we use this function to extract certain information in the file f that stores the log of the specified heuristic
def read_heur(f):
    lines = f.readlines()
    start=dict()
    
    data_names = [ 'heuristic_result', 'heuristic_time'  ]
    for name in data_names:
        start[name] = 0
    
    heuristic_result = np.array([])
    heuristic_time = np.array([])
    
    for line in lines:
        
        if line[0:9] == 'solution:':      
            start = dict.fromkeys(start, 0)
            for i,j in enumerate(line):
                if j==':' and line[i+1]==' ':
                    start['heuristic_result']=i+2
            heuristic_result = np.append(heuristic_result, float(line[start['heuristic_result']:-1]) )
            
        if line[0:8] == 'Runtime:':      
            start = dict.fromkeys(start, 0)
            for i,j in enumerate(line):
                if j==':' and line[i+1]==' ':
                    start['heuristic_time']=i+2
            heuristic_time = np.append(heuristic_time, float(line[start['heuristic_time']:-1]) )
    
    f.close()
    
    return [ np.round(np.mean(heuristic_result),2) , 
            format(np.round(np.mean(heuristic_time),2), '.2f') ]


# we compute the root gap of each mathematical method
def compute_root_gap(root_array, solution, root_computed):
    
    gap = np.array([])
    for i in range(len(root_computed)):
        if root_computed[i]== 1:
            if solution[i]!= 0:
                gap = np.append(gap, (abs(root_array[i] - solution[i])/solution[i] )*100 )
            else:
                gap = np.append(gap, root_array[i])
        elif root_computed[i]== 0:
            gap = np.append(gap, 0 )
    
    return np.round(np.mean(gap),1)


    

           
  