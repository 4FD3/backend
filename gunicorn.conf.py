# Gunicorn configuration file
import multiprocessing

max_requests = 1000
max_requests_jitter = 50

# Capture Gunicorn logs to console
#capture_output = True

log_file = "-"

bind = "0.0.0.0:3100"
# Capture Gunicorn logs to console
#capture_output = True
worker_class = "uvicorn.workers.UvicornWorker"
workers = (multiprocessing.cpu_count() * 2) + 1
# Set the log level to "info"
#loglevel = "debug"
