import sys
import numpy as np
import pandas as pd

from pandas import DataFrame, Series 

print (sys.argv)

D = {}
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))

#print( "first argument", sys.argv[0])

# read the test file
optionFile = pd.read_csv(sys.argv[1])

applRow = optionFile[optionFile.UnderlyingSymbol == sys.argv[2]]

D[sys.argv[2]] = applRow

applRow1 = optionFile[optionFile.UnderlyingSymbol == sys.argv[3]]

D[sys.argv[3]] = applRow1

#if( sys.argv[4] in D.keys()):
#    print(D[sys.argv[4]])
#else:
#    print("boooo")

print(type(applRow1))

expirationDates = applRow1.Expiration.unique()

print('Options with expiration ' + expirationDates[0])

optionForTheExpiration = applRow1[applRow1.Expiration == expirationDates[0]]
print(optionForTheExpiration)