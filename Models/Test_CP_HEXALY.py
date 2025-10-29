# -*- encoding: utf-8 -*-

# Test for CP
import pandas as pd
from CP_HEXALY import CP_HEXALY, read_instance

TL = 600
FO = 'Cmax' # Cmax, TotalCT, Tardiness or JIT
with_tt = False # With or without transportation times

instancias = []

f_small = [2, 3, 4]
n_small = [4, 6, 8, 10, 12, 14, 16]
m_small = [2, 3, 4, 5]

for nf in f_small:
    for n in n_small:
        for m in m_small:
            for i in range(1, 6):
                
                instancias.append(f'I_{nf}_{n}_{m}_{i}.txt')
                
f_large = [2, 3, 4, 5, 6, 7]
oper = [(n, m) for n in [20, 50, 100] for m in [5, 10, 20]] + \
        [(n, m) for n in [200] for m in [10, 20]] + \
        [(n, m) for n in [500] for m in [20] ]

for nf in f_large:
    idx = 0
    for n, m in oper:
        for i in range(1, 11):
            
                idx += 1
                
                if idx < 10:
                    instancias.append(f'Ta00{idx}_{nf}.txt')
                elif idx < 100:
                    instancias.append(f'Ta0{idx}_{nf}.txt')
                else:
                    instancias.append(f'Ta{idx}_{nf}.txt')

resultados = pd.DataFrame(index=instancias, columns='TYPE nf n m UB LB GAP Time Status'.split())
resultados.index.name = 'Instâncias'

print('Small Instances Test - CP Model')

f_small = [2, 3, 4]
n_small = [4, 6, 8, 10, 12, 14, 16]
m_small = [2, 3, 4, 5]

r_path = 'Instâncias/release_dates/DPFSP_Small/'
d_path = 'Instâncias/due_dates/DPFSP_Small/'

for nf in f_small:
    
    p_path = f'Instâncias/processing_times/DPFSP_Small/{nf}/'
    
    for n in n_small:
        for m in m_small:
            for i in range(1, 6):
                
                pfile = f'I_{nf}_{n}_{m}_{i}.txt'
                rfile = f'RD_{nf}_{n}_{m}_{i}.txt'
                dfile = f'DD_{nf}_{n}_{m}_{i}.txt'


                print(pfile)
                
                nf, m, n, p, r, d = read_instance(p_path+pfile, r_path+rfile, d_path+dfile)
                
                if not with_tt:
                    r[:, :] = 0
                                
                UB, LB, GAP, Time, msol, status = CP_HEXALY(p, r, d, nf, TL=TL, objective=FO)
                
                resultados['UB'][pfile] = round(UB)
                resultados['LB'][pfile] = round(LB)
                resultados['GAP'][pfile] = round(GAP, 2)
                resultados['Time'][pfile] = round(Time, 4)
                resultados['Status'][pfile] = status
                
                resultados['TYPE'][pfile] = 'Small'
                resultados['nf'][pfile] = nf
                resultados['n'][pfile] = n
                resultados['m'][pfile] = m
                
                if with_tt:
                    resultados.to_csv(f'Resultados_CP_hexaly_DFm_r_{FO}.txt')
                else:
                    resultados.to_csv(f'Resultados_CP_hexaly_DFm_{FO}.txt')

print('Large Instances Test - CP Model')

f_large = [2, 3, 4, 5, 6, 7]
oper = [(n, m) for n in [20, 50, 100] for m in [5, 10, 20]] + \
        [(n, m) for n in [200] for m in [10, 20]] + \
        [(n, m) for n in [500] for m in [20] ]
        
r_path = 'Instâncias/release_dates/DPFSP_Large/'
d_path = 'Instâncias/due_dates/DPFSP_Large/'

for nf in f_large:
    p_path = f'Instâncias/processing_times/DPFSP_Large/{nf}/'
    idx = 0
    for n, m in oper:
        for i in range(1, 11):
            
                idx += 1
                
                if idx < 10:
                    pfile = f'Ta00{idx}_{nf}.txt'
                elif idx < 100:
                    pfile = f'Ta0{idx}_{nf}.txt'
                else:
                    pfile = f'Ta{idx}_{nf}.txt'
                    
                rfile = f'RD_{nf}_{n}_{m}_{i}.txt'
                dfile = f'DD_{nf}_{n}_{m}_{i}.txt'


                print(pfile)
                
                nf, m, n, p, r, d = read_instance(p_path+pfile, r_path+rfile, d_path+dfile)
                
                if not with_tt:
                    r[:, :] = 0
                                
                UB, LB, GAP, Time, msol, status = CP_HEXALY(p, r, d, nf, TL=TL, objective=FO)
                
                resultados['UB'][pfile] = round(UB)
                resultados['LB'][pfile] = round(LB)
                resultados['GAP'][pfile] = round(GAP, 2)
                resultados['Time'][pfile] = round(Time, 4)
                resultados['Status'][pfile] = status
                
                resultados['TYPE'][pfile] = 'Large'
                resultados['nf'][pfile] = nf
                resultados['n'][pfile] = n
                resultados['m'][pfile] = m
                
                if with_tt:
                    resultados.to_csv(f'Resultados_CP_hexaly_DFm_r_{FO}.txt')
                else:
                    resultados.to_csv(f'Resultados_CP_hexaly_DFm_{FO}.txt')