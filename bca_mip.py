from pprint import pprint
import re
from ortools.linear_solver import pywraplp
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-fin', "--filein", help="input file name")
# parser.add_argument('-fout', "--fileout", help="output file name")
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

# đọc dữ liệu từ file
n, m, d, t, D, c = read_data(args.filein)

# tạo solver
solver = pywraplp.Solver.CreateSolver('CBC')

# tạo biến
x = [[solver.IntVar(0, 1, 'x['+str(i)+', '+str(j)+']') for j in range(m)] for i in range(n)] 

# D[i] là tập giáo viên có thể nhận lớp i 
for i in range(n):
    solver.Add(sum(x[i][j] for j in D[i])<=1)

for i in range(n):
    for j in range(m):
        if j not in D[i]:
            solver.Add(x[i][j]==0)

# các lớp trùng thời khóa biểu không được phân cho cùng một giáo viên 
for i in range(n):
    for j in range(n):
        if c[i][j] == 1 and i != j:
            for k in range(m):
                solver.Add(x[i][k] + x[j][k] <= 1)

# giáo viên j có thời gian đứng lớp tối đa là t[i]
for j in range(m):
    solver.Add(sum(x[i][j]*d[i] for i in range(n))<=t[j])

arr = [x[i][j] for i in range(n) for j in range(m)]

# tối ưu hóa hàm mục tiêu
solver.Maximize(sum(arr))

result_status = solver.Solve()
assert result_status==pywraplp.Solver.OPTIMAL
l={}
for i in range(n):
    l[i] = -1
    for j in D[i]:
        if x[i][j].solution_value()!=0:
            l[i] = j
            break
#     print(i, l[i])
# print(int(solver.Objective().Value()))

no = re.search('\d[.]', args.filein).group().replace('.', '')
with open(f'20173394-{no}-out.txt', 'w') as f:
    for i in range(n):
        f.write(f'{i} {l[i]}\n')
    f.write(str(int(solver.Objective().Value())))
print(time.time()-start)
