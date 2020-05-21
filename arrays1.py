
import pickle

with open('hashtable.data', 'rb') as filehandle:
    # read the data as binary data stream
    placesList = pickle.load(filehandle)
print(placesList)

def search1(hash_table, key):
    hash_key = hash(key) % len(hash_table)    
    bucket = hash_table[hash_key]
    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return v
            print(v)

print(search1(placesList,1))
print(search1(placesList,2))            