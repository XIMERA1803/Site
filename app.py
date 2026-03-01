from flask import Flask, render_template

from db import *

app = Flask(__name__, template_folder="templates")
app.debug = True
db = DataBase()

@app.route('/')
def index():
	return render_template("pages/index.html")

@app.route('/projects')
def projects():
	all_projects = db.select_all()
	return render_template("pages/projects.html", projects=all_projects)

@app.route('/about')
def about():
	return render_template("pages/about.html")

@app.errorhandler(404)
def error_not_found(error):
	return f"<h1>Страница не найдена! Илья смотри свой код!</h1> {error}", 404


if __name__ == "__main__":
	app.run()
