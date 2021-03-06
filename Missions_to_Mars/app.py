# import necessary libraries
from flask import Flask, render_template
from flask_table import Table, Col
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():

    mars = mongo.db.mars_data.find_one()

    if (mars):
        return render_template("index.html", mars_data=mars)
    else:
        mars = mongo.db.mars_data
        mars_data = scrape_mars.scrape()
        mars.update({}, mars_data, upsert=True)
        return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars_data
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)

    return render_template("index.html", mars_data=mars_data)


if __name__ == "__main__":
    app.run(debug=True)