import os
import dask.dataframe as dd
import processPipeline as pp
import json
import ElasticsearchInsertion as els
import shutil

class InputPlugin:
    ddfDataForPipeline = {}
    def getAWSData(self,sourceLink):
        print("AWS Data")
    
    def getGCPData(self,sourceLink):
        print("GCP Data")
    
    def getMySQLData(self,sourceLink):
        print("MySQL Data")
    
    def createDataframes(self,sourceLink):
        filesList = {}
        for file in os.listdir(sourceLink):
            ddf = dd.read_csv(sourceLink+''+file,sep='\t')
            filesList.update({file:ddf})
            self.ddfDataForPipeline = filesList
    
    def processDataframes(self):
        pipelineObject = pp.Pipeline()
        for i in self.ddfDataForPipeline:
            pipelineObject.columnTechnicalMetadataExtraction(i,self.ddfDataForPipeline[i])
            pipelineObject.tableTechnicalMetadataExtraction(i,self.ddfDataForPipeline[i])

    # def generateListOfDatasets(self):
    #     listOfDatasets = []
    #     for file in os.listdir("/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/Technical_Metadata/"):
    #         listOfDatasets.append(file)

    #     listOfDatasets.remove(".DS_Store")
    #     listOfDatasets.remove(".DS_S")

    #     with open("listOfFiles.json","w") as output:
    #         json.dump(listOfDatasets,output,indent=4)

###############################################################################
#Metadata Generation
try:
    dataAccessObject = InputPlugin()
    dataAccessObject.createDataframes('/Users/eshwarpendyala/Desktop/tool/data/')
    dataAccessObject.processDataframes()
    # dataAccessObject.generateListOfDatasets()
except Exception as metadataGenerationError:
    print("Error In Metadata Generation", metadataGenerationError)

###############################################################################
#Elasticsearch Indexing and Insertion
shutil.rmtree("/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/Technical_Metadata/.DS_S")
els.insertDataInElasticsearch()