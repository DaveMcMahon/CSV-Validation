#!/usr/bin/python

import urllib2
import os
import zipfile
import csv

urlOfFileName = "http://spatialkeydocs.s3.amazonaws.com/FL_insurance_sample.csv.zip"
localZipFilePath = "/Users/dave/Documents/FL_insurance_sample.csv.zip"
localExtractFilePath = "/Users/dave/Documents/files/"
webRequest = urllib2.Request(urlOfFileName)

try:
    page = urllib2.urlopen(webRequest)
    content = page.read()

    output = open(localZipFilePath, "wb")
    output.write(bytearray(content))
    output.close()
except urllib2.HTTPError, e:
    print(e.fp.read())

if os.path.exists(localZipFilePath):
    print("Cool! " + localZipFilePath + " exists..proceeding..")
    listOfFiles = []

    fh = open(localZipFilePath, "rb")
    zipFileHandler = zipfile.ZipFile(fh)

    for fileName in zipFileHandler.namelist():
        if fileName.endswith(".csv"):
            zipFileHandler.extract(fileName, localExtractFilePath)
            listOfFiles.append(localExtractFilePath + fileName)
            print("Extracted " + fileName + " from the zip file to " + (localExtractFilePath + fileName))
    print("In total we extracted " + str(len(listOfFiles)) + " files")
    fh.close()

    csvFile = listOfFiles[0]
    lineNum = 0
    listOfLists = []   #policyID(0), statecode(1), county(2)

    with open(csvFile, "rU") as file:
        lineReader = csv.reader(file, delimiter=",", quotechar="\"")

        for row in lineReader:
            lineNum = lineNum+1
            if lineNum == 1:
                continue

            policyID = row[0]
            statecode = row[1]
            county = row[2]

            resultRow = [policyID,statecode,county]
            listOfLists.append(resultRow)

    print("Iteration of csv file complete - file is now closed!")

    listOfListsSortedByPolicy = sorted(listOfLists, key=lambda x:x[0], reverse=False)

    x = 0
    for elem in listOfListsSortedByPolicy:
        if( x == 10 ):
            break
        x = x + 1
        print(elem)









