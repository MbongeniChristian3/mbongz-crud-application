#!/usr/bin/python3
"""
Starts my Flask application
"""

from flask import Flask, render_template, request, redirect
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Initialize Flask-Assets
assets = Environment(app)
scss = Bundle('scss/styles.scss', filters='libsass', output='static/styles.css')
assets.register('scss_all', scss)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
    db.create_all()

@app.route("/", methods=["POST", "GET"])
def index():
    """ Adds a new task """
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('edit.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id: int):
    """ Holds function for deleting an item """
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id: int):
    """ gives the app the ability to edit a task """
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('edit.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)
