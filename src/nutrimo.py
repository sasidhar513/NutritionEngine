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
import sys

import numpy as np

import constants
import utils
import console
import regression

np.set_printoptions(suppress=True)


def food_engine(food_list, theta_init, iterations):
    previous_cost = constants.MAX_COST
    if iterations <= 0:
        iterations = constants.ITERATIONS
    if food_list:
        final_foods = food_list
    elif constants.FIRST_RUN:
        final_foods = console.show_food_groups()
        open(constants.INPUT_FILE, 'w').write(','.join(final_foods))
    else:
        final_foods = open(constants.INPUT_FILE, 'r') \
            .read().split('\n')[0].split(',')
    daily_nutrients_limit_y = [
        constants.DAILY_NUTRIENTS_LIMIT[x]
        for x in constants.REQUIRED_NUTRIENT_LIST
    ]
    x, y, normalize_vector = utils.build_x_and_y(
        final_foods,
        constants.SAMPLE_SIZE,
        daily_nutrients_limit_y,
        constants.REQUIRED_NUTRIENT_LIST
    )
    # input_sample_size = x.shape[0]
    foods_count = x.shape[1]
    nutrients_count = x.shape[2]
    if theta_init.tolist():
        theta = theta_init
    elif constants.FIRST_RUN or food_list:
        theta = np.array(
            [[x] * nutrients_count for x in np.random.rand(foods_count)]
        )
    else:
        theta = np.array(eval(open(constants.PREVIOUS_THETA_FILE, 'r').read()))
        previous_cost = eval(open(constants.PREVIOUS_COST_FILE, 'r').read())

    for loop in range(iterations):
        regression.gradient_descent(x, y, theta)
        print(
            str(loop) + " Normalized cost",
            regression.compute_cost(x, theta, y),
            "||||", "Original Cost",
            regression.compute_cost(x / normalize_vector,
                                    theta, y / normalize_vector)
        )
        if previous_cost >= regression.compute_cost(x, theta, y):
            previous_cost = regression.compute_cost(x, theta, y)
            if loop % constants.SAVE_FREQUENCY == 0 and \
                    regression.compute_cost(x, theta, y) <= previous_cost:
                open(constants.PREVIOUS_THETA_FILE, 'w') \
                    .write(str(theta.tolist()))
                open(constants.PREVIOUS_COST_FILE, 'w') \
                    .write(str(previous_cost))
                open(constants.INPUT_FILE, 'w') \
                    .write(','.join(final_foods))
    console.display_output_normalized(
        x,
        y,
        theta,
        final_foods,
        constants.REQUIRED_NUTRIENT_LIST,
        normalize_vector
    )
    console.display_output(
        x / normalize_vector,
        y / normalize_vector,
        theta,
        final_foods,
        constants.REQUIRED_NUTRIENT_LIST
    )
    output = utils.add_or_remove_foods(x, y, theta, final_foods)
    if output:
        food_engine(output[0], output[1], output[2])


if constants.FIRST_RUN:
    weight = int(input("enter your weight\n"))
    calories = int(input("Select required calories.\n"))
    carb_percentage = int(input(
        "select required Carbohydrates. Ideal percentage -> 45%  to  60%"
    ))
    protein_percentage = int(input(
        "select required Protein percentage. Ideal percentage -> 10% to 35%"
    ))  # type: int
    fat_percentage = 100 - carb_percentage - protein_percentage
    calories_by_carbs = (carb_percentage / 100.0) * calories
    calories_by_proteins = (protein_percentage / 100.0) * calories
    calories_by_fat = (
                              (100 - carb_percentage - protein_percentage)
                              / 100.0
                      ) * calories
    if carb_percentage + protein_percentage > 95.0:
        print("Please enter correct percentages next time you use the App.")
        sys.exit(1)
    print(calories_by_carbs / 4.0, calories_by_proteins / 4.0,
          calories_by_fat / 9.0)
    constants.DAILY_NUTRIENTS_LIMIT[71] = calories
    constants.DAILY_NUTRIENTS_LIMIT[110] = calories_by_proteins / 4.0
    constants.DAILY_NUTRIENTS_LIMIT[61] = calories_by_carbs / 4.0
    constants.DAILY_NUTRIENTS_LIMIT[130] = calories_by_fat / 4.0
    constants.DAILY_NUTRIENTS_LIMIT[74] = (((min(fat_percentage, 8)) / 100.0)
                                           * calories) / 9.0
    constants.DAILY_NUTRIENTS_LIMIT[89] = (weight * 14) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[92] = (weight * 19) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[94] = (weight * 42) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[97] = (weight * 38) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[102] = (weight * 19) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[105] = (weight * 33) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[122] = (weight * 20) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[131] = (weight * 5) / 1000.0
    constants.DAILY_NUTRIENTS_LIMIT[133] = (weight * 24) / 1000.0
    print(calories_by_proteins / 4.0)
    for i in constants.REQUIRED_NUTRIENT_LIST:
        print("{0:<50}".format(constants.NUTRIENT_LIST[i][:35])
              + "{0:<20}".format(constants.DAILY_NUTRIENTS_LIMIT[i]))
        print("-" * 75)
    dailyRequirementLimitNutrientsOut = [str(x)
                                         for x in
                                         constants.DAILY_NUTRIENTS_LIMIT]
    open(constants.DAILY_NUTRIENTS_LIMIT_FILE, 'w') \
        .write(','.join(dailyRequirementLimitNutrientsOut))
    food_engine(
        constants.INPUT_FOOD_LIST,
        np.array([[i] * 0 for i in np.random.rand(0)]),
        0
    )
else:
    constants.DAILY_NUTRIENTS_LIMIT = [
        float(x) for x in
        open(constants.DAILY_NUTRIENTS_LIMIT_FILE, 'r').read().split(',')
    ]
    food_engine([], np.array([[i] * 0 for i in np.random.rand(0)]), 0)
