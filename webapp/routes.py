from webapp import app


@app.route('/')
@app.route('/index')
def hello():
    return "Hello World!"
