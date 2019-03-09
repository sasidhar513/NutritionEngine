import operator
import functools 
import numpy as np
import pickle
import copy
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
			#print("For the nutrient " +nutrientsList[reqMineralList[i]]+"\n\tratio is "+
			#str(ratio[i])+"\n\tdifference is "+str(difference[i])+
			#"\n\tComputedTotal is "+str(computedTotal[i])+
			#"\n\trequired is "+str(required[i]))
			addMoreList.append(i)
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

def showAddMoreFoods(nutrientTopFoodsDict,finalFoods):
	looper=True
	while(looper):
		looper1=True
		
		print("Added extra Foods for todays Meal:")
		print(finalFoods)
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+nutrientTopFoodsDict[i][0]+' : '+', '.join(nutrientTopFoodsDict[i][1]))
		print("\nselect nutrients that you need to add, Please enter the number associated with nutrient")
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+str(i)+" for "+nutrientTopFoodsDict[i][0])
		print("\t# to exit application")
		try:
			nutrientKey=int(input())
			if nutrientKey in nutrientTopFoodsDict.keys():
				while(looper1):	
					show_Products(nutrientKey,nutrientTopFoodsDict,nutrientTopFoodsDict[nutrientKey][2])
					food_list=nutrientTopFoodsDict[nutrientKey][2]
					foodKey=int(input())
					if foodKey in range(1,len(food_list)+1):
						nutrientTopFoodsDict[nutrientKey][1].append(nutrientTopFoodsDict[nutrientKey][2][foodKey].split('^')[1].replace(',','')[:25])
						finalFoods.append(nutrientTopFoodsDict[nutrientKey][2][foodKey].split('^')[0])
					else:
						looper1=False					
		except:
			looper=False
			print("You chose to exit or gave wrong Input, Thank you for using this Application")
	return finalFoods

def addMoreFoods(addMoreList,finalFoods):
	nutrientTopFoodsDict={}
	food_items=open(foodsWithNutrientDetalsFinalFile).read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	for i in range(len(addMoreList)):
		topList=[x for x in getTopFoodsForNutrient(False,addMoreList[i],50)[1] if x not in finalFoods]
		dictt={i:topList[i-1]+'^'+food_dict[topList[i-1]][4] for i in range(1,len(topList)+1)}
		nutrientTopFoodsDict.update({i+1:(nutrientsList[addMoreList[i]],[],dictt)})
	finalFoods=showAddMoreFoods(nutrientTopFoodsDict,finalFoods)
	print("$$$$$$$$$$$$$$$$$$$$$$$$$")
	return finalFoods


def foodEngine(foodList,thetaParam):
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
	if thetaParam.tolist():
		theta=thetaParam
	
	elif firstRun or foodList:
		theta= np.array([[i]*nutrientCount for i in np.random.rand(foodCount)])
		#try:
			#os.remove(thetaFile)
			#os.remove(costFile)
		#except OSError:
			#pass
	else:	
		theta=np.array(eval(open(thetaFile,'r').read()))
		priviousCost=eval(open(costFile,'r').read())
	for i in range(iterations):
		gradientDescent(X,y,theta)
		print(str(i)+" cost",computeCost(X, theta,y))
		if priviousCost>=computeCost(X, theta,y):
			priviousCost=computeCost(X, theta,y)
			if i%999==0 and computeCost(X, theta,y)<=priviousCost :
				print("coming thereds####################")
				open(thetaFile,'w').write(str(theta.tolist()))
				open(costFile,'w').write(str(priviousCost))
				open(inputFile,'w').write(','.join(finalFoods))
	display_output(X,y,theta,finalFoods,grams,dailyLimitList_Y,reqMineralList)
	if getAddMoreList(X,y,theta):
		initialCopy=copy.deepcopy(finalFoods)
		finalFoods=addMoreFoods(getAddMoreList(X,y,theta),finalFoods)
		appendTheta=np.array([[i]*nutrientCount for i in np.random.rand(len(finalFoods)-len(initialCopy))])
		theta=np.concatenate((theta,appendTheta),axis=0)
		foodEngine(finalFoods,theta)
		

			
		

		
foodEngine([],np.array([[i]*0 for i in np.random.rand(0)]))	
	



