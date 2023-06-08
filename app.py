import flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = flask.Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to_do_list.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
    
@app.route('/')
def home():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return flask.render_template('home.html', tasks=tasks)


@app.route('/add_task', methods=['POST', 'GET'])
def add_task():
    if flask.request.method == 'POST':
        task_title = flask.request.form['title']
        task_content = flask.request.form['content']
        
        new_task = Todo(title=task_title, content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return flask.redirect('/')
        except:
            return "There was an issue adding your task ):"
    else:
        return flask.render_template('add_task.html')
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return flask.redirect('/')
    except:
        return "There was an problem delteting that task ):"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    
    if flask.request.method == 'POST':
        task.title = flask.request.form['title']
        task.content = flask.request.form['content']
            
        try:
            db.session.commit()
            return flask.redirect('/')
        except:
            return "There was an issue adding your task ):"
    else:
        return flask.render_template('update.html', task=task)

if __name__ == '__main__':
    app.run(debug=True)
    