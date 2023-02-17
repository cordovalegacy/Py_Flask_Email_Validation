from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "eml": request.form['eml']
    }
    User.save(data)
    return redirect('/display_user')


@app.route('/display_user')
def display_user():
    users = User.get_all()
    print(users)
    return render_template('display_user.html', all_users=users)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    data={
        'id':id
    }
    User.delete_user(data)
    return redirect('/display_user')

@app.route('/edit_user/<int:id>')
def edit_user(id):
    data={
        'id':id
    }
    return render_template('edit_user.html', user=User.display_user_by_id(data))

@app.route('/updated', methods=['POST'])
def updated():
    if not User.validate_user(request.form):
        return redirect('/display_user')
    User.updated(request.form)
    return redirect('/display_user')

@app.route('/display_user_by_id/<int:id>')
def display_user_by_id(id):
    data={
        'id':id
    }
    return render_template('display_user_by_id.html', user=User.display_user_by_id(data))