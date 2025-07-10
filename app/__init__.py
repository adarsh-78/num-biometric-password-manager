from flask import Flask

app = Flask(__name__)
app.secret_key = 'ef896cd037070afd802a9c7e533d6682'

from app import routes 
