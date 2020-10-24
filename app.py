from flask import Flask,request,jsonify
from flask_cors import CORS
import os
import json
import pandas as pd
from pathlib import Path
from time import sleep
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

app = Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
client = Elasticsearch("localhost:9200")

@app.route('/getlistofdatasets', methods=['POST'])
def getListOfDatasets():
	listOfDatasets = []
	with open("/Users/eshwarpendyala/Desktop/tool/tool/list_of_files.json") as fileList:
		listOfDatasets = json.load(fileList)
	response = jsonify(listOfDatasets)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

@app.route('/columnMetadata', methods=['POST'])
def getQueryText():
	queryText = request.data.decode('utf-8')[0]
	username = request.data.decode('utf-8')[1]
	data = getColumnMetadata(queryText,username)
	response = jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

def getColumnMetadata(queryText,username):
	print("LINE 35")
	for file in os.listdir('/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/Technical_Metadata/'):
		if queryText.lower() == file.lower():
			for data in os.listdir('/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/Technical_Metadata/'+file):
				with open('/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/Technical_Metadata/'+file+'/column_metadata.json',"r") as columnMetadata:
					column_metadata = json.load(columnMetadata)
			return column_metadata
	return ""

@app.route('/tableMetadata', methods=['POST'])
def getQueryTextFromFrontend():
	data = json.loads(request.data.decode('utf-8'))
	queryText = data["query"]
	username = data["username"]
	data = getTableMetadata(queryText,username)
	response = jsonify(data)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

def getTableMetadata(queryText,username):
	for file in os.listdir(f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'):
		if queryText.lower() == file.lower():
			for data in os.listdir(f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'+file):
				with open(f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'+file+'/table_metadata.json',"r") as tableMetadata:
					table_metadata = json.load(tableMetadata)
			return table_metadata
	return ""


@app.route('/validateUser', methods=['POST'])
def login():
	credentials = json.loads(request.data.decode('utf-8'))
	username = credentials['username']
	password = credentials['password']
	response = ""
	if username == 'ESHWAR':
		if password == 'ESHWAR':
			response = jsonify({'status':'success'})
	else:
		response = jsonify({'status':'failed'})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response

###################################################################
@app.route('/getColumnMetadata', methods=['POST'])
def QueryText():
	data = json.loads(request.data.decode('utf-8'))
	queryText = data["query"]
	username = data["username"]
	# url = f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'
	# print(url)
	print("*****************************************************************************************************************")
	# print(queryText)
	for file in os.listdir(f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'):
		if queryText.lower() == file.lower():
			for data in os.listdir(f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'+file):
				with open(f'/Users/eshwarpendyala/Desktop/tool/tool/Metadata_Store/{username}/Technical_Metadata/'+file+'/column_metadata.json', "r") as columnMetadata:
					column_metadata = json.load(columnMetadata)
	response = jsonify(column_metadata)
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response
app.run()
