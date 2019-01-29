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

#finalFoods=[str(int(float(food))) for food in  [topFoodsForANutrient for topFoodsForANutrient in getTopFoodForNutrients(TopFoodsForEachVitaminCount)]if food not in exclusionList]+addList
finalFoods=showFoodGroups()
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




