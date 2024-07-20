from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from pyngrok import ngrok

app = Flask(__name__)
port = "5000"



# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize the database
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    contact_no = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    op_id = db.Column(db.String(50), nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(200), nullable=False)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    area_of_expertise = db.Column(db.String(200), nullable=False)
    summary_of_experience = db.Column(db.String(500), nullable=False)
    available = db.Column(db.Boolean, default=True)

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        contact_no=data['contact_no'],
        address=data['address'],
        op_id=data['op_id']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message': 'New patient added successfully'}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    output = []
    for patient in patients:
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'contact_no': patient.contact_no,
            'address': patient.address,
            'op_id': patient.op_id
        }
        output.append(patient_data)
    return jsonify(output)

@app.route('/patients/check_opid/<opid>', methods=['GET'])
def check_opid(opid):
    patient = Patient.query.filter_by(op_id=opid).first()
    if patient:
        return jsonify({'exists': True, 'patient': {
            'name': patient.name, 
            'age': patient.age, 
            'gender': patient.gender, 
            'contact_no': patient.contact_no, 
            'address': patient.address, 
            'op_id': patient.op_id
        }})
    else:
        return jsonify({'exists': False})

@app.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.get_json()
    new_doctor = Doctor(
        name=data['name'],
        designation=data['designation'],
        specialization=data['specialization'],
        qualification=data['qualification'],
        experience=data['experience'],
        area_of_expertise=data['area_of_expertise'],
        summary_of_experience=data['summary_of_experience'],
        available=data['available']
    )
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message': 'New doctor added successfully'}), 201

@app.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    output = []
    for doctor in doctors:
        doctor_data = {
            'id': doctor.id,
            'name': doctor.name,
            'designation': doctor.designation,
            'specialization': doctor.specialization,
            'qualification': doctor.qualification,
            'experience': doctor.experience,
            'area_of_expertise': doctor.area_of_expertise,
            'summary_of_experience': doctor.summary_of_experience,
            'available': doctor.available
        }
        output.append(doctor_data)
    return jsonify(output)

@app.route('/doctors/check_availability/<name>', methods=['GET'])
def check_doctor_availability(name):
    doctor = Doctor.query.filter_by(name=name).first()
    if doctor:
        return jsonify({'available': doctor.available})
    else:
        return jsonify({'error': 'Doctor not found'}), 404

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.get_json()
    new_appointment = Appointment(
        patient_id=data['patient_id'],
        doctor_id=data['doctor_id'],
        date=data['date'],
        time=data['time'],
        reason=data['reason']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'New appointment added successfully'}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    output = []
    for appointment in appointments:
        appointment_data = {
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'doctor_id': appointment.doctor_id,
            'date': appointment.date,
            'time': appointment.time,
            'reason': appointment.reason
        }
        output.append(appointment_data)
    return jsonify(output)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(port=port)
