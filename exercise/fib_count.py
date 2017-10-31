#-*- coding: utf-8 -*-
count = 0

def fib(n):
    global count
    count += 1
    print('[*] n = %d' % n)
    if n == 0:
        return 1;
    elif n == 1:
        return 2;
    else:
        return fib(n-1) + fib(n-2);

if __name__ == "__main__":
    result = fib(8)
    print(" [x] count = %d" % count)
    print(" [r] r = %d" % result)
# count(n) = count(n-2) + count(n-1) + 1
