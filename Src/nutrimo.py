#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    NutritionEngine: This script is used to determine ideal weights
    of suitable foods,     So that our nutritional requirement is
    satisfied Uses: Linear Regression, Gradient Descent for
    cost optimization. Try the below example and follow the
    console.
            $ python example_google.py
    Todo:
        * Lower price selection of foods to get all nutrition in
          optimal price
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

import constants
import console
import utils

np.set_printoptions(suppress=True)


def food_engine(food_list,theta_init,iters):
    previous_cost=constants.MAX_COST
    final_foods=[]
    if iters<=0:
        iters=constants.ITERATIONS
    if food_list:
        final_foods=food_list
    elif constants.FIRST_RUN:
        final_foods=console.show_food_groups()
        open(constants.INPUT_FILE,'w').write(','.join(final_foods))
    else:
        final_foods=open(constants.INPUT_FILE,'r').read().split('\n')[0].split(',')

    daily_nutrients_limit_y = [constants.DAILY_NUTRIENTS_LIMIT[x] for x in constants.REQUIRED_NUTRIENT_LIST]
    x,y,normalize_vertor=utils.build_x_and_y(final_foods,constants.SAMPLE_SIZE,constants.GRAMS,daily_nutrients_limit_y,constants.REQUIRED_NUTRIENT_LIST)
    input_sample_size=x.shape[0]        # Number of samples
    foods_count=x.shape[1]            # no of food items(features) you are giving to find out the optimal
    nutrients_count=x.shape[2]         # how many nutrients you gonna find out

    if theta_init.tolist():
        theta=theta_init
    elif constants.FIRST_RUN or food_list:
        theta= np.array([[i]*nutrients_count for i in np.random.rand(foods_count)])
    else:
        theta=np.array(eval(open(constants.PREVIOUS_THETA_FILE,'r').read()))
        previous_cost=eval(open(constants.PREVIOUS_COST_FILE,'r').read())

    for i in range(iters):
        regression.gradient_descent(x,y,theta)
        print(str(i)+" Normalized cost",regression.compute_cost(x, theta,y),"||||","Original Cost", regression.compute_cost(x/normalize_vertor,theta,y/normalize_vertor) )
        if previous_cost>=regression.compute_cost(x, theta,y):
            previous_cost=regression.compute_cost(x, theta,y)
            if i%constants.SAVE_FREQUENCY==0 and regression.compute_cost(x, theta,y)<=previous_cost :
                open(constants.PREVIOUS_THETA_FILE,'w').write(str(theta.tolist()))
                open(constants.PREVIOUS_COST_FILE,'w').write(str(previous_cost))
                open(constants.INPUT_FILE,'w').write(','.join(final_foods))
    display_output_normalized(x,y,theta,final_foods,constants.GRAMS,daily_nutrients_limit_y,constants.REQUIRED_NUTRIENT_LIST,normalize_vertor)
    display_output(x/normalize_vertor,y/normalize_vertor,theta,final_foods,constants.GRAMS,daily_nutrients_limit_y,constants.REQUIRED_NUTRIENT_LIST)
    output=add_or_remove_foods(x,y,theta,final_foods)
    if output:
        food_engine(output[0],output[1],output[2])



if  constants.FIRST_RUN:
    weight=input("enter your weight\n")
    calories=int(input("Select required calories.\n"))
    print()
    carbPercentage=int(input())
    print("select required Protein percentage. Ideal percentage -> 10% to 35%")
    proteinPecentage=int(input())
    fatPecentage=100-carbPercentage-proteinPecentage

    carbAmt=(carbPercentage/100.0)*calories
    protAmt=(proteinPecentage/100.0)*calories
    fatAmt=((100-carbPercentage-proteinPecentage)/100.0)*calories

    if carbPercentage+proteinPecentage> 95.0 :
        print("Please enter correct percentages next time you use the App.")
        sys.exit()

    print(carbAmt/4.0, protAmt/4.0, fatAmt/9.0)
    constants.DAILY_NUTRIENTS_LIMIT[71]=calories
    constants.DAILY_NUTRIENTS_LIMIT[110]=protAmt/4.0
    constants.DAILY_NUTRIENTS_LIMIT[61]=carbAmt/4.0
    constants.DAILY_NUTRIENTS_LIMIT[130]=fatAmt/4.0
    constants.DAILY_NUTRIENTS_LIMIT[74]=(((min(fatPecentage,8))/100.0)*calories)/9.0

    constants.DAILY_NUTRIENTS_LIMIT[89] =(weight*14)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[92] =(weight*19)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[94] =(weight*42)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[97] =(weight*38)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[102]=(weight*19)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[105]=(weight*33)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[122]=(weight*20)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[131]=(weight*5)/1000.0
    constants.DAILY_NUTRIENTS_LIMIT[133]=(weight*24)/1000.0



    print(protAmt/4.0)
    for i in constants.REQUIRED_NUTRIENT_LIST:
        print("{0:<50}".format(NUTRIENT_LIST[i][:35])+"{0:<20}".format(constants.DAILY_NUTRIENTS_LIMIT[i]))
        print("-"*75)
    dailyRequirementLimitNutrientsOut=[str(x) for x in constants.DAILY_NUTRIENTS_LIMIT]
    open(constants.DAILY_NUTRIENTS_LIMIT_FILE,'w').write(','.join(dailyRequirementLimitNutrientsOut))
    food_engine(constants.INPUT_FOOD_LIST,np.array([[i]*0 for i in np.random.rand(0)]),0)
else:
    constants.DAILY_NUTRIENTS_LIMIT=    [float(x) for x in open(constants.DAILY_NUTRIENTS_LIMIT_FILE,'r').read().split(',')]
    food_engine([],np.array([[i]*0 for i in np.random.rand(0)]),0)
