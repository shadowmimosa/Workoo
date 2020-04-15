from utils.upload import UploadSomething
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    UploadSomething().main()

    sched = BlockingScheduler()
    trigger = IntervalTrigger(hours=1)
    sched.add_job(UploadSomething().main, trigger, max_instances=10)
    sched.start()
