# -*- coding: utf-8 -*-
""" 
目标：优化(最大化/最小化)代价/目标函数。
方法：梯度下降
示例：求函数f(x) = x**4 - 3x**3 + 2 在x=6附近的最值
"""

x_old = 0
x_new = 6
step_size = 0.01
precision = 0.00001

# f(x) = x**4 - 3x**3 + 2 的导数
def f_derivative(x):
    return 4 * x**3 - 9* x**2

while abs(x_new - x_old) > precision:
    x_old = x_new
    x_new = x_old - step_size * f_derivative(x_old)

print('Local minimum occurs at: ', x_new)
