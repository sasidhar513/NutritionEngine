import operator
import functools 
import numpy as np
import pickle
import os
from FoodEngineConstants import *
from Console import *
from FoodEngineUtils import * 

np.set_printoptions(suppress=True)  # To not use exponential notation of the numbers	



exclusionList=[]
#exclusionList=getExclusionList(exclusionNutrientList,exclusionNutrientFoodCount)
finalFoods=[]
#finalFoods=[str(int(float(food))) for food in  [topFoodsForANutrient for topFoodsForANutrient in getTopFoodForNutrients(TopFoodsForEachVitaminCount)]if food not in exclusionList]+addList
if firstRun:
	finalFoods=showFoodGroups()
	finalFoods+=['9033', '9163', '9079', '9094', '9292', '12061', '12087', '12104', '5062', '15265', '9500', '9021', '9037', '9040', '9421', '9322', '1123', '1211', '2043', '2030', '2025', '2009', '2004', '2047', '2006', '2005', '2044', '4584', '4593', '16022', '16056', '16144', '11003', '11457', '11696', '11282', '11216', '11215', '11165']
	open(inputFile,'w').write(','.join(finalFoods))
else:
	finalFoods=open(inputFile,'r').read().split('\n')[0].split(',')
	print(finalFoods)
#finalFoods=['20058', '20038', '11003', '11052', '11080', '11215', '11216']
dailyLimitList_Y = [dailyRequirementLimitNutrients[x] for x in reqMineralList]
X,y=getXandY(finalFoods,sampleCount,grams,dailyLimitList_Y,reqMineralList)


inputSampleSize=X.shape[0]		# Number of samples
foodCount=X.shape[1]			# no of food items(features) you are giving to find out the optimal
nutrientCount=X.shape[2] 		# how many nutrients you gonna find out	
if firstRun:
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






