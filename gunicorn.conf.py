import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
accesslog = "gunicorn_access_log.txt"
errorlog =  "gunicorn_error_log.txt"
# turn this of in production
reload = True

# TODO: specify workers type
