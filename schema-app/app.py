
# *-* coding:utf-8*-*
# Laddar in alla ramverk.
from flask import Flask, render_template, redirect, url_for, request, flash, Response, jsonify
import urllib.request
from bs4 import BeautifulSoup
import pymysql.cursors
import unicodedata
import json
import urllib.parse

#  c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb

# https://api.resrobot.se/v2/location.name?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&input=Helsingborg
# HITTA STATIONS ID

# https://api.resrobot.se/v2/trip?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&originId=740000001&destId=740000002&format=json
# SÖK EFTER RESA

# Konfigurerar applikationen (VIKTIGT- SE TILL SÅ ATT SECREY_KEY ÄR RANDOM VID LAUNCH)
app = Flask(__name__)

# --------------------------------------------------------------------------------------------------------------------------

@app.route('/index.html')
@app.route('/index')
@app.route('/')
def home():
    return render_template("index.html")



@app.route('/get_mashup')
def get_mashup():
    station="Hässleholm"
    station = urllib.parse.quote_plus(station, safe='', encoding=None, errors=None)
    stationLink = "https://api.resrobot.se/v2/location.name?key=c98b8eb7-fc20-4d45-b3a9-d65189e5a8cb&format=json&input=" + station
    response = urllib.request.urlopen(stationLink).read()
    response = response.decode("utf-8")
    

    jsonList = []



# --------------------------------------------------------------------------------------------------------------------------
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(port = 8080, debug=True, threaded = True)
