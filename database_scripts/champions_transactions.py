import requests
import json
from collections import defaultdict
import pymongo
import cassiopeia as cass
from DBKEYS import database_client
from RIOTAPIKEY import key

RIOTAPIKEY = key

# Database info
mongoclient = pymongo.MongoClient(database_client)
db = mongoclient.frequentoflegends
win_champs_col = db.winning_champs
loss_champs_col = db.losing_champs
win_champs_class_col = db.winning_champs_classifier
loss_champs_class_col = db.losing_champs_classifier

# Cassioepeia info
RIOTAPIKEY = key
cass.set_riot_api_key(RIOTAPIKEY)
cass.set_default_region("NA")


# No. of champions currently in game
number_of_champions = 146 #len(cass.get_champions())

# Transaction table of all champions by matches played. The format of the table is as follows:
#           Champ1 | Champ2 | Champ3| ...
#   Match1      1       0       0
#   Match2      0       1       1
#   Match3      1       1       1
#
# The 1 represents a match where the champion was played and won

winning_champs_transaction_table = []
losing_champs_transaction_table = []

# This stores the equivalent ID's of champions put into the transaction table. While there are 140+ champions in the game, some have ID's stretching as far as the 300's. This sytem allows us to instead create our own ID's in place

transaction_table_ids_lookup = list()

# DATABASE RETRIEVALS
winning_champs = []
for document in win_champs_col.find():  # Can use .limit(n) to reduce for testing
    winning_champs.append(document)

losing_champs = []
for document in loss_champs_col.find():  # Can use .limit(n) to reduce for testing
    losing_champs.append(document)

# TRANSACTION TABLE
for match in winning_champs:
    win_transaction = [0] * number_of_champions

    for champ in match.get('winning_champions'):
        if champ not in transaction_table_ids_lookup:
            transaction_table_ids_lookup.append(champ)

        champ_index = transaction_table_ids_lookup.index(champ)
        win_transaction[champ_index] = 1

    winning_champs_transaction_table.append(win_transaction)

for match in losing_champs:
    loss_transaction = [0] * number_of_champions

    for champ in match.get('losing_champions'):
        if champ not in transaction_table_ids_lookup:
            transaction_table_ids_lookup.append(champ)

        champ_index = transaction_table_ids_lookup.index(champ)
        loss_transaction[champ_index] = 1

    losing_champs_transaction_table.append(loss_transaction)

# Write transactions to files
win_file = open('win_transactions.txt', 'w')
win_file_class = open('win_transactions_classifier.txt', 'w')
print(*[champ.replace(' ', '')
        for champ in transaction_table_ids_lookup], file=win_file)
for match in winning_champs_transaction_table:
    match_classifier = [*match, 1]
    print(*match, file=win_file)
    print(*match_classifier, file=win_file_class)
win_file.close()
win_file_class.close()

loss_file = open('loss_transactions.txt', 'w')
loss_file_class = open('loss_transactions_classifier.txt', 'w')
print(*[champ.replace(' ', '')
        for champ in transaction_table_ids_lookup], file=loss_file)
for match in losing_champs_transaction_table:
    match_classifier = [*match, -1]
    print(*match, file=loss_file)
    print(*match_classifier, file=loss_file_class)
loss_file.close()
loss_file_class.close()
