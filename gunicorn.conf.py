bind = "unix:/tmp/nginx.socket"
preload_app = True
worker_class = "gunicorn.workers.gthread.ThreadWorker"


def pre_fork(server, worker):
    with open('/tmp/app-initialized', 'a'):
        pass
