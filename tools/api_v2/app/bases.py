# -*- coding: utf-8 -*-

from flask.views import MethodView


class BaseView(MethodView):

    def dispatch_request(self, *args, **kwargs):

        # TODO 处理返回字段和处理测试条数
        return super(BaseView, self).dispatch_request(*args, **kwargs)
