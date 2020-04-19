from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
db = SQLAlchemy(app)

username, password, port= 'postgres', '7490', 5432
DB_URI = f"postgresql://{username}:{password}@localhost:{port}/todoapp"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)


###In psql: sudo su - postgres
###In psql: createdb -h localhost -p 5432 -U postgres todoapp



class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todo_items = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<Todo {self.id} {self.name}>'


#db.create_all()
@app.route('/')
def index():
    
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    lists = TodoList.query.order_by('id').all()
    active_list = TodoList.query.get(list_id)
    return render_template('index.html', todos=todos, lists=lists, active_list=active_list)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    # description = request.form.get('description', '')
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description)
        active_list = TodoList.query.get(list_id)
        todo.list = active_list
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
    
    # return redirect(url_for('index'))
    if not error:
        return jsonify(body) 
    else:
        abort(500) 


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    error = False
    try:
        completed = request.get_json()['completed']
        todo_item = Todo.query.get(todo_id)
        todo_item.completed = completed
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo_item(todo_id):
    error = False
    try:
        todo_item = Todo.query.get(todo_id)
        db.session.delete(todo_item)
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })

if __name__ == '__main__':
    app.run(debug=True)