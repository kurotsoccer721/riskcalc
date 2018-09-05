# coding: utf-8
# In[6]:
import numpy as np
import math

# shape graph
# potential risk graph
def low(r, l1, l2, l3, l4):
    if (r < l1):
        return 1.0
    elif (r <= l2):
        return (l4 - 1) * (r - l1) / (l2 - l1) + 1
    elif (r <= l3):
        return (-l4) * (r - l3) / (l3 - l2)
    else:
        return 0.0

def high(r, l1, l2, l3, l4):
    return 1 - low(r, l1, l2, l3, l4)


# distance graph
def near(d, n1, n2, n3, n4):
    if (d < n1):
        return 1.0
    elif (d <= n2):
        return (n4 - 1) * (d - n1) / (n2 - n1) + 1
    elif (d <= n3):
        return (-n4) * (d - n3) / (n3 - n2)
    else:
        return 0.0

def far(d, n1, n2, n3, n4):
    return 1 - near(d, n1, n2, n3, n4)


# calclate risk level
# high&near:10  low&near:7   high&far:4   low&far:1
def calcrisk(r, d, params):
    # r=potential risk level,d=distance(0~1)
    # fuzzy rule(this is hyper parameter)
    hn = 10.0
    ln = 7.0
    hf = 5.0
    lf = 0.0

    l1 = params[0, 0]
    l2 = params[0, 1]
    l3 = params[0, 2]
    l4 = params[1, 1]
    n1 = params[2, 0]
    n2 = params[2, 1]
    n3 = params[2, 2]
    n4 = params[3, 1]

    r1 = min(high(r, l1, l2, l3, l4), near(d, n1, n2, n3, n4)) * hn
    r2 = min(low(r, l1, l2, l3, l4), near(d, n1, n2, n3, n4)) * ln
    r3 = min(high(r, l1, l2, l3, l4), far(d, n1, n2, n3, n4)) * hf
    r4 = min(low(r, l1, l2, l3, l4), far(d, n1, n2, n3, n4)) * lf
    return r1 + r2 + r3 + r4

def calcriskmodel(a, p):    # for GA
    # a=data([location],class),p=params(3*5)
    # output is risk revel

    # potential risk(hyper param)
    bird = 0.4
    car = 0.7
    person = 0.9
    none = 0.0

    d = (1 - a[2]) * 2 #distance
    if (a[4] == 5.0):
        r = bird
    elif (a[4] == 16.0):
        r = bird
    elif (a[4] == 3.0):
        r = car
    elif (a[4] == 1.0):
        r = person
    else:
        r = none
    result = calcrisk(r, d, p)
    return result


def calcriskmodel2(a, c, p):
    # for object_detection API
    # a=[location],c=classes,p=params(n1,n2,f1,f2)
    # output is risk revel
    # potential risk(hyper param)
    bird = 0.4
    car = 0.7
    person = 0.9
    none = 0.0

    d = (1 - a[2]) * 2
    if (c == 5.0):
        r = bird
    elif (c == 16.0):
        r = bird
    elif (c == 3.0):
        r = car
    elif (c == 1.0):
        r = person
    else:
        r = none
    result = calcrisk(r, d, p)
    return result


def directionguide(a):
    # input is data([location],class)
    # output is which directuon is danger(0~5)
    # left(0)  straight(1)  right(2)  left&strainght(3)  straight&right(4)
    # all directions(5)
    d = (1 - a[2]) * 2
    exd = 0.1 * (1 - d)
    # This is extra distance depends on d.
    # This is need to avoid with enough distance

    # left-end:a[1] right-end:a[3]
    if (a[1] - exd <= 1 - a[2]):
        if (a[3] + exd <= 1 - a[2]):
            return 0
        elif (a[3] + exd <= a[2]):
            return 3
        elif (a[3] + exd > a[2]):
            return 5
    elif (a[1] - exd <= a[2]):
        if (a[3] + exd <= a[2]):
            return 1
        elif (a[3] + exd > a[2]):
            return 4
    elif (a[1] - exd > a[2]):
        return 2


def decideaction(a):
    b = np.zeros(3)
    for i in range(0, 6):
        if (i == 0):
            b[0] = b[0] + a[i]
        if (i == 1):
            b[1] = b[1] + a[i]
        if (i == 2):
            b[2] = b[2] + a[i]
        if (i == 3):
            b[0] = b[0] + a[i]
            b[1] = b[1] + a[i]
        if (i == 4):
            b[1] = b[1] + a[i]
            b[2] = b[2] + a[i]
        if (i == 5):
            b[0] = b[0] + a[i]
            b[1] = b[1] + a[i]
            b[2] = b[2] + a[i]
    if (np.min(b) == b[1]):
        if (b[1] == 0):
            return 1
        elif (b[0] == b[1] == b[2]):
            return 0
        else:
            return 1
    elif (np.min(b) == b[0]):
        return 0
    else:
        return 2