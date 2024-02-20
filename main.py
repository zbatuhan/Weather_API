from flask import Flask, render_template
import pandas as pd

#Creating app using flask
app = Flask(__name__)

#Define home page URL
@app.route("/")
def home():
    
    file = "data/stations.txt"
    df = pd.read_csv(file, skiprows=17)
    
    return render_template("main_page.html", data=df.to_html())

#Define api page URL
@app.route("/api/v1/<station>/<date>")
def api(station, date):
    file = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    
    #data processing
    df = pd.read_csv(file, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    
    #return values as JSON
    return {
        "station": station,
        "date": date,
        "temperature": temperature
    }

#Define station information page
@app.route("/api/v1/<station>/")
def stations_data(station):
    
    file = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(file, skiprows=20, parse_dates=["    DATE"])
    #change display format
    result = df.to_dict(orient="records")
    
    return result    

#Define year filter for data
@app.route("/api/v1/year/<station>/<year>")
def query_year(station, year):
    
    file = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(file, skiprows=20)
    #filter df using "startswith" for year
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    
    return result


#Allow to you see if there is any issue "TRUE"
if __name__ == "__main__":
    app.run(debug=True)
    