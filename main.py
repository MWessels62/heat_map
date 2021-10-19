import data as D
from flask import Flask,  render_template, request, redirect, url_for
import requests

#initialize flask ap
app = Flask(__name__)
page = requests.get("https://www.worldometers.info/coronavirus")



#create route for home page
@app.route('/', methods=["GET","POST"])
def home():
    obj = D.getData(page)
    obj1 = obj.scrape()
    cont_data = obj1[1]
    data_frame = obj1[2]
    all_data = obj1[0]
    country_data = obj1[3]
   
    if request.method == "GET":
        return render_template('home.html', country = country_data)
    return render_template('home.html', country = country_data)
if __name__ == "__main__":
    app.run(debug=True)