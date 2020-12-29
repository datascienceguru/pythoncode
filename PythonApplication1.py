import csv
import os.path

#filepath = "Y:\\Output\\SPX\\SPX020817P00860000.csv"
#print(filepath)

#dirContent = os.listdir("Y:")

#print(dirContent)

fileExists = os.path.isfile("Y:\\SPX\\SPX020817P00860000.csv")

if (fileExists == False):
    print ("File Does not exist")
else:
    fileHandle = open('Y:\\SPX\\SPX020817P00860000.csv')
    csvFile = csv.reader(fileHandle)
    
    outputFile = open('test.csv', 'w', newline='')
    #header = ['UnderlyingSymbol','UnderlyingPrice','Exchange',"OptionRoot","OptionExt","Type","Expiration", "DataDate","Strike","Last","Bid","Ask","Volume","OpenInterest","T1OpenInterest"]
    #header = 'UnderlyingSymbol,UnderlyingPrice,Exchange,OptionRoot,OptionExt,Type,Expiration, DataDate,Strike,Last,Bid,Ask,Volume,OpenInterest,T1OpenInterest'
    writer = csv.writer(outputFile)
    
    #writer.writerow(header)
    
    for row in csvFile:
        print(row)
        writer.writerow(row)
    outputFile.close()
    fileHandle.close()


    



print("Python using Visual studio")


