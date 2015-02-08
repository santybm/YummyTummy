from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request

import settings_local
import calendar
import operator
import json
import urllib 
from FreqAnalysis import freqAnaysis
from parse_rest.connection import register
from datetime import datetime
from parse_rest.datatypes import Object as ParseObject
from top import recEngine



app = Flask(__name__)

@app.route('/')   #give it a route, define functions underneath
def index():
    
    return render_template("index.html")  #render template returns html files




@app.route("/check")
def check():
    #name = request.args.get('name')
    #time = request.args.get('time')
    #location = request.args.get('location')
    
    t = datetime(2015,02,06,19,00) # will have to reassign time dynamically
    
    top_five = recEngine(t, 'Abbey Kaelberer', 'Baystate', 5).recommends() # attach recommends to recEngine, last param specifies the best items
    print top_five

    topFiveDict = {}
    for item in top_five:
        name,value = item
        topFiveDict[name] = value

    print (topFiveDict)

    """item_name = [top_five[x][0] for x in range(5)]
    print item_name
    
    item_freq = [top_five[x][1] for x in range(5)]
    print item_freq
    
    pre_json = {}
    for x in range(5):
        pre_json[item_name[x]] = item_freq[x]
        #print pre_json, pre_json[item_name[x]]"""
    
    
    return json.dumps(topFiveDict)

if __name__ == '__main__': # has to be the last line
    app.run(debug=True)


