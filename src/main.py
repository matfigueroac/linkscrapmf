from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from scraper import run_scraper

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    username = request.form['username']
    password = request.form['password']
    urls = request.form['urls'].splitlines()
    
    run_scraper(username, password, urls)
    
    return send_file('LinkedIn_Contacts_Info.csv', as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
