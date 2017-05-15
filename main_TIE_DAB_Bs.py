
"""
Created on 08/28/2016, @author: sbaek
    - initial release
    - scripted for TIE 
    - generate Po.csv, Bic_pk.csv, Boc_pk.csv'
    - contour plot deg vs Bic, Boc, Po
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import *

import sys, time, os
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
from collections import OrderedDict
import analysis.Cvt_Mdls as cm
import analysis.CWT as cwt
import analysis.figure_functions as ff

fs = 20000.0;

# Outer core #
ni, no = 15, 1;
mue = 4.0 * pi * 1E-7;

print '\n Outer cores specs'
ri_oc, ro_oc = 36.0 / 2 * 1E-3, 55.0 / 2 * 1E-3;

stack=0.85;
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
Vi = 3000.0;
Vb = Vi;

k_oc, beta_oc = 0.3571, 2.0694;
k_ic, beta_ic, alpha_ic = 1.2681 * 1E-5,  2.106, 1.309;

''' Ls calculation '''
cwt1=cwt.CWT(fs, ni, no, ri_oc, ro_oc, h_oc, n_oc, mue_ic, ri_ic, ro_ic, h_ic, n_ic)
Ls = cwt1.L(mue=mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)
print '\n Ls : %.2f [mH]' % (Ls * 1000)

dab=[]

def cal(fs, Vi, Ls, d, ps):
    dab1=cm.DAB(fs, Vi, Ls, d, ps)
    dab.append(dab1)

    ''' Po, Irms '''
    #print '\n Irms : %.1f [Arms]' % (dab1.Irms)
    #print '\n Po : %.2f [kW] at %.1f deg, d:%.2f' % (Po * 1E-3, dab1.deg, dab1.d)

    ''' B peaks 
    B max, min values by fomula
    '''
    Bic_pk = cwt1.Bic_pk(Vi, Ls, d, ps)
    Boc_pk = cwt1.Boc_pk( Vop= Vi * d, Ac_oc=Ac_oc)
    #print '\n Calculation : Bi_pkpk : %.2f, Bo_pkpk : %.2f [T]' % (Bic_pk * 2, Boc_pk * 2)

    '''
    check the max, min values from B waveforms with time
    plot B waveforms with time
    '''
    #Bic_t=cwt1.Bic(dab1.current)
    #Boc_t=cwt1.Boc(t_ps, Vop=d*Vi)
    #print '\n Bo_max: %.2f, Bo_min: %.2f' % (max(Boc_t), min(Boc_t))
    #print ' Bi_max: %.2f, Bi_min: %.2f' % (max(Bic_t), min(Bic_t))
    #print '\n i_max: %.2f, i_min: %.2f' % (max(current_t), min(current_t))
    #plt.plot(dab1.t, Bic_t)
    #plt.plot(dab1.t, Boc_t)
    #plt.show()
    return dab1.Po, Boc_pk, Bic_pk

''' Power with k=d '''
res=18*4
Rad = [i * pi/3/res for i in range(0, res)];  #up to 60 degree.
deg = [i * 60.0/res for i in range(0, res)];  #up to 60 degree. !!!makes sure to match Rad and deg
k = [i *0.1 for i in range(1, 20, 1)]; # k is list of d

data_sets=[];
xlimit=(0, pi / 2);
ylimit=(0, 12000);
limit, legend = [], []

df_dict=OrderedDict()
df_dict.update({'deg':deg})
for j in k:
    power = [];
    l_low, l_high=[],[];

    for i in Rad:
        '''
        - iterate and calculate power, Boc peak, Bic peak with function cal()
        '''
        Po, Boc_pk, Bic_pk=cal(fs, Vi, Ls, d=j, ps=i)
        power.append(Po)
        if j==1.0:
            print '%s, %s, %s, %s'%(i/2/pi*360, Po, Boc_pk, Bic_pk)
    limit.append([xlimit, ylimit])
    legend.append('d=%.1f' %j)
    data_sets.append([Rad, power])
    df_dict.update({'d=%.1f' %j:power})

limit.append([xlimit, ylimit])
limit.append([xlimit, ylimit])
legend.append('')
legend.append('')

#data_sets.append([Rad, l_low])
#data_sets.append([Rad, l_high])
#df_dict.update({'l_low':l_low})
#df_dict.update({'l_high':l_high})

df=pd.DataFrame(df_dict)
df.to_csv('Po.csv')
ff.plot(data_sets,  title='Po', combine=True, limit=limit,legend=legend)


''' B_pk with k=d '''
df_dict=OrderedDict()
df_dict.update({'deg':deg})
data_sets=[];
xlimit=(0, pi / 2);
ylimit=(0, 1.5);
limit, legend = [], []

for j in k:
    Bi_pk = [];
    for i in Rad:
        Po, Boc_pk, Bic_pk = cal(fs, Vi, Ls, d=j, ps=i)
        Bi_pk.append(Bic_pk)
    limit.append([xlimit, ylimit])
    legend.append('d=%.1f' %j)
    data_sets.append([deg, Bi_pk])
    df_dict.update({'d=%.1f' % j: Bi_pk})
ff.plot(data_sets,  title='Bic_pk', combine=True, limit=limit,legend=legend)
df=pd.DataFrame(df_dict)
df.to_csv('Bic_pk.csv')


df_dict=OrderedDict()
df_dict.update({'deg':deg})
data_sets = [];
for j in k:
    Bo_pk = [];
    for i in Rad:
        #Vop=Vi*j
        Po, Boc_pk, Bic_pk = cal(fs, Vi, Ls, d=j, ps=i)
        Bo_pk.append(Boc_pk)
    limit.append([xlimit, ylimit])
    legend.append('d=%.1f' %j)
    df_dict.update({'d=%.1f' % j: Bo_pk})
    data_sets.append([Rad, Bo_pk])
df = pd.DataFrame(df_dict)
df.to_csv('Boc_pk.csv')


################################
delta = 0.025
x = k
y = deg
X, Y = np.meshgrid(x, y)

df_Po = pd.read_csv("Po.csv")
df_Po.__delitem__('Unnamed: 0')    #delete index to use values only
df_Po.__delitem__('deg')           #delete deg to use values only

X=df_Po.values/1000

df_Bic = pd.read_csv("Bic_pk.csv")
df_Bic.__delitem__('Unnamed: 0')    #delete index to use values only
df_Bic.__delitem__('deg')           #delete deg to use values only

Z=df_Bic.values
levels = np.arange(0, 1.4, 0.1)  # Boost the upper limit to avoid truncation errors.
fontsize=10

plt.subplot(1, 3, 1)
#CS = plt.contour(Y, X, Z, levels, extent=(0, 60, 0, 10))
CS = plt.contour(Y, X, Z, levels)
plt.clabel(CS, inline=1, fontsize=fontsize)
plt.title('Bic')
plt.xlim(0,60)
plt.ylim(0,12)

plt.subplot(1, 3, 2)
df_Boc = pd.read_csv("Boc_pk.csv")
df_Boc.__delitem__('Unnamed: 0')    #delete index to use values only
df_Boc.__delitem__('deg')           #delete deg to use values only

Z=df_Boc.values
levels = np.arange(0, 1.4, 0.1)  # Boost the upper limit to avoid truncation errors.

#CS = plt.contour(Y, X, Z, levels, extent=(0, 60, 0, 10))
CS = plt.contour(Y, X, Z, levels)
plt.clabel(CS, inline=1, fontsize=fontsize)
plt.title('Boc')
plt.xlim(0,60)
plt.ylim(0,12)

plt.subplot(1, 3, 3)
Pnom=Vb**2/(2*pi*fs)/Ls     #calculate Pnom by base valuse
y1=[Pnom/1000.0*(pi-i)*i/(pi-2.0*i) for i in Rad]
y2=[Pnom/1000.0*(pi-2*i)*(pi-i)*i/(pi**2) for i in Rad]
plt.plot(deg, y1, 'r')
plt.plot(deg, y2, 'r')
plt.xlim(0,60)
plt.ylim(0,12)
plt.show()

plt.figure(2)
plt.subplot(1, 1, 1)
plt.plot(y, df_Po['d=0.4']/1000.0)
plt.plot(y, df_Po['d=0.6']/1000.0)
plt.plot(y, df_Po['d=0.8']/1000.0)
plt.plot(y, df_Po['d=1.0']/1000.0)
plt.plot(y, df_Po['d=1.2']/1000.0)
plt.plot(y, df_Po['d=1.4']/1000.0)
plt.plot(y, df_Po['d=1.6']/1000.0)

plt.title('Po')
plt.xlim(0,60)
plt.ylim(0,12)

plt.show()

