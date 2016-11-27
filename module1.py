import csv
import os.path
import time
import datetime
from datetime import datetime

# set the root path for file directory
dirRoot = "Y:\\SPX\\"

def writeToOutput(fullFileName):
    outputDir = "c:\\OptionAnalysis\\"
    fileHandle = open(filePath)
    csvFile = csv.reader(fileHandle)
    
    getExpiration = True

    outputFileName = None
    outputFileHandle = None
    writer = None

    for row in csvFile:

        if getExpiration:                

            optionExpiry = datetime.strptime(row[6], "%m/%d/%Y")

            outputFileName = outputDir + str(optionExpiry.year) + "_" + str(optionExpiry.month) + "_" + str(optionExpiry.day)+ ".csv"
            getExpiration = False

        
            outputFileExists = os.path.isfile(outputFileName)

            if outputFileExists == False:
                # open the file and add the header to it
                outputFileHandle = open(outputFileName, 'w', newline='')
                writer = csv.writer(outputFileHandle,delimiter = ",")
                header = ['UnderlyingSymbol','UnderlyingPrice','Exchange',"OptionRoot","OptionExt","Type","Expiration", "DataDate","Strike","Last","Bid","Ask","Volume","OpenInterest","T1OpenInterest"]
                writer.writerow(header)
                outputFileHandle.close()

        if outputFileHandle == None:
            outputFileHandle = open(outputFileName, 'a', newline='')
            writer = csv.writer(outputFileHandle,delimiter = ",")

        if outputFileHandle.closed:
            outputFileHandle = open(outputFileName, 'a', newline='')
            writer = csv.writer(outputFileHandle,delimiter = ",")
 
        writer.writerow(row)
    outputFileHandle.close()    
    fileHandle.close()



###### Main function ####
# list the contents of that directory

dirContents = os.listdir(dirRoot)

print(len(dirContents))

#for fileName in dirContents:
#    print(fileName)
for eachFile in dirContents:
    filePath = dirRoot+str(eachFile)
    print(filePath)
    writeToOutput(filePath)


print("Done")
