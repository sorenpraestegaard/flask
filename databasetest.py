from flask import Flask
from flask import request
from flask import g


#from adminpage import admin

import sqlite3

app = Flask(__name__)

DATABASE = 'ontrack.db'


def get_db():
    db = g.get('_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



@app.route("/")
@app.route('/index')
def index():
    return '''<form action="handle_data" method="post">
                <input type="text" name="tekst">
                <input type="submit" value="Send">
            </form>'''

def input_user_track(val):
    pass

@app.route('/handle_data', methods=['POST'])
def handle_data():
    # Gør noget med data
    input_user_track(request.form['tekst'])

    db = get_db()
    print(db)
    c = db.cursor()
    c.execute("SELECT COUNT(rowid) FROM Tracks;")
    i = 0
    for row in c:
        i = i + 1
        print(row)
    # returner et svar
    return str(i)



@app.route('/db')
def db():
    db = get_db()
    print(db)
    c = db.cursor()
    c.execute("SELECT * FROM Tracks;")
    i = ""
    for row in c:
        i += str(row)
    # returner et svar
    return i



@app.route('/create_db')
def create_db_tables():
    db = get_db()
    print(db)
    c = db.cursor()
    try:
        c.execute("""CREATE TABLE UserProfiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT);""")
    except Exception as e:
        print(e)
    try:
        c.execute("""CREATE TABLE Tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trackname TEXT,
            tracktype INTEGER,
            userid INTEGER);""")

    except Exception as e:
        print(e)

    try:
        c.execute("""CREATE TABLE TrackValues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trackid INTEGER,
            value NUMERIC);""")

    except Exception as e:
        print(e)

    return 'Database tables created'



if __name__ == "__main__":
    app.run(debug=True)
