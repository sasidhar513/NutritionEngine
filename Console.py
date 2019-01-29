from FoodEngineConstants import *
from Regression import *
from FoodEngineUtils import *

def show_Products(groupkey,selectedFoods,productDict):
	print('\n')
	print("daad")
	for i in range ( len(productDict)/3):
		 print ("{0:<3}".format(str(3*i+1))+' for '+"{0:<25}".format(productDict[3*i+1].split('^')[1][:25])+'  |  '+"{0:<3}".format(str(3*i+2))+' for '+"{0:<25}".format(productDict[3*i+2].split('^')[1][:25])	+'  |  '+"{0:<3}".format(str(3*i+3))+' for '+"{0:<25}".format(productDict[3*i+3].split('^')[1][:25])) 
	if len(productDict)%3==2:
		print ("{0:<3}".format(str(len(productDict)-1))+' for '+"{0:<25}".format(productDict[len(productDict)-1].split('^')[1][:25])+'  |  '+"{0:<3}".format(str(len(productDict)))+' for '+"{0:<25}".format(productDict[len(productDict)].split('^')[1][:25]))
	if len(productDict)%3==1:
		print("{0:<3}".format(str(len(productDict)))+' for '+"{0:<25}".format(productDict[len(productDict)].split('^')[1][:25]))
	print(str(len(productDict))+' for previous menu')
	print("# to exit application")

def display_output(X,y,theta,finalFoods,grams,dailyLimitList_Y,reqMineralList):
	food_items=open("nutrient_data.txt").read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(int(food_item[0])): food_item}) for food_item in food_items]
	requiredMineralNames=[nutrientNames[i] for i in reqMineralList]
	outputDoubleArray=[]
	outputDoubleArray.append(['Food Name','ID','weight']+requiredMineralNames)
	outputDoubleArray.append(['-'*27,'-'*12,'-'*12]+['-'*12]*len(requiredMineralNames))
	for looper3 in range(len(finalFoods)):
		foodName=food_dict[finalFoods[looper3]][3]
		weight=theta[:,1][looper3]*100
		id=finalFoods[looper3]
		reqNutrientValues=[float(food_dict[finalFoods[looper3]][y1] )*(float(weight/100)) for y1 in [x+4 for x in reqMineralList]]
		outputDoubleArray.append([foodName,id,weight]+reqNutrientValues)

	outputDoubleArray.append(['-'*27,'-'*12,'-'*12]+['-'*12]*len(requiredMineralNames))
	outputDoubleArray.append(['Total','','']+dotProduct(X,theta).tolist()[0])
	outputDoubleArray.append(['-'*27,'-'*12,'-'*12]+['-'*12]*len(requiredMineralNames))
	outputDoubleArray.append(['Required','','']+y.tolist()[0])
	outputDoubleArray.append(['-'*27,'-'*12,'-'*12]+['-'*12]*len(requiredMineralNames))
	outputDoubleArray.append(['Difference','','']+((y-dotProduct(X,theta)).tolist()[0]))
	outputDoubleArray.append(['-'*27,'-'*12,'-'*12]+['-'*12]*len(requiredMineralNames))
	for row in outputDoubleArray:
		outRow=''
		outRow+="{0:<27}".format(row[0][:25])+"{0:<12}".format(row[1][:10])+"{0:<12}".format(str(row[2])[:10])
		for index in range(3,len(row)):
			outRow+="{0:<12}".format(str(row[index])[:10])
		print(outRow)
#foodGroupFunctionMapperDict={1: showCereal_Grains, 2: showVegetables,3: showLegume_Products,4:showFats_And_Oils,5:showSpices,6:showDairy_And_Egg_Products, 7:showFruits, 8:showMeat_Products}

def showFoodGroups():
	finalFoods=[]
	looper=True
	while(looper):
		looper1=True
		print("selected Foods for todays Meal:")
		print(finalFoods)
		for i in selectedFoods.keys() :
			print('\t'+selectedFoods[i][0]+' : '+', '.join(selectedFoods[i][1]))
		print("\nselect FoodGroup: press")
		for i in selectedFoods.keys() :
			print('\t'+str(i)+" for "+selectedFoods[i][0])
		print("\t# to exit application")
		try:
			groupkey=int(input())
			if groupkey in range(1,9):
				while(looper1):	
					show_Products(groupkey,selectedFoods,selectedFoods[groupkey][2])
					food_dict=selectedFoods[groupkey][2]
					foodKey=int(input())
					if foodKey in range(1,len(food_dict)):
						selectedFoods[groupkey][1].append(selectedFoods[groupkey][2][foodKey].split('^')[1].replace(',','')[:25])
						finalFoods.append(selectedFoods[groupkey][2][foodKey].split('^')[0])
					else:
						looper1=False					
		except:
			looper=False
			print("You chose to exit or gave wrong Input, Thank you for using this Application")
		return finalFoods

