
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

def Boc(t, fs, Vop, ni,no, Acoc, t_ps):
    f = fs;
    T = 1.0 / fs;
    w = 2 * pi * fs
    y=Vop/ni*(t-t_ps-T/4)/Acoc/no
    return y

def Bic_pk(Vi, mue, d, Ls,  ri_ic, ni, ps, fs):
    f = fs;
    T = 1.0 / fs;
    w = 2 * pi * fs
    if d>1:
        y = (Vi / 2 * mue * ni * ((-1 + d) * pi + 2 * ps)) / (4 * w * Ls * pi * ri_ic)
    else:
        y = (Vi/ 2 * mue * ni * ((1 - d) * pi + 2 * d * ps)) / (4 * w * Ls * pi * ri_ic)
    return y


def Boc_pk(Vi, fs, no, Ac_oc):
    f = fs;
    T = 1.0 / fs;
    w = 2 * pi * fs
    y = Vi / 2  / (4 * fs * no * Ac_oc)
    return y

def L(mue, n, ri, ro, l):
    y=n**2*mue/2/pi*log(ro/ri)*l
    return y

def P(d, Vi, ps, Ls, fs):
    w = 2 * pi * fs
    y=(d*Vi**2*(pi -ps)*ps)/(w*Ls*pi)
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

    # Outer core #
    ni, no = 15, 1;
    mue = 4 * pi * 1E-7;

    print '\n Outer cores specs'
    ri_oc=36.0/2*1E-3;
    ro_oc=55.0/2*1E-3;
    print ' Di_oc :%.2f, Do_oc : %.2f [mm]' %(ri_oc*2*1E3, ro_oc*2*1E3)
    # ro_oc= sqrt(e) * riic
    h_oc = 25.0 * 1E-3;
    n_oc=20;
    l_oc=h_oc* n_oc;
    Ac_oc=(ro_oc-ri_oc)*l_oc
    print ' length :%.2f [m], Ac_oc : %.2f [cm^2]' %(l_oc, Ac_oc * 1E4)

    # Inner core #
    print '\n Inner cores specs'
    mue_ic = mue * 300;
    ri_ic = 14.7 / 2 * 1E-3;
    ro_ic = 26.9 / 2 * 1E-3;
    print ' Di_ic :%.2f, Do_ic : %.2f [mm]' %(ri_ic * 2 * 1E3, ro_ic * 2 * 1E3)
    # ro_ic= sqrt(e) * ri_ic
    h_ic = 11.2 * 1E-3;
    n_ic = 46;
    l_ic = h_oc * n_oc;
    Ac_ic = (ro_ic - ri_ic) * l_ic
    print ' length :%.2f [m], Ac_ic : %.2f [cm^2] \n' %(l_oc, Ac_ic * 1E4)

    F = (mue_ic * ni * log(ro_ic / ri_ic) / (2 * pi * (ri_ic - ro_ic)))

    ''' Ls calculation '''
    Ls = L(mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)
    print '\n Ls : %.2f [mH]' %(Ls*1000)

    ''' B peaks '''
    Bi_pkpk=Bic_pk(Vi=Vi, mue=mue_ic, d=d, Ls=Ls, ri_ic=ri_ic, ni=ni, ps=ps, fs=fs)
    Bo_pkpk=Boc_pk(Vi=Vi, fs=fs, no=no, Ac_oc=Ac_oc)
    print '\n Bi_pkpk : %.2f, Bo_pkpk : %.2f [T]' % (Bi_pkpk, Bo_pkpk)


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
        B_oc.append(-Boc(t=i + T/2, fs=fs, Vop=Vop, ni=ni, no=no, Acoc=Ac_oc, t_ps=t_ps))
    t2 = [i * step for i in range(int(t_ps / step), int((t_ps + T / 2) / step), resolution)]
    for i in t2:
        B_oc.append(Boc(t=i, fs=fs, Vop=Vop, ni=ni, no=no, Acoc=Ac_oc, t_ps=t_ps))
    t3 = [i * step for i in range(int((t_ps + T / 2) / step), int(T / step), resolution)]
    for i in t3:
        B_oc.append(-Boc(t=i - T/2, fs=fs, Vop=Vop, ni=ni, no=no, Acoc=Ac_oc, t_ps=t_ps))

    print '\n Bo_max: %.2f, Bo_min: %.2f' %(max(B_oc), min(B_oc))
    print ' Bi_max: %.2f, Bi_min: %.2f' % (max(B_ic), min(B_ic))
    print '\n i_max: %.2f, i_min: %.2f' % (max(current), min(current))

    ''' Power calculation '''
    Po = P(d=d, Vi=Vi, ps=ps, Ls=Ls, fs=fs)
    print '\n Po : %.2f [kW] at %.1f deg, d:%.2f' % (Po *1E-3, deg, d)

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



