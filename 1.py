from ortools.linear_solver import pywraplp

from collections import defaultdict
from pprint import pprint
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', "--filename", help="data file name")
args = parser.parse_args()

def default():
    return []

def read(filename):
    with open(filename, 'r') as f:
        N, K = [int(i) for i in f.readline().split()]
        d = [0]
        d.extend([int(i) for i in f.readline().split()])
        t = [[int(i) for i in f.readline().split()] for _ in range(N+1)]
        for i in range(N+1):
            for j in range(N+1):
                if i!=j:
                    t[i][j]+=d[j]
        return N, K, t
N, K, t = read(args.filename)

c = [[0 for i in range(N+2*K)] for j in range(N+2*K)]
for i in range(N):
    for j in range(N):
        c[i][j] = t[i+1][j+1]
for i in range(N, N+2*K):
    for j in range(N):
        if j< N:
            c[i][j] = t[0][j+1]
            c[j][i] = t[j+1][0]


M=1000


B = [(i, j) for i in range(N+2*K) for j in range(N+2*K)]
F1 = [(i, k+N) for i in range(N+2*K) for k in range(K)]
F2 = [(k+K+N, i) for i in range(N+2*K) for k in range(K)]
F3 = [(i, i) for i in range(N+2*K)]
A = list(set(B)-set(F1) -set(F2)-set(F3))
A1 = defaultdict(default)
A2 = defaultdict(default)
for (i, j) in A:
    A1[i].append(j)
    A2[j].append(i)

solver = pywraplp.Solver.CreateSolver('CBC')
INF =solver.infinity()
x = [[[solver.IntVar(0, 1, 'x['+str(k)+', '+str(i)+', '+str(j)+']') for j in range(N+2*K)] for i in range(N+2*K)] for k in range(K)]
g = solver.IntVar(0, INF, 'g')
z = [solver.IntVar(0, K-1, f'z[{i}]') for i in range(N+2*K)]
y = [[solver.IntVar(0, INF, f'y[{k}][{i}]') for i in range(N+2*K)] for k in range(K)]

for i in range(N):
    solver.Add(sum(x[k][i][j] for k in range(K) for j in A1[i])==1)
    solver.Add(sum(x[k][j][i] for k in range(K) for j in A2[i])==1)
       
for i in range(N):
    for k in range(K):
        solver.Add(sum(x[k][i][j] for j in A1[i])==sum(x[k][j][i] for j in A2[i]))
        
for k in range(K):
    solver.Add(sum(x[k][k+N][j] for j in range(N))==1)
    solver.Add(sum(x[k][j][k+K+N] for j in range(N))==1)
    
    solver.Add(z[k+N]==k)
    solver.Add(z[k+K+N]==k)
    solver.Add(y[k][k+N]==0)
    solver.Add(y[k][k+K+N]==sum(x[k][i][j]*c[i][j] for (i, j) in A))

for (i, j) in A:
    for k in range(K):
        solver.Add(M*(1-x[k][i][j])+z[i]>=z[j])
        solver.Add(M*(1-x[k][i][j])+z[j]>=z[i])

        solver.Add(M*(1-x[k][i][j])+y[k][j]>=y[k][i]+c[i][j])
        solver.Add(M*(1-x[k][i][j])+y[k][i]+c[i][j]>=y[k][j])

        
for k in range(K):
    solver.Add(g>=y[k][k+K+N])

t0 =  time.time()
solver.Minimize(g)
result_status = solver.Solve()
print(f'time : {time.time()-t0}')
assert result_status==pywraplp.Solver.OPTIMAL
print('object = ', solver.Objective().Value())
for k in range(K):
    t = k+N
    print(f'Buu ta {k} : {t}', end='')
    while t!=k+K+N:
        for j in A1[t]:
            if x[k][t][j].solution_value()>0:
                print(f' --> {j}', end='')
                t=j
                break
    print('\n')
