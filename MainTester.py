import sys
from datetime import datetime
import numpy as np
import pandas as pd
import os.path

from pandas import DataFrame, Series 

from OptionsDef import optionDef, fullPortfolio

myPortfolio = fullPortfolio(100000)
print("Portfolio created with initial cash" + str(myPortfolio.cash))
optionToBeTraded = optionDef("01/01/2020", 3000, "call", "SPX",2800, 0.5, 1, 5, 10, 1)

myPortfolio.tradeOption(optionToBeTraded,1,'Buy')

myPortfolio.tradeOption(optionToBeTraded,1,'Buy')

print(myPortfolio.optionsList)
myPortfolio.tradeOption(optionToBeTraded, 1, 'Sell')
print(myPortfolio.optionsList)