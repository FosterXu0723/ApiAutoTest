import time

# time_path = 'runtime.txt'


def save_time(time_path):
    times = time.strftime(' %Y-%m-%d %H点%M分%S秒'.encode('unicode_escape').decode('utf8'),
                                  time.localtime(time.time())).encode('utf-8').decode(
        'unicode_escape')

    with open(time_path, 'w') as f:
        f.write(times)
        f.close()


def get_time(time_path):
    with open(time_path, 'r') as f:
        times: str = f.read()
        f.close()
    return times
