from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" # Craigslist_app is a specific db we are connecting to
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars_data = mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_data = mongo.db.mars_data
    # Run the scrape function
    returned_results = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, returned_results, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)