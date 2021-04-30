# import standard modules
import os

# import third party modules
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# settings
STATIC_FOLDER = os.path.join('static', 'images')


app = Flask(__name__)
app.config['IMAGES'] = STATIC_FOLDER

# api = Api(app)

# set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# define database model
class FreeQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query_type = db.Column(db.Integer)
    free_text_query = db.Column(db.String(400))


# main page to collect queries
@app.route('/', methods=["GET"])
def index():

    # get the logo
    logo = os.path.join(app.config['IMAGES'], 'detective_logo.png')

    query_list = FreeQuery.query.all()
    query_type = 1
    return render_template("base.html", query_list=query_list, query_type=query_type, logo=logo)


@app.route("/add_query", methods=["POST"])
def add_query():
    # add new query
    query_type = request.form.get("query_type")
    free_text_query = request.form.get("query_input")

    new_query = FreeQuery(
        query_type=query_type,
        free_text_query=free_text_query
    )

    db.session.add(new_query)
    db.session.commit()
    return redirect(url_for("index"))


# run app
if __name__ == '__main__':
    db.create_all()                              # create a new database at launch
    app.run(host='0.0.0.0', port=81, debug=True)