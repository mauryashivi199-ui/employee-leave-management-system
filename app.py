from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'leave_mgmt_secret'

def get_db():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root123",
        database="leavedb"
    )

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            session['user'] = user
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('employee_dashboard'))
        return render_template('login.html', error="Invalid credentials!")
    return render_template('login.html')

@app.route('/employee')
def employee_dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM leaves WHERE employee_id=%s",
        (session['user']['id'],)
    )
    leaves = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(*) AS used_leaves FROM leaves WHERE employee_id=%s AND status='approved'",
        (session['user']['id'],)
    )
    used = cursor.fetchone()['used_leaves']

    cursor.execute(
        "SELECT COUNT(*) AS pending_leaves FROM leaves WHERE employee_id=%s AND status='pending'",
        (session['user']['id'],)
    )
    pending = cursor.fetchone()['pending_leaves']

    cursor.execute(
        "SELECT * FROM users WHERE id=%s",
        (session['user']['id'],)
    )
    user = cursor.fetchone()

    available = user['total_leaves'] - used

    return render_template(
        'employee_dashboard.html',
        leaves=leaves,
        user=user,
        used=used,
        pending=pending,
        available=available
    )

@app.route('/apply', methods=['GET', 'POST'])
def apply_leave():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO leaves (employee_id, leave_type, start_date, end_date, reason, status) VALUES (%s, %s, %s, %s, %s, 'pending')",
            (session['user']['id'], request.form['leave_type'], request.form['start_date'], request.form['end_date'], request.form['reason']))
        db.commit()
        return redirect(url_for('employee_dashboard'))
    return render_template('apply_leave.html', user=session['user'])

@app.route('/admin')
def admin_dashboard():
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT l.*, u.username FROM leaves l JOIN users u ON l.employee_id=u.id")
    leaves = cursor.fetchall()
    return render_template('admin_dashboard.html', leaves=leaves, user=session['user'])

@app.route('/update_leave/<int:leave_id>/<action>')
def update_leave(leave_id, action):
    if 'user' not in session or session['user']['role'] != 'admin':
        return redirect(url_for('login'))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE leaves SET status=%s WHERE id=%s", (action, leave_id))
    db.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
