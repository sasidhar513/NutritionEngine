import operator
import functools 
import numpy as np
import pickle
import os
from FoodEngineConstants import *
from Console import *

def computeCost(X, theta,y):
	pred=dotProduct(X,theta)
	return sum(sum((y-pred)**2))


def dotProduct(X,theta):
	product=X*theta
	return np.array([functools.reduce(operator.add,lis) for lis in product])


def gradientDescent(X,y,theta):	
	nutrientCount=X.shape[2] 		
	inputSampleSize=X.shape[0]
	tempTheta=np.zeros(shape=theta.shape)
	for i in range (0,theta.shape[0]):
		tempTheta[i]=  [(alpha/inputSampleSize)*sum(sum((((dotProduct(X,theta)-y) * X[:,i:i+1].reshape(inputSampleSize,nutrientCount)))))]*nutrientCount
	for i in range (0,theta.shape[0]):	
		theta[i]=theta[i]-tempTheta[i]
	for i in range (0,theta.shape[0]):	
		theta[i]=[max(x,0) for x in theta[i]]
	#theta=[[max(x,0) for x in y] for y in theta]
	#theta-=min(0,min([min(x) for x in theta.tolist()]))
