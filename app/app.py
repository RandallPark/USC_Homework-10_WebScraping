from flask import Flask, jsonify, render_template, redirect
import scrape_mars 
from scrape_mars import scrape_info
from flask_pymongo import PyMongo

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
marsdb_connect = PyMongo(app, uri="mongodb://localhost:27017/mars_info")

scraped_data = {}

@app.route("/")
def home():
    # Find one record of data from the mongo database
    scraped_data = marsdb_connect.db.mars_info_collection.find_one()
    
    # Return template and data
    return render_template("index.html", mars_data=scraped_data)

@app.route("/scrape")
def scrape():
    scraped_data = scrape_info()
    # Update the Mongo database using update and upsert=True
    marsdb_connect.db.mars_info_collection.update({}, scraped_data, upsert=True)
    # Redirect back to home page
    return redirect("/")

@app.route("/hemi")
def hemi():
    hemisphere_image_urls = scrape_mars.usgs_get_images()
    # Save to mongo
    # mongo.db.mars_info.replace_one({}, hemisphere_image_urls, upsert=True)
    return jsonify(hemisphere_image_urls)

@app.route("/json")
def json():
    global scraped_data
    # if image urls not saved yet
    if not scraped_data:
        scraped_data = scrape_info()
    # mars = mongo.db.mars
    # mars_data = scrape_mars.scrape_all()
    # mars.update({}, mars_data, upsert=True)
    #mars.replace_one({}, mars_data, upsert=True)
    return jsonify(scraped_data)



@app.route("/scrape1")
def scrape1():
    # mars = mongo.db.mars
    # mars_data = scrape_mars.scrape_all()
    # mars.update({}, mars_data, upsert=True)
    mars.replace_one({}, mars_data, upsert=True)
    return "Scraping Successful!"


if __name__ == "__main__":
    app.run(debug=True)