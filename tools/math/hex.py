# -*- coding: utf-8 -*-
base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]

print(base)
def dec2hex(num):
    l = []
    if num < 0:
        return '-' + dec2hex(abs(num))
    while True:
        rem = num % 16
        num = num // 16
        l.append(base[rem])
        if num == 0:
            return ''.join(l[::-1])

if __name__ == "__main__":
    print(dec2hex(10))
