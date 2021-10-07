from pprint import pprint
from typing import List
from ortools.linear_solver import pywraplp
from ortools.linear_solver.pywraplp import Variable
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', "--filename", help="data file name")
args = parser.parse_args()

start = time.time()
def read_data(filename):
    with open(filename, 'r') as f:
        (n, m) = [int(_) for _ in f.readline().strip().split()]
        d = [float(_) for _ in f.readline().strip().split()]
        t = [float(_) for _ in f.readline().strip().split()]
        D = [[int(i) for i in f.readline().strip().split()] for _ in range(n)]
        for i in range(n):
            D[i].remove(D[i][0])
        c = [[int(i) for i in f.readline().strip().split()] for _ in range(n)]
        return n, m, d, t, D, c


# pprint(read_data('./input/1.txt'))


n, m, d, t, D, c = read_data(args.filename)
print(time.time()-start)
solver = pywraplp.Solver.CreateSolver('GLOP')

x = [[solver.IntVar(0, 1, 'x['+str(i)+', '+str(j)+']') for j in range(m)] for i in range(n)] 
# print(time.time()-start)
# for i in range(n):
#     ct = solver.Constraint(0, 1, 'ct')
#     for j in D[i]:
#         ct.SetCoefficient(x[i][j], 1)

for i in range(n):
    for j in range(m):
        ct0 = solver.Constraint(0, 1, 'ct0')
        if j not in D[i]:
            ct = solver.Constraint(0, 0, 'ct')
            ct.SetCoefficient(x[i][j], 1)
        else:
            ct0.SetCoefficient(x[i][j], 1)

for i in range(n):
    for j in range(n):
        if c[i][j] == 1 & i!=j:
            for k in range(m):
                ct = solver.Constraint(0, 1, 'ct')
                ct.SetCoefficient(x[i][k], c[i][j])
                ct.SetCoefficient(x[j][k], c[i][j])

for j in range(m):
    ct = solver.Constraint(0, t[j], 'ct')
    for i in range(n):
        ct.SetCoefficient(x[i][j], d[i])

objective = solver.Objective()
for i in range(n):
    for j in D[i]:
        objective.SetCoefficient(x[i][j], 1)


objective.SetMaximization()
result_status = solver.Solve()
assert result_status==pywraplp.Solver.OPTIMAL


l={}
for i in range(n):
    for j in D[i]:
        if x[i][j].solution_value()!=0:
            l[i] = j
            print(i, ' ', j, ' ')
            
            # for k in l.keys():
            #     if (c[i][k]==1) & (x[k][j].solution_value()==1) & (i!=k):
            #         print('sai roi', i,' ', k)
            #         break
            # break
    if i in l.keys():
        pass 
    else:
        print(i, ' ', -1)  
print('objective = ', solver.Objective().Value())
print(time.time()-start)
     