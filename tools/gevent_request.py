# -*- encoding: utf-8 -*-
import gevent.pool
import json

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL



url = URL('https://www.baidu.com')

# setting the concurrency to 10 allow to create 10 connections and
# reuse them.
http = HTTPClient.from_url(url, concurrency=10)
print(http.__class__)
response = http.get(url.request_uri)
print(response.status_code)

# response comply to the read protocol. It passes the stream to
# the json parser as it's being read.

def print_friend_username(item):
    friend_url = URL('http://www.baidu.com')
    # the greenlet will block until a connection is available
    response = http.get(friend_url.request_uri)
    print(response.read())
    assert response.status_code == 200

# allow to run 20 greenlet at a time, this is more than concurrency
# of the http client but isn't a problem since the client has its own
# connection pool.
pool = gevent.pool.Pool(10000)
for item in range(1, 10000000):
    pool.spawn(print_friend_username, item)

pool.join()
http.close()
