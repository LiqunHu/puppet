# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 17:28:43 2022

@author: huliqun
"""

from puppet.client import Client
acc = {
    'account_no': '',
    'password': '',
    'comm_pwd': '',
    'client_path': r'C:\htwt\xiadan.exe'
}

quant = Client().login(**acc).wait(2)

deals = quant.deals

print(deals)

quant.buy('300031', 16.01, 11200)
