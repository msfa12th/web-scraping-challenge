# import necessary libraries
from flask import Flask, render_template

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def hello():
    return render_template("index.html", text="Hello World!!")

@app.route("/scrape")
def echo():
    return render_template("index.html", text="It's time to SCRAPE!!")

if __name__ == "__main__":
    app.run(debug=True)