import operator
import functools 
import numpy as np
import pickle
import os
import constants
import regression
import codecs
import console
import copy

			

#This is to pickle all foods in sorted order  
def pickle_top_foods_for_each_nutrient(pickle_all_foods = True):
	"""
	
	"""
	with open(constants.NUTRIENT_DETAILS_FILE, 'r', encoding = 'ISO-8859-1') \
			as nutrient_data_file:
		nutrient_data = nutrient_data_file.read().split('\n')[1:] 
	if not pickle_all_foods:
		nutrient_data = [x for x in nutrient_data if str(int(x.split('^')[0])) in constants.SELECTED_FOOD_IDS]
	nutrient_data = [x.split("^") for x in nutrient_data ]
	with open(constants.NUTRIENT_DETAILS_FILE, 'r', encoding = 'ISO-8859-1') \
			as nutrient_data_file:
		mineralDesc = 
			nutrient_data_file
			.read()
			.split('\n')[0]
			.split('^')[constants.NUTRIENT_START_INDEX:-1] 
	nutrient_data = np.array([x for x in nutrient_data ])
	nutrient_data = np.concatenate(
		(
			nutrient_data[:,0:1],
			nutrient_data[:,constants.NUTRIENT_START_INDEX:-1]
		),
		axis = 1
	)
	nutrient_data[nutrient_data=='']='0'
	nutrient_data = nutrient_data.astype("float")
	dictLi = []	
	for i in range(1,150):
		temp = nutrient_data[nutrient_data[:,i].argsort()[::-1]]
		dictLi.append(str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join('"{0}"'.format(w) for w in temp[:temp.shape[0],[0]].astype('str').reshape(temp.shape[0]).tolist())+'])')
	topNutritiousFood = ','.join(dictLi)
	nutrientWiseTopFoods = eval('{'+topNutritiousFood+'}')
	if pickle_all_foods:
		with open(constants.TOP_ALL_FOODS_PER_NUTRIENT_FILE,'wb') as picleLoad:
			pickle.dump(nutrientWiseTopFoods,picleLoad)
	else:
		with open(constants.TOP_SELECTED_FOODS_PER_NUTRIENT_FILE,'wb') as picleLoad:
			pickle.dump(nutrientWiseTopFoods,picleLoad)	
			
def build_x_and_y(inputFoodList, duplicateSampleCount,grams,dailyLimitList,reqMineralList):
	avg = sum(dailyLimitList)/len(dailyLimitList)
	normalizeList = [avg/x  if x > 0 else 1 for x in dailyLimitList]
	dailyLimitList = [normalizeList[i]*dailyLimitList[i] for i in range(len(normalizeList))]
	food_items = list([])
	with codecs.open(constants.NUTRIENT_DETAILS_FILE, 'r', encoding = 'utf-8', errors = 'ignore') as fdata:
		food_items = fdata.read().split('\n')[1:]
	food_items = [food_item.split("^") for food_item in food_items]
	food_dict = {}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	x = np.array([[[z*float(food_dict[x][y] )*(float(grams))/100 for y in [x1+constants.NUTRIENT_START_INDEX for x1 in reqMineralList]] for x in inputFoodList] for z in range(1,duplicateSampleCount+1)])
	x = x*normalizeList
	y = np.array([[x*m for x in dailyLimitList] for m in range (1, duplicateSampleCount+1)])
	return (x,y,normalizeList)



def getTopFoodsForNutrient(allFoods,index,length):
	nutrientWiseTopFoods = {}
	if(allFoods):
		nutrientWiseTopFoods = pickle.load(open(constants.TOP_ALL_FOODS_PER_NUTRIENT_FILE,'rb'))
	else:
		nutrientWiseTopFoods = pickle.load(open(constants.TOP_SELECTED_FOODS_PER_NUTRIENT_FILE,'rb'))
	return (nutrientWiseTopFoods[index+1][0],[str(int(float(x))) for x in nutrientWiseTopFoods[index+1][1][:length+1]])


def getAddMoreList(x,y,theta):
	dtProduct = regression.dot_product(x,theta)
	required = y[0]
	computedTotal = dtProduct[0]
	ratio = (y/dtProduct).tolist()[0]
	difference = (y-dtProduct).tolist()[0]
	addMoreList = []
	
	for i in range(len(ratio)):
		if (ratio[i]>2 or difference[i]>50):
			addMoreList.append(i)
	return [constants.REQUIRED_NUTRIENT_LIST[x] for x in addMoreList]

 
def getRemoveExistingFoodsList(x,y,theta):
	dtProduct = regression.dot_product(x,theta)
	required = y[0]
	computedTotal = dtProduct[0]
	ratio = (y/dtProduct).tolist()[0]
	difference = (y-dtProduct).tolist()[0]	
	removeExisting = []	
	for i in range(len(ratio)):
		if(ratio[i]<0.5 or  difference[i]<(-50)):
			removeExisting.append(i);
	return [constants.REQUIRED_NUTRIENT_LIST[x] for x in removeExisting]


def showAddMoreFoods(nutrientTopFoodsDict,finalFoods):
	looper = True
	while(looper):
		looper1 = True		
		print("Added extra Foods for todays Meal:")
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+nutrientTopFoodsDict[i][0]+' : '+', '.join(nutrientTopFoodsDict[i][1]))
		print("\nselect nutrients that you need to add, Please enter the number associated with nutrient")
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+str(i)+" for "+nutrientTopFoodsDict[i][0])
		print("\t# to exit application")
		try:
			nutrientKey = int(input())
			if nutrientKey in nutrientTopFoodsDict.keys():
				while(looper1):	
					console.show_Products(nutrientKey,nutrientTopFoodsDict,nutrientTopFoodsDict[nutrientKey][2])
					food_list = nutrientTopFoodsDict[nutrientKey][2]
					foodKey = int(input())
					if foodKey in range(1,len(food_list)+1):
						nutrientTopFoodsDict[nutrientKey][1].append(nutrientTopFoodsDict[nutrientKey][2][foodKey].split('^')[1].replace(',','')[:25])
						finalFoods.append(nutrientTopFoodsDict[nutrientKey][2][foodKey].split('^')[0])
					else:
						looper1 = False					
		except Exception as e:
			looper = False
			print("You chose to exit or gave wrong Input, Thank you for using this Application"+str(e))
	return finalFoods


def showDeleteFoods(nutrientTopFoodsDict,finalFoods):
	looper = True
	while(looper):
		looper1 = True		
		print("Foods That need to be removed:")
		print(finalFoods)
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+nutrientTopFoodsDict[i][0]+' : '+', '.join(nutrientTopFoodsDict[i][1]))
		print("\nselect nutrients that you need to remove, Please enter the number associated with nutrient")
		for i in nutrientTopFoodsDict.keys() :
			print('\t'+str(i)+" for "+nutrientTopFoodsDict[i][0])
		print("\t# to exit application")
		try:
			nutrientKey = int(input())
			if nutrientKey in nutrientTopFoodsDict.keys():
				while(looper1):	
					console.show_Products(nutrientKey,nutrientTopFoodsDict,nutrientTopFoodsDict[nutrientKey][2])
					food_list = nutrientTopFoodsDict[nutrientKey][2]
					foodKey = int(input())
					if foodKey in range(1,len(food_list)+1):
						nutrientTopFoodsDict[nutrientKey][1].append(nutrientTopFoodsDict[nutrientKey][2][foodKey].split('^')[1].replace(',','')[:25])
						finalFoods.append(nutrientTopFoodsDict[nutrientKey][2][foodKey].split('^')[0])
					else:
						looper1 = False					
		except:
			looper = False
			print("You chose to exit or gave wrong Input, Thank you for using this Application")
	return list(set(finalFoods))


def addMoreFoods(addMoreList,finalFoods):
	nutrientTopFoodsDict = {}
	with open(constants.NUTRIENT_DETAILS_FILE,'r', encoding = 'ISO-8859-1') as nutrient_details_file:
		food_items = nutrient_details_file.read().split('\n')[1:]
	#food_items = open(constants.NUTRIENT_DETAILS_FILE).read().split('\n')[1:]
	food_items = [food_item.split("^") for food_item in food_items]
	food_dict = {}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	for i in range(len(addMoreList)):
		topList = [x for x in getTopFoodsForNutrient(False,addMoreList[i],50)[1] if x not in finalFoods]
		dictt = {i:topList[i-1]+'^'+food_dict[topList[i-1]][4] for i in range(1,len(topList)+1)}
		nutrientTopFoodsDict.update({i+1:(constants.NUTRIENT_LIST[addMoreList[i]],[],dictt)})
	finalFoods = showAddMoreFoods(nutrientTopFoodsDict,finalFoods)
	return finalFoods

def removeExistingFoods(removeExistingList,finalFoods):
	nutrientTopFoodsDict = {}
	with open(constants.NUTRIENT_DETAILS_FILE,'r',encoding = 'ISO-8859-1') as nutrient_details_file:
		food_items = nutrient_details_file.read().split('\n')[1:]
	#food_items = open(constants.NUTRIENT_DETAILS_FILE).read().split('\n')[1:]
	food_items = [food_item.split("^") for food_item in food_items]
	food_dict = {}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	for i in range(len(removeExistingList)):
		topList = [x for x in getTopFoodsForNutrient(False,removeExistingList[i],300)[1] if x in finalFoods]
		dictt = {i:topList[i-1]+'^'+food_dict[topList[i-1]][4] for i in range(1,len(topList)+1)}
		nutrientTopFoodsDict.update({i+1:(constants.NUTRIENT_LIST[removeExistingList[i]],[],dictt)})
	removeFoods = showDeleteFoods(nutrientTopFoodsDict,[])
	return removeFoods


def add_or_remove_foods(x,y,theta,finalFoods):
	print(
		"Please analyse the output in " + constants.OUTPUT_FILE
		+ "\n"
		+ "Select one of the below items"
		+ "\n\n\t"
		+ "1 For Adding a Food yourself"
		+ "\n\t"
		+ "2 for Adding system analysed Foods"
		+ "\n\t"
		+ "3 for Removing a food item"
		+ "\n\t"
		+ "4 for Removing system analysed Foods"
		+ "\n\t"
		+ "5 for removing Zero weight foods"
		+ "\n\t"
		+ "6 for Running with specific Iterations"
		+ "\n\t"
		+ "# To Continue with previous items"
	)
	try:
		option = int(input())
		if option == 1:
			print(
				"Enter the comma seperated food item IDs that needed to be added. "
				+ "for example\n\t11080,11215"
			)
			newFoods = [
				x.strip() 
				for x in input().strip().split(',') 
				if x not in finalFoods
			]
			if len(newFoods)>0:
				appendTheta = np.array(
					[[i]*x.shape[2] for i in np.random.rand(len(newFoods))]
				)
				theta = np.concatenate((theta,appendTheta),axis = 0)			   
				finalFoods = finalFoods+newFoods
				return (finalFoods,theta,0)
			else:
				print("No food item to add")
				return None
		elif option == 2:
			if getAddMoreList(x,y,theta):
				initialCopy = copy.deepcopy(finalFoods)
				finalFoods = addMoreFoods(getAddMoreList(x,y,theta),finalFoods)
				if len(finalFoods)-len(initialCopy) >0:
					appendTheta = np.array(
						[
							[i]*x.shape[2] 
							for i in np.random.rand(len(finalFoods)-len(initialCopy))
						]
					)
					theta = np.concatenate((theta,appendTheta),axis = 0)
					return(finalFoods,theta,0)
				else:
					print("No food items to Add based on Analysis")
					return None
		elif option == 3:
			print(
				"Enter the comma seperated food item IDs that needed to be deleted."
				+ "for example\n\t11080,11215"
			)
			removeFoods = list(
				set(
					[x.strip() for x in str(input()).strip().split(',') if x in finalFoods]
				)
			)
			if len(removeFoods)>0:
				for food in removeFoods:
					indx = finalFoods.index(food)
					finalFoods.remove(food)
					theta = np.delete(theta, indx, axis = 0)
				return(finalFoods,theta,0)
			else :
				print("No food items to delete")
				return None
		elif option == 4: 
			if getRemoveExistingFoodsList(x,y,theta):
				removeFoods = removeExistingFoods(
					getRemoveExistingFoodsList(x,y,theta),
					finalFoods
				)
				if len(removeFoods) >0:
					for food in removeFoods:
						indx = finalFoods.index(food)
						finalFoods.remove(food)
						theta = np.delete(theta, indx, axis = 0)
					return (finalFoods,theta,0)
				else :
					print("No food items to delete based on Analysis")
					return None
		elif option == 5:
			while(True):
				thetaList = theta[:,0].tolist()
				try:
					indx = thetaList.index(0.0)
					food = finalFoods[indx]
					finalFoods.remove(food)
					theta = np.delete(theta, indx, axis = 0)
				except:
					break
			return (finalFoods,theta,0)	
		elif option == 6:
			print("Enter the reqired iterations")
			iters = int(input())
			if iters>0:
				return (finalFoods,theta,iters)
			else:
				return (finalFoods,theta,0)		
		else:
			print("Invalid option. Thanks for suing this Application.")
			return None
	except Exception as e:
		looper = False
		print("You chose to exit or gave wrong Input, "
			  + "Thank you for using this Application\nThe exception is \n"+ str(e))
		return (finalFoods,theta,0)
