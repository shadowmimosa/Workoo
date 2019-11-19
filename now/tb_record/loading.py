'''
进度条的三种方式
'''
from progressbar import *
import time

# 进度条的第一种形式
total = 1000
widgets = [
    'Progress: ',
    Percentage(), ' ',
    Bar(''), ' ',
    Timer(), ' ',
    ETA(), ' ',
    FileTransferSpeed()
]
progress = ProgressBar(widgets=widgets, maxval=10 * total).start()
for i in range(total):
    progress.update(10 * i + 1)
    time.sleep(0.01)
progress.finish()

# 进度条的第二种方式
a = 0
for x in range(0, 100):
    a += x
total = 1000
pro = ProgressBar()
for i in pro(range(total)):
    time.sleep(0.001)
print(a)

# # 进度条的第三种方式
# for i in tqdm(range(0, 1000)):
#     time.sleep(0.01)
