import constants
import regression
import codecs


def show_products(product_dict):
    print('\nSelect one of the below, Please enter the number associated '
          'with the Food')
    for i in range(int(len(product_dict) / 3)):
        print(
            "{0:<3}".format(str(3 * i + 1))
            + ' for '
            + "{0:<25}".format(
                product_dict[3 * i + 1].split('^')[1][:25]
            )
            + '  |  '
            + "{0:<3}".format(str(3 * i + 2))
            + ' for '
            + "{0:<25}".format(
                product_dict[3 * i + 2].split('^')[1][:25]
            )
            + '  |  '
            + "{0:<3}".format(str(3 * i + 3))
            + ' for ' + "{0:<25}".format(
                product_dict[3 * i + 3].split('^')[1][:25]
            )
        )
    if len(product_dict) % 3 == 2:
        print(
            "{0:<3}".format(str(len(product_dict) - 1))
            + ' for '
            + "{0:<25}".format(
                product_dict[len(product_dict) - 1].split('^')[1][:25]
            )
            + '  |  '
            + "{0:<3}".format(str(len(product_dict)))
            + ' for '
            + "{0:<25}".format(
                product_dict[len(product_dict)].split('^')[1][:25]
            )
        )
    if len(product_dict) % 3 == 1:
        print(
            "{0:<3}".format(str(len(product_dict)))
            + ' for '
            + "{0:<25}".format(
                product_dict[len(product_dict)].split('^')[1][:25]
            )
        )
    print('\n' + str(len(product_dict) + 1) + ' for previous menu')
    print("# to exit application")


def display_output(x, y, theta, final_foods, req_mineral_list):
    with codecs.open(
            constants.NUTRIENT_DETAILS_FILE,
            'r',
            encoding='utf-8',
            errors='ignore'
    ) as nutrient_detail_file:
        food_items = nutrient_detail_file.read().split('\n')[1:]
    food_items = [food_item.split("^") for food_item in food_items]
    food_dict = {}
    [
        food_dict.update({str(int(food_item[0])): food_item})
        for food_item in food_items
    ]
    required_mineral_names = [
        constants.NUTRIENT_LIST[i]
        for i in req_mineral_list
    ]
    output_double_array = list([])
    output_double_array.append(
        ['Food Name', 'ID', 'weight']
        + required_mineral_names
    )
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    for food in range(len(final_foods)):
        food_name = food_dict[final_foods[food]][3]
        weight = theta[:, 1][food] * 100
        food_id = final_foods[food]
        req_nutrient_values = [
            float(food_dict[final_foods[food]][y1]) * (float(weight / 100))
            for y1 in [
                x
                + constants.NUTRIENT_START_INDEX for x in req_mineral_list
            ]
        ]
        output_double_array.append(
            [food_name, food_id, weight]
            + req_nutrient_values
        )

    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_double_array.append(
        ['Total', '', '']
        + regression.dot_product(x, theta).tolist()[0]
    )
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_double_array.append(['Required', '', ''] + y.tolist()[0])
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_double_array.append(
        ['Difference', '', '']
        + ((y - regression.dot_product(x, theta)).tolist()[0])
    )
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_string = ''
    for row in output_double_array[:2]:
        out_row = ''
        out_row += "{0:<27}".format(row[0][:25]) \
                   + "{0:<12}".format(row[1][:10]) \
                   + "{0:<12}".format(str(row[2])[:10])
        for index in range(3, len(row)):
            out_row += "{0:<12}".format(str(row[index])[:10])
        # print(outRow)
        output_string += out_row
        output_string += '\n'

    for row in output_double_array[2:-7]:
        out_row = ''
        out_row += "{0:<27}".format(row[0][:25]) \
                   + "{0:<12}".format(row[1][:10]) \
                   + "{0:<12}".format(str(row[2])[:10])
        for index in range(3, len(row)):
            out_row += "{0:<12}".format(
                str('{:f}'.format(float(row[index])))[:10]
            )
        output_string += out_row
        output_string += '\n'
    for row in output_double_array[len(output_double_array) - 7:]:
        out_row = ''
        out_row += "{0:<27}".format(row[0][:25]) \
                   + "{0:<12}".format(row[1][:10]) \
                   + "{0:<12}".format(str(row[2])[:10])
        for index in range(3, len(row)):
            out_row += "{0:<12}".format(str(row[index])[:10])
        output_string += out_row
        output_string += '\n'
    open(constants.OUTPUT_FILE, 'w').write(output_string)


def display_output_normalized(
        x,
        y,
        theta,
        final_foods,
        req_mineral_list,
        normalize_list
):
    with codecs.open(
            constants.NUTRIENT_DETAILS_FILE,
            'r',
            encoding='utf-8',
            errors='ignore'
    ) as nutrients_data_file:
        food_items = nutrients_data_file.read().split('\n')[1:]
    food_items = [food_item.split("^") for food_item in food_items]
    food_dict = {}
    [
        food_dict.update({str(int(food_item[0])): food_item})
        for food_item in food_items
    ]
    required_mineral_names = [
        constants.NUTRIENT_LIST[i]
        for i in req_mineral_list
    ]
    output_double_array = [
        ['Food Name', 'ID', 'weight'] + required_mineral_names,
        ['-' * 27, '-' * 12, '-' * 12] + ['-' * 12] * len(
            required_mineral_names
        )
    ]
    for food in range(len(final_foods)):
        food_name = food_dict[final_foods[food]][3]
        weight = theta[:, 1][food] * 100
        food_id = final_foods[food]
        req_nutrient_values = [
            float(food_dict[final_foods[food]][y1]) * (float(weight / 100))
            for y1 in [
                x
                + constants.NUTRIENT_START_INDEX for x in req_mineral_list
            ]
        ]
        req_nutrient_values = [
            normalize_list[i] * req_nutrient_values[i]
            for i in range(len(req_nutrient_values))
        ]
        output_double_array.append(
            [food_name, food_id, weight] +
            req_nutrient_values
        )
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_double_array.append(
        ['Total', '', '']
        + regression.dot_product(x, theta).tolist()[0]
    )
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_double_array.append(['Required', '', ''] + y.tolist()[0])
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_double_array.append(
        ['Difference', '', '']
        + ((y - regression.dot_product(x, theta)).tolist()[0])
    )
    output_double_array.append(
        ['-' * 27, '-' * 12, '-' * 12]
        + ['-' * 12] * len(required_mineral_names)
    )
    output_string = ''
    for row in output_double_array[:2]:
        out_row = ''
        out_row += "{0:<27}".format(row[0][:25]) \
                   + "{0:<12}".format(row[1][:10]) \
                   + "{0:<12}".format(str(row[2])[:10])
        for index in range(3, len(row)):
            out_row += "{0:<12}".format(str(row[index])[:10])
        output_string += out_row
        output_string += '\n'

    for row in output_double_array[2:-7]:
        out_row = ''
        out_row += "{0:<27}".format(row[0][:25]) \
                   + "{0:<12}".format(row[1][:10]) \
                   + "{0:<12}".format(str(row[2])[:10])
        for index in range(3, len(row)):
            out_row += "{0:<12}".format(
                str('{:f}'.format(float(row[index])))[:10]
            )
        output_string += out_row
        output_string += '\n'
    for row in output_double_array[len(output_double_array) - 7:]:
        out_row = ''
        out_row += "{0:<27}".format(row[0][:25]) \
                   + "{0:<12}".format(row[1][:10]) \
                   + "{0:<12}".format(str(row[2])[:10])
        for index in range(3, len(row)):
            out_row += "{0:<12}".format(str(row[index])[:10])
        # print(outRow)
        output_string += out_row
        output_string += '\n'

    open(constants.NORMALISED_OUTPUT_FILE, 'w').write(output_string)


def show_food_groups():
    final_foods = []
    loop = True
    while loop:
        inner_loop = True
        print("selected Food for todays Meal:")
        print(final_foods)
        for i in constants.SELECTED_FOODS.keys():
            print(
                '\t'
                + constants.SELECTED_FOODS[i][0]
                + ' : '
                + ', '.join(constants.SELECTED_FOODS[i][1])
            )
        print(
            "\nselected Food Group from Below, Please enter "
            "the number associated with the Food Group"
        )
        for i in constants.SELECTED_FOODS.keys():
            print('\t' + str(i) + " for " + constants.SELECTED_FOODS[i][0])
        print("\t# to exit application")
        try:
            group_key = int(input())
            if group_key in range(1, 10):
                while inner_loop:
                    show_products(constants.SELECTED_FOODS[group_key][2])
                    food_dict = constants.SELECTED_FOODS[group_key][2]
                    food_key = int(input())
                    if food_key in range(1, len(food_dict) + 1):
                        constants.SELECTED_FOODS[group_key][1].append(
                            constants.SELECTED_FOODS[group_key][2][food_key]
                            .split('^')[1].replace(',', '')[:25]
                        )
                        final_foods.append(
                            constants.SELECTED_FOODS[group_key][2][food_key]
                            .split('^')[0]
                        )
                    else:
                        print("came", inner_loop)
                        inner_loop = False
        except ValueError:
            loop = False
            print("You chose to exit or gave wrong Input.")
    return final_foods
