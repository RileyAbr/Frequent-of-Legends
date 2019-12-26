import requests
import json
import time
import pymongo
import cassiopeia as cass
from RIOTAPIKEY import key

# Cassioepeia info
RIOTAPIKEY = key
cass.set_riot_api_key(RIOTAPIKEY)
cass.set_default_region("NA")

print(time.time())
sum_name = '' #Set this to a Summoner you would like to look up
sum = cass.get_summoner(name=sum_name)

new_match = cass.get_match_history(sum)

print(new_match)
