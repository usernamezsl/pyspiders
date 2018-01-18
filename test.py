from multiprocessing import Pool
import time
import os


def task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    print(start)
    time.sleep(3)


if __name__ == '__main__':
    print('Parent process %s' % os.getppid())
    p = Pool()
    for i in range(9):
        p.apply_async(task, args=(i,))
    print('Waiting for all subprocess done ...')
    p.close()
    p.join()
    print('All subprocess done')