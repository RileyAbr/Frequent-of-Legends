
#A skeleton for implementing K-nearest Neighbor classifier in Python.
## Author: Salem 
import numpy as np
import pandas as pd
import random
import time
import operator
import math

trainingFile = "classifier_train.txt"
testingFile = "classifier_test.txt"
Xtrain = np.loadtxt(trainingFile)
n = Xtrain.shape[0]
d = Xtrain.shape[1]-1
k = 5
print(n, d)
print(d)

#Testing .....
Xtest = np.loadtxt(testingFile)
nn = Xtest.shape[0] # Number of points in the testing data.
print(nn)
tp = 0 #True Positive
fp = 0 #False Positive
tn = 0 #True Negative
fn = 0 #False Negative

def euclidianDistance(data1, data2, length):
  distance = 0
  for x in range(length):
    distance += np.square(data1[x] - data2[x])
  return np.sqrt(distance)

def getNeighbors(trainingSet, testSet, k):
  distances = []
  length = len(testSet) - 1
  for x in range(len(trainingSet)):
    dist = euclidianDistance(testSet, trainingSet[x], length)
    distances.append(dist)
  neighbors = []
  c = np.argsort(distances)
  for x in range(k):
    neighbors.append(c[x])
  return neighbors

def getLabel(b):
  pos = 0
  neg = 0
  for x in b:
    if x == 1:
      pos += 1
    if x == -1:
      neg += 1
  if pos > neg:
    return 1
  if neg > pos:
    return -1
  
iteration_number = 0
for i in range(nn):
  f = Xtest[i]
  neighbors = getNeighbors(Xtrain, f, k)
  b = Xtrain[neighbors, d]
  prediction = getLabel(b)
  if prediction == 1 and f[d] == 1:
    tp += 1
  if prediction == 1 and f[d] == -1:
    fp += 1
  if prediction == -1 and f[d] == 1:
    fn += 1
  if prediction == -1 and f[d] == -1:
    tn += 1
  iteration_number = i
  print(i)
  


#Calculate all the measures required..

accuracy = ((tp + tn)/(tp + fp + tn + fn))
sensitivity = (tp/(tp + fn))
specificity = (tn/(fp + tn))
precision = (tp/(tp + fp))

print(nn, tp, fp, tn, fn)
print(accuracy)
print(sensitivity)
print(specificity)
print(precision)
