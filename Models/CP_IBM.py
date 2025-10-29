# -*- coding: utf-8 -*-
"""
Created on Fri May  3 08:13:43 2024

@author: levi1
"""

# Constraint programming models

from numpy import loadtxt
import docplex.cp.utils_visu as visu
from docplex.cp.model import CpoModel
from docplex.cp.expression import INTERVAL_MAX

def read_instance(pfile:str, rfile:str, dfile:str):
    
    n, m = loadtxt(pfile, max_rows=1, dtype=int)
    nf = loadtxt(pfile, skiprows=1, max_rows=1, dtype=int).tolist()
    p = loadtxt(pfile, skiprows=2, dtype=int)[:, 1::2].T
    r = loadtxt(rfile, dtype=int)
    d = loadtxt(dfile, dtype=int)
    
    return nf, m, n, p, r, d

def plot_gantt(msol, F, M, N):
    
    visu.timeline('Schedule')

    for f in F:
        visu.panel(name=f"$F_{{{f+1}}}$")
        for i in M:
            interval_list = [(msol.get_value(f"F{f}-M{i}-J{j}")[0], msol.get_value(f"F{f}-M{i}-J{j}")[1], j, f'$J_{{{j+1}}}$') 
                              for j in N if msol.get_value(f"F{f}-M{i}-J{j}") != ()]
            visu.sequence(name=f"$M_{{{i+1}}}$", intervals=interval_list)
    
    visu.show()
    
def CP_IBM(p, r, d, nf, TL=600, objective='Cmax'):
    
    m, n = p.shape
        
    F = range(nf)
    M = range(m)
    N = range(n)  
    
    modelo = CpoModel()
    
    x = [[[modelo.interval_var(name=f"F{f}-M{i}-J{j}", optional=True, size=p[i, j], start=(r[f][j], INTERVAL_MAX))
                                                for j in N] for i in M] for f in F]
    
    y = [[modelo.interval_var(name=f"M{i}-J{j}") for j in N] for i in M]
    
    mac = [[modelo.sequence_var(vars=x[f][i], 
                                ) for i in M] for f in F]
    
    if objective == 'Cmax':
        modelo.add(
            modelo.minimize(
                modelo.max( [modelo.end_of(y[m-1][j]) for j in N] )
                )
            )
    
    elif objective == 'Tardiness':
        modelo.add(
            modelo.minimize(
                modelo.sum([ modelo.max([ modelo.end_of(y[m-1][j]) - d[j], 0 ]) for j in N ])
                )
            )
        
    elif objective == 'TotalCT':
        modelo.add(
            modelo.minimize(
                modelo.sum( [modelo.end_of(y[m-1][j]) for j in N] )
                )
            )
        
    else:
        modelo.add(
            modelo.minimize(
                modelo.sum( modelo.abs( d[j] - modelo.end_of(y[m-1][j]) ) for j in N )
                )
            )       
    
    for i in range(1, m):
        for j in N:
            for f in F:
                modelo.add( 
                modelo.presence_of(x[f][0][j]) == modelo.presence_of(x[f][i][j])
                )
                
    for i in M:
        for j in N:
            modelo.add( modelo.alternative( y[i][j], [x[f][i][j] for f in F] ) )
            
    for f in F:
        for i in M:
            modelo.add( modelo.no_overlap( mac[f][i] ) )
            
    for f in F:
        for i in range(m-1):
            for j in N:
                modelo.add( modelo.end_before_start( x[f][i][j], x[f][i+1][j] ) )
                
    for f in F:
        for i in range(m-1):
            modelo.add( modelo.same_sequence(mac[f][i], mac[f][i+1]) )
        
    msol = modelo.solve(TimeLimit=TL)#, SolutionLimit=2)
    
    obj = msol.get_objective_values()[0]
    lb  = msol.get_objective_bounds()[0]
    gap = msol.get_objective_gaps()[0]
    time  = msol.get_solve_time()
    status = msol.get_solve_status()
    
    return obj, lb, gap, time, msol, status