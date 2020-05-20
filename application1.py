import csv
from tempfile import NamedTemporaryFile
import shutil
from flask import Flask, session, render_template, request,redirect,url_for
import pandas as pd
app = Flask(__name__)
song_database = 'songs1.csv'

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

def search1(hash_table, key):
    hash_key = hash(key) % len(hash_table)    
    bucket = hash_table[hash_key]
    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            return v
 


@app.route("/")
def index():
    return render_template("index.html")

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
    insert(hash_table,id,{'song':name,'artist':artist,'date':date})

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
 id=request.form.get('id');
 ans=search1(hash_table,id)
 return render_template('searchresults.html',v=ans)




@app.route("/submitupdate",methods=["POST"])
def update():
 id=request.form.get('id')
 song=request.form.get('song')
 artist=request.form.get('artist')
 album=request.form.get('album')
 date=request.form.get('date')

 insert(hash_table,id,{'song':song,'artist':artist,'date':date})
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
     with open(song_database, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(updated_data)
     return redirect(url_for('display'))
  else:
    return "Error 404:NOT FOUND"
