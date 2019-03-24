import json
import numpy as np
import configparser

config = configparser.ConfigParser()


def r_to_num(r):
    return {'two_recipes': 2, 'three_recipes': 3, 'four_recipes': 4}.get(r)


def p_to_num(p):
    return {'two_portions': 2, 'four_portions': 4}.get(p)


def fetch_portion(stock_list, num_recipe, num_portion, quantity):
    sorted_stock_list = np.array(sorted(stock_list))
    stock_index = 0
    while quantity > 0:
        if len(sorted_stock_list) < stock_index + num_recipe:
            return None
        to_fetch = min(quantity * num_portion,
                       sorted_stock_list[stock_index] - sorted_stock_list[stock_index] % num_portion)
        sorted_stock_list[stock_index:stock_index + num_recipe] = sorted_stock_list[
                                                                  stock_index:stock_index + num_recipe] - to_fetch
        quantity = quantity - (to_fetch / num_portion)
        stock_index += 1

    return sorted_stock_list


def defaults_recipe_allocation(orders_data, stock_data, debug=False):
    recipe_portion_quantity_tuple = [(r_to_num(r), p_to_num(p), orders_data[r][p]) for r in orders_data.keys() for p in
                                     orders_data[r].keys()]
    recipe_portion_quantity_tuple = sorted(recipe_portion_quantity_tuple, key=lambda c: (c[0], c[1]), reverse=True)

    stock_list = [i['stock_count'] for i in stock_data.values()]

    # preliminary_checks
    # 0 no orders or no stocks
    if len(recipe_portion_quantity_tuple) == 0:
        if len(stock_list) == 0:
            return True
        else:
            return False
    # 1 if number of recipes available is less than max num_recipes in orders
    if len(stock_list) < recipe_portion_quantity_tuple[0][0]:
        return False
    # 2 if total recipe portions in stock is less than total orders
    if sum(stock_list) < sum([a*b*c for a, b, c in recipe_portion_quantity_tuple]):
        return False

    for i, (r, p, q) in enumerate(recipe_portion_quantity_tuple):
        stock_list = fetch_portion(stock_list, r, p, q)
        if stock_list is None:
            return False
            break
        if debug:
            print(f'recipe stock list after iteration {i+1}')
            print(f'iteration {i+1} = {r} recipes, {p} portions, {q} customers')
            print(sorted(stock_list))
    if stock_list is not None:
        return True


if __name__ == '__main__':
    config.read('config.ini')
    orders_data_path = config['ORDERS']['file_path']
    stock_data_path = config['STOCKS']['file_path']

    with open(orders_data_path) as f:
        recipe_orders_data = json.load(f)
    with open(stock_data_path) as f:
        recipe_stock_data = json.load(f)
    print(defaults_recipe_allocation(recipe_orders_data, recipe_stock_data))
