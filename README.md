# Capacity-expansion-in-the-college-admission-problem

Two mathematical programming methods (quadratic and linear) and two heuristics (LP-based and greedy) to solve the problem of expanding optimally capacities in the college admission process. The goal is to allocate optimally funding that expand the capacities of the universities. The objective function is the cost of the students, which we wish to minimize.

In the instance.py file we create a random instance of the problem, generated through a uniform distribution. 

In the math_models.py file we introduce a standard integer programming model of the college admission problem. Since the stability constraints are quadratic, they make the computation harder for a MIP solver (we use Gurobi); therefore, we also provide a McCormick linearization (convex envelope) of the model.

In the heuristics.py file we present two heuristics: an LP-based and a greedy one. We use these heuristics to provide a warm-up solution (the best of the two) to the mathematical programs in the math_models.py file.

In the read.py file we present some functions to read and produce the log files of the experiments we have conducted. 

In the Complete_final_experiments folder are contained the log files of the experiments. There are 4 subfolders: Experiments for 1000 students, Experiments for 2000 students, the results of the Heuristics, the instances generated for each profile of parameters. 
