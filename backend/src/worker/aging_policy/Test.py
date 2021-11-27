import os
from pymongo import *

from bson.json_util import dumps



client = MongoClient('10.50.34.37', 27017)

# client = MongoClient(os.environ['CHANGE_STREAM_DB'])
change_stream = client.sdn01.flow_routing.watch()
for change in change_stream:
    print(dumps(change))
    print('') # for readability only