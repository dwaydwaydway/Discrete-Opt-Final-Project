# Capacity-expansion-in-the-college-admission-problem

Two mathematical programming methods (quadratic and linear) and two heuristics (LP-based and greedy) to solve the problem of expanding optimally capacities in the college admission process. The goal is to allocate optimally funding that expand the capacities of the universities. The objective function is the cost of the students, which we wish to minimize.

In the instance.py file we create a random instance of the problem, generated through a uniform distribution. 

In the math_models.py file we introduce a standard integer programming model of the college admission problem. Since the stability constraints are quadratic, they make the computation harder for a MIP solver (we use Gurobi); therefore, we also provide a McCormick linearization (convex envelope) of the model.

In the heuristics.py file we present two heuristics: an LP-based and a greedy one. We use these heuristics to provide a warm-up solution (the best of the two) to the mathematical programs in the math_models.py file.

In the read.py file we present some functions to read and produce the log files of the experiments we have conducted. 

The experiments log files are contained in the zip folders. There are 5 folders: Log files of the mathematical models for 1000 and 2000 students, the log files of the Heuristics, the generated instances for 1000 and 2000 students.
