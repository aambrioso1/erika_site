import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
	return "Hello Universe! "*5

def main():
    app.run(debug=True, port=5000)
