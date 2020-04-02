import codecs
import copy
import pickle

import numpy as np

import console
import constants
import regression


# This is to pickle all foods in sorted order
def pickle_top_foods_for_each_nutrient(pickle_all_foods=True):
    with open(constants.NUTRIENT_DETAILS_FILE, 'r', encoding='ISO-8859-1') \
            as nutrient_data_file:
        nutrient_data = nutrient_data_file.read().split('\n')[1:]
    if not pickle_all_foods:
        nutrient_data = [x for x in nutrient_data if str(
            int(x.split('^')[0])) in constants.SELECTED_FOOD_IDS]
    nutrient_data = [x.split("^") for x in nutrient_data]
    with open(constants.NUTRIENT_DETAILS_FILE, 'r', encoding='ISO-8859-1') \
            as nutrient_data_file:
        mineral_desc = nutrient_data_file.read().split('\n')[0] \
                           .split('^')[constants.NUTRIENT_START_INDEX:-1]

        nutrient_data = np.array([x for x in nutrient_data])
        nutrient_data = np.concatenate(
            (
                nutrient_data[:, 0:1],
                nutrient_data[:, constants.NUTRIENT_START_INDEX:-1]
            ),
            axis=1
        )
        nutrient_data[nutrient_data == ''] = '0'
        nutrient_data = nutrient_data.astype("float")
        dict_li = []
        for i in range(1, 150):
            temp = nutrient_data[nutrient_data[:, i].argsort()[::-1]]
            dict_li.append(
                str(i) + ':' + "('" + mineral_desc[
                    i - 1] + "_TopFoods',[" + ",".join(
                    '"{0}"'.format(w) for w in
                    temp[:temp.shape[0], [0]].astype('str').reshape(
                        temp.shape[0]).tolist()) + '])')
        top_nutritious_food = ','.join(dict_li)
        nutrient_wise_top_foods = eval('{' + top_nutritious_food + '}')
        if pickle_all_foods:
            with open(constants.TOP_ALL_FOODS_PER_NUTRIENT_FILE,
                      'wb') as pickle_file:
                pickle.dump(nutrient_wise_top_foods, pickle_file)
        else:
            with open(constants.TOP_SELECTED_FOODS_PER_NUTRIENT_FILE,
                      'wb') as pickle_file:
                pickle.dump(nutrient_wise_top_foods, pickle_file)


def build_x_and_y(input_food_list, duplicate_sample_count, daily_limit_list,
                  req_mineral_list):
    avg = sum(daily_limit_list) / len(daily_limit_list)
    normalize_list = [avg / x if x > 0 else 1 for x in daily_limit_list]
    daily_limit_list = [
        normalize_list[i] * daily_limit_list[i]
        for i in range(len(normalize_list))
    ]
    with codecs.open(constants.NUTRIENT_DETAILS_FILE, 'r', encoding='utf-8',
                     errors='ignore') as data:
        food_items = data.read().split('\n')[1:]
    food_items = [food_item.split("^") for food_item in food_items]
    food_dict = {}
    [food_dict.update({str(int(food_item[0])): food_item}) for food_item in
     food_items]
    x = np.array(
        [[[z * float(food_dict[x][y]) * (float(constants.GRAMS)) / 100 for y in
           [x1 + constants.NUTRIENT_START_INDEX for x1 in
            req_mineral_list]] for x in input_food_list] for z in
         range(1, duplicate_sample_count + 1)])
    x = x * normalize_list
    y = np.array([[x * m for x in daily_limit_list] for m in
                  range(1, duplicate_sample_count + 1)])
    return x, y, normalize_list


def get_top_foods_for_nutrient(all_foods, index, length):
    if all_foods:
        nutrient_wise_top_foods = pickle.load(
            open(constants.TOP_ALL_FOODS_PER_NUTRIENT_FILE, 'rb'))
    else:
        nutrient_wise_top_foods = pickle.load(
            open(constants.TOP_SELECTED_FOODS_PER_NUTRIENT_FILE, 'rb'))
    return (
        nutrient_wise_top_foods[index + 1][0],
        [
            str(int(float(x)))
            for x in nutrient_wise_top_foods[index + 1][1][:length + 1]
        ]
    )


def get_add_more_list(x, y, theta):
    dt_product = regression.dot_product(x, theta)
    # required = y[0]
    # computed_total = dt_product[0]
    ratio = (y / dt_product).tolist()[0]
    difference = (y - dt_product).tolist()[0]
    add_more_list = []

    for i in range(len(ratio)):
        if ratio[i] > 2 or difference[i] > 50:
            add_more_list.append(i)
    return [constants.REQUIRED_NUTRIENT_LIST[x] for x in add_more_list]


def get_remove_existing_foods_list(x, y, theta):
    dt_product = regression.dot_product(x, theta)
    # required = y[0]
    # computed_total = dt_product[0]
    ratio = (y / dt_product).tolist()[0]
    difference = (y - dt_product).tolist()[0]
    remove_existing = []
    for i in range(len(ratio)):
        if ratio[i] < 0.5 or difference[i] < (-50):
            remove_existing.append(i)
    return [constants.REQUIRED_NUTRIENT_LIST[x] for x in remove_existing]


def show_add_more_foods(nutrient_top_foods_dict, final_foods):
    loop = True
    while loop:
        loop_1 = True
        print("Added extra Foods for todays Meal:")
        for i in nutrient_top_foods_dict.keys():
            print('\t' + nutrient_top_foods_dict[i][0] + ' : ' + ', '.join(
                nutrient_top_foods_dict[i][1]))
        print(
            "\nselect nutrients that you need to add, "
            "Please enter the number associated with nutrient"
        )
        for i in nutrient_top_foods_dict.keys():
            print('\t' + str(i) + " for " + nutrient_top_foods_dict[i][0])
        print("\t# to exit application")
        try:
            nutrient_key = int(input())
            if nutrient_key in nutrient_top_foods_dict.keys():
                while loop_1:
                    console.show_products(nutrient_top_foods_dict[nutrient_key]
                                          [2])
                    food_list = nutrient_top_foods_dict[nutrient_key][2]
                    food_key = int(input())
                    if food_key in range(1, len(food_list) + 1):
                        nutrient_top_foods_dict[nutrient_key][1].append(
                            nutrient_top_foods_dict[nutrient_key][2][
                                food_key].split('^')[1].replace(',', '')[:25])
                        final_foods.append(
                            nutrient_top_foods_dict[nutrient_key][2][
                                food_key].split('^')[0])
                    else:
                        loop_1 = False
        except Exception as e:
            loop = False
            print(
                "You chose to exit or gave wrong Input, "
                "Thank you for using this Application"
                + str(e)
            )
    return final_foods


def show_delete_foods(nutrient_top_foods_dict, final_foods):
    loop = True
    while loop:
        loop_1 = True
        print("Foods That need to be removed:")
        print(final_foods)
        for i in nutrient_top_foods_dict.keys():
            print('\t' + nutrient_top_foods_dict[i][0] + ' : ' + ', '.join(
                nutrient_top_foods_dict[i][1]))
        print(
            "\nselect nutrients that you need to remove, "
            "Please enter the number associated with nutrient"
        )
        for i in nutrient_top_foods_dict.keys():
            print('\t' + str(i) + " for " + nutrient_top_foods_dict[i][0])
        print("\t# to exit application")
        try:
            nutrient_key = int(input())
            if nutrient_key in nutrient_top_foods_dict.keys():
                while loop_1:
                    console.show_products(
                        nutrient_top_foods_dict[nutrient_key][2]
                    )
                    food_list = nutrient_top_foods_dict[nutrient_key][2]
                    food_key = int(input())
                    if food_key in range(1, len(food_list) + 1):
                        nutrient_top_foods_dict[nutrient_key][1].append(
                            nutrient_top_foods_dict[nutrient_key][2][
                                food_key].split('^')[1].replace(',', '')[:25])
                        final_foods.append(
                            nutrient_top_foods_dict[nutrient_key][2][
                                food_key].split('^')[0])
                    else:
                        loop_1 = False
        except ValueError:
            loop = False
            print(
                "You chose to exit or gave wrong Input, "
                "Thank you for using this Application"
            )
    return list(set(final_foods))


def add_more_foods(add_more_list, final_foods):
    nutrient_top_foods_dict = {}
    with open(constants.NUTRIENT_DETAILS_FILE, 'r',
              encoding='ISO-8859-1') as nutrient_details_file:
        food_items = nutrient_details_file.read().split('\n')[1:]
    # food_items = open(constants.NUTRIENT_DETAILS_FILE).read().split('\n')[1:]
    food_items = [food_item.split("^") for food_item in food_items]
    food_dict = {}
    [food_dict.update({str(int(food_item[0])): food_item}) for food_item in
     food_items]
    for i in range(len(add_more_list)):
        top_list = [
            x for
            x in get_top_foods_for_nutrient(False, add_more_list[i], 50)[1]
            if x not in final_foods
        ]
        dictt = {i: top_list[i - 1] + '^' + food_dict[top_list[i - 1]][4] for i
                 in range(1, len(top_list) + 1)}
        nutrient_top_foods_dict.update(
            {i + 1: (constants.NUTRIENT_LIST[add_more_list[i]], [], dictt)})
    final_foods = show_add_more_foods(nutrient_top_foods_dict, final_foods)
    return final_foods


def removeExistingFoods(remove_existing_list, final_foods):
    nutrient_top_foods_dict = {}
    with open(constants.NUTRIENT_DETAILS_FILE, 'r',
              encoding='ISO-8859-1') as nutrient_details_file:
        food_items = nutrient_details_file.read().split('\n')[1:]
    # food_items = open(constants.NUTRIENT_DETAILS_FILE).read().split('\n')[1:]
    food_items = [food_item.split("^") for food_item in food_items]
    food_dict = {}
    [food_dict.update({str(int(food_item[0])): food_item}) for food_item in
     food_items]
    for i in range(len(remove_existing_list)):
        top_list = [
            x
            for x in get_top_foods_for_nutrient(
                False,
                remove_existing_list[i], 300
            )[1]
            if x in final_foods
        ]
        dictt = {i: top_list[i - 1] + '^' + food_dict[top_list[i - 1]][4] for i
                 in range(1, len(top_list) + 1)}
        nutrient_top_foods_dict.update({i + 1: (
            constants.NUTRIENT_LIST[remove_existing_list[i]], [], dictt)})
    remove_foods = show_delete_foods(nutrient_top_foods_dict, [])
    return remove_foods


def add_or_remove_foods(x, y, theta, final_foods):
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
                "Enter the comma separated food item IDs "
                "that needed to be added. "
                "for example\n\t11080,11215"
            )
            new_foods = [
                x.strip()
                for x in input().strip().split(',')
                if x not in final_foods
            ]
            if len(new_foods) > 0:
                append_theta = np.array(
                    [[i] * x.shape[2] for i in np.random.rand(len(new_foods))]
                )
                theta = np.concatenate((theta, append_theta), axis=0)
                final_foods = final_foods + new_foods
                return final_foods, theta, 0
            else:
                print("No food item to add")
                return None
        elif option == 2:
            if get_add_more_list(x, y, theta):
                initial_copy = copy.deepcopy(final_foods)
                final_foods = add_more_foods(get_add_more_list(x, y, theta),
                                             final_foods)
                if len(final_foods) - len(initial_copy) > 0:
                    append_theta = np.array(
                        [
                            [i] * x.shape[2]
                            for i in
                            np.random.rand(len(final_foods)
                                           - len(initial_copy))
                        ]
                    )
                    theta = np.concatenate((theta, append_theta), axis=0)
                    return final_foods, theta, 0
                else:
                    print("No food items to Add based on Analysis")
                    return None
        elif option == 3:
            print(
                "Enter the comma separated food "
                "item IDs that needed to be deleted."
                "for example\n\t11080,11215"
            )
            remove_foods = list(
                set(
                    [x.strip() for x in str(input()).strip().split(',') if
                     x in final_foods]
                )
            )
            if len(remove_foods) > 0:
                for food in remove_foods:
                    indx = final_foods.index(food)
                    final_foods.remove(food)
                    theta = np.delete(theta, indx, axis=0)
                return final_foods, theta, 0
            else:
                print("No food items to delete")
                return None
        elif option == 4:
            if get_remove_existing_foods_list(x, y, theta):
                remove_foods = removeExistingFoods(
                    get_remove_existing_foods_list(x, y, theta),
                    final_foods
                )
                if len(remove_foods) > 0:
                    for food in remove_foods:
                        indx = final_foods.index(food)
                        final_foods.remove(food)
                        theta = np.delete(theta, indx, axis=0)
                    return final_foods, theta, 0
                else:
                    print("No food items to delete based on Analysis")
                    return None
        elif option == 5:
            while True:
                theta_list = theta[:, 0].tolist()
                try:
                    indx = theta_list.index(0.0)
                    food = final_foods[indx]
                    final_foods.remove(food)
                    theta = np.delete(theta, indx, axis=0)
                except Exception as e:
                    print("Exception"+str(e))
                    break
            return final_foods, theta, 0
        elif option == 6:
            print("Enter the reqired iterations")
            iters = int(input())
            if iters > 0:
                return final_foods, theta, iters
            else:
                return final_foods, theta, 0
        else:
            print("Invalid option. Thanks for suing this Application.")
            return None
    except Exception as e:
        print(
            "You chose to exit or gave wrong Input, "
            "Thank you for using this Application\nThe exception is \n"
            + str(e)
        )
        return final_foods, theta, 0
