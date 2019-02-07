import operator
import functools 
import numpy as np
import pickle
import os
from FoodEngineConstants import *
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
def pickleTopFoodsForEveryNutrition(allFoods):
	nutrient_data=open(foodsWithNutrientDetalsFinalFile,"r").read().split('\n')[1:] #extracts all data from the file.. eliminating the header
	if not allFoods:
		nutrient_data=[x for x in nutrient_data if str(int(x.split('^')[0])) in selectedFoodIds]
	nutrient_data=[x.split("^") for x in nutrient_data ]
	mineralDesc=open(foodsWithNutrientDetalsFinalFile,"r").read().split('\n')[0].split('^')[nutrientStartIndex:] #getting all nutrient names from header
	nutrient_data=np.array([x for x in nutrient_data ])# Filter food items using the wanted food groups
	nutrient_data=np.concatenate((nutrient_data[:,0:1],nutrient_data[:,nutrientStartIndex:]), axis=1).astype("float") #Just taking Id coulumn and nutrient value columns to sort
	dictLi=[]	
	for i in range(1,150):
		temp=nutrient_data[nutrient_data[:,i].argsort()[::-1]]
		dictLi.append(str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join("'{0}'".format(w) for w in temp[:temp.shape[0],[0]].astype('str').reshape(temp.shape[0]).tolist())+'])')
		#print        (str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join('"{0}"'.format(w) for w in rr[:rr.shape[0],[0]].astype('str').reshape(rr.shape[0]).tolist())+']),')
	topNutritiousFood=','.join(dictLi)
	nutrientWiseTopFoods=eval('{'+topNutritiousFood+'}')
	if allFoods:
		with open(topNutritionFoodPickleFileAllFoods,'wb') as picleLoad:
			pickle.dump(nutrientWiseTopFoods,picleLoad)
	else:
		with open(topNutritionFoodPickleFileSelectedFoods,'wb') as picleLoad:
			pickle.dump(nutrientWiseTopFoods,picleLoad)		

def getXandY(inputFoodList, duplicateSampleCount,grams,dailyLimitList,reqMineralList):
	food_items=open(foodsWithNutrientDetalsFinalFile).read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	X=np.array([[[z*float(food_dict[x][y] )*(float(grams))/100 for y in [x1+nutrientStartIndex for x1 in reqMineralList]] for x in inputFoodList] for z in range(1,duplicateSampleCount+1)])
	y=np.array([[x*m for x in dailyLimitList] for m in range (1, duplicateSampleCount+1)])
	return (X,y)

def getExclusionList(nutrientList,limit):
	"""To eliminate unnecessary Foods affect the code. This code will give the top foods of 
	length "limit" for each of the given nutrient in nutrientList that can be used to exclude from
	the final list of foods thats going to be processed	
	"""
	out=[]
	nutrientWiseTopFoods=pickle.load(open(topNutritionFoodPickleFile,'rb'))
	for i in nutrientList:
		out+= [str(int(float(x))) for x in nutrientWiseTopFoods[i][1][:limit]]
	return out

def getTopFoodsForNutrient(allFoods,nurientIndex,length):
	nutrientWiseTopFoods={}
	if(allFoods):
		nutrientWiseTopFoods=pickle.load(open(topNutritionFoodPickleFileAllFoods,'rb'))
	else:
		nutrientWiseTopFoods=pickle.load(open(topNutritionFoodPickleFileSelectedFoods,'rb'))
		
	return (nutrientWiseTopFoods[nurientIndex+1][0],[str(int(float(x))) for x in nutrientWiseTopFoods[nurientIndex+1][1][:length+1]])
		
	
