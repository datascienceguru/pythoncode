# this is the main class that contains the option information in the portfolio
from datetime import datetime
import numpy as np
import pandas as pd



""" Design for a collection

startdate
enddate
rollconditions - delta, P&L or days elapsed
addcondition - delta
optionlist
totalinitialpremium - this is to calculate profit for the position
maxloss in a position 
"""
class optionCollection:
    def __init__(self, initialParams):
        self.optionsList = initialParams.optionsList
        self.collectionDelta = 0
        self.collectionGamma = 0
        self.collectionTheta = 0
        self.collectionVega = 0
        self.collectionValue = 0
    
    def updateCollection(self, currentOptionSet):
        self.collectionDelta = 0
        self.collectionGamma = 0
        self.collectionTheta = 0
        self.collectionVega = 0

        # find the set of options and update the prices
        for optionToBeUpdated in self.optionsList.values():
            
            #print("update portfolio option ")
            #print(optionToBeUpdated)
            optionsWithTheSameStrike = currentOptionSet[currentOptionSet["Strike"] == optionToBeUpdated.strike]
            numberOfOptions = optionsWithTheSameStrike.shape[0]
            i = 0
            
            while i < numberOfOptions:
                firstDataRow = optionsWithTheSameStrike.iloc[i]
                if ((firstDataRow["Expiry"] == optionToBeUpdated.expiryDate) and (firstDataRow["Right"] == optionToBeUpdated.optionType)):
                    #print("Old price was " + str(optionToBeUpdated.currentPrice))
                    optionToBeUpdated.currentPrice = (firstDataRow["Bid Price"]+firstDataRow["Ask Price"])/2
                    self.collectionValue = self.collectionValue + (optionToBeUpdated.currentPrice * optionToBeUpdated.quantity * 100)
                    #print("Newprice is " + str(optionToBeUpdated.currentPrice))
                    optionToBeUpdated.delta = firstDataRow["Delta"]
                    optionToBeUpdated.gamma = firstDataRow["Gamma"]
                    optionToBeUpdated.theta = firstDataRow["Theta"]
                    optionToBeUpdated.vega = firstDataRow["Vega"]
                    optionToBeUpdated.impVol = firstDataRow["ImpliedVolatility"]
                    
                    self.collectionDelta = (self.collectionDelta) + (optionToBeUpdated.delta * optionToBeUpdated.quantity * 100)
                    self.collectionGamma = (self.collectionGamma) + (optionToBeUpdated.gamma * optionToBeUpdated.quantity * 100)
                    self.collectionTheta = (self.collectionTheta) + (optionToBeUpdated.theta * optionToBeUpdated.quantity * 100)
                    self.collectionVega = (self.collectionVega) + (optionToBeUpdated.vega * optionToBeUpdated.quantity * 100)
                    
                    
                i = i+ 1

class optionDef:
    def __init__(self, expiry, strike, optionType, underLying, currentPrice, delta, gamma, theta, vega, impliedVolatility, quantity):
         self.expiryDate = expiry
         self.strike = strike
         self.optionType = optionType
         self.underLying = underLying
         self.currentPrice = currentPrice
         self.delta = delta
         self.gamma = gamma
         self.theta = theta
         self.vega = vega
         self.impVol = impliedVolatility
         self.quantity = quantity
         self.purchasePrice = currentPrice

         #print("Types of underlying, strike and expiryDate  " + type(underLying)+ "  " + type(strike) + " " + type(self.expiryDate))
         #print("Types of underlying  " + type(underLying))
         self.hashString = underLying+str(strike)+self.expiryDate
         print("Hashstring that has been created " + self.hashString)

    def updateOption(currentPrice, delta, gamma, theta, vega, impliedVolatility):
        self.currentPrice = currentPrice
        self.delta = delta
        self.gamma = gamma
        self.theta = theta
        self.vega = vega
        self.impVol = impliedVolatility

    def __str__(self):
        returnString = "Underlying " + self.underLying + " Strike " + str(self.strike) + " Expiry " + self.expiryDate
        returnString = returnString + "\nCurrent Price = " + str(self.currentPrice)
        returnString = returnString + " Delta = " + str(self.delta)
        returnString = returnString + " Gamma = " + str(self.gamma)
        returnString = returnString + " Theta = " + str(self.theta)
        returnString = returnString + " Vega = " + str(self.vega)
        returnString = returnString + " Implied Volatility = " + str(self.impVol) +"\n"
        return returnString
    
class stockDef:
    def __init__(ticker, quantity):
        self.ticker = ticker
        self.quantity = quantity
    
class fullPortfolio:
    def __init__(self,intialCash):
        self.cash = intialCash
        self.optionsList = {}
        self.stocksList = {}
        self.currentNAV = intialCash
        self.portfolioDelta = 0
        self.portfolioGamma = 0
        self.portfolioTheta = 0
        self.portfolioVega = 0


    def updatePortfolio(self, currentOptionSet):
        self.portfolioDelta = 0
        self.portfolioGamma = 0
        self.portfolioTheta = 0
        self.portfolioVega = 0
        # find the set of options and update the prices
        for optionToBeUpdated in self.optionsList.values():
            
            #print("update portfolio option ")
            #print(optionToBeUpdated)
            optionsWithTheSameStrike = currentOptionSet[currentOptionSet["Strike"] == optionToBeUpdated.strike]
            numberOfOptions = optionsWithTheSameStrike.shape[0]
            i = 0
            
            while i < numberOfOptions:
                firstDataRow = optionsWithTheSameStrike.iloc[i]
                if ((firstDataRow["Expiry"] == optionToBeUpdated.expiryDate) and (firstDataRow["Right"] == optionToBeUpdated.optionType)):
                    #print("Old price was " + str(optionToBeUpdated.currentPrice))
                    optionToBeUpdated.currentPrice = (firstDataRow["Bid Price"]+firstDataRow["Ask Price"])/2
                    #print("Newprice is " + str(optionToBeUpdated.currentPrice))
                    optionToBeUpdated.delta = firstDataRow["Delta"]
                    optionToBeUpdated.gamma = firstDataRow["Gamma"]
                    optionToBeUpdated.theta = firstDataRow["Theta"]
                    optionToBeUpdated.vega = firstDataRow["Vega"]
                    optionToBeUpdated.impVol = firstDataRow["ImpliedVolatility"]
                    
                    self.portfolioDelta = (self.portfolioDelta) + (optionToBeUpdated.delta * optionToBeUpdated.quantity * 100)
                    self.portfolioGamma = (self.portfolioGamma) + (optionToBeUpdated.gamma * optionToBeUpdated.quantity * 100)
                    self.portfolioTheta = (self.portfolioTheta) + (optionToBeUpdated.theta * optionToBeUpdated.quantity * 100)
                    self.portfolioVega = (self.portfolioVega) + (optionToBeUpdated.vega * optionToBeUpdated.quantity * 100)
                    
                    
                i = i+ 1
                    
    def updateNAV(self):
        self.currentNAV = self.cash
        # iterate over all the options and update cash
        for optionToBeCalculated in self.optionsList.values():
            #print("Old cash " + str(self.cash))
            #print("Updated prices quantity and price are " + str(optionToBeCalculated.quantity) + " " + str(optionToBeCalculated.currentPrice))
            self.currentNAV = self.currentNAV + (optionToBeCalculated.quantity*optionToBeCalculated.currentPrice*100)
            #print("New cash " + str(self.cash))

    def __str__(self):
        returnString = " Current Cash = " + str(self.cash) + " Current NAV " + str(self.currentNAV) + "\n"
        for optionsToBePrinted in self.optionsList.values():
            returnString = returnString + str(optionsToBePrinted)
        returnString = returnString + "Portfolio Delta = " + str(self.portfolioDelta) + \
                        " Portfolio Gamma = " + str(self.portfolioGamma) + \
                        " Portfolio Theta = " + str(self.portfolioTheta) + \
                        " Portfolio Vega = " + str(self.portfolioVega) + "\n"
        return returnString

    def tradeOption( self, optionObject, quantity, transactionType):
        if (transactionType == 'Buy'):
            # lookup if the option exists in the list, otherwise add it in
            #print("Object added - Hashstring " + optionObject.hashString)
            # see if the object exits
            try:
                currentObject = self.optionsList.get(optionObject.hashString)
                if(currentObject != None):
                    # update exisitng object
                    #print("Object found - updating")
                    currentObject.purchasePrice =((optionObject.purchasePrice*quantity)+(currentObject.purchasePrice*currentObject.quantity))/(currentObject.quantity+quantity)
                    currentObject.quantity = currentObject.quantity + quantity
                else:
                    #print("object not found creating")
                    self.optionsList[optionObject.hashString] = optionObject
                    optionObject.quantity = quantity
                    
                # update portfolio cash
                self.cash = self.cash - (optionObject.purchasePrice*quantity*100)
            except:
                print("Exception Handler 1 in tradeOption method")
                
        else:
            # remove the option from the list or decrement the quantity
            print("Object to be removed - Hashstring " + optionObject.hashString)
            try:
                self.optionsList.pop(optionObject.hashString)
            except:
                print("Exception handler 2 in trade object method - Option object" + self.optionObject.hashString +" does not exist")




