from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
mongo = PyMongo(app)



@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)

@app.route("/scrape")
def scrape():  
    mars_info = mongo.db.mars_info  

    mars_parts = scrape_mars.mars_news_scrape()
    mars_parts = scrape_mars.mars_feature_img_scrape()
    mars_parts = scrape_mars.mars_weather()
    mars_parts = scrape_mars.mars_facts()
    mars_parts = scrape_mars.mars_hemis()

    mars_info.update({}, mars_parts, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
