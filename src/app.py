import pyshorteners

from flask import Flask, render_template, request, redirect, url_for
import os 
import database as db 

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicación
@app.route('/')
def home():

    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM urls")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario 
    insertObject = []
    columnNames = [column[0] for column in cursor.description] 
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))

    cursor.close()
    return render_template('index.html', data=insertObject)

@app.route('/', methods=['GET', 'POST'])
def shorten_url():
    if request.method == 'POST':
        long_url = request.form['url']
        short_url = shorten(long_url)
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

def shorten(url):
    shortener = pyshorteners.Shortener()
    short_url = shortener.tinyurl.short(url)
    return short_url

def save_url(long_url, short_url):
    query = "INSERT INTO urls (long_url, short_url) VALUES (%s, %s)"
    values = (long_url, short_url)
    db.execute_query(query, values)

if __name__ == '__main__':
    app.run()
