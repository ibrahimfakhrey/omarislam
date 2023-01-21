from flask import  Flask,render_template
import requests
from datetime import date

key="868c5469fc5add3122d3e7e8313c8f3e"
url="https://api.openweathermap.org/data/2.5/weather"
paramaters={
    "lon":"31.187016",
    "lat":"30.449173",
    "appid":key
}
app = Flask(__name__)

name="omar"

today = date.today()


d2 = today.strftime("%B %d, %Y")
print(d2)

@app.route('/')
def hi():
    response = requests.get(url=url, params=paramaters)
    data = response.json()
    temp_inc = int(data["main"]["temp"]) - 273.15
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    return  render_template("index.html",nm=int(temp_inc),d=d2)



@app.route('/<name>')
def by(name):
    return name

if __name__=="__main__":
    app.run(debug=True)