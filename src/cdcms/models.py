from cdcms import db, login_manager
from flask import session
from flask_login import UserMixin
from cdcms import bcrypt
@login_manager.user_loader
def load_user(user_id):
    type = session.get("type")
    if type == "doctor":
        return Employee.query.get(int(user_id))
    elif type == "hospital":
        return Hospital.query.get(int(user_id))

class Employee(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(80), nullable=False)
    access_level = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    associated_hospital = db.Column(db.Integer, db.ForeignKey('hospital.id'))
    associated_patient = db.relationship('Patient', backref='doctor_employee', lazy=True)
    password_hash = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def is_doctor(self):
        return True
    
    def is_hospital(self):
        return False
    
    def get_urole(self):
            return "doctor"

class Hospital(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(80), nullable=False)
    associated_employee = db.relationship('Employee', backref='worker_employee', lazy=True)
    associated_patient = db.relationship('Patient', backref='admitting_hospital', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def is_hospital(self):
        return True
    
    def is_doctor(self):
        return False
    
    def get_urole(self):
        return "hospital"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    associated_hospital = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    associated_employee = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    symptoms = db.Column(db.String(500), nullable=False)
    actual_disease = db.Column(db.String(100), nullable=False)
    medication_given = db.Column(db.String(100), nullable=False)
    aadhar_number = db.Column(db.String(12), nullable=False)
    date_of_admission = db.Column(db.Date(), nullable=False)
    previous_records = db.Column(db.Boolean(), nullable=False)
    def __repr__(self):
        return '<Patient %r>' % self.name