#!/usr/bin/python

import urllib2
import os
import zipfile
import csv
import xlsxwriter

listOfLists = []
urlOfFileName = "http://spatialkeydocs.s3.amazonaws.com/FL_insurance_sample.csv.zip"
localZipFilePath = "/Users/dave/Documents/FL_insurance_sample.csv.zip"
localExtractFilePath = "/Users/dave/Documents/files/"

def main():
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
        try:
            print("Cool! " + localZipFilePath + " exists..proceeding..")
            createMatrix()
            createWorkbook( "Summary_Results.xlsx", "Summary Tab" )
        except:
            print(sys.exc()[0])


def createWorkbook(wbTitle, wsTitle):
    workBook = xlsxwriter.Workbook(wbTitle)
    worksheet = workBook.add_worksheet(wsTitle)

    worksheet.write_row("A1", ["Summary of Policy Numbers"])
    worksheet.write_row("A2", ["PolicyID", "State Code", "County"])

    listOfListsSortedByPolicy = sorted(listOfLists, key=lambda x:x[0], reverse=False)


    for rowNum in range(10):
        eachRow = listOfListsSortedByPolicy[rowNum]
        worksheet.write_row("A" + str( rowNum + 3 ), eachRow )

    workBook.close()

def createMatrix():
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

    lineNum = 0
    csvFile = listOfFiles[0]

    with open(csvFile, "rU") as file:
        lineReader = csv.reader(file, delimiter=",", quotechar="\"")

        for row in lineReader:
            lineNum = lineNum + 1
            if lineNum == 1:
                continue

            policyID = row[0]
            statecode = row[1]
            county = row[2]

            resultRow = [policyID,statecode,county]
            listOfLists.append(resultRow)

    print("Iteration of csv file complete - file is now closed!")


if ( __name__ == '__main__' ):
    main()
