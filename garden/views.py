from flask import render_template
from garden import app, model


@app.route("/")
def index():
    with model.env.read():
        return render_template("index.j2", gardens=model.Garden.cursor())
        
        
@app.route("/gardens/add")
def add_garden():
    pass


@app.route("/seasons/<season_id>")
def season(season_id):
    pass

    
@app.route("/gardens/<garden_id>/add_season")
def add_season(garden_id):
    pass