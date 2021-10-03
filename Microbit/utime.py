import time

def ticks_ms():
    return int(time.time() * 1000)

def ticks_us():
    return int(time.time() * 1e6)

def ticks_diff(time1, time2):
    return time1 - time2
