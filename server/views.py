# import standard modules
import os
import uuid
import random

# import third party modules
from flask import Flask, render_template, request, redirect, url_for

# import project related modules
from settings import app, db
from models import FreeQuery
from generators.tables import QueryTable


def index():
    """
    creates the default view showing two tables and the input form for the user.
    """

    # get the logo from the static files
    logo = os.path.join(app.config['IMAGES'], 'detective_logo.png')

    try:
        # select randomly a query type - random choice provides a uniform distribution
        query_type = random.choice(list(range(12)))
        input_table, output_table = QueryTable().query_task(query_type)

        # in case the incoming url holds a streak value than get it and convert it to int
        streak = request.args.get('streak')
        streak = int(streak)

    except (KeyError, ValueError, TypeError):
        streak = "0"
        redirect(url_for("index", streak=streak))

    return render_template(
        "base.html",
        query_type=query_type,
        input_table=input_table,
        output_table=output_table,
        logo=logo,
        streak=streak
    )


def add_query():
    """
    post view not showing anything but taking a post request to create a new database entry.
    It will redirect to the index view after post request an increase the count of the streak by 1.
    """

    # get the variables
    query_type = request.form.get("query_type")
    free_text_query = request.form.get("query_input")
    streak = request.form.get("streak", 0)
    streak = str(int(streak) + 1)

    try:
        # add new query
        new_query = FreeQuery(
            id=uuid.uuid1(),
            query_type=query_type,
            free_text_query=free_text_query
        )

        db.session.add(new_query)
        db.session.commit()

    except Exception as exc:
        print(exc)

    return redirect(url_for("index", streak=streak))


def skip():
    """
    view to handle the skip button. It will just get the streak and redirect to index view again.
    :return:
    """
    streak = request.form.get("streak-break")
    return redirect(url_for("index", streak=streak))