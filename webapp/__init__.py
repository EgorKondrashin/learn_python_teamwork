from flask import Flask
app = Flask(__name__)
from webapp import routes

'''@app.route("/")
def hello():
    return "Hello World!"


if __name__=="__main__":
    app.run()'''