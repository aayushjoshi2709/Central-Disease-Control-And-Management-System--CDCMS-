from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from cdcms.models import Employee, Hospital

class employee_registration_form(FlaskForm):
    def validate_username(self, username_to_check):
        user = Employee.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
    def validate_email(self, email_to_check):
        email = Employee.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email.')
    name = StringField(label='Name ', validators=[Length(min=2, max=80), DataRequired()])
    designation = StringField(label='Designation ', validators=[Length(min=2, max=80), DataRequired()])
    access_level = StringField(label='Access Level ', validators=[Length(min=2, max=80), DataRequired()])
    contact = StringField(label='Contact ', validators=[Length(min=10,max=10),DataRequired()])
    username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(message='Invalid Email Address'), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class employee_login_form(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign In')

class hospital_login_form(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField(label='Sign In')



class hospital_registration_form(FlaskForm):
    def validate_username(self, username_to_check):
        user = Hospital.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username.')
    def validate_email(self, email_to_check):
        email = Hospital.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists! Please try a different email.')
    name = StringField(label='Name ', validators=[Length(min=2, max=80), DataRequired()])
    address = StringField(label='Address ', validators=[Length(min=2, max=80), DataRequired()])
    contact = StringField(label='Contact ', validators=[Length(min=10,max=10),DataRequired()])
    username = StringField(label='User Name', validators=[Length(min=2,max=30), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(message='Invalid Email Address'), DataRequired()])
    city = StringField(label='City', validators=[Length(min=6), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

class patient_registration_form(FlaskForm):
    name = StringField(label='Name ', validators=[Length(min=2, max=80), DataRequired()])
    age = StringField(label='Age ', validators=[Length(min=1, max=3), DataRequired()])
    aadhar_no = StringField(label='Aadhar No ', validators=[Length(min=12, max=12), DataRequired()])
    address = StringField(label='Address ', validators=[Length(min=2, max=80), DataRequired()])
    contact = StringField(label='Contact ', validators=[Length(min=10, max=10), DataRequired()])
    symptoms = StringField(label='Symptoms (Seprated by colon(;) sign) ', validators=[Length(min=2, max=80), DataRequired()])
    actual_disease = StringField(label='Actual Disease ', validators=[Length(min=2, max=80), DataRequired()])
    medication_given = StringField(label='Medication Given ', validators=[Length(min=2, max=80), DataRequired()])
    date_of_admission = DateField(label='Date of Admission ', validators=[DataRequired()])
    previous_records = BooleanField(label='Any Previous Records ')
    submit = SubmitField(label='Add Patient')

class search_cases_form(FlaskForm):
    query = StringField(label='Search Query ', validators=[Length(min=2, max=80), DataRequired()])
    type = SelectField(label="Search Type", choices=[('name', 'Name'), ('aadhar_no', 'Aadhar No'), ('contact', 'Contact'), ('actual_disease', 'Actual Disease')], validators=[DataRequired()])
    submit = SubmitField(label='Search')