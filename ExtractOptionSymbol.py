import sys
from datetime import datetime
import numpy as np
import pandas as pd
import os.path
import os

from pandas import DataFrame, Series 

# inputs to the program - symbol, inputdirector with csv files, output directory with extracted csv files

# defaults are given below
underlyingSymbol = "SPX"
inputDirectory = "/Users/srirama/temp"
outputDirectory = "/Users/srirama/temp1"

useCommandLineArgs = True

# main code
if(useCommandLineArgs):
    underlyingSymbol = sys.argv[1]
    inputDirectory = sys.argv[2]
    outputDirectory = sys.argv[3]


# read the contents of the directory
dirListing = os.listdir(inputDirectory)

# read each file and extract all the options related to the symbol

for inputFile in dirListing:
    inputFileDF = pd.DataFrame()
    try:
        print("processing file " + inputDirectory + inputFile)
        inputFileDF = pd.read_csv(inputDirectory + inputFile)
    except:
        print(inputFile + 'file does not exist')
    
    #print("Columns in the file")
    #print(inputFileDF.columns)

    underlyingSymbolOptions = inputFileDF[inputFileDF["UnderlyingSymbol"] == underlyingSymbol]
    outputFileName = underlyingSymbol + inputFile

    # write to the output 
    underlyingSymbolOptions.to_csv(outputDirectory + outputFileName, index=False, header= True)


