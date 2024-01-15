from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'password'
DB_HOST = '0.0.0.0'

def get_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM Doctor;')
    doctors = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', doctors=doctors)
    
@app.route('/doctor/<int:doctor_id>', methods=['GET', 'POST'])
def doctor(doctor_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        patient_name = request.form['patient_name']
        date_of_treatment = request.form['date_of_treatment']
        cur.execute('INSERT INTO History (doctor_id, patient_name, date_of_treatment) VALUES (%s, %s, %s)', (doctor_id, patient_name, date_of_treatment))
        conn.commit()

    cur.execute("SELECT * FROM Doctor WHERE id = %s;", (doctor_id, ))
    doctor = cur.fetchone()

    cur.execute('SELECT * FROM History WHERE doctor_id = %s;', (doctor_id, ))
    histories = cur.fetchall()

    cur.close()
    conn.close()
    
    return render_template('doctor.html', doctor=doctor, histories=histories)

@app.route('/history')
def history():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT h.id, d.name AS doctor_name, h.patient_name, h.date_of_treatment FROM History h JOIN Doctor d ON h.doctor_id = d.id')
    histories = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('history.html', histories=histories)
    
if __name__ == '__main__':
    app.run(debug=True)