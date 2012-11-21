import multiprocessing

bind = "127.0.0.1:24892"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
