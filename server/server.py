# import standard modules
import os
import random

# import third party modules
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

# import project related modules
from generators.tables import QueryTable

# settings
STATIC_FOLDER = os.path.join('static', 'images')
DATA_FOLDER = os.path.join('static', 'data')

app = Flask(__name__)
app.config['IMAGES'] = STATIC_FOLDER
app.config['DATA'] = DATA_FOLDER

# api = Api(app)

# set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# filter for all query in database
# query_list = FreeQuery.query.all()


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

    # select randomly a query type
    # query_type = random.choice(list(range(12)))
    query_type = 3 # random.choice(list(range(12)))
    input_table, output_table = QueryTable().query_task(query_type)
    print(input_table, output_table)
    try:
        streak = request.args.get('streak')
        streak = int(streak)
    except (KeyError, ValueError, TypeError):
        streak = "0"

    return render_template(
        "base.html",
        query_type=query_type,
        input_table=input_table,
        output_table=output_table,
        logo=logo,
        streak=streak
    )


@app.route("/add_query", methods=["POST"])
def add_query():
    # add new query
    query_type = request.form.get("query_type")
    free_text_query = request.form.get("query_input")
    streak = request.form.get("streak", 0)
    streak = str(int(streak) + 1)

    new_query = FreeQuery(
        query_type=query_type,
        free_text_query=free_text_query
    )

    db.session.add(new_query)
    db.session.commit()
    return redirect(url_for("index", streak=streak))


@app.route("/skip", methods=["POST"])
def skip():
    streak = request.form.get("streak-break")
    return redirect(url_for("index", streak=streak))


# run app
if __name__ == '__main__':
    db.create_all()                              # create a new database at launch
    app.run(host='0.0.0.0', port=81, debug=True)