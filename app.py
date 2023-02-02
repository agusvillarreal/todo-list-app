from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath

app = Flask(__name__)

#UPLOADS_PATH = join(dirname(realpath(__file__)), '../static/uploads/..')

 
#app.secret_key = "secret key"
#app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
#def allowed_file(filename):
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Initialize the databse
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['UPLOAD_FOLDER'] = 'static/uploads'
#app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
db = SQLAlchemy(app)


# Create a calss to manage every task
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    #description = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    priority = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Express the route of our index page
@app.route('/')
def index():
    # Show all todos
    todo_list = Todo.query.order_by(Todo.priority).all()
    #todo_list = Todo.query.all()
    print(todo_list)
    return render_template('index2.html', todo_list=todo_list)

# add the new item and send to another route
@app.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get("title")
    #description=request.form.get('description')
    priority = request.form.get("priority")
    date=request.form.get('date')
    new_todo = Todo(title=title, priority=priority, date=date, completed=False)
    db.session.add(new_todo)
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

@app.route("/reorganize", methods=["POST"])
def reorganize():
    todo_list = Todo.query.all()
    for todo in todo_list:
        todo.priority = request.form.get(f"priority_{todo.id}")
        db.session.commit()
    return redirect(url_for("index"))

'''
@app.route('/images', methods=['GET','POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('index2.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
'''
# Initialize the local host
if __name__ == '__main__':
    db.create_all()

    new_todo = Todo(title='Todo1', complete=False, priority=False, date=False)
    db.session.add(new_todo)
    db.session.commit()
    

    app.run(debug=True)