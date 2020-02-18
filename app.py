from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_yelp

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/test")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    # Not sure exactly the MongoDB/Pymongo syntax for referencing a
    # particular document (in this case yelp and citibike) within the collection
    citibike_c = mongo.db.citibike.find()
    yelp_c = mongo.db.yelp.find()
    citibike_data = []
    yelp_data = []
    for cursor in citibike_c:
        del cursor["_id"]
        citibike_data.append(cursor)
    for cursor in yelp_c:
        del cursor["_id"]
        yelp_data.append(cursor)

    combined_data = [citibike_data, yelp_data]

    # Return template and data
    return render_template("index.html", combined_data=combined_data)

# Route to render logic.js template using data from Mongo
# Should this be a part of home route or a seperate route like this?
@app.route("/logic.js")
def logic():

    # Find one record of data from the mongo database
    # Not sure exactly the MongoDB/Pymongo syntax for referencing a
    # particular document (in this case yelp and citibike) within the collection
    citibike_c = mongo.db.citibike.find()
    yelp_c = mongo.db.yelp.find()
    citibike_data = []
    yelp_data = []
    for cursor in citibike_c:
        del cursor["_id"]
        citibike_data.append(cursor)
    for cursor in yelp_c:
        del cursor["_id"]
        yelp_data.append(cursor)

    combined_data = [citibike_data, yelp_data]
    # Return template and data
    return render_template("logic.js", combined_data=combined_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    new_yelp_data = scrape_yelp.scrape()

    # Update the Mongo database using update and upsert=True
    # Again: Not sure exactly the MongoDB/Pymongo syntax for referencing a
    # particular document (in this case yelp) within the collection
    mongo.db.collection.yelp.update({}, new_yelp_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)