from flask import render_template, Flask, url_for, request, redirect
from chatterbot import ChatBot
from hazardlyBot import myChatBot
from armourBot import armBot
import sqlite3 as sql
from textComms import volunteeringquery, messagequery
from stats import get_region_insights, get_habitat_score_within, get_hospitals_within
import json
dbConn = sql.connect('calamitigator.db')

try:
    c = dbConn.cursor()
    c.execute(""" CREATE TABLE population (
        Firstname text NOT NULL,
        Lastname text NOT NULL,
        Phonenumber text NOT NULL PRIMARY KEY,
       Email text NOT NULL,
        location text NOT NULL,
        Emergencycontact integer NOT NULL,
        ProfilePicture blob,
        Voluntering bool NOT NULL
    )""")
    dbConn.execute("CREATE TABLE hazardly (datetime TEXT NOT NULL, phoneNum TEXT NOT NULL, "
                  "location TEXT NOT NULL, description TEXT NOT NULL) ")
    dbConn.execute("CREATE TABLE armour (datetime TEXT NOT NULL, phoneNum TEXT NOT NULL, "
                  "location TEXT NOT NULL, description TEXT NOT NULL) ")

    dbConn.commit()
    dbConn.close()

except sql.OperationalError:
    print('something')




app = Flask(__name__)



class SeshData():
    def __init__(self, currentBot):
        self.currentBot = currentBot


simple_line_icons = "vendors/simple-line-icons/css/simple-line-icons.css"
flag_icons = "vendors/flag-icon-css/css/flag-icon.min.css"
bundle = "vendors/css/vendor.bundle.base.css"
styles = "css/style.css"
styles2 = "css/styes2.css"

sesh = SeshData('flag')
css = [simple_line_icons, flag_icons, bundle, styles]

favicon = "images/favicon.png"

bundlejs = "js/vendor.bundle.base.js"
canvas = "js/off-canvas.js"
misc = "js/misc.js"
charts = "vendors/chart.js/Chart.min.js"
moment = "vendors/moment/moment.min.js"
name = "Hackers@A'beckett"

js = [bundlejs, canvas, misc]


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@app.route('/home')
def index():
    return render_template('index.html', css=css, favicon=favicon, js=js,
                           name=name)


@app.route("/maps")
def mapsss():
    return render_template("pages/lucifer/maps.html", css=css, favicon=favicon, js=js)


@app.route("/insights")
def insight():
    return render_template("pages/insights/insight.html", css=css, favicon=favicon, js=js)


@app.route("/emergency")
def emergency():
    return render_template("pages/emergency/emergency.html", css=css, favicon=favicon, js=js)


@app.route("/updateBot")
def update_bot_name():
    sesh.currentBot = request.args.get('botName')
    print(sesh.currentBot)
    return str(sesh.currentBot)


@app.route("/getMyBot")
def get_bot_naem():
    return str(sesh.currentBot)


@app.route("/gethazardly")
def get_bot_response():
    print(request.args)
    userText = request.args.get('msg')
    return str(myChatBot.get_response(userText))


@app.route("/getarmour")
def get_arm_response():
    print(request.args)
    userText = request.args.get('msg')
    return str(myChatBot.get_response(userText))

@app.route("/getCoords")
def getCoords():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    target  = request.args.get('target')

    if(target=='insights'):
       obj = json.load(get_region_insights(lat, lon))
       return insight
    elif target== 'insightsandvolunteers':
        obj = json.load(get_region_insights(lat, lon))
        volun  = str(volunteeringquery())
        newObj = {'insights':obj, 'vol':volun}
        return newObj
    elif target == 'personal':
        countHospt = get_hospitals_within((lat, lon))
        return render_template('index.html', css=css, favicon=favicon, js=js,
                           name=name)

    return redirect("/emergency")

@app.route("/sendMessage")
def send():
    messagequery()
    return 1

if __name__ == "__main__":
    app.run(debug=True)
