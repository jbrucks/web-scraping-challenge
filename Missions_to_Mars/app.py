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

    mars_parts = sprape_mars.mars_scrape()

    # mars_parts = {
    #     'news_title': scrape_mars.mars_news_scrape(),
    #     'feature_photo_url' : scrape_mars.mars_feature_img_scrape(),
    #     'mars_weather' : scrape_mars.mars_weather(),
    #     'mars_html_table' : scrape_mars.mars_facts(),
    #     'hemisphere_img_urls' : scrape_mars.mars_hemis()
    # }

    mars_info.update({}, mars_parts, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
