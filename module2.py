import csv
import os.path
import time
import datetime
from datetime import datetime

# read a file 
filePath = "z:\\bb_options_20020208"

fileHandle = open(filePath)
csvFile = csv.reader(fileHandle)

print("CSV File rows = ")

print(len(csvFile))
