from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'cambiar_esto_a_una_clave_segura'
def get_db_connection():
    return psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password="sanandres1_",
        database="flasklab",
        port=5432
    )


def login_required(view):
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        if not email or not password:
            flash('Por favor ingresa usuario y contraseña.', 'danger')
            return render_template('login.html')

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            'SELECT id, nombre, email, password, rol FROM usuarios WHERE email = %s AND rol = %s',
            (email, 'admin')
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and user['password'] and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            session['user_email'] = user['email']
            session['user_role'] = user['rol']
            return redirect(url_for('admin_panel'))

        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin_panel():
    return render_template('admin.html')


@app.route('/users')
@login_required
def users_list():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, nombre, email, rol FROM usuarios ORDER BY id')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('users.html', users=users)


@app.route('/users/new', methods=['GET', 'POST'])
@login_required
def create_user():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        rol = request.form['rol']

        if not nombre or not email or not password:
            flash('Todos los campos obligatorios deben completarse.', 'danger')
            return render_template('user_form.html', user={}, action='Crear')

        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO usuarios (nombre, email, password, rol) VALUES (%s, %s, %s, %s)',
                (nombre, email, hashed_password, rol)
            )
            conn.commit()
            flash('Usuario creado correctamente.', 'success')
            return redirect(url_for('users_list'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('El email ya existe. Usa otro email.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('user_form.html', user={}, action='Crear')


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, nombre, email, rol FROM usuarios WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('users_list'))

    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        email = request.form['email'].strip()
        rol = request.form['rol']

        if not nombre or not email:
            flash('Nombre y email son obligatorios.', 'danger')
            return render_template('user_form.html', user=user, action='Editar')

        try:
            cursor.execute(
                'UPDATE usuarios SET nombre=%s, email=%s, rol=%s WHERE id=%s',
                (nombre, email, rol, user_id)
            )
            conn.commit()
            flash('Usuario actualizado correctamente.', 'success')
            return redirect(url_for('users_list'))
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('El email ya existe. Usa otro email.', 'danger')

    cursor.close()
    conn.close()
    return render_template('user_form.html', user=user, action='Editar')


@app.route('/users/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if session['user_id'] == user_id:
        flash('No puedes eliminar tu propio usuario mientras estás conectado.', 'warning')
        return redirect(url_for('users_list'))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT id, nombre, email FROM usuarios WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('users_list'))

    if request.method == 'POST':
        cursor.execute('DELETE FROM usuarios WHERE id = %s', (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Usuario eliminado correctamente.', 'success')
        return redirect(url_for('users_list'))

    cursor.close()
    conn.close()
    return render_template('confirm_delete.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
