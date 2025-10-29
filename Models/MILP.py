import numpy as np
from pyomo.environ import ConcreteModel, Var, Binary, NonNegativeReals, minimize, Constraint, SolverFactory
from pyomo.core.util import quicksum
from pyomo.opt import TerminationCondition

def read_instance(pfile:str, rfile:str, dfile:str):
    
    n, m = np.loadtxt(pfile, max_rows=1, dtype=int)
    nf = np.loadtxt(pfile, skiprows=1, max_rows=1, dtype=int).tolist()
    p = np.loadtxt(pfile, skiprows=2, dtype=int)[:, 1::2].T
    r = np.loadtxt(rfile, dtype=int)
    d = np.loadtxt(dfile, dtype=int)
    
    return nf, m, n, p, r, d

def MILP(p, r, d, nf, TL=600, method='cplex', objective='Cmax'):
    
    mac, n = p.shape
    
    p = p.T
           
    # m building
    m = ConcreteModel()
    
    # Sets
    M = range(mac)
    N = range(n)
    F = range(nf)
    
    # Decision variables
    m.Cmax = Var(within=NonNegativeReals)
    m.C = Var(N, M, F, within=NonNegativeReals)
    m.X = Var(N, N, F, within=Binary)
    
    BigM = p.sum()
    
    # Objective function
    
    if objective == 'Cmax':
        
        @m.Constraint(N, F)
        def constraint_C4(m, k, f):
            return m.Cmax >= m.C[k,mac-1,f]
        
        @m.Objective()
        def makespan(m, sense=minimize):
            return m.Cmax
        
    elif objective == 'TotalCT':
        
        m.CC = Var(N, within=NonNegativeReals)

        @m.Constraint(N, F)
        def constraint_C4_2(m, k, f):
            return m.CC[k] >= m.C[k,mac-1,f]
        
        @m.Objective()
        def makespan(m, sense=minimize):
            return quicksum(m.CC[k] for k in N)
        
    elif objective == 'Tardiness':
        
        m.T = Var(N, F, within=NonNegativeReals)
        
        @m.Constraint(N, F)
        def constraint_C4(m, k, f):
            return m.T[k, f] >= m.C[k,mac-1,f] - quicksum(m.X[j,k,f]*d[j] for j in N) - BigM*(1 - quicksum(m.X[j,k,f] for j in N))
        
        @m.Objective()
        def tardiness(m, sense=minimize):
            return quicksum(m.T[k, f] for k in N for f in F)
        
    else:
        
        m.E = Var(N, F, within=NonNegativeReals)
        m.T = Var(N, F, within=NonNegativeReals)
        
        @m.Constraint(N, F)
        def constraint_C4_1(m, k, f):
            return m.T[k, f] >= m.C[k,mac-1,f] - quicksum(m.X[j,k,f]*d[j] for j in N) - BigM*(1 - quicksum(m.X[j,k,f] for j in N))

        @m.Constraint(N, F)
        def constraint_C4_2(m, k, f):
            return m.E[k, f] >= quicksum(m.X[j,k,f]*d[j] for j in N) - m.C[k,mac-1,f] - BigM*(1 - quicksum(m.X[j,k,f] for j in N))

        @m.Objective()
        def tardiness(m, sense=minimize):
            return quicksum(m.T[k, f] + m.E[k, f] for k in N for f in F)        
        
    # Constraints
    @m.Constraint(N, M, F)
    def constraint_C1(m, k, i, f):
        if i > 0:
            return m.C[k,i,f] >= m.C[k,i-1,f] + quicksum(m.X[j,k,f]*p[j][i] for j in N)
        return Constraint.Skip
    
    @m.Constraint(N, M, F)
    def constraint_C2(m, k, i, f):
        if k > 0:
            return m.C[k,i,f] >= m.C[k-1,i,f] + quicksum(m.X[j,k,f]*p[j][i] for j in N)
        return Constraint.Skip
    
    @m.Constraint(N, F)     
    def constraint_C3(m, k, f):
        return m.C[k,0,f] >= quicksum(m.X[j,k,f]*(p[j][0]+r[f][j]) for j in N)  
    
    @m.Constraint(N)    
    def constraint_C5(m, j):
        return quicksum(m.X[j,k,f] for k in N for f in F)  == 1
    
    @m.Constraint(N)    
    def constraint_C6(m, k):
        return quicksum(m.X[j,k,f] for j in N for f in F)  == 1
    
    #solve with cplex or gurobi_direct
    
    if method == 'cplex':
        solver = SolverFactory('cplex')# cplex
        
        try:
            results = solver.solve(m, tee=True, timelimit=TL)
        except:
            return 0, 0, 0, TL, m, 'NoSolutionFound'
    else:
        solver = SolverFactory('gurobi_direct')# cplex
        
        try:
            results = solver.solve(m, tee=True, options={'TimeLimit': TL})
        except:
            return 0, 0, 0, TL, m, 'NoSolutionFound'
    
    status = results.solver.termination_condition
    
    if (status == TerminationCondition.optimal) or (status == TerminationCondition.maxTimeLimit):
        # Do something when the solution is feasible
        
        obj = results['Problem']()['Upper bound']
        lb  = results['Problem']()['Lower bound']
        
        if method == 'cplex':
            time = results['Solver']()['Time']
            if obj != 0.0:
                gap = abs ( lb - obj ) / ( abs (obj) + 1e-10 ) # GAP CPLEX
            else:
                gap = 0.0
        else:
            time = results['Solver']()['Wallclock time']
            if obj != 0.0:
                gap = abs ( lb - obj ) / ( abs (obj) ) # GAP GUROBI
            else:
                gap = 0.0
        
        return obj, lb, gap, time, m, str(status)
    
    elif (status == TerminationCondition.infeasible):
        # Do something when m in infeasible
        return 0, 0, 0, TL, m, str(status)
    
    else:
        # Something else is wrong
        return 0, 0, 0, TL, m, str(status)
