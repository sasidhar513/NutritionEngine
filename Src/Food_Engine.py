import operator
import functools 
import numpy as np
import pickle
import os
from FoodEngineConstants import *
from Console import *
from FoodEngineUtils import * 

np.set_printoptions(suppress=True)  # To not use exponential notation of the numbers	

def getAddMoreList(X,y,theta):
	dtProduct=dotProduct(X,theta)
	required=y[0]
	computedTotal=dtProduct[0]
	ratio=(y/dtProduct).tolist()[0]
	difference=(y-dtProduct).tolist()[0]
	addMoreList=[]

	for i in range(len(ratio)):
		if (ratio[i]>2 or difference[i]>50):
			print("For the nutrient " +nutrientsList[reqMineralList[i]]+"\n\tratio is "+
			str(ratio[i])+"\n\tdifference is "+str(difference[i])+
			"\n\tComputedTotal is "+str(computedTotal[i])+
			"\n\trequired is "+str(required[i]))
			addMoreList.append(i)
	print([reqMineralList[x] for x in addMoreList])
	return [reqMineralList[x] for x in addMoreList]
 
def getRemoveExistingFoodsList(X,y,theta):
	dtProduct=dotProduct(X,theta)
	required=y[0]
	computedTotal=dtProduct[0]
	ratio=(y/dtProduct).tolist()[0]
	difference=(y-dtProduct).tolist()[0]
	removeExisting=[]
	for i in range(len(ratio)):
		if(ratio[i]<0.5 or  difference[i]<(-50)):
			removeExisting.append(i);
	return removeExisting


def addMoreFoods(addMoreList,finalFoods):
	allTopFoodsForAddtionDict=[]
	for i in addMoreList:
		topFoods=[x for x in getTopFoodsForNutrient(False,i,50) if x not  in finalFoods]
		dailyRequirementLimitNutrients[i-1]

def foodEngine(foodList):
	global priviousCost
	finalFoods=[]
	
	if foodList:
		finalFoods=foodList
		
	elif firstRun:
		finalFoods=showFoodGroups()
		open(inputFile,'w').write(','.join(finalFoods))
		
	else:
		finalFoods=open(inputFile,'r').read().split('\n')[0].split(',')
	print(finalFoods)
	dailyLimitList_Y = [dailyRequirementLimitNutrients[x] for x in reqMineralList]
	X,y=getXandY(finalFoods,sampleCount,grams,dailyLimitList_Y,reqMineralList)
	inputSampleSize=X.shape[0]		# Number of samples
	foodCount=X.shape[1]			# no of food items(features) you are giving to find out the optimal
	nutrientCount=X.shape[2] 		# how many nutrients you gonna find out	
	if firstRun or foodList:
		theta= np.array([[i]*nutrientCount for i in np.random.rand(foodCount)])
		try:
			os.remove(thetaFile)
			os.remove(costFile)
		except OSError:
			pass
	else:	
		theta=np.array(eval(open(thetaFile,'r').read()))
		priviousCost=eval(open(costFile,'r').read())
	for i in range(iterations):
		gradientDescent(X,y,theta)
		print(str(i)+" cost",computeCost(X, theta,y))
		if priviousCost>=computeCost(X, theta,y):
			priviousCost=computeCost(X, theta,y)
			if i%999==0 and computeCost(X, theta,y)<=priviousCost :
				open(thetaFile,'w').write(str(theta.tolist()))
				open(costFile,'w').write(str(priviousCost))
	display_output(X,y,theta,finalFoods,grams,dailyLimitList_Y,reqMineralList)
	if getAddMoreList(X,y,theta):
		if addMoreFoods(getAddMoreList(X,y,theta)):
			foodEngine(finalFoods+addMoreFoods(getAddMoreList(X,y,theta),finalFoods))
			
		

		
foodEngine(['20131', '20011', '20316', '20647', '20090'])	
	



