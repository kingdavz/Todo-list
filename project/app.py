#!/usr/bin/python
"""a module that handles the to do list"""


from flask import Flask, render_template, request, session, redirect, url_for
from util import (
    hash_password, verify_password, user_exists, 
    save_user, get_user, add_task, get_user_tasks, 
    update_task, delete_task, get_task
)
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    data = {'message': '', 'type': ''}
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirmPassword', '').strip()
        
        if not username or not email or not password:
            data['message'] = 'All fields required'
            data['type'] = 'error'
        elif len(username) < 3:
            data['message'] = 'Username must be at least 3 characters'
            data['type'] = 'error'
        elif len(password) < 6:
            data['message'] = 'Password must be at least 6 characters'
            data['type'] = 'error'
        elif password != confirm_password:
            data['message'] = 'Passwords do not match'
            data['type'] = 'error'
        elif user_exists(username):
            data['message'] = 'Username already exists'
            data['type'] = 'error'
        else:
            hashed_password = hash_password(password)
            if save_user(username, email, hashed_password):
                data['message'] = 'Account created! Redirecting to login...'
                data['type'] = 'success'
                return redirect(url_for('login'))
            else:
                data['message'] = 'Error creating account'
                data['type'] = 'error'
    
    return render_template('signup.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = {'message': '', 'type': ''}
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        user = get_user(username)
        
        if user and verify_password(password, user['password']):
            session['username'] = username
            session['email'] = user['email']
            return redirect(url_for('dashboard'))
        else:
            data['message'] = 'Invalid username or password'
            data['type'] = 'error'
    
    return render_template('login.html', data=data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    email = session['email']
    data = {'message': '', 'type': ''}
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            
            if title:
                add_task(username, title, description)
                data['message'] = 'Task added successfully!'
                data['type'] = 'success'
            else:
                data['message'] = 'Task title required'
                data['type'] = 'error'
        
        elif action == 'delete':
            task_id = request.form.get('task_id')
            if delete_task(username, task_id):
                data['message'] = 'Task deleted successfully!'
                data['type'] = 'success'
        
        elif action == 'toggle':
            task_id = request.form.get('task_id')
            update_task(username, task_id, {'completed': 'toggle'})
            data['type'] = 'success'
        
        elif action == 'update':
            task_id = request.form.get('task_id')
            title = request.form.get('title', '').strip()
            description = request.form.get('description', '').strip()
            
            if title:
                update_task(username, task_id, {
                    'title': title,
                    'description': description
                })
                return redirect(url_for('dashboard'))
    
    tasks = get_user_tasks(username)
    return render_template('index.html', username=username, email=email, tasks=tasks, data=data)

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    task = get_task(username, task_id)
    
    if not task:
        return redirect(url_for('dashboard'))
    
    data = {'message': '', 'type': ''}
    return render_template('edit_task.html', username=username, task=task, data=data)

if __name__ == '__main__':
    if not os.path.exists('data'):

        os.makedirs('data')
    app.run(host="0.0.0.0", port=5000, debug=True)