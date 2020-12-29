# This script takes a file that contains a list of .csv files and loads 
# the options related to a particular ticker into a set of expiration date stamped directories and files

import sys
from datetime import datetime
import numpy as np
import pandas as pd
import os.path

from pandas import DataFrame, Series 

# the arguments are the filelist, ticker, output directory
print (sys.argv)

#declare all the global variables
ticker = sys.argv[2]

optionData = {}

#read the file list
filesToProcess = pd.read_csv(sys.argv[1])['File Name'].tolist()

for optionFile in filesToProcess:
    print(optionFile)

    #read the option file
    optionFileDF = pd.read_csv(optionFile)
    
    #filter the rows in the option file to contain only ticker related rows 
    optionRows = optionFileDF[optionFileDF.UnderlyingSymbol == ticker]

    # extract all the expiration dates
    expirationDates = optionRows.Expiration.unique()

    # add to optionData
    for expiryDate in expirationDates:
        optionsForTheExpiration = optionRows[optionRows.Expiration == expiryDate]

        if (expiryDate in optionData.keys()):
            optionData[expiryDate] = optionData[expiryDate].append(optionsForTheExpiration)
#            print(optionData[expiryDate].shape)
        else:
            optionData[expiryDate] = optionsForTheExpiration
#            print(optionData[expiryDate].shape)

#change working directory to the output path given on the command line
os.chdir(sys.argv[3])

for expiryDate in optionData.keys():
    formattedDate = datetime.strptime(str(expiryDate),"%m/%d/%Y").strftime("%m_%d_%Y")
    print(formattedDate)
    outputFileName = formattedDate + ".csv"
    if (os.path.isfile(outputFileName)):
        optionData[expiryDate].to_csv(outputFileName, mode='a', header=False, index=False)
    else:
        optionData[expiryDate].to_csv(outputFileName, index=False)
        
  

#print(optionData)




