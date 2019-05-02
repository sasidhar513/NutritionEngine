#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
	NutritionEngine: This script is used to determine ideal weights of suitable foods,
	So that our nutritional requirement is satisfied
	Uses: Linear Regression, Gradient Descent for cost optimization
	Try the below example and follow the console.:
			$ python example_google.py
			
	Todo:
		* Lower price selection of foods to get all nutrition in optimal price
		* Improving the performance of existing cost reduction function.
		
   	http://www.nutremo.com
	http://www.nutremo.in
"""

import operator
import functools 
import pickle
import copy
import os
import sys

import numpy as np

from FoodEngineConstants import *
from Console import *
from FoodEngineUtils import * 

np.set_printoptions(suppress=True)  # To not use exponential notation of the numbers	





def foodEngine(foodList,thetaParam,iters):
	global priviousCost
	finalFoods=[]

	if iters<=0:
		iters=iterations
	
	if foodList:
		finalFoods=foodList		
	elif firstRun:
		finalFoods=showFoodGroups()
		open(inputFile,'w').write(','.join(finalFoods))		
	else:
		finalFoods=open(inputFile,'r').read().split('\n')[0].split(',')	
		
	dailyLimitList_Y = [dailyRequirementLimitNutrients[x] for x in reqMineralList]
	X,y,normalizeList=getXandY(finalFoods,sampleCount,grams,dailyLimitList_Y,reqMineralList)
	inputSampleSize=X.shape[0]		# Number of samples
	foodCount=X.shape[1]			# no of food items(features) you are giving to find out the optimal
	nutrientCount=X.shape[2] 		# how many nutrients you gonna find out	
	
	if thetaParam.tolist():
		theta=thetaParam	
	elif firstRun or foodList:
		theta= np.array([[i]*nutrientCount for i in np.random.rand(foodCount)])
	else:	
		theta=np.array(eval(open(thetaFile,'r').read()))
		priviousCost=eval(open(costFile,'r').read())
		
	for i in range(iters):
		gradientDescent(X,y,theta)
		print(str(i)+" Normalized cost",computeCost(X, theta,y),"||||","Original Cost", computeCost(X/normalizeList,theta,y/normalizeList) )
		if priviousCost>=computeCost(X, theta,y):
			priviousCost=computeCost(X, theta,y)
			if i%99==0 and computeCost(X, theta,y)<=priviousCost :
				open(thetaFile,'w').write(str(theta.tolist()))
				open(costFile,'w').write(str(priviousCost))
				open(inputFile,'w').write(','.join(finalFoods))
	display_output_normalized(X,y,theta,finalFoods,grams,dailyLimitList_Y,reqMineralList,normalizeList)
	display_output(X/normalizeList,y/normalizeList,theta,finalFoods,grams,dailyLimitList_Y,reqMineralList)
	
	output=add_or_remove_foods(X,y,theta,finalFoods)
	if output:
		foodEngine(output[0],output[1],output[2])
			
		

inputList="4047,4513,12108,1145,12115,12104,4602,12117,2043,1045,1229,17005,4536,2011,2042,1116,1230,1211,1117,2030,9144,1175,20008,2014,5062,20011,12087,9079,2009,12119,2005,2004,1125,20647,15265,20648,1123,1118,2046,12151,16085,2027,12014,2010,9542,11215,9087,11362,9040,9326,16144,20031,5053,5080,16130,5023,5027,5025,5137,5020,5011,20035,4593,4589,4584,4583,5105,9033,5332,9021,9145,20028,9139,9132,9111,9110,9107,9094,9089,20029,9078,9077,9070,9061,9060,9050,9042,9037,4531,20038,4055,4529,2002,2019,2018,20066,20067,20075,2006,20080,20090,20105,2024,20118,20124,20130,20131,20140,1124,20314,20316,2022,2025,4514,2065,20040,4058,9150,4053,20058,4042,4037,2069,2050,2028,2047,2044,20061,20062,2037,2033,20064,2029,9148,9165,9159,11304,12131,12120,16135,16157,16167,16426,12100,20004,12061,12036,12023,12021,12006,11696,11670,11620,11601,11457,11429,12142,12147,12154,16056,16112,16108,16101,16087,16080,16078,16076,16062,16027,12155,16022,16133,15004,15003,15002,15001,12220,12174,11422,11282,9163,11278,9302,9298,9297,9292,9286,9279,9266,9260,9252,9246,9236,9226,9218,9200,9190,9184,9176,16115,9164,20012,9311,9313,11124,11270,11260,11253,11233,11216,11209,11205,11165,11109,9316,11090,11080,11052,11003,9500,9421,9322,9321,9307".split(',')
if  firstRun:
	weight=input("enter your weight\n")
	print("Select required calories.")
	calories=int(input())
	print("select required Carbohydrates. Ideal percentage -> 45%  to  60%")
	carbPercentage=int(input())
	print("select required Protein percentage. Ideal percentage -> 10% to 35%")
	proteinPecentage=int(input())
	fatPecentage=100-carbPercentage-proteinPecentage

	carbAmt=(carbPercentage/100.0)*calories
	protAmt=(proteinPecentage/100.0)*calories
	fatAmt=((100-carbPercentage-proteinPecentage)/100.0)*calories

	if carbPercentage+proteinPecentage> 95.0 :
		Print("Please enter correct percentages next time you use the App.")
		sys.exit()

	print(carbAmt/4.0, protAmt/4.0, fatAmt/9.0)
	dailyRequirementLimitNutrients[71]=calories
	dailyRequirementLimitNutrients[110]=protAmt/4.0
	dailyRequirementLimitNutrients[61]=carbAmt/4.0
	dailyRequirementLimitNutrients[130]=fatAmt/4.0
	dailyRequirementLimitNutrients[74]=(((min(fatPecentage,8))/100.0)*calories)/9.0

	dailyRequirementLimitNutrients[89] =(weight*14)/1000.0
	dailyRequirementLimitNutrients[92] =(weight*19)/1000.0
	dailyRequirementLimitNutrients[94] =(weight*42)/1000.0
	dailyRequirementLimitNutrients[97] =(weight*38)/1000.0
	dailyRequirementLimitNutrients[102]=(weight*19)/1000.0
	dailyRequirementLimitNutrients[105]=(weight*33)/1000.0
	dailyRequirementLimitNutrients[122]=(weight*20)/1000.0
	dailyRequirementLimitNutrients[131]=(weight*5)/1000.0
	dailyRequirementLimitNutrients[133]=(weight*24)/1000.0



	print(protAmt/4.0)
	for i in reqMineralList:
		print("{0:<50}".format(nutrientsList[i][:35])+"{0:<20}".format(dailyRequirementLimitNutrients[i]))
		print("-"*75)
	dailyRequirementLimitNutrientsOut=[str(x) for x in dailyRequirementLimitNutrients]
	open(dailyRequirementLimitNutrientsFile,'w').write(','.join(dailyRequirementLimitNutrientsOut))
	foodEngine(inputList,np.array([[i]*0 for i in np.random.rand(0)]),0)	
else:	
	dailyRequirementLimitNutrients=	[float(x) for x in open(dailyRequirementLimitNutrientsFile,'r').read().split(',')]
	foodEngine([],np.array([[i]*0 for i in np.random.rand(0)]),0)	









