from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


username, password, port= 'postgres', '7490', 5432
DB_URI = f"postgresql://{username}:{password}@localhost:{port}/todoapp"


###In psql: sudo su - postgres
###In psql: createdb -h localhost -p 5432 -U postgres todoapp

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/')
def index():
    data = Todo.query.all()
    return render_template('index.html', data=data)


@app.route('/todos/create', methods=['POST'])
def create_todo():
    description = request.form.get('description', '')
    todo_item = Todo(description=description)
    db.session.add(todo_item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)