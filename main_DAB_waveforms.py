import matplotlib.pyplot as plt
import pandas as pd
from math import *

import sys, time, os
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
import analysis.Cvt_Mdls as cm
import analysis.CWT as cwt


current, B_oc, B_ic = [], [], []
step = 1E-7
resolution = 1

fs = 20000.0;
T = 1.0 / fs;


# Outer core #
ni, no = 15, 1;
mue = 4.0 * pi * 1E-7;

print '\n Outer cores specs'
ri_oc, ro_oc = 36.0 / 2 * 1E-3, 55.0 / 2 * 1E-3;

stack=0.8;
print ' Di_oc :%.2f, Do_oc : %.2f [mm]' % (ri_oc * 2 * 1E3, ro_oc * 2 * 1E3)
# ro_oc= sqrt(e) * riic
h_oc = 25.0 * 1E-3;
n_oc = 20;
l_oc = h_oc * n_oc;
Ac_oc = stack*(ro_oc - ri_oc) * l_oc
V_oc = pi * (ro_oc ** 2 - ri_oc ** 2) * l_oc;
print ' length :%.2f [m], Ac_oc : %.2f [cm^2], V_oc : %.2f [cm^2]' % (l_oc, Ac_oc * 1E4, V_oc * 1E6)

# Inner core #
print '\n Inner cores specs'
mue_ic = mue * 300;
ri_ic, ro_ic = 14.7 / 2 * 1E-3, 26.9 / 2 * 1E-3;
print ' Di_ic :%.2f, Do_ic : %.2f [mm]' % (ri_ic * 2 * 1E3, ro_ic * 2 * 1E3)
# ro_ic= sqrt(e) * ri_ic
h_ic = 11.2 * 1E-3;
n_ic = 46;
l_ic = h_ic * n_ic;
Ac_ic = (ro_ic - ri_ic) * l_ic;
Ac_ic = 65.4*1E-6*n_ic;
V_ic = pi * (ro_ic ** 2 - ri_ic ** 2) * l_ic;
print ' length :%.2f [m], Ac_ic : %.2f [cm^2], V_ic : %.2f [cm^2] \n' % (l_ic, Ac_ic * 1E4, V_ic * 1E6)

f = fs;
T = 1.0 / fs;
w = 2 * pi * fs

d = 1.0;
deg = 45.0;
time_shift = T / 4.0;
ps = deg / 360.0 * 2.0 * pi;
shift = int(time_shift / step);

t_ps = T * ps / (2 * pi)
Vi = 3000.0;
Vop = Vi * d;
Vb = Vi;

t_ps = ps / (2 * pi) * T;


''' Ls calculation '''
cwt1=cwt.CWT(fs, ni, no, ri_oc, ro_oc, h_oc, n_oc, mue_ic, ri_ic, ro_ic, h_ic, n_ic)
Ls = cwt1.L(mue=mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)
print '\n Ls : %.2f [mH]' % (Ls * 1000)

dab1=cm.DAB(fs, Vi, Ls, d, ps)

''' rms '''
print '\n Irms : %.1f [Arms]' % (dab1.Irms)

''' B peaks '''
Bic_pk = cwt1.Bic_pk(Vi, Ls, d, ps)
Boc_pk = cwt1.Boc_pk(Vop, Ac_oc)

Bic_t=cwt1.Bic(dab1.current)
Boc_t=cwt1.Boc(t_ps, Vop=d*Vi)

print '\n Calculation : Bi_pkpk : %.2f, Bo_pkpk : %.2f [T]' % (Bic_pk * 2, Boc_pk * 2)
print '\n Bo_max: %.2f, Bo_min: %.2f' % (max(Boc_t), min(Boc_t))
print ' Bi_max: %.2f, Bi_min: %.2f' % (max(Bic_t), min(Bic_t))
print '\n i_max: %.2f, i_min: %.2f' % (max(dab1.current), min(dab1.current))

plt.plot(dab1.t, Bic_t)
plt.plot(dab1.t, Boc_t)
plt.show()

''' Power calculation '''
print '\n Po : %.2f [kW] at %.1f deg, d:%.2f' % (dab1.Po * 1E-3, dab1.deg, dab1.d)

''' Loss coefficents '''
k_oc, beta_oc = 0.3571, 2.0694;
k_ic, beta_ic, alpha_ic = 1.2681 * 1E-5,  2.106, 1.309;


P_loss_oc = cwt1.Loss_oc(k_oc=k_oc, beta_oc=beta_oc, Bpk=Boc_pk)
print '\n P_loss_oc : %.1f [W] at %.2f [T]' % (P_loss_oc, Boc_pk)
P_loss_ic = cwt1.Loss_ic(k_ic=k_ic, Bpk=Bic_pk, alpha_ic=alpha_ic, beta_ic=beta_ic, ps=ps)
print '\n P_loss_ic : %.1f [W] at %.2f [T]' % (P_loss_ic, Bic_pk)



