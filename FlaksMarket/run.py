from market import app
from waitress import serve

if __name__=="__main__":
    #serve(app,host="127.0.0.1",port=5000)
    app.run(host="0.0.0.0")