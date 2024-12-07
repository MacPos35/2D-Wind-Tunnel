import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

c = 0.16 #m
q_inf = 335.7613443 #Pa
p_s = 99495.54635 #Pa

PPS = pd.read_excel('DATA_ANALYSIS/PPS.xlsx', skiprows = 2, usecols = [1, 2], sheet_name = 1)
PPS = PPS.to_numpy()
print(PPS)


with open('DATA_ANALYSIS/raw_2d.txt', 'r') as f:
    lines = f.readlines()
data = [line.strip().split('\t') for line in lines[2:]]
alphas = [float(row[2]) for row in data]
delta_pbs = [float(row[3]) for row in data]      
p_bars = [float(row[4]) for row in data]
temps = [float(row[5]) for row in data]
rpms = [float(row[6]) for row in data]
rhos = [float(row[7]) for row in data]

cps = []
deli = []
for a,b in zip(delta_pbs,p_bars):
    delminbar = a - 100 * b
    deli.append(delminbar)
for c in deli:
    cp = c / q_inf 
    cps.append(cp)
plt.plot(alphas, cps)
plt.xlabel('alpha')
plt.ylabel('Pressure coef')
plt.title('cp vs alpha')
plt.show()