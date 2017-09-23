from . import app
from flask import render_template, request
import random


@app.errorhandler(404)
def page_not_found(e):
    return "Error."
