import csv
import os.path
import time
import datetime
from datetime import datetime

# read a file 
filePath = "z:\\bb_options_20020208.csv"

fileHandle = open(filePath)
csvFile = csv.reader(fileHandle)

print("CSV File rows = ")

rowCount = sum(1 for row in csvFile)

print(rowCount)


# read the list of files to be processed

# loop on each file

# within each file get the symbol and stick it to the correct output file

