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
    if (i <= s3[0,0]):
        return 0.0
    elif (i <= s3[1,0]):
        return s3[1,1]*(i-s3[0,0])/(s3[1,0]-s3[0,0])
    elif(i < s3[2,0]):
        return (1-s3[1,1])*(i-s3[2,0])/(s3[2,0]-s3[1,0])+1
    else:
        return 1.0

def low4(i,s4):
    if (i <= s4[0,0]):
        return 1.0
    elif (i <= s4[1,0]):
        return (s4[1,1]-1)*(i-s4[0,0])/(s4[1,0]-s4[0,0])+1
    elif(i <= s4[2,0]):
        return (s4[2,1]-s4[1,1])*(i-s4[1,0])/(s4[2,0]-s4[1,0])+s4[1,1]
    elif(i < s4[3,0]):
        return (-s4[2,1])*(i-s4[3,0])/(s4[3,0]-s4[2,0])
    else:
        return 0.0

def high4(i,s4):
    if (i <= s4[0,0]):
        return 0.0
    elif (i <= s4[1,0]):
        return s4[1,1]*(i-s4[0,0])/(s4[1,0]-s4[0,0])
    elif(i <= s4[2,0]):
        return (s4[2,1]-s4[1,1])*(i-s4[1,0])/(s4[2,0]-s4[1,0])+s4[1,1]
    elif(i < s4[3,0]):
        return (1-s4[2,1])*(i-s4[3,0])/(s4[3,0]-s4[2,0])+1
    else:
        return 1.0