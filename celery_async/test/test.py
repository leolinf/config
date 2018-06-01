# -*- coding: utf-8 -*-

from bin.tasks import app

# 加入对应的权重值
def execute_add():
    print(app)
    print(dir(app))
    app.send_task('rd.group.test.add', args=(1, 10))
    app.send_task('rd.group.test.get_args', args=(1,2,3,4,5,6,7,8,9))


if __name__ == "__main__":
    execute_add()
