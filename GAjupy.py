import numpy as np
import pickle
import random
import fuzzyfunc as fz
import sys

sys.setrecursionlimit(10000000)

with open('bird_teacher.pickle', 'rb')as f:
    bird = pickle.load(f)
with open('car_teacher.pickle', 'rb')as f:
    car = pickle.load(f)
with open('person_teacher.pickle', 'rb')as f:
    person = pickle.load(f)

def calcloss(p):
    for i in range(0, 10):
        sumbird = 0.0
        for j in range(bird.shape[0]):
            f = fz.calcriskmodel(bird[j], p[i])
            l = f - bird[j, 5]
            sumbird = sumbird + (l * l)
        sumcar = 0.0
        for j in range(car.shape[0]):
            f = fz.calcriskmodel(car[j], p[i])
            l = f - car[j, 5]
            sumcar = sumcar + (l * l)
        sumperson = 0.0
        for j in range(person.shape[0]):
            f = fz.calcriskmodel(bird[j], p[i])
            l = f - bird[j, 5]
            sumbird = sumbird + (l * l)
        sum = (sumbird + sumcar + sumperson) / (bird.shape[0] + car.shape[0] + person.shape[0])
        p[i, 2, 0] = sum
    return p


def tournament(p):
    b = np.arange(150, dtype=np.float).reshape(10, 5, 3)
    for i in range(0, 10):
        n = np.random.randint(0, 10)
        m = np.random.randint(0, 10)
        if (p[n, 4, 0] < p[m, 4, 0]):
            b[i] = p[n]
        else:
            b[i] = p[m]
    return b


def crossover(p):
    x = np.arange(150, dtype=np.float).reshape(10, 5, 3)
    for i in range(0, 10, 2):
        # crossover near
        n = np.random.randint(0, 2)
        a, b = np.hsplit(p[i, 0], [n + 1])
        c, d = np.hsplit(p[i + 1, 0], [n + 1])
        x[i, 0] = np.hstack((a, d))
        x[i + 1, 0] = np.hstack((c, b))

        # crossover far
        m = np.random.randint(0, 2)
        a, b = np.hsplit(p[i, 2], [m + 1])
        c, d = np.hsplit(p[i + 1, 2], [m + 1])
        x[i, 2] = np.hstack((a, d))
        x[i + 1, 2] = np.hstack((c, b))
    for j in range(0, 10):
        x[j, 1] = p[j, 1]
        x[j, 3] = p[j, 3]
        x[j, 4] = p[j, 4]
    return x


def mutation(p):
    s = 0.01  # strangth of mutation(hyper param)
    for i in range(0, 10):
        for j in range(0, 4, 2):
            # mutation n1~n3,f1~f3
            for m in range(0, 3):
                n = np.random.randint(0, 2)  # n=0:not mutate n=1:mutate
                l = np.random.randint(0, 2)  # l=0:mutate for+   l=1:mutate for-
                k = np.random.randint(0, 10)  # how mutate
                if (n == 1):
                    if (l == 0):
                        p[i, j, m] = p[i, j, m] + (s * k)
                        if (p[i, j, m] > 1):
                            p[i, j, m] = p[i, j, m] - (s * k)
                    if (l == 1):
                        p[i, j, m] = p[i, j, m] - (s * k)
                        if (p[i, j, m] < 0):
                            p[i, j, m] = p[i, j, m] + (s * k)
        for j in range(1, 4, 2):
            # mutation n4,f4
            n = np.random.randint(0, 2)  # n=0:not mutate n=1:mutate
            l = np.random.randint(0, 2)  # l=0:mutate for+   l=1:mutate for-
            k = np.random.randint(0, 10)  # how mutate
            if (n == 1):
                if (l == 0):
                    p[i, j, 1] = p[i, j, 1] + (s * k)
                    if (p[i, j, 1] > 1):
                        p[i, j, 1] = p[i, j, 1] - (s * k)
                if (l == 1):
                    p[i, j, 1] = p[i, j, 1] - (s * k)
                    if (p[i, j, 1] < 0):
                        p[i, j, 1] = p[i, j, 1] + (s * k)

    return p


def sort(p):
    for i in range(0, 10):
        for j in range(0, 4, 2):
            p[i, j] = np.sort(p[i, j])
    return p


def select(p, b):
    best = np.arange(15, dtype=np.float).reshape(5, 3)
    best = b
    for i in range(10):
        if (p[i, 4, 0] <= best[4, 0]):
            best = p[i]
    return best


def loop(a, b, n, l):
    if (n == 1):
        ax = calcloss(sort(mutation(crossover(tournament(a)))))
        bx = select(ax, b)
        l.append(bx[4, 0])
        return bx, l
    else:
        ax = calcloss(sort(mutation(crossover(tournament(a)))))
        bx = select(ax, b)
        if (n % 500 == 0):
            print (bx[4, 0])
            l.append(bx[4, 0])
        return loop(ax, bx, n - 1, l)


# ----------------------------------------------------------------------------------

# make 10 1st generations(p[0]~p[9])
p=np.arange(150,dtype=np.float).reshape(10,5,3)
for i in range(0,10):
    for j in range(0,5):
        for k in range(0,3):
            p[i,j,k]=np.random.rand()
        if (j%2==0):
            p[i,j]=np.sort(p[i,j])
    p[i,1,0]=1.0
    p[i,1,2]=0.0
    p[i,3,0]=1.0
    p[i,3,2]=0.0
p = calcloss(p)
p=tournament(p)
p=crossover(p)
p=mutation(p)
p=sort(p)
p=calcloss(p)
b0=select(p,p[0])
# b0:best of 0th generations

# ----------------------------------------------------------------------------------
# loss memory
list = []
best, loss = loop(p, b0, 100000, list)
print ("end")
print ("best:\n", best)
print ("loss:\n",loss)