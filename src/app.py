from flask import Flask
from flask_restx import Api

APP = Flask(__name__)
API = Api(
    APP,
    version='0.0.1',
    title='apply2jobs API',
    description='Search for and apply to jobs.'
)

APP.run(debug=True)

