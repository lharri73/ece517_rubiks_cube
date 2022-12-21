import errno
import os
import signal
import functools
import time
import multiprocessing
import os


class TimeoutError(Exception):
    pass


class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)


def work():
    print(f"start {os.getpid()}")
    with timeout(2):
        time.sleep(3)
    print(f"done {os.getpid()}")


if __name__ == "__main__":
    procs = []
    for i in range(10):
        cur = multiprocessing.Process(target=work)
        procs.append(cur)
        cur.start()
        time.sleep(0.25)
    
    for proc in procs:
        proc.join()
