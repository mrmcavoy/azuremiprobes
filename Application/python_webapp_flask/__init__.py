"""
The flask application package.
"""

from flask import Flask
from os import environ
#from applicationinsights.requests import WSGIApplication
app = Flask(__name__)
#app.wsgi_app = WSGIApplication(environ.get('APPINSIGHTS_INSTRUMENTATIONKEY'), app.wsgi_app)
#app.wsgi_app = WSGIApplication("703a7d6b-285b-4a27-b7fe-aad4a029fd1e", app.wsgi_app)
import python_webapp_flask.views




