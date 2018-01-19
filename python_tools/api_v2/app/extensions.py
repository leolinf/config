# -*- coding: utf-8 -*-

import functools

from raven.contrib.flask import Sentry
from flask_cache import Cache
from flask_zipkin import Zipkin

from .core.functions import check_whether_cache_from_response


class CustomCache(Cache):

    def __init__(self, *args, **kwargs):
        super(CustomCache, self).__init__(*args, **kwargs)

    def memoize(self, timeout=None, make_name=None, unless=None):

        def memoize(f):
            @functools.wraps(f)
            def decorated_function(*args, **kwargs):
                if callable(unless) and unless() is True:
                    return f(*args, **kwargs)

                try:
                    cache_key = decorated_function.make_cache_key(f, *args, **kwargs)
                    rv = self.cache.get(cache_key)
                except Exception:
                    raise
                    return f(*args, **kwargs)

                if rv is None:
                    rv = f(*args, **kwargs)
                    # 判断是否需要缓存
                    if check_whether_cache_from_response(rv):
                        try:
                            self.cache.set(cache_key, rv,
                                       timeout=decorated_function.cache_timeout)
                        except Exception:
                            raise
                return rv

            decorated_function.uncached = f
            decorated_function.cache_timeout = timeout
            decorated_function.make_cache_key = self._memoize_make_cache_key(
                                                make_name, decorated_function)
            decorated_function.delete_memoized = lambda: self.delete_memoized(f)

            return decorated_function
        return memoize

sentry = Sentry()
cache = CustomCache()
zipkin = Zipkin()
