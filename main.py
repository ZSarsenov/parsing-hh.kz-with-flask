import requests
from flask import Flask, render_template, request, redirect, send_file
from parser import getJobs
from exporter import save_to_csv

app = Flask('JobScrapper')
db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        getDB = db.get(keyword)
        if getDB:
            jobs = getDB
        else:
            jobs = getJobs(keyword)
            db[keyword] = jobs
    else:
        return redirect('/')
    return render_template('report.html', searchBy=keyword, search_results=len(jobs), jobs=jobs)

@app.route('/export')
def export():
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            raise Exception()
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        send_file('jos.csv')
        return 'файл скачан'
    except:
        return redirect('/')

def plus(a, b):
    return a + b

def mult(a, b):
    return a * b

app.run()
