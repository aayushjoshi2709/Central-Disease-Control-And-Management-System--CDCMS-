from cdcms import app,db
from flask import render_template, redirect, url_for, flash, session
from cdcms.models import Employee, Hospital, Patient
from cdcms.forms import hospital_login_form,patient_registration_form, hospital_registration_form, employee_login_form, employee_registration_form, search_cases_form
from flask_login import login_user, logout_user, current_user
from functools import wraps
import joblib
from sqlalchemy import func

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
               return app.login_manager.unauthorized()
            urole = current_user.get_urole()
            if ( (urole != role) and (role != "ANY")):
                return app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def predict_disease(symptoms):
    pipeline = joblib.load('../pipeline.pkl')
    return pipeline.predict(symptoms)


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('Home.html')

def get_unique(s):
    return list(set(s.split(";")))

@app.route("/dashboard")
@login_required(role="ANY")
def dashboard_page():
    diseases = db.session.query(Patient.actual_disease,func.group_concat(Patient.symptoms,";"),func.count(Patient.id)).group_by(Patient.actual_disease).order_by(func.count(Patient.id).desc()).all()
    print(diseases)
    return render_template('Dashboard.html', diseases=diseases, get_unique=get_unique)

@app.route("/doctor/signup", methods=['GET', 'POST']) 
@login_required(role="hospital")
def doctor_signup_page():
    form  = employee_registration_form()
    if form.validate_on_submit():
        doctor_to_create = Employee(name=form.name.data,
                                    designation=form.designation.data,
                                    access_level=form.access_level.data,
                                    contact=form.contact.data,
                                    username=form.username.data,
                                    email=form.email.data,
                                    password=form.password1.data,
                                    associated_hospital=current_user.id)
        db.session.add(doctor_to_create)
        db.session.commit()
        flash(f'Account created successfully!', category='success')
        return redirect(url_for('dashboard_page'))
    if len(form.errors) > 0:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a doctor: {err_msg}', category='danger')
    return render_template('SignUpDoctor.html', form = form)

@app.route("/doctor/signin", methods=['GET', 'POST']) 
def doctor_signin_page():
    form = employee_login_form()
    if form.validate_on_submit():
        attempted_user = Employee.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            session.permanent = True
            session["type"] = "doctor"
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('SignInDoctor.html', form = form)

@app.route("/hospital/signup", methods=['GET', 'POST']) 
def hospital_signup_page():
    form = hospital_registration_form()
    if form.validate_on_submit():
        hospital_to_create = Hospital(name=form.name.data,
                                    address=form.address.data,
                                    contact=form.contact.data,
                                    username=form.username.data,
                                    email=form.email.data,
                                    city=form.city.data,
                                    password=form.password1.data)
        db.session.add(hospital_to_create)
        db.session.commit()
        print(hospital_to_create)
        session.permanent = True
        session["type"] = "hospital"
        login_user(hospital_to_create)
        flash(f'Account created successfully! You are now logged in as {hospital_to_create.username}', category='success')
        return redirect(url_for('dashboard_page'))
    if len(form.errors) > 0:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a hospital: {err_msg}', category='danger')
    return render_template('SignupHospital.html', form=form)

@app.route("/hospital/signin", methods=['GET', 'POST']) 
def hospital_signin_page():
    form = hospital_login_form()
    if form.validate_on_submit():
        attempted_user = Hospital.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            session.permanent = True
            session["type"] = "hospital"
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('SignInHospital.html', form=form)

@app.route("/patient/new", methods=['GET', 'POST'])
@login_required(role="doctor")
def patient_add_page():
    form = patient_registration_form()
    if form.validate_on_submit():
        patient_to_create = Patient(name=form.name.data,
                                    age=form.age.data,
                                    address=form.address.data,
                                    contact=form.contact.data,
                                    associated_employee=current_user.id,
                                    associated_hospital=current_user.associated_hospital,
                                    symptoms=form.symptoms.data,
                                    actual_disease=form.actual_disease.data,
                                    medication_given=form.medication_given.data,
                                    aadhar_number=form.aadhar_no.data,
                                    date_of_admission=form.date_of_admission.data,
                                    previous_records=form.previous_records.data)
        db.session.add(patient_to_create)
        db.session.commit()
        flash(f'Patient added successfully!', category='success')
        return redirect(url_for('dashboard_page'))
    if len(form.errors) > 0:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a hospital: {err_msg}', category='danger')
    return render_template('PatientRegistration.html', form=form)

@app.route("/cases/search", methods=['GET', 'POST'])
@login_required(role="ANY")
def search_cases_page():
    form = search_cases_form()
    if form.validate_on_submit():
        patients = None
        query = form.query.data.upper()
        if form.type.data == "aadhar_no":
            patients = Patient.query.filter(func.upper(Patient.aadhar_number)==query).all()
        elif form.type.data == "name":
            patients = Patient.query.filter(func.upper(Patient.name)==query).all()
        elif form.type.data == "actual_disease":
            patients = Patient.query.filter(func.upper(Patient.actual_disease)==query).all()
        elif form.type.data == "contact":
            patients = Patient.query.filter(func.upper(Patient.contact)==query).all()   
        return render_template('SearchCases.html', form = form, patients=patients, get_unique=get_unique)
    if len(form.errors) > 0:
        for err_msg in form.errors.values():
            flash(f'There was an error in searching: {err_msg}', category='danger')
    return render_template('SearchCases.html', form = form, patients=None)

@app.route("/logout")
def logout_page():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('home_page'))