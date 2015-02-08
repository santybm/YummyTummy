from flask import Flask
from flask import render_template

app = Flask(__name__)



@app.route('/')   #give it a route, define functions underneath

def index():
    return render_template("index.html")  #render template returns html files


@app.route('/category/<categoryName>')

def category_response(categoryName):

	return "Hello world"

@app.route('/lala')

def lala():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('lala.html', title='Home', user=user)



if __name__ == '__main__': # has to be the last line
    app.run(debug=True)


