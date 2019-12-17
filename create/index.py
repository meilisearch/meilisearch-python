import json
import time 
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import meilisearch


client = meilisearch.Client("http://127.0.0.1:7700", "123")
index = client.create_index(name="movies", uid="test_uid")
response = index.update_schema({
            'id': ['indexed','displayed','identifier'],
            'title':['displayed','indexed'],
            'poster':['displayed','indexed'],
            'overview':['indexed','displayed'],
            'release_date':['indexed','displayed', 'ranked']
        })

json_file = open('./datasets/movies.json')
data = json.load(json_file)
response = index.add_documents(data);
time.sleep(5)
response = index.add_settings({
        "rankingOrder": [
            "_sum_of_typos",
            "_number_of_words",
            "_word_proximity",
            "_sum_of_words_attribute",
            "_sum_of_words_position",
            "_exact",
            # "release_date"
        ]
        # "distinctField": "",
        # "rankingRules": {
        #     "release_date": "dsc"
        # }
    })