

from flask import Flask

app = Flask(__name__)

@app.route('/') #call the function below when the app starts
def hello():
    #name = 'World'
    #return render_template('index.html', name=name)
    return "HI HI !!"

if __name__ == "__main__": # start program at the main function 
   app.run()






