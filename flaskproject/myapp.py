#!/usr/bin/env python
from flask import Flask, render_template, request, Response
from run_model import *

app = Flask(__name__)

@app.route('/')
def root():return render_template('input.html')

@app.route('/index')
def index():return render_template('input.html')

@app.route('/input')
def input():

    return render_template('input.html')

@app.route('/example')
def example():
    return render_template('example.html')

@app.route('/cameron')
def cameron():
    return render_template('cameron.html')

@app.route('/sean')
def sean():
    return render_template('sean.html')


@app.route('/hendrix')
def hendrix():
    return render_template('Hendrix.html')

@app.route('/indiana')
def indiana():
    return render_template('indiana.html')

@app.route('/output', methods=['POST'])
def output():
    times = request.form.to_dict() # dictionary
    teams=mk_output(times)
    if teams:
        return render_template('output.html',teams=teams)
    else:
        return render_template('fail.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


@app.route("/input.html", methods=['GET', 'POST'])
def test():
    select = request.form.get('50fr')

    print(select)
    return(str(select)) # just to see what select is
