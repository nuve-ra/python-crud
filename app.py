# from asyncio import tasks

# from flask import Flask, redirect,render_template, request,url_for
# # now we are talking about databases
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db' #this is the path of database here ///=means relative path and ////=means absolute path
# db=SQLAlchemy(app) #database is intialized

# #lets create a database model
# class Todo(db.Model):
#     id=db.Column(db.Integer,primary_key=True)
#     content=db.Column(db.String(200),nullable=False)
#     completed=db.Column(db.Integer,default=0) #0 means not completed and 1 means completed
#     date_created=db.Column(db.DateTime,default=datetime.utcnow) #could be ignored user dont need access to it

#     def __repr__(self):
#         return '<Task %r>' %self.id


# @app.route("/", methods=['POST', 'GET'])
# def index():
#     if request.method=='POST':
#         task_content=request.form['content']
#         new_task=Todo(content=task_content)
        
#         try:
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "There was an issue adding your task"

#     else:
#         tasks=Todo.query.order_by(Todo.date_created).all() #this will return all the tasks in the database and order them by date created
#     # return render_template("index.html")
#         return render_template("index.html", tasks=tasks)


# @app.route('/delete/<int:id>')
# # //app.route("/delete/<int:id>")
# def delete(id):
#     task_to_delete=Todo.query.get_or_404(id)

#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return "There was a problem deleting that task"

# @app.route('/update/<int:id>',methods=['GET','POST'])
# def update(id):
#     return ""
#     # return "Flask is working!"
# if __name__ == "__main__":
   
#     with app.app_context(): #this will create the database in the current directory where app.py is located
#         db.create_all()

#         app.run(debug=True)
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating your task"

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
