from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .services import hitas_text_post
from datetime import datetime, timedelta

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)


    @scheduler.scheduled_job('interval', hours=3, name='hitas', next_run_time=datetime.now() + timedelta(seconds=20))
    def job():
        hitas_text_post()
    
    scheduler.start()