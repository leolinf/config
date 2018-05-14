#!/usr/bin/env python
# coding=utf-8

import sys
import json
import threading
import requests
from pyquery import PyQuery as pq
from Queue import Queue

mutex = threading.Lock()
queue = Queue()

import time
import hashlib
import urllib

uri = 'http://www.test.com'


def gen_sign(secret, data):

    now = str(time.time())

    data.update({'t': now, 'app_key': '9438780765'})

    l = []
    for k in data:
        if k == 'sign':
            continue
        l.append(k + urllib.quote(data[k].encode('utf-8')))

    s = secret + ''.join(sorted(l)) + secret
    return hashlib.md5(s).hexdigest()


def querystring(data):

    secret = 'zmhyvz86tu75n0o0i14f868tuz8p29lc'
    sign = gen_sign(secret, data)
    for k in data:
        data[k] = data[k].encode('utf-8')
    data.update({'sign': sign})
    return urllib.urlencode(data)


def get_new_phone_oper(phone):

    url = '%s/operator/Multiplatform/?%s'%(uri, querystring({"phone": phone}))
    response = requests.get(url, timeout=20).json()
    response.update({"phone": phone})
    return json.dumps(response, ensure_ascii=False).encode("utf-8")


class ThreadCrawl(threading.Thread):

    def __init__(self, queue):
        super(ThreadCrawl, self).__init__()
        self.queue = queue

    def run(self):
        while 1:
            if self.queue.qsize() == 0:
                break
            try:
                phone = self.queue.get_nowait()
            except Exception as e:
                pass
            try:
                data = get_new_phone_oper(phone)
                print(data)
            except Exception as e:
                print(e)
                f = open('error.json', 'a+')
                f.write(phone)
                f.write('\n')
                f.close()


def start():
    with open(sys.argv[2],'r') as f:
        for line in f:
            data = int(line.strip()) + 1
            queue.put(str(data))
    main()


def main():
    Thread_num = sys.argv[1]
    threads = []

    for thread_num in range(int(Thread_num)):
        thread_again = ThreadCrawl(queue)
        threads.append(thread_again)
        thread_again.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    start()
