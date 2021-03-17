from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

# clear all existing data out of the collection.
# For demo purposes only, 
# you may not want to do this for an app you're building!
mongo.db.mars_dict.drop()

@app.route("/")
def index():
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars_dict=mars_dict)


@app.route("/scrape")
def scraper():
    mars_dict = mongo.db.mars_dict
    mars_dict_data = scrape_mars.scrape()
    mars_dict.update({}, mars_dict_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
