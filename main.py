from flask import Flask
import login

app=Flask(__name__)


@app.route("/<year>/<data>/<username>/<password>")
def index(year,data,username,password):
    a=login.get_table(year,data,username,password)
    return a

app.config['JSON_AS_ASCII'] = False

def handler(environ,start_response):
    return app(environ,start_response)

if __name__=="__main__":
    app.run()