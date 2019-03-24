import json
from recipe_allocator import defaults_recipe_allocation
from flask import Flask, request
import configparser
app = Flask(__name__)

config = configparser.ConfigParser()


@app.route('/static/')
def get_static_recipe_allocation():
    config.read('config.ini')
    orders_data_path = config['ORDERS']['file_path']
    stock_data_path = config['STOCKS']['file_path']
    with open(orders_data_path) as f:
        recipe_orders_data = json.load(f)
    with open(stock_data_path) as f:
        recipe_stock_data = json.load(f)
    return str(defaults_recipe_allocation(orders_data=recipe_orders_data, stock_data=recipe_stock_data, debug=False))


@app.route('/dynamic/', methods=["POST"])
def get_dynamic_recipe_allocation():
    # print(request.get_json())
    input_json = request.get_json()
    recipe_orders_data = input_json['orders']
    recipe_stock_data = input_json['stocks']
    return str(defaults_recipe_allocation(orders_data=recipe_orders_data, stock_data=recipe_stock_data, debug=False))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
