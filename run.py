from app import app
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
    
                                                                                     
if __name__ == "__main__":
    app.run()                                                                    