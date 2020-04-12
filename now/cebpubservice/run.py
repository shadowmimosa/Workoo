from utils.spider_cebpubservice import CebpubService
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    CebpubService().main()
    
    sched = BlockingScheduler()
    sched.add_job(CebpubService().main, 'interval', hours=1, max_instances=10)
    sched.start()