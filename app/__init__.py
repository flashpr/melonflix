from flask import Flask

app = Flask(__name__)

def redirect_url(default='index'):
    return request.args.get('next') or request.referrer or url_for(default)

from app import routes
