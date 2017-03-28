from __future__ import absolute_import, unicode_literals
import os
import sys
from celery import Celery
# set the default Django settings module for the 'celery' program.
# Relative path to the Django main project folder

# include Upper Folders for Vimto package
sys.path.append("../../")
sys.path.append("/var/www/workspace/Vimto/vimto/local_apps/")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vimto.settings')


worker_app = Celery(
    'celerymain'
)



# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
worker_app.config_from_object('django.conf:settings')



if __name__ == '__main__':
    worker_app.start()
