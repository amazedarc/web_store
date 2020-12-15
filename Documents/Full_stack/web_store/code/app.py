from flask import Flask
import flask_restful

app = Flask('__name__')


@app.route('/')
def main_route():
    return "Welcome, to may page!"


app.run(port=4400, debug=True)
