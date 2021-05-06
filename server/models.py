# import third party modules
from flask_sqlalchemy import SQLAlchemy

# define database model
db = SQLAlchemy()


class FreeQuery(db.Model):
    """
    Database Table used for the DataCollect service. It holds just three columns
    id - primary key and random generated uuid
    query_type - indicating a predefined filter / action provided by the index view
    free_text_query - task response from the user
    """

    __tablename__ = 'FreeQuery'

    id = db.Column(db.String(50), primary_key=True)
    query_type = db.Column(db.Integer())
    free_text_query = db.Column(db.String(400))

    def __init__(self, id, query_type, free_text_query):
        self.id = id
        self.query_type = query_type
        self.free_text_query = free_text_query

    def __repr__(self):
        return f"query_type_{self.query_type}"