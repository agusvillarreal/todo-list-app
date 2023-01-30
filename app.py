from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
# Initialize the databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a calss to manage every task
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

# Express the route of our index page
@app.route('/')
def index():
    # Show all todos
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('index.html', todo_list=todo_list)

# add the new item and send to another route
@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo, datetime.datetime.now())
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    # add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    # add new item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


# Initialize the local host
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)