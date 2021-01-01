import sys
from datetime import datetime
import numpy as np
import pandas as pd
import os.path

from pandas import DataFrame, Series 

from OptionsDef import optionDef, fullPortfolio

""" This is the format of the file. 
Timestamp             object
Ticker                object
Bid Price            float64
Bid Size               int64
Ask Price            float64
Ask Size               int64
Expiry                object
Strike               float64
Right                 object
Underlying           float64
ImpliedVolatility    float64
Delta                float64
Gamma                float64
Vega                 float64
Theta                float64
Rho                  float64
"""

debugProgram = False

def debugPrint(stringToBePrinted):
    if (debugProgram):
        print(stringToBePrinted)

def loadOptionFile(dataDate, ticker, dirPath):
    optionDF = pd.DataFrame()

    formattedFileDate = dataDate.strftime("%Y-%m-%d")
    try:
        fileName = dirPath+"/"+ticker+"-"+formattedFileDate+"-greeks.csv"
        debugPrint("Filename " + fileName)
        optionDF = pd.read_csv(fileName)
        #break
    except:
        debugPrint('file does not exist')
        
    return optionDF

def getOptionsWithDelta(optionDataFrame, delta):
    returnDataFrame = pd.DataFrame(columns= optionDataFrame.columns)
    deltaDataFrame = optionDataFrame[(optionDataFrame["Delta"]>(delta-0.05)) & (optionDataFrame["Delta"] < (delta + 0.05))]
    uniqueDates = deltaDataFrame.Expiry.unique()
    debugPrint(uniqueDates)

    # get the middle row in the options
    for date in uniqueDates:
        # count the number of 
        optionsInTheRange = deltaDataFrame[deltaDataFrame["Expiry"] == date]
        #debugPrint(optionsInTheRange.head())
        numberOfOptions = optionsInTheRange.shape[0]
        #debugPrint("Number of options is " + str(numberOfOptions))
        correctRow = int((numberOfOptions+1)/2)
        #debugPrint("Correct Row is")
        #debugPrint(correctRow)
        correctRowData = optionsInTheRange.iloc[correctRow - 1]
        #debugPrint("Correct Row Data")
        #debugPrint(correctRowData)
        returnDataFrame = returnDataFrame.append(correctRowData, ignore_index= True)
    
    return returnDataFrame

def getOptionWithDaystoExpiry(numberOfDays, optionsDataFrame):
    numberOfOptions = optionsDataFrame.shape[0]
    i = 0

    currentDifference = 10000
    currentRow = i
    debugPrint("Number of options " + str(numberOfOptions))

    while i < numberOfOptions:
        
        firstDataRow = optionsDataFrame.iloc[i]   
        newDifference = datetime.strptime(firstDataRow["Expiry"], '%m/%d/%Y') - datetime.strptime(firstDataRow["Timestamp"], '%m/%d/%Y')
        
        if (abs(newDifference.days-numberOfDays) < currentDifference):
            currentDifference = abs(newDifference.days-numberOfDays)
            currentRow = i
            
            
        i = i +1
        

    #debugPrint("Current Row " + str(currentRow) + " Current Differnce " + str(currentDifference)) 
    return optionsDataFrame.iloc[currentRow]
            
useCommandLineArgs = True

# main code
if(useCommandLineArgs):
    print("Start date given" + sys.argv[1])
    print("End date given" + sys.argv[2])
    print("Directory " + sys.argv[3])


    startDate = datetime.strptime(sys.argv[1], '%m/%d/%y')
    endDate = datetime.strptime(sys.argv[2], '%m/%d/%y')
    dataDirectory = sys.argv[3]
else:
    startDate = datetime.strptime("01/01/20", '%m/%d/%y')
    endDate = datetime.strptime("05/01/20", '%m/%d/%y')
    dataDirectory = "/Users/srirama/Documents/toSrirama/SPX.options"

dateRange = pd.date_range(start = startDate, end = endDate)
debugPrint(dateRange)
initializePortfolio = False
myPortfolio = fullPortfolio(1000000)
backTestDaysToExpiry = 100
strike1 = -0.40
strike2 = -0.28
strike3 = -0.10


for dataDate in dateRange:
    df = loadOptionFile(dataDate, "SPX", dataDirectory)
    if (df.empty):
        debugPrint("No dataframe returned")
        
    else:
        debugPrint("opened file for date" + dataDate.strftime("%m/%d/%Y"))
 
        if (initializePortfolio == False):         
            deltaStrike1Options = getOptionsWithDelta(df, strike1)
            theRightStrike1Option = getOptionWithDaystoExpiry(backTestDaysToExpiry, deltaStrike1Options)
            debugPrint(theRightStrike1Option)
            tradedStrike1Option = optionDef(theRightStrike1Option["Expiry"],theRightStrike1Option["Strike"], theRightStrike1Option["Right"],
                                theRightStrike1Option["Ticker"], (theRightStrike1Option["Bid Price"]+theRightStrike1Option["Ask Price"])/2, theRightStrike1Option["Delta"], 
                                theRightStrike1Option["Gamma"],theRightStrike1Option["Theta"], theRightStrike1Option["Vega"],
                                theRightStrike1Option["ImpliedVolatility"], 0)
            myPortfolio.tradeOption(tradedStrike1Option, 10, "Buy")

            deltaStrike2Options = getOptionsWithDelta(df, strike2)
            theRightStrike2Option = getOptionWithDaystoExpiry(backTestDaysToExpiry, deltaStrike2Options)
            debugPrint(theRightStrike2Option)
            tradedStrike2Option = optionDef(theRightStrike2Option["Expiry"],theRightStrike2Option["Strike"], theRightStrike2Option["Right"],
                                theRightStrike2Option["Ticker"], (theRightStrike2Option["Bid Price"]+theRightStrike2Option["Ask Price"])/2, theRightStrike2Option["Delta"], 
                                theRightStrike2Option["Gamma"],theRightStrike2Option["Theta"], theRightStrike2Option["Vega"],
                                theRightStrike2Option["ImpliedVolatility"], 0)
            myPortfolio.tradeOption(tradedStrike2Option, -20, "Buy")

            deltaStrike3Options = getOptionsWithDelta(df, strike3)
            theRightStrike3Option = getOptionWithDaystoExpiry(backTestDaysToExpiry, deltaStrike3Options)
            debugPrint(theRightStrike3Option)
            tradedStrike3Option = optionDef(theRightStrike3Option["Expiry"],theRightStrike3Option["Strike"], theRightStrike3Option["Right"],
                                theRightStrike3Option["Ticker"], (theRightStrike3Option["Bid Price"]+theRightStrike3Option["Ask Price"])/2, theRightStrike3Option["Delta"], 
                                theRightStrike3Option["Gamma"],theRightStrike3Option["Theta"], theRightStrike3Option["Vega"],
                                theRightStrike3Option["ImpliedVolatility"], 0)
            myPortfolio.tradeOption(tradedStrike3Option, 10, "Buy")
            
            myPortfolio.updatePortfolio(df)
            myPortfolio.updateNAV()
            debugPrint("Contents of my portfolio")
            debugPrint("Cash in my portfolio " + str(myPortfolio.cash))
            debugPrint("My porfolio options")
            debugPrint(myPortfolio.optionsList)
            initializePortfolio = True
            print("Portfolio on " + dataDate.strftime("%m/%d/%Y") + " SPX =" + str(theRightStrike1Option["Underlying"]))
            print(myPortfolio)
        else: 
            myPortfolio.updatePortfolio(df)

            myPortfolio.updateNAV()
            debugPrint("NAV is " + str(myPortfolio.cash))
            firstDataRow = df.iloc[1]
            print("Portfolio on " + dataDate.strftime("%m/%d/%Y") + "SPX = "+ str(firstDataRow["Underlying"]))
            print(myPortfolio)


