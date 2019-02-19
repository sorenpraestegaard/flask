from flask import Flask, render_template, request, redirect, url_for, send_file, session

import io
import matplotlib.pyplot as plt
from user import User

app = Flask(__name__)
app.secret_key = 'very secret string'

posts = [
    {
        'author': 'Søren',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Ferbuar, 2019'
    },
    {
        'author': 'En anden',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Februar, 2019'
    }
]


def get_user_id(user):
    #TODO: Use the database to fetch id
    return 1

def get_login_status():
    return 'currentuser' in session

@app.route('/login_user', methods=['POST'])
def login_user():
    pw = request.form['password']
    user = request.form['username']

    if login_success(user, pw):
        #Create user object, store in session.
        session['currentuser'] = get_user_id(user)
        return my_render('home.html')
    else:
        session.pop('currentuser', None)
        return my_render('login.html', success = False)

def register_success(user, pw, email):
    return user == 'Søren'

def login_success(user, pw):
    return user == 'Søren'

def my_render(template, **kwargs):
    login_status = get_login_status()
    return render_template(template, loggedin=login_status, **kwargs)


@app.route('/register_user', methods=['POST'])
def register_user():
    pw = request.form['password']
    user = request.form['username']
    email = request.form['email']

    if register_success(user, pw, email):
        #Create user object, store in session
        session['currentuser'] = get_user_id(user)
        return my_render('home.html')
    else:
        session.pop('currentuser', None)
        if len(pw) == 0 or len(user) == 0:
            return my_render('register.html', success = False, complete = False)
        else:
            return my_render('register.html', success = False, complete = True)




@app.route('/fig/<figure_key>')
def fig(figure_key):
    plt.title(figure_key)
    plt.plot([1,2,3,4], [1,3,2,4])
    img = io.BytesIO()
    plt.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route("/")
@app.route("/home")
def home():
    return my_render('home.html', posts=posts)

@app.route("/register")
def register():
    return my_render('register.html', success= True, complete = True)

@app.route("/login")
def login():
    return my_render('login.html', success = True)

@app.route("/logout")
def logout():
    session.pop('currentuser', None)
    return my_render('home.html')


@app.route("/about")
def about():
    return my_render('about.html', title='Om OnTrack')

@app.route("/contact")
def contact():
    return my_render('contact.html', title='Kontakt')


if __name__ == '__main__':
    app.run(debug=True)
