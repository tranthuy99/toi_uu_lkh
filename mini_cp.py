from ortools.linear_solver.pywraplp import Solver
from ortools.sat.python import cp_model
from pprint import pprint
import numpy as np
import time
model = cp_model.CpModel()
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', "--filename", help="data file name")
args = parser.parse_args()

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

M=np.sum(c)


x = [model.NewIntVar(0, N+2*K-1, f'x[{i}]') for i in range(N+K)]
IR = [model.NewIntVar(0, K-1, f'IR[{i}]') for i in range(N+2*K)]
l = [model.NewIntVar(0, int(M), f'l[{i}]') for i in range(N+2*K)]
y = model.NewIntVar(0, int(M), 'y')


for i in range(N, N+K):
    model.Add(l[i]==0)


model.AddAllDifferent(x)

for i in range(K):
    model.Add(IR[N+i]==IR[N+K+i])

for i in range(N+K):
    model.AddAllDifferent([x[i], i])

b=[[model.NewBoolVar(f'b[{i}][{j}]') for j in range(N+2*K)] for i in range(N+K)]
for i in range(N+K):
    for j in range(N+2*K):
        model.Add(x[i]==j).OnlyEnforceIf(b[i][j])
        model.Add(x[i]!=j).OnlyEnforceIf(b[i][j].Not())
        model.Add(IR[i]==IR[j]).OnlyEnforceIf(b[i][j])
        model.Add(l[j]-l[i]==c[i][j]).OnlyEnforceIf(b[i][j])



for i in range(N+K):
    for j in range(N, N+K):
        model.AddAllDifferent([x[i], j])
        
# startIR = [IR[i] for i in range(N, N+K)]
# model.AddAllDifferent(startIR)


for i in range(N+K, N+2*K):
    model.Add(y-l[i]>=0)

model.Minimize(y)
solver=cp_model.CpSolver()
t0 =time.time()
status = solver.Solve(model)
print('time: '+str(time.time()-t0))
assert status == cp_model.OPTIMAL
print('Minimum of objective function: %i\n' % solver.ObjectiveValue())

for i in range(N, N+K):
    j=i
    print(f'Phu ta {j-N+1}: {i}   ', end='')
    while j<N+K:
        print(solver.Value(x[j]),  '   ', end='')
        j=solver.Value(x[j])
    print('\n')

