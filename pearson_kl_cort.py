import numpy as np
from numpy.linalg import norm
import scipy.stats

def CORTxy(X,Y):
    up=0
    x_s=0
    y_s=0
    for i in (range(1,len(X))):
        up+=(X[i]-X[i-1])*(Y[i]-Y[i-1])
        x_s+=(X[i]-X[i-1])*(X[i]-X[i-1])
        y_s+= (Y[i] - Y[i - 1]) * (Y[i] - Y[i - 1])
    return up/(np.sqrt(x_s)*np.sqrt(y_s))



real=[43,67,108,145,152,155,186,190,195,201,193,191,181,175,171,153,153,149,142,128, 124,118,109]
simu=[ 43.,  74., 117., 145., 161., 177., 174., 191., 199., 205., 196., 189., 178., 170.,167., 171., 175., 161., 159., 157., 153., 155., 151.]
print(np.corrcoef(real, simu))
print(np.dot(real,simu)/(norm(real)*norm(simu)))
print(CORTxy(real,simu))
KL = scipy.stats.entropy(real, simu)
print(KL)