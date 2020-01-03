import operator
import functools 
import numpy as np
import pickle
import os
from FoodEngineConstants import *
import regression
import codecs

from Console import *
import copy

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
	finalFoods=list(set([nutrient for food in pickedTopFoods  for nutrient in food]))
	return finalFoods


#This is to pickle all foods in sorted order  
def pickleTopFoodsForEveryNutrition(allFoods):
	nutrient_data=open(foodsWithNutrientDetalsFinalFile,"r").read().split('\n')[1:] #extracts all data from the file.. eliminating the header
	if not allFoods:
		nutrient_data=[x for x in nutrient_data if str(int(x.split('^')[0])) in SELECTED_FOOD_IDS]
	nutrient_data=[x.split("^") for x in nutrient_data ]
	mineralDesc=open(foodsWithNutrientDetalsFinalFile,"r").read().split('\n')[0].split('^')[NUTRIENT_START_INDEX:] #getting all nutrient names from header
	nutrient_data=np.array([x for x in nutrient_data ])# Filter food items using the wanted food groups
	nutrient_data=np.concatenate((nutrient_data[:,0:1],nutrient_data[:,NUTRIENT_START_INDEX:]), axis=1).astype("float") #Just taking Id coulumn and nutrient value columns to sort
	dictLi=[]	
	for i in range(1,150):
		temp=nutrient_data[nutrient_data[:,i].argsort()[::-1]]
		dictLi.append(str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join('"{0}"'.format(w) for w in temp[:temp.shape[0],[0]].astype('str').reshape(temp.shape[0]).tolist())+'])')
		#print        (str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join('"{0}"'.format(w) for w in rr[:rr.shape[0],[0]].astype('str').reshape(rr.shape[0]).tolist())+']),')
	topNutritiousFood=','.join(dictLi)
	nutrientWiseTopFoods=eval('{'+topNutritiousFood+'}')
	if allFoods:
		with open(TOP_ALL_FOODS_PER_NUTRIENT_FILE,'wb') as picleLoad:
			pickle.dump(nutrientWiseTopFoods,picleLoad)
	else:
		with open(TOP_SELECTED_FOODS_PER_NUTRIENT_FILE,'wb') as picleLoad:
			pickle.dump(nutrientWiseTopFoods,picleLoad)		

			
def build_x_and_y(inputFoodList, duplicateSampleCount,GRAMS,dailyLimitList,reqMineralList):
	avg=sum(dailyLimitList)/len(dailyLimitList)
	normalizeList=[avg/x  if x > 0 else 1 for x in dailyLimitList]
	dailyLimitList=[normalizeList[i]*dailyLimitList[i] for i in range(len(normalizeList))]
	food_items = list([])
	with codecs.open(foodsWithNutrientDetalsFinalFile, 'r', encoding='utf-8', errors='ignore') as fdata:
		food_items=fdata.read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	x=np.array([[[sz*float(food_dict[x][y] )*(float(GRAMS))/100 for y in [x1+NUTRIENT_START_INDEX for x1 in reqMineralList]] for x in inputFoodList] for z in range(1,duplicateSampleCount+1)])
	x=X*normalizeList
	y=np.array([[x*m for x in dailyLimitList] for m in range (1, duplicateSampleCount+1)])
	return (x,y,normalizeList)


def getExclusionList(nutrientList,limit):
	"""To eliminate unnecessary Foods affect the code. This code will give the top foods of 
	length "limit" for each of the given nutrient in nutrientList that can be used to exclude from
	the final list of foods thats going to be processed	
	"""
	out=[]
	nutrientWiseTopFoods=pickle.load(open(TOP_ALL_FOODS_PER_NUTRIENT_FILE,'rb'))
	for i in nutrientList:
		out+= [str(int(float(x))) for x in nutrientWiseTopFoods[i][1][:limit]]
	return out


def getTopFoodsForNutrient(allFoods,index,length):
	nutrientWiseTopFoods={}
	if(allFoods):
		nutrientWiseTopFoods=pickle.load(open(TOP_ALL_FOODS_PER_NUTRIENT_FILE,'rb'))
	else:
		nutrientWiseTopFoods=pickle.load(open(TOP_SELECTED_FOODS_PER_NUTRIENT_FILE,'rb'))
	return (nutrientWiseTopFoods[index+1][0],[str(int(float(x))) for x in nutrientWiseTopFoods[index+1][1][:length+1]])


def getAddMoreList(x,y,theta):
	dtProduct=regression.dot_product(x,theta)
	required=y[0]
	computedTotal=dtProduct[0]
	ratio=(y/dtProduct).tolist()[0]
	difference=(y-dtProduct).tolist()[0]
	addMoreList=[]
	
	for i in range(len(ratio)):
		if (ratio[i]>2 or difference[i]>50):
			addMoreList.append(i)
	return [reqMineralList[x] for x in addMoreList]

 
def getRemoveExistingFoodsList(x,y,theta):
	dtProduct=regression.dot_product(x,theta)
	required=y[0]
	computedTotal=dtProduct[0]
	ratio=(y/dtProduct).tolist()[0]
	difference=(y-dtProduct).tolist()[0]	
	removeExisting=[]	
	for i in range(len(ratio)):
		if(ratio[i]<0.5 or  difference[i]<(-50)):
			removeExisting.append(i);
	return [reqMineralList[x] for x in removeExisting]


def showAddMoreFoods(nutrientTopFoodsDict,finalFoods):
	looper=True
	while(looper):
		looper1=True		
		print("Added extra Foods for todays Meal:")
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


def showDeleteFoods(nutrientTopFoodsDict,finalFoods):
	looper=True
	while(looper):
		looper1=True		
		print("Foods That need to be removed:")
		print(finalFoods)
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+nutrientTopFoodsDict[i][0]+' : '+', '.join(nutrientTopFoodsDict[i][1]))
		print("\nselect nutrients that you need to remove, Please enter the number associated with nutrient")
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
	return list(set(finalFoods))


def addMoreFoods(addMoreList,finalFoods):
	nutrientTopFoodsDict={}
	food_items=open(foodsWithNutrientDetalsFinalFile).read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	for i in range(len(addMoreList)):
		topList=[x for x in getTopFoodsForNutrient(False,addMoreList[i],50)[1] if x not in finalFoods]
		dictt={i:topList[i-1]+'^'+food_dict[topList[i-1]][4] for i in range(1,len(topList)+1)}
		nutrientTopFoodsDict.update({i+1:(NUTRIENT_LIST[addMoreList[i]],[],dictt)})
	finalFoods=showAddMoreFoods(nutrientTopFoodsDict,finalFoods)
	return finalFoods

def removeExistingFoods(removeExistingList,finalFoods):
	nutrientTopFoodsDict={}
	food_items=open(foodsWithNutrientDetalsFinalFile).read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	for i in range(len(removeExistingList)):
		topList=[x for x in getTopFoodsForNutrient(False,removeExistingList[i],300)[1] if x in finalFoods]
		dictt={i:topList[i-1]+'^'+food_dict[topList[i-1]][4] for i in range(1,len(topList)+1)}
		nutrientTopFoodsDict.update({i+1:(NUTRIENT_LIST[removeExistingList[i]],[],dictt)})
	removeFoods=showDeleteFoods(nutrientTopFoodsDict,[])
	return removeFoods


def add_or_remove_foods(x,y,theta,finalFoods):
	print("Please analyse the output in "+OUTPUT_FILE+"\nand Select one of the below items\n\n\t1 for Adding a Food myself\n\t2 for Adding system analysed Foods\n\t3 for Removing a food item\n\t4 for Removing system analysed Foods\n\t5 for removing Zero weight foods\n\t6 for Running with specific Iterations\n\t# To Continue with previous items")
	try:
		option=int(input())
		if option == 1:
			print("Enter the comma seperated food item IDs that needed to be added. for example\n\t11080,11215")
			newFoods=[x.strip() for x in raw_input().strip().split(',') if x not in finalFoods]
			if len(newFoods)>0:
				appendTheta=np.array([[i]*x.shape[2] for i in np.random.rand(len(newFoods))])
				theta=np.concatenate((theta,appendTheta),axis=0)			   
				finalFoods=finalFoods+newFoods
				return (finalFoods,theta,0)
			else:
				print("No food item to add")
				return None
		elif option == 2:
			if getAddMoreList(x,y,theta):
				initialCopy=copy.deepcopy(finalFoods)
				finalFoods=addMoreFoods(getAddMoreList(x,y,theta),finalFoods)
				if len(finalFoods)-len(initialCopy) >0:
					appendTheta=np.array([[i]*x.shape[2] for i in np.random.rand(len(finalFoods)-len(initialCopy))])
					theta=np.concatenate((theta,appendTheta),axis=0)
					return(finalFoods,theta,0)
				else:
					print("No food items to Add based on Analysis")
					return None
		elif option == 3:
			print("Enter the comma seperated food item IDs that needed to be deleted. for example\n\t11080,11215")
			removeFoods=list(set([x.strip() for x in str(raw_input()).strip().split(',') if x in finalFoods]))
			if len(removeFoods)>0:
				for food in removeFoods:
					indx=finalFoods.index(food)
					finalFoods.remove(food)
					theta=np.delete(theta, indx, axis=0)
				return(finalFoods,theta,0)
			else :
				print("No food items to delete")
				return None
		elif option == 4: 
			if getRemoveExistingFoodsList(x,y,theta):
				removeFoods=removeExistingFoods(getRemoveExistingFoodsList(x,y,theta),finalFoods)
				if len(removeFoods) >0:
					for food in removeFoods:
						indx=finalFoods.index(food)
						finalFoods.remove(food)
						theta=np.delete(theta, indx, axis=0)
					return (finalFoods,theta,0)
				else :
					print("No food items to delete based on Analysis")
					return None
		elif option == 5:
			while(True):
				thetaList=theta[:,0].tolist()
				try:
					indx=thetaList.index(0.0)
					food=finalFoods[indx]
					finalFoods.remove(food)
					theta=np.delete(theta, indx, axis=0)
				except:
					break
			return (finalFoods,theta,0)
	
		elif option == 6:
			print("Enter the reqired iterations")
			iters=int(input())
			if iters>0:
				return (finalFoods,theta,iters)
			else:
				return (finalFoods,theta,0)
				
				
			
			
		else:
			print("Invalid option. Thanks for suing this Application.")
			return None
	except:
		looper=False
		#print("You chose to exit or gave wrong Input, Thank you for using this Application")
		return (finalFoods,theta,0)
