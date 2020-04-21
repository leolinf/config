# -*- coding: utf-8 -*-

def find(b, targ):
    if targ == 0:
        return True
    if not b:
        return False
    m1 = find(b[1:], targ - b[0])
    m2 = find(b[1:], targ)
    return m1 or m2


while True:
    try:
        a = int(raw_input())
        b = map(int, raw_input().split())
        sumb = sum(b)
        if sumb % 2 == 1:
            print('false')
            continue
        l1 = []
        l2 = []
        b1 = []
        for i in b:
            if i % 5 == 0:
                l1.append(i)
            elif i % 3 == 0:
                l2.append(i)
            else:
                b1.append(i)
        targ1 = sumb/2 - sum(l1)
        print(str(find(b1, targ1)).lower())
    except:
        break
