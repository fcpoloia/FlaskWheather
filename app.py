from flask import Flask, redirect, request, render_template
import requests
import json

def to_direction(degree):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                  'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    idx = int((degree / 22.5) + 0.5) % 16
    return directions[idx]

def fetch(loc):
    response = requests.request("GET",f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{loc}?unitGroup=metric&key=US22YBYLSJNC28D2ETFPYN7KU&contentType=json")
    if response.status_code != 200:
        return f":( {response.status_code}"
    else: return response.json()

app = Flask(__name__)
data = {}

@app.context_processor
def utility_processor():
    return dict(tD=to_direction)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        loc = request.form['location']
        data = fetch(loc)
        if type(data) == str:return data
        else:
            return render_template("display.html",
                desc=data["description"],
                days=data["days"],
                days_ammount=len(data["days"],
                )
            )
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
