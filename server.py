import functools
from flask import Flask, request, jsonify
import time
import sys
import threading
from puppet.client import Client

import os

client = Client()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

client_path = None


def run_client():
    os.system('start ' + client_path)


lock = threading.Lock()
next_time = 0
interval = 0.5


def interval_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global interval
        global lock
        global next_time
        lock.acquire()
        now = time.time()
        if now < next_time:
            time.sleep(next_time - now)
        try:
            rt = func(*args, **kwargs)
        except Exception as e:
            rt = ({'code': 1, 'status': 'failed', 'msg': '{}'.format(e)}, 400)
        next_time = time.time() + interval
        lock.release()
        return rt
    return wrapper


@app.route('/account/balance', methods=['GET'])
@interval_call
def get_balance():
    balance = client.balance
    return jsonify({'balance': balance}), 200


@app.route('/account/position', methods=['GET'])
@interval_call
def get_position():
    position = client.position
    return jsonify({'position': position}), 200


@app.route('/account/market_value', methods=['GET'])
@interval_call
def get_market_value():
    market_value = client.market_value
    return jsonify({'market_value': market_value}), 200


@app.route('/account/deals', methods=['GET'])
@interval_call
def get_deals():
    deals = client.deals
    return jsonify({'deals': deals}), 200


@app.route('/account/entrustment', methods=['GET'])
@interval_call
def get_entrustment():
    entrustment = client.entrustment
    return jsonify({'entrustment': entrustment}), 200


@app.route('/account/cancelable', methods=['GET'])
@interval_call
def get_cancelable():
    cancelable = client.cancelable
    return jsonify({'cancelable': cancelable}), 200


@app.route('/account/new', methods=['GET'])
@interval_call
def get_new():
    new = client.new
    return jsonify({'new': new}), 200


@app.route('/account/sell', methods=['POST'])
@interval_call
def sell():
    stock = request.json['stock_no']
    amount = request.json['amount']
    price = request.json['price']
    if price is not None:
        price = float(price)
        client.sell(stock, price, int(amount))
    return jsonify({}), 200


@app.route('/account/buy', methods=['POST'])
@interval_call
def buy():
    stock = request.json['stock_no']
    amount = request.json['amount']
    price = request.json['price']
    if price is not None:
        price = float(price)
        client.buy(stock, price, int(amount))
    return jsonify({}), 200


@app.route('/account/cancel', methods=['POST'])
@interval_call
def cancel():
    stock = request.json['stock_no']
    client.cancel(stock)
    return jsonify({}), 200


@app.route('/account/cancelall', methods=['POST'])
@interval_call
def cancel_all():
    client.cancel_all()
    return jsonify({'code': 0, 'status': 'succeed'}), 200


@app.route('/account/cancel_buy', methods=['POST'])
@interval_call
def cancel_buy():
    client.cancel_buy()
    return jsonify({'code': 0, 'status': 'succeed'}), 200


@app.route('/account/cancel_sell', methods=['POST'])
@interval_call
def cancel_sell():
    client.cancel_sell()
    return jsonify({'code': 0, 'status': 'succeed'}), 200


@app.route('/account/echo', methods=['POST'])
@interval_call
def echo():
    req = request.json
    return jsonify({'data': req['data']})


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    app.run(host=host, port=port)
