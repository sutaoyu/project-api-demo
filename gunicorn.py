import multiprocessing
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, ".logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

name = "NPC_Backend"

accesslog = ".logs/gunicorn-access.log"
errorlog = ".logs/gunicorn-error.log"

bind = "0.0.0.0:8106"

worker_class = "uvicorn.workers.UvicornH11Worker"
workers = multiprocessing.cpu_count() * 2 + 1
