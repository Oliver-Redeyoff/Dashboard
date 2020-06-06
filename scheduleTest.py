import sched, time
s = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    print("From print_time", time.time(), a)

s.enter(20, 1, print_time, kwargs={'a': 'keyword'})
s.run()

