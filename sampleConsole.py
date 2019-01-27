from FoodEngineConstants import *

def show_Products(groupkey,selectedFoods,productDict):
	print('\n')
	for i in range ( len(productDict)/3):
		 print ("{:<3}".format(str(3*i+1))+' for '+"{:<25}".format(productDict[3*i+1].split('^')[1][:25])+'  |  '+"{:<3}".format(str(3*i+2))+' for '+"{:<25}".format(productDict[3*i+2].split('^')[1][:25])	+'  |  '+"{:<3}".format(str(3*i+3))+' for '+"{:<25}".format(productDict[3*i+3].split('^')[1][:25])) 
	if len(productDict)%3==2:
		print ("{:<3}".format(str(len(productDict)-1))+' for '+"{:<25}".format(productDict[len(productDict)-1].split('^')[1][:25])+'  |  '+"{:<3}".format(str(len(productDict)))+' for '+"{:<25}".format(productDict[len(productDict)].split('^')[1][:25]))
	if len(productDict)%3==1:
		print("{:<3}".format(str(len(productDict)))+' for '+"{:<25}".format(productDict[len(productDict)].split('^')[1][:25]))
	print(str(len(productDict))+' for previous menu')
	print("# to exit application")




#foodGroupFunctionMapperDict={1: showCereal_Grains, 2: showVegetables,3: showLegume_Products,4:showFats_And_Oils,5:showSpices,6:showDairy_And_Egg_Products, 7:showFruits, 8:showMeat_Products}
print('Hi, Welcome to ...')
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
					print("cameHer");
					looper1=False					
	except:
		looper=False
		print("You chose to exit or gave wrong Input, Thank you for using this Application")

print(finalFoods)

