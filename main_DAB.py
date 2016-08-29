
"""
Created on 08/28/2016, @author: sbaek
    - initial release
"""

import sys, time
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
from collections import OrderedDict

from math import *
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import analysis.figure_functions as ff

f = 20000;
T = 1.0/f;
w= 2*pi*f
Vi = 3000;
d = 0.8;
Vop = Vi*d;
L = 0.003;
Ls=L*1000; #[mH]
Vb = Vi;
ps =pi/4;
t_ps=pi/4/(2*pi)*T;
deg=int(ps/2/pi*360)

th=5E-3
Aoc=0.5*th
no=1

Aic=0.0023840506
ni=15

mue = 4*pi*1E-7 *300

roic = 1.47/2*1E-2;
riic = sqrt(e)*roic

F=(mue*ni*log(roic/riic)/(2*pi*(roic-riic)))

def i1(t):
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th + d*th - d * ps))) / (2 * L * w)
    return y

def i2(t):
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th - d*th + d * ps))) / (2 * L * w)
    return y

def Boc(t):
    y=Vop/ni*(t-t_ps-T/4)/Aoc/no
    return y

def main():
    current = []
    B_oc, B_ic = [], []
    t_ps = T * ps / (2 * pi)
    step = 1E-7
    resolution = 4

    ''' current'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        current.append(i1(i))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        current.append(i2(i))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        current.append(-i1(i - T / 2))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        current.append(-i2(i - T / 2))
    t = t1 + t2 + t3 + t4

    ''' Bic'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_ic.append(F * i1(i))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        B_ic.append(F * i2(i))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        B_ic.append(-F * i1(i - T / 2))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        B_ic.append(-F * i2(i - T / 2))
    t = t1 + t2 + t3 + t4

    ''' Boc '''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_oc.append(-Boc(i + T / 2))
    t2 = [i * step for i in range(int(t_ps / step), int((t_ps + T / 2) / step), resolution)]
    for i in t2:
        B_oc.append(Boc(i))
    t3 = [i * step for i in range(int((t_ps + T / 2) / step), int(T / step), resolution)]
    for i in t3:
        B_oc.append(-Boc(i - T / 2))

    data = OrderedDict()
    data.update({'t': t})
    data.update({'i': current})
    data.update({'Boc': B_oc})
    data.update({'Bic': B_ic})
    df = pd.DataFrame(data)
    df.to_csv('data_L%.1f_d%.1f_deg%s.csv' % (Ls, d, deg), index=False)

    ff.plot([[t, current]], title='current')
    ff.plot([[t, B_oc], [t, B_ic]], legend=['Boc', 'Bic'], title='B1')
    ff.plot([[t, B_oc], [t, B_ic]], legend=['Boc', 'Bic'], title='B2', combine=True)
    pass

if __name__ == '__main__':
    main()