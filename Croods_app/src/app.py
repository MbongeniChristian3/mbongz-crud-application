#!/usr/bin/python3
"""
starts my flask
"""
from flask import Flask, render_template
from flask_css import css
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer , default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"Task {self.id}"

@app.route("/",methods=["POST","GET"])
def index():
    """ adds a new task"""
    if request.method == "POST":
        current_task =nrequest.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"

    else:
        tasks =MyTask.query.order_by(MyTask.created).all()
        return render_template('home.html', tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id:int):
    """ it holds function for deleting an item"""
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR:{e}"

@app.route("/edit/<int:id>", methods=["GET", "POST"})
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        exception Exception as e:
            return f"Error:{e}"
    else:
        return render_template('edit.html',task=task)

if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='127.0.0.1', port='5000' )
