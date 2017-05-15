
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
#import data_aq_lib.analysis.figure_functions as ff
import analysis.figure_functions as ff
#import data_aq_lib.analysis.waveform_func as wf
import analysis.waveform_func as wf


current, B_oc, B_ic = [], [], []
step = 1E-7
resolution = 1

fs = 20000.0;
T = 1.0 / fs;


# Outer core #
ni, no = 15, 1;
mue = 4.0 * pi * 1E-7 ;

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
mue_ic = mue * 300*65.4/68.3 #based on effective Ac, mue_r287;
ri_ic = 14.7 / 2 * 1E-3;
ro_ic = 26.9 / 2 * 1E-3;
print ' Di_ic :%.2f, Do_ic : %.2f [mm]' % (ri_ic * 2 * 1E3, ro_ic * 2 * 1E3)
# ro_ic= sqrt(e) * ri_ic
h_ic = 11.2 * 1E-3;
n_ic = 46;
l_ic = h_ic * n_ic;
Ac_ic = (ro_ic - ri_ic) * l_ic;
V_ic = pi * (ro_ic ** 2 - ri_ic ** 2) * l_ic;
print ' length :%.2f [m], Ac_ic : %.2f [cm^2], V_ic : %.2f [cm^2] \n' % (l_oc, Ac_ic * 1E4, V_ic * 1E6)


k_oc = 0.3571;
beta_oc = 2.0694;

k_ic = 1.2681* 1E-5;
beta_ic = 2.106;
alpha_ic = 1.309;

f = fs;
T = 1.0 / fs;
w = 2 * pi * fs

Fi = (mue_ic * ni * log(ro_ic / ri_ic) / (2 * pi * (ro_ic - ri_ic)))


def i1(Vi, t, Ls, d, ps):
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th + d*th - d * ps))) / (2 * Ls * w)
    return y

def i2(Vi, t, Ls, d, ps):
    th = 2 * pi * f * t
    y=(Vi*((-1 + d)*pi + 2*(th - d*th + d * ps))) / (2 * Ls * w)
    return y

def Bi1(Vi, t, F, Ls, d, ps ):
    y=F*i1(Vi, t, Ls, d, ps)
    return y

def Bi2(Vi, t, F, Ls, d, ps):
    y=F*i2(Vi, t, Ls, d, ps)
    return y

def Irms(Vi, Ls, d, ps):
    a=Vi*sqrt((d-1)**2*pi**3+12.0*d*pi*ps**2-8*d*ps**3)
    b=2*w*Ls*sqrt(3*pi)
    y=a/b
    return y


def Boc(Vop, t, t_ps):
    y=Vop/ni*(t-t_ps-T/4)/Ac_oc/no
    return y

def Bic_pk(Vi, Ls, F, d, ps):
    if d>1:
        #y = (Vi / 2 * mue * ni * ((-1 + d) * pi + 2 * ps)) / (4 * w * Ls * pi * ri_ic)
        t_ps=ps/2/pi*T;
        y= F*i1(Vi=Vi, t=t_ps, Ls=Ls, d=d, ps=ps)
    else:
        #y = (Vi/ 2 * mue * ni * ((1 - d) * pi + 2 * d * ps)) / (4 * w * Ls * pi * ri_ic)
        y = F*i2(Vi=Vi, t=T/2, Ls=Ls, d=d, ps=ps)

    return y

def Boc_pk(Vop):
    y = Vop/ni * T / 2.0 / 2.0/ Ac_oc
    return y

def L(mue, n, ri, ro, l):
    y=n**2*mue/2/pi*log(ro/ri)*l
    return y

def P(d, Vi, ps, Ls, fs):
    w = 2 * pi * fs
    y=(d*Vi**2*(pi -ps)*ps)/(w*Ls*pi)
    return y

def Loss_oc(k_oc, B, beta_oc, V_oc):
    y=k_oc*1E6*B**beta_oc*V_oc
    return y

def Loss_ic(k_ic, Bi, alpha_ic, beta_ic, V_ic, fs, ps):
    fs2=fs * pi / ps;
    y= k_ic *1E6 * (Bi) ** beta_ic * (fs2) ** (alpha_ic - 1) * fs * V_ic
    return y

def bound_low(Vi, ps, Ls):
    Pb=Vi**2/(Ls*w)
    y=Pb*(pi-ps)*ps/(pi-2*ps)
    return y

def bound_high(Vi, ps, Ls):
    Pb=Vi**2/(Ls*w)
    y=Pb*((pi-2* ps)*(pi-ps)*ps)/(pi**2)
    return y


def read(filepath, filename):
    file = filepath + filename + '.csv'
    print ' read file %s' % file
    df = pd.read_csv(file)
    #df = convert_1st_key_t(df)  # change the first key(column) to 't' which is compatible with waveform_func.py

    waves = wf.waveforms(filename=filename, filepath=filepath, df=df)
    waves.get_rms()
    waves.get_avg()
    waves.get_pkpk()
    zeros = waves.get_zero_crossing(waves.get_labels()[0])
    freq = waves.get_freq(waves.get_labels()[0], zeros)
    print ' %.1f kHz' % (freq / 1000)

    print waves
    waves.plot_all()


''' Ls calculation '''
Ls = L(mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)#*65.4/68.3 #based on effective Ac
print '\n Ls : %.2f [mH], length :%.2f' %(Ls*1000, l_ic)

''' Loss calculation '''
data_sets=[];
xlimit=(20, 60);
ylimit=(0, 100);
limit, legend = [], []

power, loss_ic, loss_oc, loss_c, Ii = [], [], [], [],[];

d=1.0;
Vi = 3000.0;
Vop = Vi * d;

deg = [i for i in range (5,65,5)]
Vo = [200]


power, loss_ic, loss_oc, loss_c, loss_w, Ii, eff = [], [], [], [], [], [], [];

#Vin=[0.5*3000,1.0*3000]
#k=[100.0/(Vi/15.0), 150.0/(Vi/15.0)]
for j in Vo:
    Vi=j*15.0/d
    Vop=Vi*d
    Rac=0;
    power, loss_ic, loss_oc, loss_c,loss,irms  = [], [], [], [], [], [];
    for i in deg:
        ps = i / 360.0 * 2 * pi;
        Bi_pk = Bic_pk(Vi=Vi, Ls=Ls, F=Fi, d=d, ps=ps)
        Bo_pk = Boc_pk(Vop)
        Po = P(d=d, Vi=Vi, ps=ps, Ls=Ls, fs=fs)
        iLV=ni*Irms(Vi=Vi, Ls=Ls, d=d, ps=ps)
        P_loss_oc = Loss_oc(k_oc=k_oc, beta_oc=beta_oc, B=Bo_pk, V_oc=V_oc)
        P_loss_ic = Loss_ic(k_ic=k_ic, Bi=Bi_pk, alpha_ic=alpha_ic, beta_ic=beta_ic, V_ic=V_ic, fs=fs, ps=ps)
        P_loss_c = P_loss_ic + P_loss_oc
        P_loss_w=Rac*iLV**2;
        P_loss=P_loss_c+P_loss_w;
        Eff=(Po-P_loss)/Po*100.0;

        eff.append(Eff);
        power.append(Po);
        loss_c.append(P_loss_c);
        loss_ic.append(P_loss_ic);
        loss_oc.append(P_loss_oc);
        loss_w.append(P_loss_w);
        irms.append(iLV);
        loss.append(P_loss);
        limit.append([xlimit, ylimit]);

        print '\n Po : %.2f [kW], Irms_LV=%.1f at d=% .1f, Vi=% .1f, Vo=% .1f, deg :%.1f ' % (Po/1000, iLV, d, Vi, j, i)
        print '\n Bi_pk : %.2f, Bo_pk : %.2f [T]' % (Bi_pk, Bo_pk)
        print '\n P_loss_oc: %.1f, P_loss_ic: %.1f,  loss_c :: %.1f' % (P_loss_oc, P_loss_ic, P_loss_c)
    #legend.append('al Vo=%.1f' % (Vi/15.0*d))
    legend.append('')

df=pd.DataFrame({'deg':deg,
                 'loss':loss, 'loss_w':loss_w,
                 'loss_c':loss_c, 'loss_oc':loss_oc, 'loss_ic':loss_ic,
                 'power': power, 'eff': eff, 'irms_LV':irms})
df.to_csv('data.csv')

ff.plot([
    [df['deg'], df['loss_c']],
    [df['deg'], df['loss_ic']],
    [df['deg'], df['loss_oc']],
    [df['deg'], df['loss_w']]
    ], filename='loss', title='loss', combine=True,  legend=legend, figsize=(8, 5))

ff.plot([
    [df['deg'], df['loss_c']/df['power']],
    [df['deg'], df['loss_ic']/df['power']],
    [df['deg'], df['loss_oc']/df['power']],
    [df['deg'], df['loss_w']/df['power']],
    [df['deg'], df['power']/ 10000.0]
    ], filename='loss_ratio', title='loss_ratio', combine=True,  legend=legend, figsize=(8, 5))


ff.plot([
    [df['deg'], df['power']]
    ] , filename='Po1', title='Po1', combine=True,  legend=legend, figsize=(8, 5))
ff.plot([[df['deg'], df['eff']]], title='Eff', combine=True,  legend=legend, figsize=(8, 5))





