"""
## Licensed under the Apache License, Version 2.0 (the "License"). 
- Copyright 2024 QuantInsti Quantitative Learnings Pvt Ltd. 
- You may not use this file except in compliance with the License. 
- You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
- Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# Import the engine file
from ib_forex_setup import engine
"""

# Import the necessary libraries
from ibapi.order import Order
from ibapi.client import Contract
from ibapi.execution import ExecutionFilter

def marketOrder(direction,quantity):
    ''' Function to set the market order object'''
    # Set the variable as an Order object
    order = Order()
    # Set the direction of the market order: Buy or Sell
    order.action = direction
    # Set the order as a market one
    order.orderType = "MKT"
    # Set the quantity
    order.totalQuantity = quantity
    # Transmit the order
    order.transmit = True
    # Trade with electronic quotes
    order.eTradeOnly = 0
    # Trade with firm quotes
    order.firmQuoteOnly = 0        
    return order

def stopOrder(direction,quantity,st_price,trail):
    ''' Function to set the stop loss order object'''
    # Set the variable as an Order object
    order = Order()
    # Set the direction of the stop loss order: Buy or Sell
    order.action = direction
    # Set the quantity
    order.totalQuantity = quantity
    # Transmit the order
    order.transmit = True
    if trail == False:
        # Set the order as a stop loss one
        order.orderType = "STP"
        # Set the stop loss breach price
        order.auxPrice = st_price
    elif trail == True:
        # Set the order as a stop loss one
        order.orderType = "TRAIL"
        # Set the stop loss breach price
        order.auxPrice = st_price
        # Set the trailing stop loss breach price
        order.trailStopPrice = st_price
    # Trade with electronic quotes
    order.eTradeOnly = 0
    # Trade with firm quotes
    order.firmQuoteOnly = 0        
    return order

def tpOrder(direction,quantity,tp_price):
    ''' Function to set the take profit order object'''
    # Set the variable as an Order object
    order = Order()
    # Set the direction of the take profit order: Buy or Sell
    order.action = direction
    # Set the order as a limit order
    order.orderType = "LMT"
    # Set the quantity
    order.totalQuantity = quantity
    # Transmit the order
    order.transmit = True
    # Set the take profit breach price
    order.lmtPrice = tp_price
    # Trade with electronic quotes
    order.eTradeOnly = 0
    # Trade with firm quotes
    order.firmQuoteOnly = 0        
    return order

def ForexContract(symbol,sec_type="CASH",exchange="IDEALPRO"):
    ''' Function to set the Forex contract object'''
    # Set the variable as a contract object
    contract = Contract()
    # Set the base currency
    contract.symbol = symbol[0:3]
    # Set the type of asset
    contract.secType = sec_type
    # Set the quote currency
    contract.currency = symbol[3:]
    # Set the IB exchange to trade Forex
    contract.exchange = exchange
    return contract

def executionFilter(time_):
    ''' Function to set the executions filter object'''
    # Set the executions filter
    execFilter = ExecutionFilter()
    # Set the time to be used to request the executions data based on the filter
    execFilter.time = time_
    return execFilter
