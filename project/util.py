import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

USERS_FILE = 'data/users.csv'
TASKS_FILE = 'data/tasks.csv'

# ==========================================
# PASSWORD FUNCTIONS
# ==========================================

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    return check_password_hash(hashed_password, password)

# ==========================================
# USER MANAGEMENT
# ==========================================

def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'email', 'password', 'created_at'])
            writer.writeheader()

def user_exists(username):
    ensure_users_file()
    try:
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row['username'] == username:
                    return True
    except:
        pass
    return False

def save_user(username, email, hashed_password):
    try:
        ensure_users_file()
        with open(USERS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['username', 'email', 'password', 'created_at'])
            writer.writerow({
                'username': username,
                'email': email,
                'password': hashed_password,
                'created_at': str(datetime.now())
            })
        return True
    except:
        return False

def get_user(username):
    ensure_users_file()
    try:
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row['username'] == username:
                    return row
    except:
        pass
    return None

# ==========================================
# TASK MANAGEMENT
# ==========================================

def ensure_tasks_file():
    if not os.path.exists(TASKS_FILE):
        os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
        with open(TASKS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'username', 'title', 'description', 'completed', 'created_at'])
            writer.writeheader()

def get_next_task_id(username):
    ensure_tasks_file()
    max_id = 0
    try:
        with open(TASKS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row['username'] == username:
                    try:
                        task_id = int(row['id'])
                        if task_id > max_id:
                            max_id = task_id
                    except:
                        pass
    except:
        pass
    return str(max_id + 1)

def get_user_tasks(username):
    ensure_tasks_file()
    tasks = []
    try:
        with open(TASKS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row['username'] == username:
                    tasks.append(row)
    except:
        pass
    return tasks

def get_task(username, task_id):
    tasks = get_user_tasks(username)
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

def add_task(username, title, description=''):
    try:
        ensure_tasks_file()
        task_id = get_next_task_id(username)
        created_at = str(datetime.now())
        
        with open(TASKS_FILE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'username', 'title', 'description', 'completed', 'created_at'])
            writer.writerow({
                'id': task_id,
                'username': username,
                'title': title,
                'description': description,
                'completed': 'False',
                'created_at': created_at
            })
        return True
    except:
        return False

def update_task(username, task_id, data):
    try:
        ensure_tasks_file()
        all_tasks = []
        
        with open(TASKS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row['username'] == username and row['id'] == task_id:
                    if 'title' in data:
                        row['title'] = data['title']
                    if 'description' in data:
                        row['description'] = data['description']
                    if 'completed' in data:
                        if data['completed'] == 'toggle':
                            row['completed'] = 'False' if row['completed'] == 'True' else 'True'
                        else:
                            row['completed'] = str(data['completed'])
                all_tasks.append(row)
        
        with open(TASKS_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'username', 'title', 'description', 'completed', 'created_at'])
            writer.writeheader()
            for task in all_tasks:
                if task:
                    writer.writerow(task)
        return True
    except:
        return False

def delete_task(username, task_id):
    try:
        ensure_tasks_file()
        all_tasks = []
        found = False
        
        with open(TASKS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row['username'] == username and row['id'] == task_id:
                    found = True
                else:
                    if row:
                        all_tasks.append(row)
        
        if found:
            with open(TASKS_FILE, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'username', 'title', 'description', 'completed', 'created_at'])
                writer.writeheader()
                for task in all_tasks:
                    writer.writerow(task)
            return True
    except:
        pass
    return False