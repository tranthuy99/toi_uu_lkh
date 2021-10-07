import random
# print(random.randint(0, 3))
n=500
m=400
with open('data500_10.txt','w') as f:
    f.write(f'{n} {m}\n')
    for _ in range(n):
        f.write('3.0 ') 
    f.write('\n')

    for _ in range(m):
        f.write('18.0 ') 
    f.write('\n')

    for _ in range(n):
        k = random.randint(0, 20)
        f.write(str(k)+' ')
        tmp = random.sample(range(m), k)
        for i in tmp:
            f.write(str(i)+' ')
        f.write('\n')

    c = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        c[i][i] = 1
    for i in range(1500):
        t, k =  random.sample(range(n), 2)
        c[t][k] = c[k][t] = 1
    for i in range(n):
        for j in c[i]:
            f.write(str(j)+' ')
        f.write('\n')
     