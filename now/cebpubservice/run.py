from utils.spider_cebpubservice import CebpubService
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    CebpubService().run()
    
    # sched = BlockingScheduler()
    # trigger = IntervalTrigger(hours=1)
    # sched.add_job(CebpubService().main, trigger, max_instances=10)
    # sched.start()