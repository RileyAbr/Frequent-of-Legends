
#A skeleton for implementing Naive Bayes Classifier in Python.
## Author: Salem 

import numpy
import pandas
import random
import time
import operator
import math
import random

trainingFile = "classifier_train.txt"
testingFile = "classifier_test.txt"
Xtrain = numpy.loadtxt(trainingFile)
n = Xtrain.shape[0]
d = Xtrain.shape[1]-1
print(n, d)
#Training... Collect mean and standard deviation for each dimension for each class..
#Also, calculate P(C+) and P(C-)

#Testing .....
Xtest = numpy.loadtxt(testingFile)
nn = Xtest.shape[0] # Number of points in the testing data.

tp = 0 #True Positive
fp = 0 #False Positive
tn = 0 #True Negative
fn = 0 #False Negative


#Iterate over all points in testing data
  #For each point find the P(C+|Xi) and P(C-|Xi) and decide if the point belongs to C+ or C-..
  #Recall we need to calculate P(Xi|C+)*P(C+) ..
  #P(Xi|C+) = P(Xi1|C+) * P(Xi2|C+)....P(Xid|C+)....Do the same for P(Xi|C-)
  #Now that you've calculate P(Xi|C+) and P(Xi|C-), we can decide which is higher 
  #P(Xi|C-)*P(C-) or P(Xi|C-)*P(C-) ..
  #increment TP,FP,FN,TN accordingly, remember the true lable for the ith point is in Xtest[i,d]

#}

#Calculate all the measures required..
 
def calculate_probability(xi, mean, stdev):
	exponent = math.exp(-((xi-mean)**2/(2 * stdev**2)))
	return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

def accuracy():
	return ((tp +tn) / (tp + fp + tn +fn))

def precision():
	return (tp / (tp + fp))

def recall():
	return (tp / (tp + fn))

pos = 0
neg = 0

for i in range(n):
	x = Xtrain[i]
	if x[d] == 1:
		pos += 1
	if x[d] == -1:
		neg += 1

#for P(C+)
posClass = (pos/(n))
#for P(C-)
negClass = (neg/(n))


posIds = Xtrain[:,d] == 1
negIds = Xtrain[:,d] == -1

xTrainPos = Xtrain[posIds,]
xTrainNeg = Xtrain[negIds,]

meanTrainPos = numpy.mean(xTrainPos[:,0:d], axis=0)
stdTrainPos = numpy.std(xTrainPos[:,0:d], axis=0)

meanTrainNeg = numpy.mean(xTrainNeg[:,0:d], axis=0)
stdTrainNeg = numpy.std(xTrainNeg[:,0:d], axis=0)

iteration_number = 0

for i in range(nn):
	iteration_number = i
	print(i)
	x = Xtest[i,0:d]
	xlabel = Xtest[i,d]
	predictedLabel = 0
	posTest = 1
	for i in range(d):
		posTest = calculate_probability(x[i], meanTrainPos[i], stdTrainPos[i])
		posTest *= posTest
	posCompare = posTest * posClass
	negTest = 1
	for i in range(d):
		negTest = calculate_probability(x[i], meanTrainNeg[i], stdTrainNeg[i])
		negTest *= negTest
	negCompare = negTest * negClass

	if posCompare > negCompare:
		predLabel = 1
	if negCompare > posCompare:
		predLabel = -1
	
	if predLabel == 1 and xlabel == 1:
		tp += 1
	if predLabel == 1 and xlabel == -1:
		fp += 1
	if predLabel == -1 and xlabel == -1:
		tn += 1
	if predLabel == -1 and xlabel == 1:
		fn += 1


print(nn, tp, fp, tn, fn)
print(accuracy())
print(precision())
print(recall())
