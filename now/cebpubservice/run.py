from utils.spider_cebpubservice import CebpubService, spider_main
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import freeze_support
import sys

if __name__ == "__main__":
    # CebpubService().run()
    # freeze_support()
    # arg = sys.argv[1]
    # CebpubService().main(arg)
    spider_main()

    # sched = BlockingScheduler()
    # trigger = IntervalTrigger(hours=1)
    # sched.add_job(CebpubService().main, trigger, max_instances=10)
    # sched.start()