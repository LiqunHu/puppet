# -*- coding: utf-8 -*-
import tushare as ts
import pymongo
import datetime
import time

from puppet.client import Client
acc = {
        'account_no': '666622093901',
        'password': '851226',
        'comm_pwd': '600119',
        'client_path': r'C:\htwt\xiadan.exe'
    }

quant = Client().login(**acc).wait(2)

mongo_client = pymongo.MongoClient('localhost', 27017)
db = mongo_client.stockTrade
commissionedTran = db.commissionedTran
successTran = db.successTran
account = db.account


def getPrice(stockcode):
    expectRange = 0.0145
    df = ts.get_realtime_quotes(stockcode)  # Single stock symbol
    pre_close = df['pre_close'][0]
    price = df['price'][0]
    # expectprice = float(openprice) * expectRange + float(price)
    return float(price), float(pre_close)

def f2str(fnum):
    return "%0.2f" % fnum


if __name__ == '__main__':
    contract = quant.cancel_all()
    print(contract) 
    price, openprice = getPrice('002745')
    sellprice = f2str(openprice * 1.08)
    print(sellprice)
    contract = quant.sell('002745', sellprice, '100')
    print(contract) 
    sellprice = f2str(openprice * 0.91)
    print(sellprice)
    contract = quant.buy('002745', sellprice, '100')
    print(contract) 
    
    # while True:
    #     quant.cancel_sell().wait(2)
    #     dt = datetime.datetime.now()
    #     # entrustment = quant.entrustment
    #     todayStr = dt.strftime('%Y-%m-%d')
    #     print(todayStr)

    #     # cTrans = commissionedTran.find(
    #     #     {'tradeState': '提交', 'tranDate': todayStr})

    #     # for ct in cTrans:
    #     #     print(ct)
    #     #     for et in entrustment:
    #     #         if et['合同编号'] == ct.tradeno:
    #     #             ct.tradeState = et['操作']
    #     #             collection.update_one({"_id": ct._id}, {"$set": ct})

    #     price, openprice = getPrice('002745')

    #     quant.sell('002745', '9.32', '100')

    #     print(price, openprice)

    #     time.sleep(60)


# print(df[['code','name','open','price','bid','ask','volume','amount','time']])
