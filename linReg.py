# Me and dad exploring mean squared error and supervised learning for linear regression

import numpy as np
import random
#import matplotlib.pyplot as plt

eta = random.uniform(0, 0.06)  # adjust
#eta = 0
n = 1000
xi = np.array([5, 9, 0, 2, 4])     # given data sets
yi = np.array([15, 21, 4, 7, 11])

xii = np.array([4, 5, 0, 1])   # predict y values with regression line
yii = np.empty(xii.size)

def initial(m, c, eta, dataX, dataY):
  yhat = np.empty(dataX.size)
  etaArr = np.empty(n)
  jArr = np.empty(n)
  mArr = np.empty(n)
  cArr = np.empty(n)
  for k in range(n):
#    print("m: "+ str(m))
#    print("c: "+ str(c))
    mArr[k] = m
    cArr[k] = c
#    eta = random.uniform(0, 0.06)    
#    eta = eta + 0.01
    for i in range(dataX.size):
      yhat[i] = m*dataX[i] + c
    J = np.sum(np.square(np.subtract(dataY, yhat))) / dataX.size  # J is MSE
    djdm = np.sum(np.multiply(np.subtract(dataY, yhat),np.negative(dataX))) / dataX.size  # derivative of J w respect to m (partial derivative)
    djdc = np.sum(np.subtract(dataY, yhat)) / dataX.size   # derivative of J w respect to c 
    m = m - eta*djdm
    c = c - eta*djdc
    etaArr[k] = eta
    jArr[k] = J
#    print("eta"+ str(eta))
#    print("J: "+ str(J))
#    print("yhat: "+ str(yhat))
#    print('\n')
  print(etaArr)
  print(jArr)
  ind = np.min(jArr)   # find the minimum error iteration and then return its slope and intercept
  for l in range(jArr.size):
    if(ind == jArr[l]):
      print(l)
      print(str(mArr[l]) + " " + str(cArr[l]))
      m_slope = mArr[l]
      c_intercept = cArr[l]
      return [m_slope, c_intercept]

# input starting m and c (slope and intercept)      
results = initial(2, 3, eta, xi, yi)
for z in range(xii.size):
  yii[z] = results[0]*xii[z] + results[1]
print(yii) # prediction based on slope and intercept
