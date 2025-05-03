from flask import Flask, render_template, request, redirect, session
from jinja2 import Environment, select_autoescape
from database import get_db
from datetime import datetime, date



app = Flask(__name__)

# Register a custom Jinja2 filter for date formatting
@app.template_filter('date')
def format_date(value, format='%Y-%m-%d'):
    return value.strftime(format) if value else ''


app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Necesario para manejar sesiones




@app.route('/')
def index():
    return render_template('login.html')




#--------------------------------------------login para manager y empleado --------------------------------------------

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    db = get_db()
    cursor = db.cursor()
    
    # Verificar si es un manager con correo activo
    cursor.execute("""
        SELECT m.* 
        FROM manager m
        JOIN manager_emails e ON e.manager_id = m.id
        WHERE e.email = %s AND m.password = %s AND e.status = 'Activo'
    """, (email, password))
    manager = cursor.fetchone()
    
    if manager:
        if manager['status'] == 'Inactivo':
            error = "Error: El administrador está inactivo."
            return render_template('login.html', error=error)
        session['user'] = email
        session['role'] = 'manager'
        session['manager_name'] = manager['first_name']
        return redirect('/dashboard')

    # Verificar si es un empleado con correo activo
    cursor.execute("""
        SELECT e.*
        FROM employees e
        JOIN employee_emails em ON em.employee_id = e.id
        WHERE em.email = %s AND e.password = %s AND em.status = 'Activo'
    """, (email, password))
    employee = cursor.fetchone()
    
    if employee:
        session['user'] = email
        session['role'] = 'employee'
        return redirect('/dashboard')

    return render_template('login.html', error="Usuario o contraseña incorrectos")




#--------------------------------------------dashboard para iniciar la base de datos--------------------------------------------

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor()

    if session['role'] == 'manager':
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.execute("SELECT * FROM employee_emails")
        employee_emails = cursor.fetchall()
        cursor.execute("SELECT * FROM manager_emails")
        manager_emails = cursor.fetchall()
        cursor.execute("SELECT * FROM clients")
        clients = cursor.fetchall()
        cursor.execute("SELECT * FROM suppliers")
        suppliers = cursor.fetchall()
        cursor.execute("SELECT * FROM positions")
        positions = cursor.fetchall()
        cursor.execute("SELECT * FROM supplies")
        supplies = cursor.fetchall()
        cursor.execute("SELECT * FROM income_table")
        salaries = cursor.fetchall()
        cursor.execute("SELECT * FROM manager")
        manager = cursor.fetchall()
        cursor.execute("SELECT * FROM deleted_employees")
        deleted_employees = cursor.fetchall()
        cursor.execute("SELECT * FROM deleted_clients")
        deleted_clients = cursor.fetchall()
        cursor.execute("SELECT * FROM deleted_suppliers")
        deleted_suppliers = cursor.fetchall()
        return render_template('dashboard.html', employees=employees, clients=clients, suppliers=suppliers, positions=positions, supplies=supplies, salaries=salaries, manager=manager, deleted_employees=deleted_employees, deleted_clients=deleted_clients, deleted_suppliers=deleted_suppliers, employee_emails=employee_emails, manager_emails=manager_emails)

    elif session['role'] == 'employee':
        cursor.execute("SELECT * FROM employees WHERE id=(SELECT employee_id FROM employee_emails WHERE email=%s)", (session['user'],))
        employee = cursor.fetchone()
        return render_template('dashboard.html', employee=employee)

    return redirect('/')




#--------------------------------------------logout para cerrar sesión--------------------------------------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#--------------------------------------------menu para el manager y sus diferentes opciones--------------------------------------------

@app.route('/menu')
def menu():
    if 'user' not in session:
        return redirect('/')
    
    if session['role'] == 'manager':
        return render_template('dashboard.html')
    
    return redirect('/')

@app.route('/menu/empleados', methods=['GET', 'POST'])
def menu_empleados_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('menu/empleados.html', employees=employees)

@app.route('/menu/clientes', methods=['GET', 'POST'])
def menu_clientes_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    return render_template('menu/clientes.html', clients=clients)

@app.route('/menu/suministros', methods=['GET', 'POST'])
def menu_suministros_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM supplies")
    supplies = cursor.fetchall()
    return render_template('menu/suministros.html', supplies=supplies)

@app.route('/menu/cargos', methods=['GET', 'POST'])
def menu_puestos_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM positions")
    positions = cursor.fetchall()
    return render_template('menu/cargos.html', positions=positions)

@app.route('/menu/proveedores', methods=['GET', 'POST'])
def menu_proveedores_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    return render_template('menu/proveedores.html', suppliers=suppliers)

@app.route('/menu/salarios', methods=['GET', 'POST'])
def menu_salarios_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM income_table")
    salaries = cursor.fetchall()
    return render_template('menu/salarios.html', salaries=salaries)

@app.route('/menu/administradores', methods=['GET', 'POST'])
def menu_administradores_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM manager")
    managers = cursor.fetchall()
    return render_template('menu/administradores.html', managers=managers)

@app.route('/menu/salarios_administrador', methods=['GET', 'POST'])
def menu_salarios_administrador_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM manager_income_table")
    salaries = cursor.fetchall()
    return render_template('menu/salarios_administrador.html', salaries=salaries)




#--------------------------------------------opciones multiples para administrador--------------------------------------------

@app.route('/managers', methods=['GET'])
def managers():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM manager")
    managers = cursor.fetchall()
    return render_template('managers/managers.html', managers=managers)

#--------------------------------------------agrega administrador-------------------------------------------

@app.route('/add_manager', methods=['GET', 'POST'])
def add_manager():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        identification = request.form['identification']
        birthdate = request.form['birthdate']
        phone = request.form['phone_number']
        address = request.form['address']
        password = request.form['password']
        created_by = session['manager_name']

        # Validar edad
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))

        if age < 18 or age > 65:
            error = "Error: La edad debe estar entre 18 y 65 años."
            return render_template('managers/add_manager.html', error=error)

        db = get_db()
        cursor = db.cursor()

        # Validar si la identificación es única
        cursor.execute("SELECT id FROM manager WHERE identification = %s", (identification,))
        existing_identification = cursor.fetchone()
        if existing_identification:
            identification_error = "Error: La identificación ya está registrada."
            return render_template('managers/add_manager.html', error=identification_error)
        
        # Validar si el teléfono es único
        cursor.execute("SELECT id FROM manager WHERE phone_number = %s", (phone,))
        existing_phone = cursor.fetchone()
        if existing_phone:
            phone_error = "Error: El número de teléfono ya está registrado."
            return render_template('managers/add_manager.html', error=phone_error)

        # Validar si la contraseña es única
        cursor.execute("SELECT id FROM manager WHERE password = %s", (password,))
        existing_manager = cursor.fetchone()
        if existing_manager:
            password_error = "Error: Las contraseñas deben ser únicas."
            return render_template('managers/add_manager.html', password_error=password_error)

        cursor.execute("""
            INSERT INTO manager (first_name, last_name, gender, 
            identification, birthdate, phone_number, 
            address, password, created_by) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, gender, identification, birthdate, phone, address, password, created_by))
        db.commit()
        return redirect('/dashboard')

    return render_template('managers/add_manager.html')

#--------------------------------------------edita administrador-------------------------------------------

@app.route('/edit_manager/<int:id>', methods=['GET', 'POST'])
def edit_manager(id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']

        # Check if the password is unique
        cursor.execute("SELECT id FROM manager WHERE password = %s AND id != %s", (password, id))
        existing_manager = cursor.fetchone()

        if existing_manager:
            password_error = "Error: Las contraseñas deben ser únicas."
            cursor.execute("SELECT * FROM manager WHERE id=%s", (id,))
            manager = cursor.fetchone()
            return render_template('managers/edit_manager.html', manager=manager, password_error=password_error)
        
        # Check if the phone number is unique
        cursor.execute("SELECT id FROM manager WHERE phone_number = %s AND id != %s", (phone, id))
        existing_phone = cursor.fetchone()
        if existing_phone:
            phone_error = "Error: El número de teléfono ya está registrado."
            cursor.execute("SELECT * FROM manager WHERE id=%s", (id,))
            manager = cursor.fetchone()
            return render_template('managers/edit_manager.html', manager=manager, phone_error=phone_error)

        if password:
            cursor.execute("UPDATE manager SET phone_number=%s, password=%s, address=%s WHERE id=%s",
                           (phone, password, address, id))
        else:
            cursor.execute("UPDATE manager SET phone_number=%s, address=%s WHERE id=%s",
                           (phone, address, id))
        db.commit()
        return redirect('/menu/administradores')

    cursor.execute("SELECT * FROM manager WHERE id=%s", (id,))
    manager = cursor.fetchone()
    return render_template('managers/edit_manager.html', manager=manager)

#--------------------------------------------muestra administradores eliminados-------------------------------------------

@app.route("/deleted_manager", methods=["GET"])
def show_deleted_manager():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    # Mostrar los administradores eliminados
    cursor.execute("""
        SELECT dm.manager_id, m.first_name, m.last_name, m.gender, m.identification, 
               m.birthdate, m.phone_number, m.address
        FROM deleted_managers dm
        JOIN manager m ON dm.manager_id = m.id
    """)
    managers = cursor.fetchall()
    
    return render_template('managers/deleted_manager.html', managers=managers)


#--------------------------------------------elimina administradores-------------------------------------------
@app.route("/delete_manager/<int:manager_id>", methods=["GET"])
def delete_manager(manager_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el administrador existe
        cursor.execute("SELECT * FROM manager WHERE id = %s", (manager_id,))
        manager = cursor.fetchone()

        if manager is None:
            error = "Error: El administrador no existe."
            return render_template('managers/deleted_manager.html', error=error)

        # Insertar los datos del administrador en la tabla deleted_manager
        cursor.execute("""
            INSERT INTO deleted_managers (manager_id, first_name, last_name, 
            gender, identification, birthdate, phone_number, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            manager['id'], manager['first_name'], manager['last_name'], 
            manager['gender'], manager['identification'], manager['birthdate'], 
            manager['phone_number'], manager['address']
        ))

        # Actualizar el estado del administrador a 'Inactivo' en la tabla manager
        cursor.execute("UPDATE manager SET status = 'Inactivo' WHERE id = %s", (manager_id,))
        db.commit()
        return redirect("/managers")
    
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el administrador: {str(e)}"
        return render_template('managers/deleted_manager.html', error=error)

#--------------------------------------------restaura administradores eliminados-------------------------------------------

@app.route("/restore_manager/<int:manager_id>", methods=["GET"])
def restore_manager(manager_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el administrador existe
        cursor.execute("SELECT * FROM manager WHERE id = %s AND status = 'Inactivo'", (manager_id,))
        manager = cursor.fetchone()

        if manager is None:
            error = "Error: El administrador no existe o no está inactivo."
            return render_template('managers/deleted_manager.html', error=error)

        # Eliminar los datos del administrador de la tabla deleted_managers
        cursor.execute("DELETE FROM deleted_managers WHERE manager_id = %s", (manager_id,))

        # Actualizar el estado del administrador a 'Activo'
        cursor.execute("UPDATE manager SET status = 'Activo' WHERE id = %s", (manager_id,))
        db.commit()

        return redirect("/deleted_manager")

    except Exception as e:
        db.rollback()
        error = f"Error al restaurar el administrador: {str(e)}"
        return render_template('managers/deleted_manager.html', error=error)




#--------------------------------------------opciones multiples para empleado--------------------------------------------

@app.route('/employees', methods=['GET'])
def employees():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return render_template('employees/employees.html', employees=employees)

#--------------------------------------------agrega empleado-------------------------------------------

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    if request.method == 'POST':
        first_name = request.form['first_name']
        second_name = request.form.get('second_name', None)
        last_name = request.form['last_name']
        gender = request.form['gender']
        identification = request.form['identification']
        birthdate = request.form['birthdate']
        phone = request.form['phone_number']
        address = request.form['address']
        password = request.form['password']
        created_by = session['manager_name']

        # Validar edad
        birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d").date()
        today = date.today()
        age = today.year - birthdate_obj.year - ((today.month, today.day) < (birthdate_obj.month, birthdate_obj.day))

        if age < 18 or age > 65:
            error = "Error: La edad debe estar entre 18 y 65 años."
            return render_template('employees/add_employee.html', error=error)

        db = get_db()
        cursor = db.cursor()

        # Validar si la contraseña es única
        cursor.execute("SELECT id FROM employees WHERE password = %s", (password,))
        existing_employee = cursor.fetchone()
        if existing_employee:
            password_error = "Error: Las contraseñas deben ser únicas."
            return render_template('employees/add_employee.html', error=password_error)

        cursor.execute("""
            INSERT INTO employees (first_name, second_name, last_name, 
            gender, identification, birthdate, phone_number, 
            address, password, created_by) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, second_name, last_name, gender, identification, birthdate, phone, address, password, created_by))
        db.commit()
        return redirect('/dashboard')

    return render_template('employees/add_employee.html')

#--------------------------------------------edita empleado-------------------------------------------

@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']

        # Check if the password is unique
        cursor.execute("SELECT id FROM employees WHERE password = %s AND id != %s", (password, id))
        existing_employee = cursor.fetchone()

        if existing_employee:
            password_error = "Error: Las contraseñas deben ser únicas."
            cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
            employee = cursor.fetchone()
            return render_template('employees/edit_employee.html', employee=employee, password_error=password_error)

        if password:
            cursor.execute("UPDATE employees SET phone_number=%s, password=%s, address=%s WHERE id=%s",
                           (phone, password, address, id))
        else:
            cursor.execute("UPDATE employees SET phone_number=%s, address=%s WHERE id=%s",
                           (phone, address, id))
        db.commit()
        return redirect('/menu/empleados')

    cursor.execute("SELECT * FROM employees WHERE id=%s", (id,))
    employee = cursor.fetchone()
    return render_template('employees/edit_employee.html', employee=employee)

#--------------------------------------------muestra empleados eliminados-------------------------------------------

@app.route("/deleted_employee", methods=["GET"]) # tabla de empleados eliminados
def show_delete_employee():
    db = get_db()
    cursor = db.cursor()

    #mostrar los empleados eliminados
    cursor.execute("SELECT * FROM employees WHERE status = 'Inactivo'")
    employees = cursor.fetchall()
    return render_template('employees/deleted_employee.html', employees=employees)

#--------------------------------------------elimina empleados-------------------------------------------

@app.route("/deleted_employee/<int:employee_id>", methods=["GET"])
def delete_employee(employee_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el empleado existe
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()

        if employee is None:
            error = "Error: El empleado no existe."
            return render_template('employees/deleted_employee.html', error=error)

        # Insertar los datos del empleado en la tabla deleted_employees
        cursor.execute("""
            INSERT INTO deleted_employees (employee_id, first_name, second_name, 
            last_name, gender, identification, birthdate, 
            phone_number, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            employee['id'], employee['first_name'], employee['second_name'], 
            employee['last_name'], employee['gender'], employee['identification'], 
            employee['birthdate'], employee['phone_number'], employee['address']
        ))

        # Actualizar el estado del empleado a 'Inactivo' en la tabla employees
        cursor.execute("UPDATE employees SET status = 'Inactivo' WHERE id = %s", (employee_id,))
        db.commit()
        return redirect("/employees")
    
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el empleado: {str(e)}"
        return render_template('employees/deleted_employee.html', error=error)

#--------------------------------------------restaura empleados eliminados-------------------------------------------

@app.route("/restore_employee/<int:employee_id>", methods=["GET"])
def restore_employee(employee_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el empleado existe
        cursor.execute("SELECT * FROM employees WHERE id = %s AND status = 'Inactivo'", (employee_id,))
        employee = cursor.fetchone()

        if employee is None:
            error = "Error: El empleado no existe o no está inactivo."
            return render_template('employees/deleted_employee.html', error=error)
        
        # Insertar los datos del empleado en la tabla deleted_employees

        cursor.execute("""
            DELETE FROM deleted_employees WHERE employee_id = %s
        """, (employee_id,))

        # Actualizar el estado del empleado a 'Activo'
        cursor.execute("UPDATE employees SET status = 'Activo' WHERE id = %s", (employee_id,))
        db.commit()

        return redirect("/deleted_employee")
    
    except Exception as e:
        db.rollback()
        error = f"Error al restaurar el empleado: {str(e)}"
        return render_template('employees/deleted_employee.html', error=error)
    
#--------------------------------------------agregar emails-------------------------------------------

@app.route('/add_email_employee', methods=['GET', 'POST'])
def add_email_employee():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        employee_id = request.form['employee_id']
        created_by = session['manager_name']

        db = get_db()
        cursor = db.cursor()
        try:
            # Validate if the employee ID exists
            cursor.execute("SELECT id FROM employees WHERE id = %s AND status != 'Inactivo'", (employee_id,))
            if cursor.fetchone() is None:
                error = "Error: El ID del empleado no existe o está inactivo."
                return render_template('emails/add_email_employee.html', error=error)

            cursor.execute("""
                INSERT INTO employee_emails (email, employee_id, created_by) 
                VALUES (%s, %s, %s)
            """, (email, employee_id, created_by))
            db.commit()
            return redirect('/emails_employee')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el correo electrónico del empleado: {str(e)}"
            return render_template('emails/add_email_employee.html', error=error)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, first_name, last_name FROM employees WHERE status != 'Inactivo'")
    employees = cursor.fetchall()
    return render_template('emails/add_email_employee.html', employees=employees)


@app.route('/add_email_manager', methods=['GET', 'POST'])
def add_email_manager():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        email = request.form['email']
        manager_id = request.form['manager_id']
        created_by = session['manager_name']

        try:
            # Validar si el ID del gerente existe
            cursor.execute("SELECT id FROM manager WHERE id = %s AND status != 'Inactivo'", (manager_id,))
            if cursor.fetchone() is None:
                error = "Error: El ID del gerente no existe o está inactivo."
                return render_template('emails/add_email_manager.html', error=error)

            # Insertar el email
            cursor.execute("""
                INSERT INTO manager_emails (email, manager_id, created_by) 
                VALUES (%s, %s, %s)
            """, (email, manager_id, created_by))
            db.commit()
            return redirect('/emails_manager')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el correo electrónico del gerente: {str(e)}"
            return render_template('emails/add_email_manager.html', error=error)

    # Obtener la lista de gerentes para el formulario
    cursor.execute("SELECT id, first_name, last_name FROM manager")
    managers = cursor.fetchall()
    return render_template('emails/add_email_manager.html', managers=managers)

#--------------------------------------------ver emails-------------------------------------------

@app.route('/emails_employee', methods=['GET'])
def emails_employee():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT ee.* 
        FROM employee_emails ee
        JOIN employees e ON ee.employee_id = e.id
        WHERE e.status = 'Activo'
    """)
    emails = cursor.fetchall()
    return render_template('emails/emails_employee.html', emails=emails)

from collections import defaultdict

from collections import defaultdict

@app.route('/emails_manager', methods=['GET'])
def emails_manager():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT me.* 
        FROM manager_emails me
        JOIN manager m ON me.manager_id = m.id
        WHERE m.status = 'Activo'
    """)
    rows = cursor.fetchall()

    # Ahora como no tenemos 'dictionary', convertimos manualmente
    columns = [desc[0] for desc in cursor.description]
    emails = []
    for row in rows:
        email = dict(zip(columns, row))
        emails.append(email)

    # Contar cuántos correos tiene cada manager
    manager_email_count = defaultdict(int)
    for email in emails:
        manager_email_count[email['manager_id']] += 1

    # Agregar el conteo a cada email
    for email in emails:
        email['manager_email_count'] = manager_email_count[email['manager_id']]

    return render_template('emails/emails_manager.html', emails=emails)


#--------------------------------------------elimina emails-------------------------------------------
@app.route("/delete_email_employee/<int:email_id>", methods=["GET"])
def delete_email_employee(email_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el email existe
        cursor.execute("SELECT * FROM employee_emails WHERE email_id = %s", (email_id,))
        email = cursor.fetchone()

        if email is None:
            error = "Error: El correo electrónico no existe."
            return render_template('emails/emails_employee.html', error=error)

        # Actualizar el estado del email a 'Inactivo' en la tabla employee_emails
        cursor.execute("UPDATE employee_emails SET status = 'Inactivo' WHERE email_id = %s", (email_id,))
        db.commit()
        return redirect("/emails_employee")
    
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el correo electrónico: {str(e)}"
        return render_template('emails/emails_employee.html', error=error)
    
from collections import defaultdict

@app.route("/correos_managers")
def correos_managers():
    # Obtener todos los correos
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM manager_emails")
    emails = cursor.fetchall()
    
    # Contar cuántos correos tiene cada manager
    manager_email_count = defaultdict(int)
    for email in emails:
        manager_email_count[email['manager_id']] += 1

    # Agregar el conteo a cada email
    for email in emails:
        email['manager_email_count'] = manager_email_count[email['manager_id']]

    return render_template("correos_managers.html", emails=emails)
    
@app.route("/delete_email_manager/<int:email_id>", methods=["GET"])
def delete_email_manager(email_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el email existe
        cursor.execute("SELECT * FROM manager_emails WHERE email_id = %s", (email_id,))
        email = cursor.fetchone()

        if email is None:
            error = "Error: El correo electrónico no existe."
            return render_template('emails/emails_manager.html', error=error)

        # Actualizar el estado del email a 'Inactivo' en la tabla manager_emails
        cursor.execute("UPDATE manager_emails SET status = 'Inactivo' WHERE email_id = %s", (email_id,))
        db.commit()
        return redirect("/emails_manager")
    
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el correo electrónico: {str(e)}"
        return render_template('emails/emails_manager.html', error=error)
    
#--------------------------------------------restaura emails empleados-------------------------------------------

@app.route("/restore_email_employee/<int:email_id>", methods=["GET"])
def restore_email_employee(email_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el email existe y está inactivo
        cursor.execute("SELECT * FROM employee_emails WHERE email_id = %s AND status = 'Inactivo'", (email_id,))
        email = cursor.fetchone()

        if email is None:
            error = "Error: El correo electrónico no existe o no está inactivo."
            return render_template('emails/emails_employee.html', error=error)

        # Actualizar el estado del email a 'Activo' en la tabla employee_emails
        cursor.execute("UPDATE employee_emails SET status = 'Activo' WHERE email_id = %s", (email_id,))
        db.commit()
        return redirect("/emails_employee")
    
    except Exception as e:
        db.rollback()
        error = f"Error al restaurar el correo electrónico: {str(e)}"
        return render_template('emails/emails_employee.html', error=error)
    
#--------------------------------------------restaura emails administradores-------------------------------------------

@app.route("/restore_email_manager/<int:email_id>", methods=["GET"])
def restore_email_manager(email_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el email existe y está inactivo
        cursor.execute("SELECT * FROM manager_emails WHERE email_id = %s AND status = 'Inactivo'", (email_id,))
        email = cursor.fetchone()

        if email is None:
            error = "Error: El correo electrónico no existe o no está inactivo."
            return render_template('emails/emails_manager.html', error=error)

        # Actualizar el estado del email a 'Activo' en la tabla manager_emails
        cursor.execute("UPDATE manager_emails SET status = 'Activo' WHERE email_id = %s", (email_id,))
        db.commit()
        return redirect("/emails_manager")
    
    except Exception as e:
        db.rollback()
        error = f"Error al restaurar el correo electrónico: {str(e)}"
        return render_template('emails/emails_manager.html', error=error)


#--------------------------------------------opciones multiple para cliente-------------------------------------------

@app.route('/clients', methods=['GET'])
def clients():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    return render_template('clients/clients.html', clients=clients)

#--------------------------------------------agregar cliente-------------------------------------------

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        created_by = session['manager_name']

        db = get_db()
        cursor = db.cursor()
        try:
            # Validate if the phone number already exists
            cursor.execute("SELECT client_id FROM clients WHERE contact = %s", (contact,))
            existing_contact = cursor.fetchone()
            if existing_contact:
                phone_error = "Error: El número de teléfono ya está registrado."
                return render_template('clients/add_client.html', error=phone_error)

            cursor.execute("""
                INSERT INTO clients (name, contact, address, created_by) 
                VALUES (%s, %s, %s, %s)
            """, (name, contact, address, created_by))
            db.commit()
            return redirect('/clients')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el cliente: {str(e)}"
            return render_template('clients/add_client.html', error=error)

    return render_template('clients/add_client.html')

#--------------------------------------------edita cliente-------------------------------------------
@app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
def edit_client(id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        address = request.form['address']

        # Check if the phone number is unique
        cursor.execute("SELECT client_id FROM clients WHERE contact = %s AND client_id != %s", (contact, id))
        existing_contact = cursor.fetchone()
        if existing_contact:
            phone_error = "Error: El número de teléfono ya está registrado."
            cursor.execute("SELECT * FROM clients WHERE client_id=%s", (id,))
            client = cursor.fetchone()
            return render_template('clients/edit_client.html', client=client, phone_error=phone_error)

        cursor.execute("UPDATE clients SET name=%s, contact=%s, address=%s WHERE client_id=%s",
                       (name, contact, address, id))
        db.commit()
        return redirect('/clients')

    cursor.execute("SELECT * FROM clients WHERE client_id=%s", (id,))
    client = cursor.fetchone()
    return render_template('clients/edit_client.html', client=client)

#--------------------------------------------muestra clientes eliminados-------------------------------------------

@app.route("/deleted_client", methods=["GET"]) # tabla de clientes eliminados
def show_delete_client():
    db = get_db()
    cursor = db.cursor()

    #mostrar los clientes eliminados
    cursor.execute("SELECT * FROM clients WHERE status = 'Inactivo'")
    clients = cursor.fetchall()
    return render_template('clients/deleted_client.html', clients=clients)

#--------------------------------------------elimina clientes-------------------------------------------

@app.route("/deleted_client/<int:client_id>", methods=["GET"])
def delete_client(client_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el cliente existe
        cursor.execute("SELECT * FROM clients WHERE client_id = %s", (client_id,))
        client = cursor.fetchone()

        if client is None:
            error = "Error: El cliente no existe."
            return render_template('clients/deleted_client.html', error=error)

        # Insertar los datos del cliente en la tabla deleted_clients
        cursor.execute("""
            INSERT INTO deleted_clients (client_id, name, contact, address)
            VALUES (%s, %s, %s, %s)
        """, (
            client['client_id'], client['name'], client['contact'], client['address']
        ))

        # Actualizar el estado del cliente a 'Inactivo' en la tabla clients
        cursor.execute("UPDATE clients SET status = 'Inactivo' WHERE client_id = %s", (client_id,))
        db.commit()
        return redirect("/clients")
    
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el cliente: {str(e)}"
        return render_template('clients/deleted_client.html', error=error)

#--------------------------------------------restaura clientes eliminados-------------------------------------------

@app.route("/restore_client/<int:client_id>", methods=["GET"])
def restore_client(client_id):
    db = get_db()
    cursor = db.cursor()
    try:
        # Verificar si el cliente existe
        cursor.execute("SELECT * FROM clients WHERE client_id = %s AND status = 'Inactivo'", (client_id,))
        client = cursor.fetchone()

        if client is None:
            error = "Error: El cliente no existe o no está inactivo."
            return render_template('clients/deleted_client.html', error=error)
        
        # Insertar los datos del cliente en la tabla deleted_clients

        cursor.execute("""
            DELETE FROM deleted_clients WHERE client_id = %s
        """, (client_id,))

        # Actualizar el estado del cliente a 'Activo'
        cursor.execute("UPDATE clients SET status = 'Activo' WHERE client_id = %s", (client_id,))
        db.commit()

        return redirect("/deleted_client")
    
    except Exception as e:
        db.rollback()
        error = f"Error al restaurar el cliente: {str(e)}"
        return render_template('clients/deleted_client.html', error=error)




#--------------------------------------------opciones multiple para proveedor-------------------------------------------

@app.route('/suppliers', methods=['GET'])
def suppliers_view():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT supplier_id, name, contact, created_by, status FROM suppliers WHERE status != 'Inactivo'")
    suppliers = cursor.fetchall()
    return render_template('suppliers/suppliers.html', suppliers=suppliers)

#--------------------------------------------agregar proveedor-------------------------------------------

@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        location = request.form['location']
        created_by = session['manager_name']

        db = get_db()
        cursor = db.cursor()
        try:
            # Validate if the supplier name is unique
            cursor.execute("SELECT supplier_id FROM suppliers WHERE name = %s", (name,))
            existing_name = cursor.fetchone()
            if existing_name:
                name_error = "Error: El nombre del proveedor ya está registrado."
                return render_template('suppliers/add_supplier.html', name_error=name_error)

            # Validate if the contact is unique
            cursor.execute("SELECT supplier_id FROM suppliers WHERE contact = %s", (contact,))
            existing_contact = cursor.fetchone()
            if existing_contact:
                phone_error = "Error: El contacto del proveedor ya está registrado."
                return render_template('suppliers/add_supplier.html', phone_error=phone_error)

            cursor.execute("""
                INSERT INTO suppliers (name, contact, location, created_by) 
                VALUES (%s, %s, %s, %s)
            """, (name, contact, location, created_by))
            db.commit()
            return redirect('/suppliers')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el proveedor: {str(e)}"
            return render_template('suppliers/add_supplier.html', error=error)

    return render_template('suppliers/add_supplier.html')

#--------------------------------------------editar proveedor-------------------------------------------

@app.route('/edit_supplier/<int:supplier_id>', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        location = request.form['location']

        # Validate if the supplier name is unique
        cursor.execute("SELECT supplier_id FROM suppliers WHERE name = %s AND supplier_id != %s", (name, supplier_id))
        existing_name = cursor.fetchone()
        if existing_name:
            name_error = "Error: El nombre del proveedor ya está registrado."
            cursor.execute("SELECT * FROM suppliers WHERE supplier_id=%s", (supplier_id,))
            supplier = cursor.fetchone()
            return render_template('suppliers/edit_supplier.html', supplier=supplier, name_error=name_error)

        # Validate if the contact is unique
        cursor.execute("SELECT supplier_id FROM suppliers WHERE contact = %s AND supplier_id != %s", (contact, supplier_id))
        existing_contact = cursor.fetchone()
        if existing_contact:
            phone_error = "Error: El contacto del proveedor ya está registrado."
            cursor.execute("SELECT * FROM suppliers WHERE supplier_id=%s", (supplier_id,))
            supplier = cursor.fetchone()
            return render_template('suppliers/edit_supplier.html', supplier=supplier, phone_error=phone_error)

        cursor.execute("""
            UPDATE suppliers 
            SET name=%s, contact=%s, location=%s 
            WHERE supplier_id=%s
        """, (name, contact, location, supplier_id))
        db.commit()
        return redirect('/suppliers')

    cursor.execute("SELECT * FROM suppliers WHERE supplier_id=%s", (supplier_id,))
    supplier = cursor.fetchone()
    return render_template('suppliers/edit_supplier.html', supplier=supplier)

#--------------------------------------------mostrar proveedores eliminados-------------------------------------------

@app.route("/deleted_supplier", methods=["GET"])
def show_deleted_supplier():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM suppliers WHERE status = 'Inactivo'")
    suppliers = cursor.fetchall()
    return render_template('suppliers/deleted_supplier.html', suppliers=suppliers)

#--------------------------------------------eliminar proveedor-------------------------------------------

@app.route("/delete_supplier/<int:supplier_id>", methods=["GET"])
def delete_supplier(supplier_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
        supplier = cursor.fetchone()

        if supplier is None:
            error = "Error: El proveedor no existe."
            return render_template('suppliers/deleted_supplier.html', error=error)
        
        cursor.execute("""
            INSERT INTO deleted_suppliers (supplier_id, name, contact, location)
            VALUES (%s, %s, %s, %s)
        """, (
            supplier['supplier_id'], supplier['name'], supplier['contact'], supplier['location']
        ))

        cursor.execute("""
            UPDATE suppliers 
            SET status = 'Inactivo' 
            WHERE supplier_id = %s
        """, (supplier_id,))
        db.commit()
        return redirect("/suppliers")
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el proveedor: {str(e)}"
        return render_template('suppliers/deleted_supplier.html', error=error)

#--------------------------------------------restaurar proveedor-------------------------------------------

@app.route("/restore_supplier/<int:supplier_id>", methods=["GET"])
def restore_supplier(supplier_id):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s AND status = 'Inactivo'", (supplier_id,))
        supplier = cursor.fetchone()

        if supplier is None:
            error = "Error: El proveedor no existe o no está inactivo."
            return render_template('suppliers/deleted_supplier.html', error=error)
        
        cursor.execute("""
            DELETE FROM deleted_suppliers WHERE supplier_id = %s
        """, (supplier_id,))
        # Actualizar el estado del proveedor a 'Activo'

        cursor.execute("""
            UPDATE suppliers 
            SET status = 'Activo' 
            WHERE supplier_id = %s
        """, (supplier_id,))
        db.commit()
        return redirect("/deleted_supplier")
    except Exception as e:
        db.rollback()
        error = f"Error al restaurar el proveedor: {str(e)}"
        return render_template('suppliers/deleted_supplier.html', error=error)
    



#--------------------------------------------opciones multiple para suministros-------------------------------------------

#---------------------------------------------mostrar suministros-------------------------------------------

@app.route('/supplies', methods=['GET'])
def supplies():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM supplies")
    supplies = cursor.fetchall()
    return render_template('supplies/supplies.html', supplies=supplies)

#--------------------------------------------agregar suministros-------------------------------------------

@app.route('/add_supply', methods=['GET', 'POST'])
def add_supply():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        description = request.form['description']
        price = request.form['price']
        supplier_id = request.form['supplier_id']
        created_by = session['manager_name']

        db = get_db()
        cursor = db.cursor()
        try:
            # Validate if the supplier ID exists and is active
            cursor.execute("SELECT name FROM suppliers WHERE supplier_id = %s AND status = 'Activo'", (supplier_id,))
            supplier = cursor.fetchone()
            if supplier is None:
                error = "Error: El ID del proveedor no existe o está inactivo."
                return render_template('supplies/add_supply.html', error=error)

            supplier_name = supplier['name']

            cursor.execute("""
                INSERT INTO supplies (name, quantity, description, price, supplier_id, created_by) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, quantity, description, price, supplier_id, created_by))
            db.commit()
            return redirect('/supplies')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el suministro: {str(e)}"
            return render_template('supplies/add_supply.html', error=error)

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT supplier_id, name FROM suppliers WHERE status = 'Activo'")
    suppliers = cursor.fetchall()
    return render_template('supplies/add_supply.html', suppliers=suppliers)


#--------------------------------------------eliminar suministros-------------------------------------------

@app.route("/delete_supply/<int:supply_id>", methods=["GET"])
def delete_supply(supply_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM supplies WHERE supply_id = %s", (supply_id,))
        supply = cursor.fetchone()

        if supply is None:
            error = "Error: El suministro no existe."
            return render_template('supplies/deleted_supply.html', error=error)

        cursor.execute("DELETE FROM supplies WHERE supply_id = %s", (supply_id,))
        db.commit()
        return redirect("/supplies")
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el suministro: {str(e)}"
        return render_template('supplies/deleted_supply.html', error=error)
    
#--------------------------------------------muestra suministros eliminados-------------------------------------------
@app.route("/deleted_supply", methods=["GET"])
def show_deleted_supply():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM supplies WHERE status = 'Inactivo'")
    supplies = cursor.fetchall()
    return render_template('supplies/deleted_supply.html', supplies=supplies)

#--------------------------------------------editar suministros-------------------------------------------

@app.route('/edit_supply/<int:supply_id>', methods=['GET', 'POST'])
def edit_supply(supply_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        description = request.form['description']
        price = request.form['price']
        supplier_id = request.form['supplier_id']

        # Validate if the supplier ID exists and is active
        cursor.execute("SELECT supplier_id FROM suppliers WHERE supplier_id = %s AND status = 'Activo'", (supplier_id,))
        supplier = cursor.fetchone()
        if supplier is None:
            error = "Error: El ID del proveedor no existe o está inactivo."
            cursor.execute("SELECT * FROM supplies WHERE supply_id=%s", (supply_id,))
            supply = cursor.fetchone()
            return render_template('supplies/edit_supply.html', supply=supply, error=error)

        cursor.execute("""
            UPDATE supplies 
            SET name=%s, quantity=%s, description=%s, price=%s, supplier_id=%s 
            WHERE supply_id=%s
        """, (name, quantity, description, price, supplier_id, supply_id))
        db.commit()
        return redirect('/supplies')

    cursor.execute("SELECT * FROM supplies WHERE supply_id=%s", (supply_id,))
    supply = cursor.fetchone()

    cursor.execute("SELECT supplier_id, name FROM suppliers WHERE status = 'Activo'")
    suppliers = cursor.fetchall()

    return render_template('supplies/edit_supply.html', supply=supply, suppliers=suppliers, supplies=[])









#--------------------------------------------opciones multiple para cargos-------------------------------------------

#--------------------------------------------mostrar cargos-------------------------------------------

@app.route('/positions', methods=['GET'])
def positions():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.* 
        FROM positions p
        LEFT JOIN employees e ON p.employee_id = e.id
        WHERE e.status != 'Inactivo' OR p.employee_id IS NULL
    """)
    positions = cursor.fetchall()
    return render_template('positions/positions.html', positions=positions)

#--------------------------------------------agregar cargos-------------------------------------------

@app.route('/add_position', methods=['GET', 'POST'])
def add_position():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']
        employee_id = request.form.get('employee_id')  # AQUÍ sí lo obtienes
        created_by = session['manager_name']

        if employee_id == '':
            employee_id = None  # Si no selecciona empleado, lo dejas en NULL

        try:
            cursor.execute("""
                INSERT INTO positions (name, employee_id, created_by) 
                VALUES (%s, %s, %s)
            """, (name, employee_id, created_by))
            db.commit()
            return redirect('/positions')  # Redirige donde corresponde
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el cargo: {str(e)}"
            return render_template('positions/add_position.html', error=error)

    # ESTE SELECT es el correcto para traer empleados activos sin cargo:
    cursor.execute("""
        SELECT id, first_name, last_name 
        FROM employees 
        WHERE status = 'Activo' 
        AND id NOT IN (SELECT employee_id FROM positions WHERE employee_id IS NOT NULL)
    """)

    employees = cursor.fetchall()
    return render_template('positions/add_position.html', employees=employees)


#--------------------------------------------editar cargos-------------------------------------------
@app.route('/edit_position/<int:position_id>', methods=['GET', 'POST'])
def edit_position(position_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        name = request.form['name']

        # Update only the position name, keeping the same employee assigned
        cursor.execute("""
            UPDATE positions 
            SET name=%s 
            WHERE position_id=%s
        """, (name, position_id))
        db.commit()
        return redirect('/positions')

    cursor.execute("SELECT * FROM positions WHERE position_id=%s", (position_id,))
    position = cursor.fetchone()
    return render_template('positions/edit_position.html', position=position)

#--------------------------------------------eliminar cargos-------------------------------------------

@app.route("/delete_position/<int:position_id>", methods=["GET"])
def delete_position(position_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM positions WHERE position_id = %s", (position_id,))
        position = cursor.fetchone()

        if position is None:
            error = "Error: El cargo no existe."
            return render_template('positions/deleted_position.html', error=error)

        cursor.execute("DELETE FROM positions WHERE position_id = %s", (position_id,))
        db.commit()
        return redirect("/positions")
    except Exception as e:
        db.rollback()
        error = f"Error al eliminar el cargo: {str(e)}"
        return render_template('positions/deleted_position.html', error=error)

    



#--------------------------------------------opciones multiple para salarios-------------------------------------------

#--------------------------------------------mostrar salarios-------------------------------------------

@app.route('/salaries', methods=['GET'])
def salaries():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM income_table")
    salaries = cursor.fetchall()
    return render_template('salaries/salaries.html', salaries=salaries)

#--------------------------------------------agregar salarios-------------------------------------------

@app.route('/add_salary', methods=['GET', 'POST'])
def add_salary():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        income = request.form['income']
        ini_date = request.form['ini_date']
        account_number = request.form['account_number']
        created_by = session['manager_name']

        try:
            cursor.execute("""
                INSERT INTO income_table (employee_id, income, ini_date, account_number, created_by) 
                VALUES (%s, %s, %s, %s, %s)
            """, (employee_id, income, ini_date, account_number, created_by))
            db.commit()
            return redirect('/salaries')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el salario: {str(e)}"
            return render_template('salaries/add_salary.html', error=error)

    # SOLO empleados que NO tengan salario asignado y que estén activos
    cursor.execute("""
        SELECT id, first_name, last_name 
        FROM employees 
        WHERE id NOT IN (SELECT employee_id FROM income_table) AND status = 'Activo'
    """)
    employees = cursor.fetchall()

    return render_template('salaries/add_salary.html', employees=employees)



#--------------------------------------------editar salarios-------------------------------------------

@app.route('/edit_salary/<int:salary_id>', methods=['GET', 'POST'])
def edit_salary(salary_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        income = request.form['income']
        ini_date = request.form['ini_date']
        account_number = request.form['account_number']

        cursor.execute("""
            UPDATE income_table 
            SET income=%s, ini_date=%s, account_number=%s 
            WHERE income_id=%s
        """, (income, ini_date, account_number, salary_id))
        db.commit()
        success = "Salario actualizado correctamente."
        cursor.execute("SELECT * FROM income_table WHERE income_id=%s", (salary_id,))
        salary = cursor.fetchone()
        return render_template('salaries/edit_salary.html', salary=salary, success=success)

    cursor.execute("SELECT * FROM income_table WHERE income_id=%s", (salary_id,))
    salary = cursor.fetchone()
    return render_template('salaries/edit_salary.html', salary=salary)

#--------------------------------------------mostrar salarios manager-------------------------------------------

@app.route('/salaries_manager', methods=['GET'])
def salaries_manager():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM manager_income_table")
    salaries = cursor.fetchall()
    return render_template('salaries/salaries_manager.html', salaries=salaries)

#--------------------------------------------agregar salarios-------------------------------------------

@app.route('/add_salary_manager', methods=['GET', 'POST'])
def add_salary_manager():
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        manager_id = request.form['manager_id']
        income = request.form['income']
        ini_date = request.form['ini_date']
        account_number = request.form['account_number']
        created_by = session['manager_name']

        try:
            cursor.execute("""
                INSERT INTO manager_income_table (manager_id, income, ini_date, account_number, created_by) 
                VALUES (%s, %s, %s, %s, %s)
            """, (manager_id, income, ini_date, account_number, created_by))
            db.commit()
            return redirect('/salaries_manager')
        except Exception as e:
            db.rollback()
            error = f"Error al agregar el salario: {str(e)}"
            return render_template('salaries/add_salary_manager.html', error=error)

    # SOLO gerentes que NO tengan salario asignado y que estén activos
    cursor.execute("""
        SELECT id, first_name, last_name 
        FROM manager 
        WHERE id NOT IN (SELECT manager_id FROM manager_income_table) AND status = 'Activo'
    """)
    managers = cursor.fetchall()

    return render_template('salaries/add_salary_manager.html', managers=managers)

#--------------------------------------------editar salarios-------------------------------------------

@app.route('/edit_salary_manager/<int:salary_id>', methods=['GET', 'POST'])
def edit_salary_manager(salary_id):
    if 'user' not in session or session['role'] != 'manager':
        return redirect('/')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        income = request.form['income']
        ini_date = request.form['ini_date']
        account_number = request.form['account_number']

        cursor.execute("""
            UPDATE manager_income_table 
            SET income=%s, ini_date=%s, account_number=%s 
            WHERE income_id=%s
        """, (income, ini_date, account_number, salary_id))
        db.commit()
        success = "Salario actualizado correctamente."
        cursor.execute("SELECT * FROM manager_income_table WHERE income_id=%s", (salary_id,))
        salary = cursor.fetchone()
        return render_template('salaries/edit_salary_manager.html', salary=salary, success=success)

    cursor.execute("SELECT * FROM manager_income_table WHERE income_id=%s", (salary_id,))
    salary = cursor.fetchone()
    return render_template('salaries/edit_salary_manager.html', salary=salary)

if __name__ == '__main__':
    app.run(debug=True)