from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
  {
    "author": 'Liya',
    "title": 'First post',
    "content": "first content",
    "date posted": "april 1 2018"
  },
  {
    "author": 'josi',
    "title": '2nd post',
    "content": "2nd content",
    "date posted": "april 5 2018"
  }
]


@app.route("/")
@app.route("/home")
def home():
  return render_template('home.html', posts=posts)

@app.route("/about")
def about():
  return render_template('about.html', title="About")

if __name__ == '__main__':
  app.run(debug=True)