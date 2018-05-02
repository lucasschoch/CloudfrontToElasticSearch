from __future__ import print_function
from pprint import pprint
import boto3
import json
import zlib
import datetime
from itertools import groupby


from elasticsearch import Elasticsearch, RequestsHttpConnection
from StringIO import StringIO

import urllib
import json

s3 = boto3.client('s3')
now = datetime.datetime.now()
cfindex = 'cloudfront-' + str(now.year) + '-' + str(now.month)

print('Loading function')

indexDoc = {
    "dataRecord" : {
        "properties" : {
          "logdate" : {
            "type" : "string"
          }, 
          "logtime" : {
            "type" : "string"
          },
          "edge" : {
            "type" : "string"
          },
          "bytessent" : {
            "type" : "float"
          },
          "cip" : {
            "type" : "string"
          },
          "method" : {
            "type" : "string"
          },
          "host" : {
            "type" : "string"
          },
          "uri" : {
            "type" : "string"
          },
          "status" : {
            "type" : "string"
          },
          "creferrer" : {
            "type" : "string"
          },
          "useragent" : {
            "type" : "string"
          },
          "cs_uri_query" : {
            "type" : "string"
          },
          "cookie" : {
            "type" : "string"
          },
          "x_edge_result_type" : {
            "type" : "string"
          },
          "x_edge_request_id" : {
            "type" : "string"
          },
          "x_host_header" : {
            "type" : "string"
          },
          "protocol" : {
            "type" : "string"
          },
          "cs_bytes" : {
            "type" : "string"
          },
          "time_taken" : {
            "type" : "float"
          }
        }
      },
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
      }
    }


def connectES(esEndPoint):
    print ('Connecting to the ES Endpoint {0}'.format(esEndPoint))
    try:
        esClient = Elasticsearch(
            hosts=[{'host': esEndPoint, 'port': 443}],
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection)
        return esClient
    except Exception as E:
        print("Unable to connect to {0}".format(esEndPoint))
        print(E)
        exit(3)

def createIndex(esClient):
    try:
        res = esClient.indices.exists(cfindex)
        if res is False:
            esClient.indices.create(cfindex, body=indexDoc)
	    return 1
    except Exception as E:
            print("Unable to Create Index {0}".format(cfindex))
            print(E)
            exit(4)

def indexDocElement(esClient,key,response):
    try:
	print('----------------Intro-----------------')
        body = response['Body']
        data = body.read()
        data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
        x = 0
        for line in data.splitlines():
            if x >= 2:
                retval = esClient.index(index=cfindex, doc_type='YOUR-DOC-TYPE', body={
                 'logdate': line.split('\t')[0],
                 'logtime': line.split('\t')[1],
                 'edge': line.split('\t')[2],
                 'bytessent': float(line.split('\t')[3]),
                 'cip': line.split('\t')[4],
                 'method': line.split('\t')[5],
                 'host': line.split('\t')[6],
                 'uri': line.split('\t')[7],
                 'status': line.split('\t')[8],
                 'creferrer': line.split('\t')[9],
                 'useragent': line.split('\t')[10],
                 'cs_uri_query': line.split('\t')[11],
                 'cookie': line.split('\t')[12],
                 'x_edge_result_type': line.split('\t')[13],
                 'x_edge_request_id': line.split('\t')[14],
                 'x_host_header': line.split('\t')[15],
                 'protocol': line.split('\t')[16],
                 'cs_bytes': line.split('\t')[17],
                 'time_taken': float(line.split('\t')[18])
                })
            else:
                x += 1
	print('----------------Final-----------------')
    except Exception as E:
	print("Document not indexed")
	print("Error: ",E)
	exit(5)	
	  


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    esClient = connectES("search-YOUR-DOMAIN-ADDRESS.sa-east-1.es.amazonaws.com")
    createIndex(esClient)

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
	indexDocElement(esClient,key,response)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
