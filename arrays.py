import pickle

# define a list of places
hash_table = [[] for _ in range(15)]

def insert(hash_table, key, value):
    hash_key = hash(key) % len(hash_table)
    key_exists = False
    bucket = hash_table[hash_key]    
    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            key_exists = True 
            break
    if key_exists:
        bucket[i] = ((key, value))
    else:
        bucket.append((key, value))

def delete1(hash_table, key):
    hash_key = hash(key) % len(hash_table)    
    key_exists = False
    bucket = hash_table[hash_key]
    for i, kv in enumerate(bucket):
        k, v = kv 
        if key == k:
            key_exists = True 
            break
    if key_exists:
        del bucket[i]


insert(hash_table,1,{'1':'lolwa','2':'lel'})
insert(hash_table,2,{'5':'lolwa','6':'lel'})
insert(hash_table,1,{'1':'qhdhqud'})
with open('listfile.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(hash_table, filehandle)