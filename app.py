from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
import os

app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)
app.config['SECRET_KEY'] = 'shms_secret_key_2024'

DB_PATH = 'health.db'

# ── DB Init ──────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'doctor',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            class TEXT,
            section TEXT,
            blood_group TEXT,
            contact TEXT,
            parent_contact TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            diagnosis TEXT,
            symptoms TEXT,
            treatment TEXT,
            medications TEXT,
            weight REAL,
            height REAL,
            blood_pressure TEXT,
            temperature REAL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            reason TEXT,
            status TEXT DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id),
            FOREIGN KEY (doctor_id) REFERENCES users(id)
        );
    ''')

    # Seed demo doctor
    pw = hashlib.sha256('doctor123'.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
                  ('Dr. Thanusree', 'doctor@school.com', pw, 'doctor'))
    except:
        pass

    # Seed demo patients
    students = [
        ('S001','Arjun Kumar',17,'Male','12','A','O+','9876543210','9876543211','Chennai'),
        ('S002','Priya Sharma',16,'Female','11','B','A+','8765432109','8765432110','Bengaluru'),
        ('S003','Rahul Verma',15,'Male','10','C','B+','7654321098','7654321099','Mumbai'),
        ('S004','Sneha Patel',17,'Female','12','B','AB+','6543210987','6543210988','Delhi'),
        ('S005','Kiran Rao',16,'Male','11','A','O-','5432109876','5432109877','Hyderabad'),
        ('S006','Divya Nair',15,'Female','10','A','A-','4321098765','4321098766','Kochi'),
        ('S007','Amit Singh',17,'Male','12','C','B-','3210987654','3210987655','Jaipur'),
        ('S008','Meera Iyer',16,'Female','11','B','AB-','2109876543','2109876544','Pune'),
    ]
    for s in students:
        try:
            c.execute("""INSERT INTO patients 
                (student_id,name,age,gender,class,section,blood_group,contact,parent_contact,address)
                VALUES (?,?,?,?,?,?,?,?,?,?)""", s)
        except:
            pass

    conn.commit()

    # Seed health records
    doctor = c.execute("SELECT id FROM users WHERE email='doctor@school.com'").fetchone()
    if doctor:
        did = doctor['id']
        records = [
            (1, did, '2024-03-01', 'Common Cold', 'Fever, Runny nose', 'Rest and fluids', 'Paracetamol 500mg', 55.0, 168.0, '110/70', 37.8, 'Recovering well'),
            (2, did, '2024-03-05', 'Migraine', 'Headache, Sensitivity to light', 'Avoid screen time', 'Ibuprofen 400mg', 52.0, 162.0, '105/68', 36.9, 'Needs follow-up'),
            (3, did, '2024-03-08', 'Sprained Ankle', 'Ankle pain, Swelling', 'RICE therapy', 'Pain balm', 65.0, 170.0, '118/76', 36.7, 'Avoid sports for 2 weeks'),
            (4, did, '2024-03-10', 'Allergic Reaction', 'Skin rash, Itching', 'Antihistamine', 'Cetirizine 10mg', 58.0, 165.0, '112/72', 37.1, 'Avoid allergen'),
            (5, did, '2024-03-12', 'Viral Fever', 'High fever, Body ache', 'Rest, plenty of fluids', 'Paracetamol + Vitamin C', 60.0, 167.0, '108/70', 38.9, 'Monitor for 3 days'),
            (1, did, '2024-03-15', 'Follow-up', 'Mild cough remaining', 'Continue medication', 'Cough syrup', 55.5, 168.0, '112/70', 36.8, 'Full recovery expected'),
            (6, did, '2024-03-18', 'Stomach Ache', 'Abdominal pain, Nausea', 'Light diet, rest', 'Antacid', 48.0, 158.0, '100/65', 37.2, 'No serious concern'),
            (7, did, '2024-03-20', 'Eye Infection', 'Red eye, Discharge', 'Eye drops', 'Chloramphenicol eye drops', 68.0, 175.0, '120/78', 36.9, 'Keep eye clean'),
            (2, did, '2024-03-22', 'Follow-up Migraine', 'Headache reduced', 'Continue rest', 'Multivitamins', 52.0, 162.0, '108/68', 36.7, 'Good improvement'),
            (8, did, '2024-03-25', 'Dental Pain', 'Toothache', 'Dentist referral', 'Clove oil', 54.0, 163.0, '110/70', 36.8, 'Referred to dental clinic'),
        ]
        for r in records:
            try:
                c.execute("""INSERT INTO health_records 
                    (patient_id,doctor_id,visit_date,diagnosis,symptoms,treatment,medications,weight,height,blood_pressure,temperature,notes)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""", r)
            except:
                pass

        # Seed appointments
        apts = [
            (1, did, '2024-04-10', '09:00', 'Regular checkup', 'scheduled'),
            (2, did, '2024-04-10', '09:30', 'Migraine follow-up', 'scheduled'),
            (3, did, '2024-04-11', '10:00', 'Ankle review', 'scheduled'),
            (4, did, '2024-04-11', '10:30', 'Allergy test results', 'completed'),
            (5, did, '2024-04-09', '11:00', 'Fever checkup', 'completed'),
        ]
        for a in apts:
            try:
                c.execute("""INSERT INTO appointments 
                    (patient_id,doctor_id,appointment_date,appointment_time,reason,status)
                    VALUES (?,?,?,?,?,?)""", a)
            except:
                pass

    conn.commit()
    conn.close()

# ── Auth Helpers ──────────────────────────────────────────────────────────────
def make_token(user_id, email, role):
    payload = {
        'user_id': user_id, 'email': email, 'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(req):
    auth = req.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    try:
        return jwt.decode(auth[7:], app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None

def require_auth(f):
    from functools import wraps
    @wraps(f)
    def wrapper(*args, **kwargs):
        payload = verify_token(request)
        if not payload:
            return jsonify({'error': 'Unauthorized'}), 401
        request.user = payload
        return f(*args, **kwargs)
    return wrapper

# ── Auth Routes ───────────────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    pw = hashlib.sha256(data['password'].encode()).hexdigest()
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email=? AND password=?",
                        (data['email'], pw)).fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = make_token(user['id'], user['email'], user['role'])
    return jsonify({'token': token, 'user': {'id': user['id'], 'name': user['name'],
                                              'email': user['email'], 'role': user['role']}})

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    pw = hashlib.sha256(data['password'].encode()).hexdigest()
    conn = get_db()
    try:
        conn.execute("INSERT INTO users (name, email, password, role) VALUES (?,?,?,?)",
                     (data['name'], data['email'], pw, data.get('role', 'doctor')))
        conn.commit()
        user = conn.execute("SELECT * FROM users WHERE email=?", (data['email'],)).fetchone()
        token = make_token(user['id'], user['email'], user['role'])
        conn.close()
        return jsonify({'token': token, 'user': {'id': user['id'], 'name': user['name'],
                                                  'email': user['email'], 'role': user['role']}})
    except Exception as e:
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400

# ── Patient Routes ────────────────────────────────────────────────────────────
@app.route('/api/patients', methods=['GET'])
@require_auth
def get_patients():
    q = request.args.get('q', '')
    conn = get_db()
    if q:
        patients = conn.execute(
            "SELECT * FROM patients WHERE name LIKE ? OR student_id LIKE ? OR class LIKE ?",
            (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    else:
        patients = conn.execute("SELECT * FROM patients ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(p) for p in patients])

@app.route('/api/patients/<int:pid>', methods=['GET'])
@require_auth
def get_patient(pid):
    conn = get_db()
    p = conn.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone()
    records = conn.execute(
        """SELECT hr.*, u.name as doctor_name FROM health_records hr
           JOIN users u ON hr.doctor_id=u.id WHERE hr.patient_id=? ORDER BY hr.visit_date DESC""",
        (pid,)).fetchall()
    conn.close()
    if not p:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'patient': dict(p), 'records': [dict(r) for r in records]})

@app.route('/api/patients', methods=['POST'])
@require_auth
def add_patient():
    d = request.json
    conn = get_db()
    try:
        conn.execute("""INSERT INTO patients 
            (student_id,name,age,gender,class,section,blood_group,contact,parent_contact,address)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (d['student_id'], d['name'], d.get('age'), d.get('gender'), d.get('class'),
             d.get('section'), d.get('blood_group'), d.get('contact'),
             d.get('parent_contact'), d.get('address')))
        conn.commit()
        pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return jsonify({'id': pid, 'message': 'Patient added'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/patients/<int:pid>', methods=['PUT'])
@require_auth
def update_patient(pid):
    d = request.json
    conn = get_db()
    conn.execute("""UPDATE patients SET name=?,age=?,gender=?,class=?,section=?,
        blood_group=?,contact=?,parent_contact=?,address=? WHERE id=?""",
        (d['name'], d.get('age'), d.get('gender'), d.get('class'), d.get('section'),
         d.get('blood_group'), d.get('contact'), d.get('parent_contact'), d.get('address'), pid))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Updated'})

@app.route('/api/patients/<int:pid>', methods=['DELETE'])
@require_auth
def delete_patient(pid):
    conn = get_db()
    conn.execute("DELETE FROM health_records WHERE patient_id=?", (pid,))
    conn.execute("DELETE FROM appointments WHERE patient_id=?", (pid,))
    conn.execute("DELETE FROM patients WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Deleted'})

# ── Health Record Routes ───────────────────────────────────────────────────────
@app.route('/api/records', methods=['POST'])
@require_auth
def add_record():
    d = request.json
    conn = get_db()
    conn.execute("""INSERT INTO health_records 
        (patient_id,doctor_id,visit_date,diagnosis,symptoms,treatment,medications,
         weight,height,blood_pressure,temperature,notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (d['patient_id'], request.user['user_id'], d['visit_date'], d.get('diagnosis'),
         d.get('symptoms'), d.get('treatment'), d.get('medications'),
         d.get('weight'), d.get('height'), d.get('blood_pressure'),
         d.get('temperature'), d.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Record added'})

# ── Appointment Routes ─────────────────────────────────────────────────────────
@app.route('/api/appointments', methods=['GET'])
@require_auth
def get_appointments():
    conn = get_db()
    apts = conn.execute("""
        SELECT a.*, p.name as patient_name, p.student_id, p.class, p.section
        FROM appointments a JOIN patients p ON a.patient_id=p.id
        WHERE a.doctor_id=? ORDER BY a.appointment_date, a.appointment_time
    """, (request.user['user_id'],)).fetchall()
    conn.close()
    return jsonify([dict(a) for a in apts])

@app.route('/api/appointments', methods=['POST'])
@require_auth
def add_appointment():
    d = request.json
    conn = get_db()
    conn.execute("""INSERT INTO appointments 
        (patient_id,doctor_id,appointment_date,appointment_time,reason,status)
        VALUES (?,?,?,?,?,?)""",
        (d['patient_id'], request.user['user_id'], d['appointment_date'],
         d['appointment_time'], d.get('reason'), d.get('status', 'scheduled')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appointment booked'})

@app.route('/api/appointments/<int:aid>', methods=['PUT'])
@require_auth
def update_appointment(aid):
    d = request.json
    conn = get_db()
    conn.execute("UPDATE appointments SET status=? WHERE id=?", (d['status'], aid))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Updated'})

# ── Analytics Route ────────────────────────────────────────────────────────────
@app.route('/api/analytics', methods=['GET'])
@require_auth
def analytics():
    conn = get_db()

    total_patients = conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
    total_records = conn.execute("SELECT COUNT(*) FROM health_records").fetchone()[0]
    total_appointments = conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]
    today_appointments = conn.execute(
        "SELECT COUNT(*) FROM appointments WHERE appointment_date=date('now')").fetchone()[0]

    diagnoses = conn.execute("""
        SELECT diagnosis, COUNT(*) as count FROM health_records 
        WHERE diagnosis IS NOT NULL GROUP BY diagnosis ORDER BY count DESC LIMIT 6
    """).fetchall()

    monthly = conn.execute("""
        SELECT strftime('%Y-%m', visit_date) as month, COUNT(*) as visits
        FROM health_records GROUP BY month ORDER BY month DESC LIMIT 6
    """).fetchall()

    gender_dist = conn.execute("""
        SELECT gender, COUNT(*) as count FROM patients 
        WHERE gender IS NOT NULL GROUP BY gender
    """).fetchall()

    class_dist = conn.execute("""
        SELECT class, COUNT(*) as count FROM patients 
        WHERE class IS NOT NULL GROUP BY class ORDER BY class
    """).fetchall()

    blood_groups = conn.execute("""
        SELECT blood_group, COUNT(*) as count FROM patients 
        WHERE blood_group IS NOT NULL GROUP BY blood_group
    """).fetchall()

    conn.close()
    return jsonify({
        'summary': {
            'total_patients': total_patients,
            'total_records': total_records,
            'total_appointments': total_appointments,
            'today_appointments': today_appointments
        },
        'diagnoses': [dict(d) for d in diagnoses],
        'monthly_visits': [dict(m) for m in monthly],
        'gender_dist': [dict(g) for g in gender_dist],
        'class_dist': [dict(c) for c in class_dist],
        'blood_groups': [dict(b) for b in blood_groups]
    })

# ── Serve Frontend ─────────────────────────────────────────────────────────────
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    print("🏥 Student Health Management System running at http://localhost:5000")
    print("📧 Login: doctor@school.com | Password: doctor123")
    app.run(debug=True, port=5000)
