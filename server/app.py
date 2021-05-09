from settings import app
from views import index, add_query, skip

# set urls
app.add_url_rule('/', 'index', index, methods=["GET"])
app.add_url_rule('/add_query', 'add_query', add_query, methods=["POST"])
app.add_url_rule('/skip', 'skip', skip, methods=["GET"])


# run app
if __name__ == '__main__':
    # db.create_all()                              # create a new database at launch
    app.run(host='0.0.0.0', port=8080, debug=True)