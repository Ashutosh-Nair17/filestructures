import jinja2
import pandas as pd
import csv
from flask import Flask, session, render_template, request,redirect,url_for
app = Flask(__name__)


@app.route("/")
def display():
	data=pd.read_csv("songs.csv")
	result=list(data.values)
	print(result)
	return render_template('display.html',songs=result)

