from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import pandas as pd
from scraper import run_scraper  # Asegúrate de tener esta importación correcta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    username = request.form['username']
    password = request.form['password']
    urls = request.form['urls'].splitlines()
    
    # Llama a la función de scraping
    run_scraper(username, password, urls)
    
    # Devuelve el archivo CSV generado
    return send_file('LinkedIn_Contacts_Info.csv', as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
