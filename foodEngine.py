import operator
import functools 
import numpy as np
import pickle 

np.set_printoptions(suppress=True)  # To not use exponential notation of the numbers
alpha = 0.00003975999999999999999999999999
iters = 1000


'''
	getTopFoodForNutrients(length)
	parameters:
		length:long  is the limit of top foods for each nutrient
	output:
		list<string> returns the distinct list of all top food items for all nutrient		
'''
def getTopFoodForNutrients(length):
	nutrient_data=open("nutrient_data.txt","r").read().split('\n')[1:] #extracts all data from the file.. eliminating the header
	mineralDesc=open("nutrient_data.txt","r").read().split('\n')[0].split('^')[4:] #getting all nutrient names from header
	nutrient_data=[x.split("^") for x in nutrient_data ]
	inclusiveFoodGroups=['0100','0400','0500','0900','1100','1200','1500','1600','1700','2000'] #we are limiting the food groups so eliminating baby foods , fast foods etc
	nutrient_data=np.array([x for x in nutrient_data if x[1] in inclusiveFoodGroups ])# Filter food items using the wanted food groups
	nutrient_data=np.concatenate((nutrient_data[:,0:1],nutrient_data[:,4:]), axis=1).astype("float") 
	temp=nutrient_data
	li=[]
	for i in range(1,36):
		rr=temp[temp[:,i].argsort()[::-1]]
		#print mineralDesc[i-1]
		#print(rr[:length,[0,i]])
		''' To pickle
		#print(str(i)+':'+"('"+mineralDesc[i-1]+"_TopFoods',["+",".join('"{0}"'.format(w) for w in rr[:rr.shape[0],[0]].astype('str').reshape(rr.shape[0]).tolist())+']),')
		with open('topNutritionFood.pickle','wb') as picleLoad:
			pickle.dump(rr,picleLoad)
		'''
		li.append(",".join(rr[:length,[0]].astype('str').reshape(length).tolist()))
	return list(set(",".join(li).split(',')))

		
def computeCost(X, theta,y):
	pred=dotProduct(X,theta)
	return sum(sum((y-pred)**2))

def dotProduct(X,theta):
	product=X*theta
	return np.array([functools.reduce(operator.add,lis) for lis in product])

def mean(X):
	return sum(sum(X))/2

def variance(X,mean):
	return sum((X-mean)**2)

def gradientDescent(X,y,theta):	
	tempTheta=np.zeros(shape=theta.shape)
	for i in range (0,theta.shape[0]):
		tempTheta[i]=  [(alpha/inputSampleSize)*sum(sum((((dotProduct(X,theta)-y) * X[:,i:i+1].reshape(inputSampleSize,nutrientCount)))))]*nutrientCount
	for i in range (0,theta.shape[0]):	
		theta[i]=theta[i]-tempTheta[i]
	#theta-=min(0,min([min(x) for x in theta.tolist()]))

def getXandY(inputFoodList, duplicateSampleCount,grams):
	dailyLimitList=[1200.0, 325.0, 300.0, 550.0, 2.0, 2500.0, 20.0, 2.0, 10.0, 400.0, 400.0, 25.0, 15000.0, 350.0, 5.0, 16.0, 6.0, 1000.0, 3500.0, 56.0, 1.6, 55.0, 2400.0, 35.0, 500.0, 2.0, 60.0, 90.0, 900.0, 6.0, 2.0, 12.0, 120.0, 15.0, 30]
	food_items=open("nutrient_data.txt").read().split('\n')[1:]
	food_items=[food_item.split("^") for food_item in food_items]
	food_dict={}
	[food_dict.update({str(float(food_item[0])): food_item}) for food_item in food_items]
	X=np.array([[[z*float(food_dict[x][y] )*(float(grams))/100for y in range(4,39)] for x in inputFoodList] for z in range(1,duplicateSampleCount+1)])
	y=np.array([[x*m for x in dailyLimitList] for m in range (1, duplicateSampleCount+1)])
	return (X,y)
	
nutrientWiseTopFoods=pickle.load(open('topNutritionFood.pickle','rb'))
exclusionList=[]

X,y=getXandY([x for x in getTopFoodForNutrients(10) if x not in exclusionList],1,10)


inputSampleSize=X.shape[0]		# Number of samples
foodCount=X.shape[1]			# no of food items(features) you are giving to find out the optimal
nutrientCount=X.shape[2] 		# how many nutrients you gonna find out	
theta= np.array([[i]*nutrientCount for i in np.random.rand(foodCount)])


#working test data
#X=np.array([[[1,2,3],[2,3,1],[3,1,2],[1,3,2]],[[3,1,2],[1,2,3],[2,3,1],[1,3,2]]])
#y=np.array([[18, 23, 19],[15, 26, 19]])
#theta= np.array([[i]*nutrientCount for i in np.random.rand(foodCount)])

print(str(i)+" cost",computeCost(X, theta,y))

for i in range(1000):
	gradientDescent(X,y,theta)
	print(str(i)+" cost",computeCost(X, theta,y))
	
print(theta[:,0])

