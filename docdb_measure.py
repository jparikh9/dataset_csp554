# -*- coding: utf-8 -*-
"""docdb_measure.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jspPuvAm2ByZCDgf-y1xSRst_mllJt8D
"""

from pymongo import MongoClient
import time

# details of documentdb database for connection string
DB_CLUSTER_ENDPOINT = 'docdb-2023-12-02-21-57-48.cluster-cwxr4ybijym6.us-east-2.docdb.amazonaws.com'
DB_PORT = 27017
DB_NAME = 'myntraProductsDB'
DB_USER = 'jinit009'
DB_PASSWORD = 'bigdataDocdb'

# Connecting to AWS DocumentDB
client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_CLUSTER_ENDPOINT}:{DB_PORT}/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false")
database = client[DB_NAME]
collection = database['products']

def measure_read(pid):
  start_time = time.time()
  # Perform Read operation
  read_document = collection.find_one({"ProductID": pid})
  end_time = time.time()
  read_time = round((end_time - start_time)*1000,2)
  print(f"Read operation took {read_time} ms")
  print(read_document)

def measure_write(doc):
  count = collection.count_documents({})
  print("Count before insert:",count)
  start_time = time.time()
  # Perform Create operation
  new_document = doc
  collection.insert_one(new_document)
  end_time = time.time()
  create_time = round((end_time - start_time)*1000,2)
  print(f"Create operation took {create_time} ms")
  count = collection.count_documents({})
  print("Count after insert:",count)

def measure_delete(pid):
  count = collection.count_documents({})
  print("Count before delete:",count)
  start_time = time.time()
  # Perform Delete operation
  delete_query = {"ProductID": pid}
  collection.delete_one(delete_query)
  end_time = time.time()
  delete_time = round((end_time - start_time)*1000,2)
  print(f"Delete operation took {delete_time} ms")
  count = collection.count_documents({})
  print("Count after delete:",count)

def measure_update(pid, key_value):
  start_time = time.time()
  update_query = {"ProductID": pid}
  update_data = {"$set": key_value}
  collection.update_one(update_query, update_data)
  end_time = time.time()
  update_time = round((end_time - start_time)*1000,2)
  print(f"Update operation took {update_time} ms")
  measure_read(pid)

# Measure time for CRUD operations

print("\n")
measure_read(10138615)
time.sleep(5)
print("\n")
measure_write({"ProductID": 999999, "ProductName":"Jeans", "ProductBrand":"levis","Gender":"Men","Price (INR)":2500, "NumImages":4, "Description":"old school straight jeans","PrimaryColor":"Navy Blue"})
time.sleep(5)
print("\n")
measure_update(999999, {"Price (INR)": 2600})
time.sleep(5)
print("\n")
measure_delete(999999)

client.close()