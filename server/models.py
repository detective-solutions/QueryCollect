from flask_sqlalchemy import SQLAlchemy

# define database model
db = SQLAlchemy()


class FreeQuery(db.Model):
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