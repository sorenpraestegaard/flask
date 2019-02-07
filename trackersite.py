from flask import Flask, render_template, url_for, send_file

import io
import matplotlib.pyplot as plt

app = Flask(__name__)



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
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


if __name__ == '__main__':
    app.run(debug=True)
