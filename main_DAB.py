
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

current, B_oc, B_oc_avg, B_ic = [], [], [], []
step = 1E-7
resolution = 2

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
ri_oc = 36.0 / 2 * 1E-3;
ro_oc = 55.0 / 2 * 1E-3;
print ' Di_oc :%.2f, Do_oc : %.2f [mm]' % (ri_oc * 2 * 1E3, ro_oc * 2 * 1E3)
# ro_oc= sqrt(e) * riic
h_oc = 25.0 * 1E-3;
n_oc = 20;
l_oc = h_oc * n_oc;
Ac_oc = (ro_oc - ri_oc) * l_oc
V_oc = pi * (ro_oc ** 2 - ri_oc ** 2) * l_oc;
print ' length :%.2f [m], Ac_oc : %.2f [cm^2], V_oc : %.2f [cm^2]' % (l_oc, Ac_oc * 1E4, V_oc * 1E6)

# Inner core #
print '\n Inner cores specs'
mue_ic = mue * 300;
ri_ic = 14.7 / 2 * 1E-3;
ro_ic = 26.9 / 2 * 1E-3;
print ' Di_ic :%.2f, Do_ic : %.2f [mm]' % (ri_ic * 2 * 1E3, ro_ic * 2 * 1E3)
# ro_ic= sqrt(e) * ri_ic
h_ic = 11.2 * 1E-3;
n_ic = 46;
l_ic = h_oc * n_oc;
Ac_ic = (ro_ic - ri_ic) * l_ic;
V_ic = pi * (ro_ic ** 2 - ri_ic ** 2) * l_ic;
print ' length :%.2f [m], Ac_ic : %.2f [cm^2], V_ic : %.2f [cm^2] \n' % (l_oc, Ac_ic * 1E4, V_ic * 1E6)


k_oc = 0.3571;
beta_oc = 2.0694;

f = fs;
T = 1.0 / fs;
w = 2 * pi * fs

Fi = (mue_ic * ni * log(ro_ic / ri_ic) / (2 * pi * (ro_ic - ri_ic)))




def i1(t, Ls):
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th + d*th - d * ps))) / (2 * Ls * w)
    return y

def i2(t, Ls):
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th - d*th + d * ps))) / (2 * Ls * w)
    return y

def Bi1(t, F, Ls):
    y=F*i1(t, Ls)
    return y

def Bi2(t, F, Ls):
    y=F*i2(t, Ls)
    return y

def Boc_avg(t):
    y=Vop/ni*(t-t_ps-T/4)/Ac_oc/no
    return y

def Bic_pk(Ls, F, t_ps):
    if d>1:
        #y = (Vi / 2 * mue * ni * ((-1 + d) * pi + 2 * ps)) / (4 * w * Ls * pi * ri_ic)
        y= F*i1(t_ps, Ls)
    else:
        #y = (Vi/ 2 * mue * ni * ((1 - d) * pi + 2 * d * ps)) / (4 * w * Ls * pi * ri_ic)
        y = F*i2(T/2, Ls)

    return y

def Boc_pk():
    y = Vi * T / 2 / 2/ ( ni * Ac_oc)
    return y

def L(mue, n, ri, ro, l):
    y=n**2*mue/2/pi*log(ro/ri)*l
    return y

def P(d, Vi, ps, Ls, fs):
    w = 2 * pi * fs
    y=(d*Vi**2*(pi -ps)*ps)/(w*Ls*pi)
    return y

def Loss_oc(k_oc, B, beta_oc, V_oc):
    y=k_oc*B**beta_oc*V_oc
    return y

def main():
    ''' Ls calculation '''
    Ls = L(mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)
    print '\n Ls : %.2f [mH]' %(Ls*1000)

    ''' B peaks '''
    Bi_pk=Bic_pk(Ls=Ls, F=Fi, t_ps=t_ps)
    Bo_pk=Boc_pk()
    print '\n Calculation : Bi_pkpk : %.2f, Bo_pkpk : %.2f [T]' % (Bi_pk*2, Bo_pk*2)


    ''' current'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        current.append(i1(t=i, Ls=Ls))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        current.append(i2(t=i, Ls=Ls))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        current.append(-i1(t=i - T / 2, Ls=Ls))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        current.append(-i2(t=i - T / 2, Ls=Ls))
    t = t1 + t2 + t3 + t4

    ''' Bic'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_ic.append(Bi1(t=i, F=Fi, Ls=Ls))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        B_ic.append(Bi2(t=i, F=Fi, Ls=Ls))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        B_ic.append(-Bi1(t=i - T / 2, F=Fi, Ls=Ls))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        B_ic.append(-Bi2(t=i - T / 2, F=Fi, Ls=Ls))
    t = t1 + t2 + t3 + t4

    ''' Boc '''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_oc_avg.append(-Boc_avg(t=i + T/2))
    t2 = [i * step for i in range(int(t_ps / step), int((t_ps + T / 2) / step), resolution)]
    for i in t2:
        B_oc_avg.append(Boc_avg(t=i))
    t3 = [i * step for i in range(int((t_ps + T / 2) / step), int(T / step), resolution)]
    for i in t3:
        B_oc_avg.append(-Boc_avg(t=i - T/2))

    print '\n Bo_avg_max: %.2f, Bo_avg_min: %.2f' %(max(B_oc_avg), min(B_oc_avg))
    print ' Bi_max: %.2f, Bi_min: %.2f' % (max(B_ic), min(B_ic))
    print '\n i_max: %.2f, i_min: %.2f' % (max(current), min(current))


    ''' Power calculation '''
    Po = P(d=d, Vi=Vi, ps=ps, Ls=Ls, fs=fs)
    print '\n Po : %.2f [kW] at %.1f deg, d:%.2f' % (Po *1E-3, deg, d)

    ''' Loss calculation '''
    P_loss_oc=Loss_oc(k_oc=k_oc, beta_oc=beta_oc, B=Bo_pk, V_oc=V_oc)
    print '\n P_loss_oc : %.1f [W]' % (P_loss_oc)


    data = OrderedDict()
    data.update({'t': t})
    data.update({'i_%s_%s'%(deg, d): current})
    data.update({'Boc_avg_%s_%s'%(deg, d): B_oc_avg})
    data.update({'Bic_%s_%s'%(deg, d): B_ic})
    df = pd.DataFrame(data)
    df.to_csv('data_L%.1f_d%.1f_deg%s.csv' % (Ls, d, deg), index=False)

    ff.plot([[t, current]], title='current')
    ff.plot([[t, B_oc_avg], [t, B_ic]], legend=['Boc', 'Bic'], title='B1')
    ff.plot([[t, B_oc_avg], [t, B_ic]], legend=['Boc', 'Bic'], title='B2', combine=True)
    pass

if __name__ == '__main__':
    main()



