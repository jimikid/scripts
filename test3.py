
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
mue = 4.0 * pi * 1E-7 ;

class DAB:
    def __init__(self):
        current, B_oc, B_ic = [], [], []
        step = 1E-7
        resolution = 1

        self.fs = 20000.0;
        self.T = 1.0 / self.fs;

        # Outer core #
        self.ni, self.no = 15, 1;
        self.ri_oc = 36.0 / 2 * 1E-3;
        self.ro_oc = 55.0 / 2 * 1E-3;

        stack=0.8;

        h_oc = 25.0 * 1E-3;
        n_oc = 20;
        self.l_oc = h_oc * n_oc;
        self.Ac_oc = stack*(self.ro_oc - self.ri_oc) * self.l_oc
        self.V_oc = pi * (self.ro_oc ** 2 - self.ri_oc ** 2) * self.l_oc;

        self.mue_ic = mue * 300*65.4/68.3 #based on effective Ac, mue_r287;
        self.ri_ic = 14.7 / 2 * 1E-3;
        self.ro_ic = 26.9 / 2 * 1E-3;

        h_ic = 11.2 * 1E-3;
        n_ic = 46;
        self.l_ic = h_ic * n_ic;
        self.Ac_ic = (self.ro_ic - self.ri_ic) * self.l_ic;
        self.V_ic = pi * (self.ro_ic ** 2 - self.ri_ic ** 2) * self.l_ic;

        self.k_oc = 0.3571;
        self.beta_oc = 2.0694;

        self.k_ic = 1.2681* 1E-5;
        self.beta_ic = 2.106;
        self.alpha_ic = 1.309;

        self.w = 2 * pi * self.fs

        self.Fi = (self.mue_ic * self.ni * log(self.ro_ic / self.ri_ic) / (2 * pi * (self.ro_ic - self.ri_ic)))

    def __str__(self):
        print '\n Outer cores specs'
        print ' Di_oc :%.2f, Do_oc : %.2f [mm]' % (self.ri_oc * 2 * 1E3, self.ro_oc * 2 * 1E3)
        print ' length :%.2f [m], Ac_oc : %.2f [cm^2], V_oc : %.2f [cm^2]' % (self.l_oc, self.Ac_oc * 1E4, self.V_oc * 1E6)
        print '\n Inner cores specs'
        print ' Di_ic :%.2f, Do_ic : %.2f [mm]' % (self.ri_ic * 2 * 1E3, self.ro_ic * 2 * 1E3)
        print ' length :%.2f [m], Ac_ic : %.2f [cm^2], V_ic : %.2f [cm^2] \n' % (self.l_oc, self.Ac_ic * 1E4, self.V_ic * 1E6)


    def i1(self, Vi, t, Ls, d, ps):
        th = 2 * pi * self.fs * t
        y=(Vi*((-1 + d)*pi + 2*(th + d*th - d * ps))) / (2 * Ls *  self.w )
        return y

    def i2(self,Vi, t, Ls, d, ps):
        th = 2 * pi * self.fs * t
        y=(Vi*((-1 + d)*pi + 2*(th - d*th + d * ps))) / (2 * Ls *  self.w )
        return y

    def Bi1(self,Vi, t, F, Ls, d, ps ):
        y=F*self.i1(Vi, t, Ls, d, ps)
        return y

    def Bi2(self,Vi, t, F, Ls, d, ps):
        y=F*self.i2(Vi, t, Ls, d, ps)
        return y

    def Irms(self,Vi, Ls, d, ps):
        a=Vi*sqrt((d-1)**2*pi**3+12.0*d*pi*ps**2-8*d*ps**3)
        b=2*self.w*Ls*sqrt(3*pi)
        y=a/b
        return y


    def Boc(self, Vop, t, t_ps, Ac_oc):
        y=Vop/self.ni*(t-t_ps-self.T/4)/self.Ac_oc/self.no
        return y

    def Bic_pk(self, Vi, Ls, F, d, ps):
        if d>1:
            #y = (Vi / 2 * mue * ni * ((-1 + d) * pi + 2 * ps)) / (4 * w * Ls * pi * ri_ic)
            t_ps=ps/2/pi*self.T;
            y= F*self.i1(Vi=Vi, t=t_ps, Ls=Ls, d=d, ps=ps)
        else:
            #y = (Vi/ 2 * mue * ni * ((1 - d) * pi + 2 * d * ps)) / (4 * w * Ls * pi * ri_ic)
            y = F*self.i2(Vi=Vi, t=self.T/2, Ls=Ls, d=d, ps=ps)

        return y

    def Boc_pk(self, Vop, Ac_oc):
        y = Vop/self.ni * self.T / 2.0 / 2.0/ Ac_oc
        return y

    def L(self, mue, n, ri, ro, l):
        y=n**2*mue/2/pi*log(ro/ri)*l
        return y

    def P(self, d, Vi, ps, Ls, fs):
        w = 2 * pi * fs
        y=(d*Vi**2*(pi -ps)*ps)/(self.w*Ls*pi)
        return y

    def Loss_oc(self, k_oc, B, beta_oc, V_oc):
        y=k_oc*1E6*B**beta_oc*V_oc
        return y

    def Loss_ic(self, k_ic, Bi, alpha_ic, beta_ic, V_ic, fs, ps):
        fs2=fs * pi / ps;
        y= k_ic *1E6 * (Bi) ** beta_ic * (fs2) ** (alpha_ic - 1) * fs * V_ic
        return y

    def bound_low(self, Vi, ps, Ls):
        Pb=Vi**2/(Ls*self.w)
        y=Pb*(pi-ps)*ps/(pi-2*ps)
        return y

    def bound_high(self, Vi, ps, Ls):
        Pb=Vi**2/(Ls*self.w)
        y=Pb*((pi-2* ps)*(pi-ps)*ps)/(pi**2)
        return y


    def read(self, filepath, filename):
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

if __name__ == '__main__':
    from user import DAB
    ''' Ls calculation '''
    a=DAB()

    Ls = a.L(self.mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)#*65.4/68.3 #based on effective Ac
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
            Bi_pk = a.Bic_pk(Vi=Vi, Ls=Ls, F=a.Fi, d=d, ps=ps)
            Bo_pk = a.Boc_pk(Vop, a.Ac_oc)
            Po = a.P(d=d, Vi=Vi, ps=ps, Ls=Ls, fs=a.fs)
            iLV=a.ni*a.Irms(Vi=Vi, Ls=Ls, d=d, ps=ps)
            P_loss_oc = a.Loss_oc(k_oc=a.k_oc, beta_oc=a.beta_oc, B=Bo_pk, V_oc=a.V_oc)
            P_loss_ic = a.Loss_ic(k_ic=a.k_ic, Bi=a.Bi_pk, alpha_ic=a.alpha_ic, beta_ic=a.beta_ic, V_ic=a.V_ic, fs=a.fs, ps=ps)
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





