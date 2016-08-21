from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap, WebCDN
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

import subprocess
from time import sleep
from datetime import datetime
import thread

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)
db = SQLAlchemy(app)

app.extensions['bootstrap']['cdns']['jquery'] = WebCDN(
    '//cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/'
)

# Load default config and override config from an environment variable
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///database.db',
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

location = "living room"


class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperature = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(50), nullable=False)

    def __init__(self, temperature, time, location):
        self.temperature = temperature
        self.time = time
        self.location = location

    def __repr__(self):
        return '<Temperature %r>' % self.temperature


@app.route('/')
def index():
    tempetures = Temperature.query.all()

    return render_template('index.html', tempetures=tempetures)


@app.route('/timeperiod', methods=['GET'])
def timeperiod():
    start = request.args.get('start')
    end = request.args.get('end')

    start = datetime.strptime(start, '%m/%d/%Y %I:%M %p')
    end = datetime.strptime(end, '%m/%d/%Y %I:%M %p')


    tempetures = db.session.query(Temperature).filter(Temperature.time > start, Temperature.time < end).all()

    return render_template('index.html', tempetures=tempetures)


def tempeture_monitor():
    while True:
        # cmd = ["sudo","temper-poll","-c"]
        temp = subprocess.Popen("sudo temper-poll -c", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip()
        time = datetime.now()

        print temp

        tempeture = Temperature(float(temp), time, location)
        db.session.add(tempeture)
        db.session.commit()

        sleep(900)


if __name__ == '__main__':
    db.create_all()
    thread.start_new(tempeture_monitor,())

    app.run(host="0.0.0.0", port=5000)
