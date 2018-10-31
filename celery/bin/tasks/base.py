# -*- coding: utf-8 -*-

import logging
from celery import Task

log = logging.getLogger()


class BaseTask(Task):

    #def on_success(self, retval, task_id, args, kwargs):
    #    clogger.info('task done. task_id: {0}, retval: {1}, args: {2}, kwargs: {3}'.format(
    #            task_id, retval, args, kwargs))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        '''什么时候会认为任务失败？1.异常抛到celery层 2.task retry已到达最大值'''
        log.warn('task fail! task_id: %s, args: %s, kwargs: %s, einfo: %s' % (task_id, args, kwargs, einfo))
        return super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)
