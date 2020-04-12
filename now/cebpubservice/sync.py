from utils.upload import UploadSomething
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    UploadSomething().main()
    
    sched = BlockingScheduler()
    sched.add_job(UploadSomething().main,
                  'interval',
                  hours=1,
                  max_instances=10)
    sched.start()
