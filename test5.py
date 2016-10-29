
"""
Created on 08/28/2016, @author: sbaek
    - initial release
"""

import sys, time, os
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
from collections import OrderedDict
from collections import OrderedDict
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


from test3 import DAB
from math import *
import pandas as pd
#import data_aq_lib.analysis.figure_functions as ff
import analysis.figure_functions as ff
#import data_aq_lib.analysis.waveform_func as wf
import analysis.waveform_func as wf


def plot_map(df, item='eff', figsize=(5, 7), xlim=(26, 46), ylim=(140, 300)):
    p_ac_out = df['p_ac_out']
    eff = df[item]
    plt.figure(1, figsize=figsize)
    # volt_in = df['volt_in']
    # volt_in = df['Vdc'] # there are cases fail to boot up
    volt_in = df['volt_in']
    fault_ = df['fault']

    seed(0)
    x, y, z = volt_in, p_ac_out, eff

    # define grid.
    xi = np.linspace(26, 46, 100)
    yi = np.linspace(130, 300, 100)
    # grid the data.
    zi = griddata(x, y, z, xi, yi, interp='linear')
    # contour the gridded data, plotting dots at the nonuniform data points.
    CS = plt.contour(xi, yi, zi, 10, linewidths=0.1, colors='k')
    CS = plt.contourf(xi, yi, zi, 10, cmap=plt.cm.rainbow, vmax=zi.max(), vmin=zi.min(), alpha=0.3)

    plt.colorbar()
    plt.scatter(x, y, marker='o', c='b', s=30, zorder=20, alpha=0.9)

    ''' fault check - add red dots'''
    for j in range(len(fault_)):
        if fault_[j] == True:
            plt.scatter(x[j - 1], y[j - 1] + 3, marker='o', c='r', s=60, zorder=20, alpha=1)

    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title("%s" % item)
    plt.xlabel('Vdc [V]')
    plt.ylabel('P_ac_out [W]')
    name = self.path + '/%s_map_' % item + self.filename + '.png'
    print ' save : %s \n' % name
    plt.savefig(name)
    plt.close()




mue = 4.0 * pi * 1E-7 ;
current, B_oc, B_ic = [], [], []
step, resolution = 1E-7, 1

fs = 20000.0;
ni, no = 15, 1;
ri_oc, ro_oc, h_oc   = 36.0 / 2 * 1E-3,  55.0 / 2 * 1E-3, 25.0 * 1E-3;
n_oc = 20;

mue_ic=300.0
ri_ic, ro_ic, h_ic  = 14.7 / 2 * 1E-3, 26.9 / 2 * 1E-3, 11.2 * 1E-3;
n_ic = 46;

a=DAB(fs, ni, no, ri_oc, ro_oc, h_oc, n_oc, mue_ic, ri_ic, ro_ic, h_ic, n_ic)

''' Ls calculation '''

Ls = a.L(a.mue_ic, n=a.ni, ri=a.ri_ic, ro=a.ro_ic, l=a.l_ic)#*65.4/68.3 #based on effective Ac
print '\n Ls : %.2f [mH], length :%.2f' %(Ls*1000, a.l_ic)

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
        Bi_pk = a.Bic_pk(Vi=Vi, Ls=Ls, F=a.Fi, d=d, ps=ps)
        Bo_pk = a.Boc_pk(Vop, a.Ac_oc)
        Po = a.P(d=d, Vi=Vi, ps=ps, Ls=Ls, fs=a.fs)
        iLV=a.ni*a.Irms(Vi=Vi, Ls=Ls, d=d, ps=ps)
        P_loss_oc = a.Loss_oc(k_oc=a.k_oc, beta_oc=a.beta_oc, B=Bo_pk, V_oc=a.V_oc)
        P_loss_ic = a.Loss_ic(k_ic=a.k_ic, Bi=Bi_pk, alpha_ic=a.alpha_ic, beta_ic=a.beta_ic, V_ic=a.V_ic, fs=a.fs, ps=ps)
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
                 'power': power, 'eff': eff, 'irms_LV':irms, 'Bi_pk':Bi_pk, 'Bo_pk':Bo_pk})
df.to_csv('data.csv')

ff.plot([
    [df['deg'], df['loss_c']],
    [df['deg'], df['loss_ic']],
    [df['deg'], df['loss_oc']],
    [df['deg'], df['loss_w']]
    ], title='loss', combine=True,  legend=legend, figsize=(8, 5))

ff.plot([
    [df['deg'], df['loss_c']/df['power']],
    [df['deg'], df['loss_ic']/df['power']],
    [df['deg'], df['loss_oc']/df['power']],
    [df['deg'], df['loss_w']/df['power']],
    [df['deg'], df['power']/ 10000.0]
    ], title='loss_ratio', combine=True,  legend=legend, figsize=(8, 5))


ff.plot([
    [df['deg'], df['power']]
    ]  , title='Po1', combine=True,  legend=legend, figsize=(8, 5))
ff.plot([[df['deg'], df['eff']]], title='Eff', combine=True,  legend=legend, figsize=(8, 5))





