import sys
import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame, Series 

print("loading mibian")
import mibian
print("loaded mibian")

# globals
intRate = 0.02

#c=mibian.BS([2250,2230,0.02,50], callPrice=49.5)
#c = mibian.GK([1.4565, 1.45, 1, 2, 30], callPrice=0.0359)

#print("IV = " + str(c.impliedVolatility))


optionFile = pd.read_csv(sys.argv[1])
delta = []
gamma = []
theta = []
rho = []
vega = []


#print(optionFile)
for i, row in optionFile.iterrows():
    #print('i ' + str(i))
    #print('Data date ' + str(row[' DataDate']))

    currentDate = datetime.strptime(str(row[' DataDate']),"%m/%d/%Y")
    expiryDate = datetime.strptime(str(row['Expiration']),"%m/%d/%Y")

    #print(currentDate)
    #print(expiryDate)
    daystoExpiration = expiryDate - currentDate
    #daystoExpiration = 30

    print('Days to expiration ' + str(daystoExpiration))
    #print(row)

    optionPrice = (row['Bid'] + row['Ask'])/2
    if (optionPrice < 0.05):
        delta.append(0)
        theta.append(0)
        rho.append(0)
        vega.append(0)
        gamma.append(0)
        print('skip')
    else:
          
        if (row['Type'] == 'call'):
            c = mibian.BS([row['UnderlyingPrice'], row['Strike'], intRate, daystoExpiration.days], callPrice=optionPrice)
            d = mibian.BS([row['UnderlyingPrice'], row['Strike'], intRate, daystoExpiration.days],volatility = c.impliedVolatility)
            delta.append(d.callDelta)
            theta.append(d.callTheta)
            rho.append(d.callRho)
        else:
            c = mibian.BS([row['UnderlyingPrice'], row['Strike'], intRate, daystoExpiration.days], putPrice=optionPrice)
            d = mibian.BS([row['UnderlyingPrice'], row['Strike'], intRate, daystoExpiration.days],volatility = c.impliedVolatility)
            delta.append(d.putDelta)
            theta.append(d.putTheta)
            rho.append(d.putRho)

        vega.append(d.vega)
        gamma.append(d.gamma)

optionFile['Delta'] = Series(delta)
optionFile['Gamma'] = Series(gamma)
optionFile['Theta'] = Series(theta)
optionFile['Vega'] = Series(vega)
optionFile['Rho'] = Series(rho)

print(optionFile)
optionFile.to_csv("Greek" + sys.argv[1], index = False)

    
     