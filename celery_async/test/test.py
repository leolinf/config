# -*- coding: utf-8 -*-

from bin.tasks import app, test

# 加入对应的权重值
def execute_add():
    priority = [9, 6, 0, 4, 2, 6, 4, 8, 4, 0]
    for i in range(10):
        print("%s + 10 = %s, and priority is %s" % (i, i+10, priority[i]))
        import time
        time.sleep(5)
        test.add.apply_async(args=(i, 10), priority=priority[i])
        test.add.delay(i, 10)


if __name__ == "__main__":
    execute_add()
