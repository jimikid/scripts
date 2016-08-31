
"""
Created on 08/28/2016, @author: sbaek
    - initial release
"""

import sys, time, os
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
from collections import OrderedDict

from math import *
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import analysis.figure_functions as ff


def i1(t, Vi, fs, Ls, d, ps):
    f = fs;
    T = 1.0 / fs;
    w = 2 * pi * fs
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th + d*th - d * ps))) / (2 * Ls * w)
    return y

def i2(t, Vi, fs, Ls, d, ps):
    f = fs;
    T = 1.0 / fs;
    w = 2 * pi * fs
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th - d*th + d * ps))) / (2 * Ls * w)
    return y

def L(mue, n, ri, ro, h):
    print ' Di: %.1f [mm]' %(2*ri*1000)
    print ' Do: %.1f [mm]' %(2*ro*1000)
    print ' h: %.1f [mm]' % (h * 1000)
    y=n**2*mue/2/pi*log(ro/ri)*h
    return y

def Boc(t, fs, Vop, ni,no, Aoc, t_ps):
    f = fs;
    T = 1.0 / fs;
    w = 2 * pi * fs
    y=Vop/ni*(t-t_ps-T/4)/Aoc/no
    return y

def main():
    current, B_oc, B_ic = [], [], []
    step = 1E-7
    resolution = 4

    fs = 20000;
    T = 1.0 / fs;
    ps = pi / 4;

    t_ps = T * ps / (2 * pi)
    Vi = 3000;
    d = 0.8;
    Vop = Vi * d;
    Vb = Vi;

    t_ps = pi / 4 / (2 * pi) * T;
    deg = int(ps / 2 / pi * 360)

    th = 5E-3
    Aoc = 0.5 * th
    no = 1

    Aic = 0.0023840506;
    ni, no = 15, 1
    mue = 4 * pi * 1E-7 * 300;
    riic = 14.7 / 2 * 1E-3;
    #roic= sqrt(e) * riic
    roic=26.9/2 *1E-3;
    h=11.2*1E-3*46;

    F = (mue * ni * log(roic / riic) / (2 * pi * (riic - roic)))

    ''' Ls calculation '''
    Ls = L(mue, n=ni, ri=riic, ro=roic, h=h)
    print 'Ls : %.2f [mH]' %(Ls*1000)

    ''' current'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        current.append(i1(t=i, Vi=Vi, fs=fs, Ls=Ls, d=d, ps=ps))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        current.append(i2(t=i, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        current.append(-i1(t=i - T / 2, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        current.append(-i2(t=i - T / 2, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t = t1 + t2 + t3 + t4

    ''' Bic'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_ic.append(F * i1(t=i, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        B_ic.append(F * i2(t=i, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        B_ic.append(-F*i1(t=i - T / 2, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        B_ic.append(-F*i2(t=i - T / 2, Vi=Vi,  fs=fs, Ls=Ls, d=d, ps=ps))
    t = t1 + t2 + t3 + t4

    ''' Boc '''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_oc.append(-Boc(t=i + T/2, fs=fs, Vop=Vop, ni=ni, no=no, Aoc=Aoc, t_ps=t_ps))
    t2 = [i * step for i in range(int(t_ps / step), int((t_ps + T / 2) / step), resolution)]
    for i in t2:
        B_oc.append(Boc(t=i, fs=fs, Vop=Vop, ni=ni, no=no, Aoc=Aoc, t_ps=t_ps))
    t3 = [i * step for i in range(int((t_ps + T / 2) / step), int(T / step), resolution)]
    for i in t3:
        B_oc.append(-Boc(t=i - T/2, fs=fs, Vop=Vop, ni=ni, no=no, Aoc=Aoc, t_ps=t_ps))

    data = OrderedDict()
    data.update({'t': t})
    data.update({'i_%s_%s'%(deg, d): current})
    data.update({'Boc_%s_%s'%(deg, d): B_oc})
    data.update({'Bic_%s_%s'%(deg, d): B_ic})
    df = pd.DataFrame(data)
    df.to_csv('data_L%.1f_d%.1f_deg%s.csv' % (Ls, d, deg), index=False)

    ff.plot([[t, current]], title='current')
    ff.plot([[t, B_oc], [t, B_ic]], legend=['Boc', 'Bic'], title='B1')
    ff.plot([[t, B_oc], [t, B_ic]], legend=['Boc', 'Bic'], title='B2', combine=True)
    pass

if __name__ == '__main__':
    main()



