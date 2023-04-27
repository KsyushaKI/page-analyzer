from flask import Flask
from flask import render_template
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def hello_world():
    return render_template('main/index.html')
