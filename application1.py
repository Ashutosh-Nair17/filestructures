import csv
import pickle
from tempfile import NamedTemporaryFile
import shutil
from flask import Flask, session, render_template, request,redirect,url_for
import pandas as pd
app = Flask(__name__)
song_database = 'songs1.csv'


hash_table = [[] for _ in range(15)]
print(hash_table)

with open('hashtable.data', 'rb') as filehandle:
    # read the data as binary data stream
    hash_table= pickle.load(filehandle)
print(hash_table)

def insert(key, value):
    global hash_table
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

def search1(key):
    global hash_table
    print("inside search")
    print(hash_table)
    hash_key = hash(key) % len(hash_table)    
    bucket = hash_table[hash_key]
    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return v
 
def delete1( key):
    global hash_table
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





@app.route("/")
def index():
    return render_template("index.html")


@app.route('/hashtable',methods=["GET"])
def hashing():
    return render_template('hash.html',results=hash_table)

@app.route("/adpr")
def adpr():
    return render_template("add.html")




@app.route("/adpr/add",methods=["POST"])
def add():
    
    song_data = []
    id=request.form.get('id')
    song_data.append(id)
    name=request.form.get('name')
    song_data.append(name)
    artist=request.form.get('artist')
    song_data.append(artist)
    album=request.form.get('album')
    song_data.append(album)
    date=request.form.get('date')
    song_data.append(date)
    
    with open(song_database, "a", encoding="utf-8") as f:
                                        writer = csv.writer(f)
                                        writer.writerows([song_data])

    print(hash_table)
    # update the hash_table                                    
    insert(id,{'song':name,'artist':artist,'date':date})
    print(hash_table)   
    # update the hash_tabale permanently
    with open('hashtable.data', 'wb') as filehandle:
    # store the data as binary data stream
      pickle.dump(hash_table, filehandle)

    return redirect(url_for('adpr'))





@app.route("/display")
def display():
  data=pd.read_csv("songs1.csv")
  result=list(data.values)
  return render_template('display.html',songs=result)



@app.route("/s")
def searchdisplay():
    return render_template('search.html')



@app.route("/s/search",methods=["POST"])
def search():
 print(hash_table)
 id=request.form.get('id')
 ans=search1(id)
 print(ans)
 return render_template('searchresults.html',v=ans)




@app.route("/submitupdate",methods=["POST"])
def update():
 id=request.form.get('id')
 song=request.form.get('song')
 artist=request.form.get('artist')
 album=request.form.get('album')
 date=request.form.get('date')
 
 # updates the hash_tables key:value pair
 insert(id,{'song':song,'artist':artist,'date':date})

 # update the hash_table permanently
 with open('hashtable.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(hash_table, filehandle)

 # it will update the records file 'songs/songs1.csv'
 tempfile = NamedTemporaryFile(mode='w', delete=False)
 fields = ['id', 'song', 'artist', 'album','release-date']
 with open(song_database, 'r') as csvfile, tempfile:
  reader = csv.DictReader(csvfile, fieldnames=fields)
  writer = csv.DictWriter(tempfile, fieldnames=fields)
  for row in reader:
    if row['id'] == id:
      row['song'], row['artist'], row['album'], row['release-date'] = song, artist, album,date
    row = {'id': row['id'], 'song': row['song'], 'artist': row['artist'], 'album': row['album'], 'release-date':row['release-date']}
    writer.writerow(row)

 shutil.move(tempfile.name, song_database)
 return redirect(url_for('display'))



@app.route("/update")
def displayupdate():
 return render_template('update.html')



@app.route("/delete")
def delete():
        return render_template("delete.html")


@app.route("/submitdelete",methods=["POST"])
def submitdelete():

  id=request.form.get('id')
  student_found = False
  updated_data = []
  with open(song_database, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    counter = 0
    for row in reader:
      if len(row) > 0:
          if id != row[0]:
            updated_data.append(row)
            counter += 1
          else:
            student_found = True

  if student_found is True:
    # deletes the id from songs/songs1.csv
    with open(song_database, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(updated_data)
    # updates the hash_table
    delete1(id)
    # update in hash_table file
    print(hash_table)
    with open('hashtable.data', 'wb') as filehandle:
    # store the data as binary data stream
       pickle.dump(hash_table, filehandle)

    return redirect(url_for('display'))
  else:
    return "Error 404:NOT FOUND"
