
"""
Created on 08/28/2016, @author: sbaek
    - initial release
"""

import sys, time, os
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))

import analysis.figure_functions as ff
import analysis.waveform_func as wf
import pandas as pd
from math import *

import sys, time, os
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
from collections import OrderedDict
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
ri_oc = 36.0 / 2 * 1E-3;
ro_oc = 55.0 / 2 * 1E-3;

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
ri_ic = 14.7 / 2 * 1E-3;
ro_ic = 26.9 / 2 * 1E-3;
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

''' Loss coefficents '''
k_oc, beta_oc = 0.3571, 2.0694;
k_ic, beta_ic, alpha_ic = 1.2681 * 1E-5,  2.106, 1.309;

power, loss_ic, loss_oc, loss_c, Ii = [], [], [], [],[];

d=1.0;
Vi = 3000.0;
Vop = Vi * d;

deg = [i for i in range (5,65,5)]
deg = [i for i in range (3,63,3)]
Vo = [200]

cwt1 = cwt.CWT(fs, ni, no, ri_oc, ro_oc, h_oc, n_oc, mue_ic, ri_ic, ro_ic, h_ic, n_ic)
Ls = cwt1.L(mue=mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)
print '\n Ls : %.2f [mH]' % (Ls * 1000)


power, loss_ic, loss_oc, loss_c, loss_w, Ii, eff = [], [], [], [], [], [], [];
for j in Vo:
    Vi=j*15.0/d
    Vop=Vi*d
    Rac=0;


    power, loss_ic, loss_oc, loss_c,loss,irms  = [], [], [], [], [], [];
    for i in deg:
        ps = i / 360.0 * 2 * pi;
        ''' B peaks '''
        Bic_pk = cwt1.Bic_pk(Vi, Ls, d, ps)
        Boc_pk = cwt1.Boc_pk(Vop, Ac_oc)

        dab1 = cm.DAB(fs, Vi, Ls, d, ps)

        iLV=ni*dab1.Irms
        P_loss_oc = cwt1.Loss_oc(k_oc=k_oc, beta_oc=beta_oc, Bpk=Boc_pk)
        P_loss_ic = cwt1.Loss_ic(k_ic=k_ic, Bpk=Bic_pk, alpha_ic=alpha_ic, beta_ic=beta_ic, ps=ps)

        P_loss_c = P_loss_ic + P_loss_oc
        P_loss_w=Rac*iLV**2;
        P_loss=P_loss_c+P_loss_w;
        Eff=(dab1.Po-P_loss)/dab1.Po*100.0;

        eff.append(Eff);
        power.append(dab1.Po);
        loss_c.append(P_loss_c);
        loss_ic.append(P_loss_ic);
        loss_oc.append(P_loss_oc);
        loss_w.append(P_loss_w);
        irms.append(iLV);
        loss.append(P_loss);

        print '\n Po : %.2f [kW], Irms_LV=%.1f at d=% .1f, Vi=% .1f, Vo=% .1f, deg :%.1f ' % (dab1.Po/1000, iLV, d, Vi, j, i)
        print '\n Bic_pk : %.2f, Boc_pk : %.2f [T]' % (Bic_pk, Boc_pk)
        print '\n P_loss_oc: %.1f, P_loss_ic: %.1f,  loss_c :: %.1f' % (P_loss_oc, P_loss_ic, P_loss_c)

df=pd.DataFrame({'deg':deg,
                 'loss':loss, 'loss_w':loss_w,
                 'loss_c':loss_c, 'loss_oc':loss_oc, 'loss_ic':loss_ic,
                 'power': power, 'eff': eff, 'irms_LV':irms})
df.to_csv('data.csv')

ff.plot([
    [df['deg'], df['loss_c']],
    [df['deg'], df['loss_ic']], [df['deg'], df['loss_oc']],
    [df['deg'], df['loss_w']]
    ], filename='loss', title='loss', combine=True, figsize=(8, 5))

ff.plot([
    [df['deg'], df['loss_c']/df['power']],
    [df['deg'], df['loss_ic']/df['power']], [df['deg'], df['loss_oc']/df['power']],
    [df['deg'], df['loss_w']/df['power']],
    [df['deg'], df['power']/ 10000.0]
    ], filename='loss_ratio', title='loss_ratio', combine=True,  figsize=(8, 5))

ff.plot([
    [df['deg'], df['power']]
    ] , filename='Po1', title='Po1', combine=True, figsize=(8, 5))
ff.plot([[df['deg'], df['eff']]], title='Eff', combine=True, figsize=(8, 5))





