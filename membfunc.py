import numpy as np
import math

def low3(i,s3):
    if (i < s3[0,0]):
        return 1.0
    elif (i <= s3[1,0]):
        return (s3[1,1]-1)*(i-s3[0,0])/(s3[1,0]-s3[0,0])+1
    elif(i <= s3[2,0]):
        return (-s3[1,1])*(i-s3[0,2])/(s3[0,2]-s3[0,1])
    else:
        return 0.0

def high3(i,s3):
    if (i < s3[0,0]):
        return 0.0
    elif (i <= s3[1,0]):
        return s3[1,1]*(i-s3[0,0])/(s3[1,0]-s3[0,0])
    elif(i <= s3[2,0]):
        return (1-s3[1,1])*(i-s3[0,3])/(s3[0,3]-s3[0,2])+1
    else:
        return 1.0


a = np.arange(6,dtype=float).reshape(3,2)
a[0,0] = 0.25
a[1,0] = 0.5
a[2,0] = 0.75
a[1,1] = 0.5

print(high3(0.49,a))