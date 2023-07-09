from cdcms import app
from cdcms import db
from cdcms.models import Patient
from classifier import fit_data, build_model
from sqlalchemy import func
import logging
from cdcms import scheduler

logging.basicConfig(filename='cron.log', level=logging.INFO)

def my_cron_job():
    logging.info("Running my cron job!")
    diseases = None
    disease_dict = dict()
    with app.app_context():
        diseases = db.session.query(Patient.actual_disease,func.group_concat(Patient.symptoms,";")).group_by(Patient.actual_disease).all()
        for disease in diseases:
            disease_dict[disease[0].lower()] = list(map(lambda x: x.strip().lower(), list(set(disease[1].split(";")))))
    fit_data(disease_dict)
    build_model()
    logging.info("finished")

@app.route('/run_cron')
def run_cron():
    my_cron_job()
    return 'Cron job executed!'

@scheduler.task('cron', id='my_cron_job', hour=0, minute=2)
def run_my_cron_job():
    my_cron_job()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)