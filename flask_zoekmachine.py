from flask import Flask
from flask import render_template
from flask import request
import Zoekmachine


documenten = ['artikel1.txt', 'artikel2.txt', 'artikel3.txt', 'artikel4.txt', 'artikel5.txt', 'artikel6.txt', 'artikel7.txt', 'artikel8.txt', 'artikel9.txt', 'artikel10.txt']

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('zoekbar.html')

@app.route('/resultaatpagina', methods=['POST', 'GET'])
def resultpage():
    page = request.args.get('page', 0, type=int)
    if 'zoekopdracht' in request.form:
        zoekopdracht = request.form ['zoekopdracht']
    else:
        zoekopdracht = request.args.get('zoekopdracht')
    similarity = Zoekmachine.similarity(zoekopdracht)
    pages = getpages(similarity)
    if page >= len(pages):
        return render_template('zoekbar.html')
    return render_template('resultaatpagina.html', zoekopdracht = zoekopdracht, similarity = pages[page], page = page)

def getpages(similarity):
    similarity = list(similarity.items())
    print(similarity)
    lengte = len(similarity)
    start = 0
    pages = []
    for index in range(1, lengte):
        if index == lengte - 1:
            page = similarity[start:index + 1]
            pages.append(page)
        if index %5 == 0:
            eind = index
            page = similarity[start:eind]
            start = eind 
            pages.append(page)
    return pages




if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.config['DEBUG'] = True
    app.config['SERVER_NAME'] = "127.0.0.1:5000"
    app.run()