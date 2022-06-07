from flask import Flask, render_template
from werkzeug.serving import run_simple
from engine.buildEngine import *
import engine.matcher as mt
from engine.spellchecker import print_suggestion
from flask import request
from engine.query_optimizer import *


print('starting ...')

app = Flask(__name__)

init_DS('ds1')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/search' , methods=['POST'])
def search():
    
    query = request.form['query']
    image = request.files['image']

    if request.files['image'].filename != '' : 
        res = get_tags_by_image(image)
        for token in res :
            query += ' ' + token['tag']['en']
            
    print(query)
    
    initMatcher('ds1')
    suggest = print_suggestion(query)
    match = mt.match(query)
    
    data = {
        'match' : match,
        'suggest' : suggest
    }
    
    return render_template('search.html' , data=data)

     

if __name__ == '__main__':
    run_simple('localhost', 3000, app)