from application import app, db
from sqlalchemy import or_
from flask import flash, jsonify, make_response, redirect, render_template, request, send_from_directory, session, url_for
from application.helpers import *
from application.models import *
from application.forms import *

@app.route("/")
def index():
    return render_template("index.html")