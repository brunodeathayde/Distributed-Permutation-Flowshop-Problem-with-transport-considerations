# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 19:17:58 2025

@author: levi1
"""

from numpy import loadtxt
import hexaly.optimizer

def read_instance(pfile:str, rfile:str, dfile:str):
    
    n, m = loadtxt(pfile, max_rows=1, dtype=int)
    nf = loadtxt(pfile, skiprows=1, max_rows=1, dtype=int).tolist()
    p = loadtxt(pfile, skiprows=2, dtype=int)[:, 1::2].T
    r = loadtxt(rfile, dtype=int)
    d = loadtxt(dfile, dtype=int)
    
    return nf, m, n, p, r, d

def CP_HEXALY(p, r, d, nf, TL=600, objective='Cmax'):
    
    with hexaly.optimizer.HexalyOptimizer() as optimizer:
        
        mac, n = p.shape
        
        F = range(nf)
        M = range(mac)
        N = range(n)
        
        BigM = r.sum() + p.sum()
    
        #
        # Declare the optimization model
        #
        
        m = optimizer.model
    
        x =  m.array([[ m.interval(0, BigM) for j in N] for i in M])
        
        Gamma  =  m.array([m.list(n) for f in F])
        
        # Constraints
        
        m.constraint( m.partition( Gamma ) ) # cada job em apenas uma fábrica
        
        
        for i in M:
            for j in N:
                m.constraint( m.length(x[i][j]) == p[i][j] )
                
        for f in F:
            for j in N:
                m.constraint( m.start( x[0][j] ) >= r[f][j]*m.contains(Gamma[f], j) )
                
        for i in M:
            for j in N:
                if i > 0:
                    m.constraint( x[i][j] > x[i-1][j] )
                
        for f in F:
            for i in M:
                m.constraint( m.and_( m.range(1, m.count(Gamma[f])), 
                                     m.lambda_function(lambda k: x[i][Gamma[f][k]] > x[i][Gamma[f][k-1]]) 
                                      ) )
            

        if objective == 'Cmax':
            FO = m.max( [m.end( x[mac-1][j] ) for j in N] ) 
            m.minimize( FO )
            
        elif objective == 'TotalCT':
            FO = m.sum( [m.end( x[mac-1][j] ) for j in N] )
            m.minimize( FO )
        
        elif objective == 'Tardiness':
            FO = m.sum( [m.max( [m.end( x[mac-1][j] ) - d[j], 0] ) for j in N] )
            m.minimize( FO )
            
        else:
            FO = m.sum( [m.abs( d[j] - m.end( x[mac-1][j] ) ) for j in N] )
            m.minimize( FO )
        
            
    
        
        m.close()
        
        optimizer.param.time_limit = TL
    
        optimizer.solve()
            
        obj = FO.value
        lb = optimizer.get_solution().get_objective_bound(0)
        gap = optimizer.get_solution().get_objective_gap(0)
        time = optimizer.get_statistics().get_running_time()
        msol = [str(x.value), str(Gamma.value)]  
        status = str(optimizer.solution.get_status()).split('.')[1]
        
        return obj, lb, gap, time, msol, status
