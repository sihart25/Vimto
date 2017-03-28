from __future__ import absolute_import

import logging
import time
import sys
import datetime
# from celery import  Celery
from celery.utils.log import get_task_logger
from celery import shared_task
from celery import task
from celery import current_task
from celery.result import AsyncResult
from celeryproj.celerymain import worker_app
from polls.models import Model_MyCelModel

NUM_OBJ_TO_CREATE = 1000
# Get an instance of a logger
logger = logging.getLogger(__name__)


@worker_app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y


@worker_app.task
def mul(x, y):
    logger.info('Mul {0} + {1}'.format(x, y))
    return x * y


@worker_app.task
def xsum(numbers):
    logger.info('xsum :'+numbers)
    return sum(numbers)


# when this task is called, it will create 1000 objects in the database
@worker_app.task
def create_models():
    for i in range(1, NUM_OBJ_TO_CREATE+1):
        fn = 'Fn %s' % i
        ln = 'Ln %s' % i
        my_model = Model_MyCelModel(fn=fn, ln=ln)
        my_model.save()

    process_percent = int(100 * float(i) / float(NUM_OBJ_TO_CREATE))
    logger.info('process_percent:' + str(process_percent))
    time.sleep(0.1)
    current_task.update_state(state='PROGRESS', meta={'process_percent': process_percent})

# when this task is called, it will create 1000 objects in the database
@worker_app.task()
def create_Sections():
    for i in range(1, NUM_OBJ_TO_CREATE+1):
        fn = 'Fn %s' % i
        ln = 'Ln %s' % i
        my_model = Model_MyCelModel(fn=fn, ln=ln)
        my_model.save()

    process_percent = int(100 * float(i) / float(NUM_OBJ_TO_CREATE))
    logger.info('process_percent:' + str(process_percent))
    time.sleep(0.1)
    current_task.update_state(state='PROGRESS', meta={'process_percent': process_percent})



@worker_app.task
def longtime_add(x, y):
    logger.info('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    logger.info('long time task finished')
    return x + y


@worker_app.task
def test_rabbit_running():
    utcnow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info('CELERY RUNNING'+utcnow)
    return utcnow


@worker_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
