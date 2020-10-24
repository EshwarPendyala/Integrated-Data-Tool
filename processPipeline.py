#######################################################################################
#Imports

import os
import dask.dataframe as dd
import numpy as np
from datetime import datetime
import json
import pandas as pd
from dateutil.parser import parse

#######################################################################################

class Pipeline:

    def metadataStore(self, typeOfMetadata, propertyOfMetadata, tableName):
        cwdir = os.getcwd()
        metadataPath = os.path.join(cwdir, r'Metadata_Store')
        if not os.path.exists(metadataPath):
            os.makedirs(metadataPath)

        typeOfMetadataPath = os.path.join(metadataPath, typeOfMetadata)
        if not os.path.exists(typeOfMetadataPath):
            os.makedirs(typeOfMetadataPath)

        fileMetadataPath = os.path.join(typeOfMetadataPath, tableName)
        if not os.path.exists(fileMetadataPath):
            os.makedirs(fileMetadataPath)
        return fileMetadataPath

#######################################################################################

    def columnTechnicalMetadataExtraction(self, fileName, ddf):
        tableName = fileName[:-4]
        numberOfDistinctValues = 0
        numberOfRows = len(ddf)
        fileMetadataPath = self.metadataStore('Technical_Metadata', 'Column_Metadata', tableName)
        filePath = str(fileMetadataPath+"/column_metadata.json")

        tokenOpen = '['
        with open(filePath, "w") as jsonFormatAppend:
            jsonFormatAppend.seek(0, 0)
            jsonFormatAppend.write(tokenOpen)

        for index in range(len(ddf.columns)):
            columnName = ddf.columns.tolist()[index]
            missingValueCount = int(ddf[columnName].isna().sum().compute())
            dataType = str(ddf.dtypes[index])

            if dataType == 'int64' or dataType == 'float64':
                if numberOfRows != missingValueCount:
                    meanValue = float(ddf[columnName].mean().compute())
                    standardDeviation = float(ddf[columnName].std().compute())
                    maxValue = float(ddf[columnName].max().compute())
                    minValue = float(ddf[columnName].min().compute())
                maxLengthOfString = 'Not Applicable'
                numberOfDistinctValues = int(ddf[columnName].nunique().compute())

            else:
                sampleData = ddf[columnName].dropna()
                sampleData = sampleData.head(4)
                
                for rowIndex in sampleData:
                    try:
                        dataType = ddf[columnName].astype('M8[us]').dtype
                        parse(rowIndex)
                    except Exception as e:
                        dataType = "string"

                meanValue = 'Not Applicable'
                maxValue = 'Not Applicable'
                minValue = 'Not Applicable'
                standardDeviation = 'Not Applicable'
                maxLengthOfString = ddf[columnName].str.len().max().compute()

            jsonData = {"columnName": str(columnName), "dataType": str(dataType), "missingValueCount": missingValueCount,"meanValue": str(meanValue), "maxValue": str(maxValue), "minValue": str(minValue), "maxLengthOfString": maxLengthOfString,"numberOfDistinctValues":numberOfDistinctValues,"standardDeviation":str(standardDeviation),"tableName":tableName}
            with open(filePath, "a") as initData:
                json.dump(jsonData, initData)
            if index != len(ddf.columns)-1:
                newLine = '\n'
                with open(filePath, 'a') as addNewLine:
                    addNewLine.write(newLine)
        
        tokenClose = ']'
        with open(filePath,"a") as jsonFormatAppend:
            jsonFormatAppend.seek(0,0)
            jsonFormatAppend.write(tokenClose)

#######################################################################################

    def tableTechnicalMetadataExtraction(self, fileName,ddf):
        tableName = fileName[:-4]
        numberOfColumns = len(ddf.columns)
        numberOfRows = len(ddf)
        jsonData = {'tableName':tableName,'numberOfColumns':numberOfColumns,'numberOfRows':numberOfRows}
        fileMetadataPath = self.metadataStore('Technical_Metadata','Table_Metadata',tableName)
        filePath = str(fileMetadataPath+"/table_metadata.json")
        with open(filePath,"w") as initData:
            json.dump(jsonData,initData)

#######################################################################################
