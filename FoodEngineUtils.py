import operator
import functools 
import numpy as np
import pickle
import os
from FoodEngineConstants import *
from Food_Engine import * 
from Regression import *

def printTopFoodForNutrients(nutrientList,length):
	food_items=open("nutrient_data.txt").read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	nutrientWiseTopFoods=pickle.load(open('topNutritionFood.pickle','rb'))
	for nutrient in nutrientList:
	#for nutrient in nutrientWiseTopFoods:
		print (nutrientWiseTopFoods[nutrient][0])#[0])
		for i in range(1,length):
			foodCode=nutrientWiseTopFoods[nutrient][1][i]
			foodCode=str(int(float(foodCode)))
			print("\t\t"+foodCode+" : "+food_dict[foodCode][3]+" |->|  "+food_dict[foodCode][2])

#Get top foods of given length for each nutrient from pickled dictionary 
def getTopFoodForNutrients(length):
	nutrientWiseTopFoods=pickle.load(open('topNutritionFood.pickle','rb'))
	pickedTopFoods= [nutrientWiseTopFoods[j][1][:length] for j in range(1,35)]
	print(pickedTopFoods)
	finalFoods=list(set([nutrient for food in pickedTopFoods  for nutrient in food]))
	return finalFoods

#This is to pickle all foods in sorted order  
def pickleTopFoodsForEveryNutrition():
	nutrient_data=open("nutrient_data.txt","r").read().split('\n')[1:] #extracts all data from the file.. eliminating the header
	nutrient_data=[x.split("^") for x in nutrient_data ]
	mineralDesc=open("nutrient_data.txt","r").read().split('\n')[0].split('^')[4:] #getting all nutrient names from header
	inclusiveFoodGroups=['0100','0400','0500','0900','1100','1200','1500','1600','1700','2000'] #we are limiting the food groups so eliminating baby foods , fast foods etc
	nutrient_data=np.array([x for x in nutrient_data if x[1] in inclusiveFoodGroups ])# Filter food items using the wanted food groups
	nutrient_data=np.concatenate((nutrient_data[:,0:1],nutrient_data[:,4:]), axis=1).astype("float") #Just taking Id coulumn and nutrient value columns to sort
	dictLi=[]	
	for i in range(1,36):
		temp=nutrient_data[nutrient_data[:,i].argsort()[::-1]]
		dictLi.append(str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join("'{0}'".format(w) for w in temp[:temp.shape[0],[0]].astype('str').reshape(temp.shape[0]).tolist())+'])')
	topNutritiousFood=','.join(dictLi)
	nutrientWiseTopFoods=eval('{'+topNutritiousFood+'}')
	with open('topNutritionFood.pickle','wb') as picleLoad:
		pickle.dump(nutrientWiseTopFoods,picleLoad)

def getXandY(inputFoodList, duplicateSampleCount,grams,dailyLimitList,reqMineralList):
	food_items=open("nutrient_data.txt").read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	X=np.array([[[z*float(food_dict[x][y] )*(float(grams))/100 for y in [x1+4 for x1 in reqMineralList]] for x in inputFoodList] for z in range(1,duplicateSampleCount+1)])
	y=np.array([[x*m for x in dailyLimitList] for m in range (1, duplicateSampleCount+1)])
	return (X,y)

def getExclusionList(nutrientList,limit):
	"""To eliminate unnecessary Foods affect the code. This code will give the top foods of 
	length "limit" for each of the given nutrient in nutrientList that can be used to exclude from
	the final list of foods thats going to be processed	
	"""
	out=[]
	nutrientWiseTopFoods=pickle.load(open(topNutritionFoodPickleFile,'rb'))
	print(nutrientWiseTopFoods.keys())
	for i in nutrientList:
		print('Hi')
		print(nutrientWiseTopFoods[i][0])
		out+= [str(int(float(x))) for x in nutrientWiseTopFoods[i][1][:limit]]
		print('Hello')
	return out

