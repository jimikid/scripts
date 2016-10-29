
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
import analysis.waveform_func as wf

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

def Boc(Vop, t, t_ps):
    y=Vop/ni*(t-t_ps-T/4)/Ac_oc/no
    return y

def Irms(Vi, Ls, d, ps):
    a=Vi*sqrt((d-1)**2*pi**3+12.0*d*pi*ps**2-8*d*ps**3)
    b=2*w*Ls*sqrt(3*pi)
    y=a/b
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
    #y=n**2*mue/2/pi*log(ro/ri)*l*65.35/68.32
    y = n ** 2 * mue / 2 / pi * log(ro / ri) * l
    return y

def P(d, Vi, ps, Ls, fs):
    w = 2 * pi * fs
    y=(d*Vi**2*(pi -ps)*ps)/(w*Ls*pi)
    return y

def Loss_oc(k_oc, B, beta_oc, V_oc):
    y=k_oc*B**beta_oc*V_oc
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



def main():
    d = 1.0;
    deg = 60.0;
    time_shift = T / 4.0;
    ps = deg / 360.0 * 2.0 * pi;
    shift = int(time_shift / step);

    t_ps = T * ps / (2 * pi)
    Vi = 3000.0;
    Vop = Vi * d;
    Vb = Vi;

    t_ps = ps / (2 * pi) * T;
    # deg = int(ps / 2 / pi * 360)


    ''' Ls calculation '''
    Ls = L(mue_ic, n=ni, ri=ri_ic, ro=ro_ic, l=l_ic)
    print '\n Ls : %.2f [mH]' %(Ls*1000)

    ''' B peaks '''
    Bi_pk=Bic_pk(Vi=Vi, Ls=Ls, F=Fi, d=d, ps=ps)
    Bo_pk=Boc_pk(Vop)
    print '\n Calculation : Bi_pkpk : %.2f, Bo_pkpk : %.2f [T]' % (Bi_pk*2, Bo_pk*2)


    ''' current'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        current.append(i1(Vi=Vi,t=i, Ls=Ls, d=d, ps=ps))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        current.append(i2(Vi=Vi,t=i, Ls=Ls, d=d, ps=ps))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        current.append(-i1(Vi=Vi,t=i - T / 2, Ls=Ls, d=d, ps=ps))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        current.append(-i2(Vi=Vi,t=i - T / 2, Ls=Ls, d=d, ps=ps))


    ''' Bic'''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_ic.append(Bi1(Vi=Vi, t=i, F=Fi, Ls=Ls, d=d, ps=ps))
    t2 = [i * step for i in range(int(t_ps / step), int(T / step / 2), resolution)]
    for i in t2:
        B_ic.append(Bi2(Vi=Vi, t=i, F=Fi, Ls=Ls, d=d, ps=ps))
    t3 = [i * step for i in range(int(T / step / 2), int(T / step / 2) + int(t_ps / step), resolution)]
    for i in t3:
        B_ic.append(-Bi1(Vi=Vi, t=i - T / 2, F=Fi, Ls=Ls, d=d, ps=ps))
    t4 = [i * step for i in range(int(T / step / 2) + int(t_ps / step), int(T / step), resolution)]
    for i in t4:
        B_ic.append(-Bi2(Vi=Vi, t=i - T / 2, F=Fi, Ls=Ls, d=d, ps=ps))

    ''' Boc '''
    t1 = [i * step for i in range(0, int(t_ps / step), resolution)]
    for i in t1:
        B_oc.append(-Boc(Vop=Vop, t=i + T/2, t_ps=t_ps))
    t2 = [i * step for i in range(int(t_ps / step), int((t_ps + T / 2) / step), resolution)]
    for i in t2:
        B_oc.append(Boc(Vop=Vop,t=i,  t_ps=t_ps))
    t3 = [i * step for i in range(int((t_ps + T / 2) / step), int(T / step), resolution)]
    for i in t3:
        B_oc.append(-Boc(Vop=Vop,t=i - T/2,  t_ps=t_ps))

    print '\n Bo_max: %.2f, Bo_min: %.2f' %(max(B_oc), min(B_oc))
    print ' Bi_max: %.2f, Bi_min: %.2f' % (max(B_ic), min(B_ic))
    print '\n i_max: %.2f, i_min: %.2f' % (max(current), min(current))


    ''' Power calculation '''
    Po = P(d=d, Vi=Vi, ps=ps, Ls=Ls, fs=fs)
    print '\n Po : %.2f [kW] at %.1f deg, d:%.2f' % (Po *1E-3, deg, d)

    ''' Loss calculation '''
    P_loss_oc=Loss_oc(k_oc=k_oc, beta_oc=beta_oc, B=Bo_pk, V_oc=V_oc)
    print '\n P_loss_oc : %.1f [W]' % (P_loss_oc)

    ''' rms '''
    a = [(i) ** 2 for i in current]
    cur=sqrt(sum(a) / len(a))
    print '\n Irms : %.1f [Arms]' % (cur)

    ''' two cycle'''
    cycle=2
    t = [i * step for i in range(0, int(cycle * T / step), resolution)]
    Is = current * cycle
    Bi=B_ic*cycle
    Bo=B_oc*cycle

    ''' shift '''
    shift=T*45.0/360+t_ps/2+T/2
    t = [i * step for i in range(0, int( T / step), resolution)]
    Is = Is[int( shift / step):int( (T+shift) / step)]
    Bi = Bi[int( shift / step):int( (T+shift) / step)]
    Bo = Bo[int( shift / step):int( (T+shift) / step)]

    data = OrderedDict()
    data.update({'t': t})
    data.update({'is_%s_%s'%(deg, d): Is})
    data.update({'Boc_%s_%s'%(deg, d): Bo})
    data.update({'Bic_%s_%s'%(deg, d): Bi})
    df = pd.DataFrame(data)

    spec = 'L%.1f_d%.1f_deg%s' % (Ls * 1000, d, deg)
    df.to_csv('data_%s.csv' % (spec), index=False)
    ff.plot()

    ff.plot([[t, Is]], title='current_%s'%spec)
    #ff.plot([[t, B_oc_avg], [t, B_ic]], legend=['Boc', 'Bic'], title='B1_%s'%spec)
    ff.plot([[t, Bo], [t, Bi]], legend=['Boc', 'Bic'], title='B2_%s'%spec, combine=True)


    ''' Power with k=d '''

    res=18
    Rad = [i * pi/2/res for i in range(0, res)];
    deg = [i * 90.0/res for i in range(0, res)];
    k = [i *0.1 for i in range(6, 15, 2)];
    data_sets=[];
    xlimit=(0, pi / 2);
    ylimit=(0, 12000);
    limit, legend = [], []

    df_dict=OrderedDict()
    df_dict.update({'deg':deg})

    #df=pd.DataFrame()


    for j in k:
        power, cur = [],[];
        l_low, l_high=[],[];

        for i in Rad:
            power.append(P(d=j, Vi=Vi, ps=i, Ls=Ls, fs=fs))
            cur.append(2**0.5*Irms(Vi=Vi, Ls=Ls, d=j, ps=i)) #Irms*2^0.5

        limit.append([xlimit, ylimit])
        legend.append('d=%.1f' %j)
        data_sets.append([Rad, power])
        df_dict.update({'dp=%.1f' %j:power, 'di=%.1f' %j:cur})


    for i in Rad:
        l_low.append(bound_low(Vi=Vi,ps=i, Ls=Ls))
        l_high.append(bound_high(Vi=Vi,ps=i, Ls=Ls))


    limit.append([xlimit, ylimit])
    limit.append([xlimit, ylimit])
    legend.append('')
    legend.append('')

    data_sets.append([Rad, l_low])
    data_sets.append([Rad, l_high])

    df_dict.update({'l_low':l_low})
    df_dict.update({'l_high':l_high})

    df=pd.DataFrame(df_dict)
    df.to_csv('data_dab.csv')
    ff.plot(data_sets,  title='Po', combine=True, limit=limit,legend=legend)


    ''' B_pk with k=d '''

    Rad = [i * pi/2/res for i in range(0, res)];
    k = [i *0.1 for i in range(4, 21, 2)];
    data_sets=[];
    xlimit=(0, pi / 2);
    ylimit=(0, 1.5);
    limit, legend = [], []

    for j in k:
        Bi_pk = [];
        for i in Rad:
            Bi_pk.append(Bic_pk(Vi=Vi, Ls=Ls, F=Fi, d=j, ps=i))
        limit.append([xlimit, ylimit])
        print Bi_pk
        legend.append('d=%.1f' %j)
        df_dict.update({'dBic=%.1f' % j: Bi_pk})
        data_sets.append([deg, Bi_pk])
    print data_sets
    ff.plot(data_sets,  title='Bic_pk', combine=True,legend=legend)

    data_sets = [];
    for j in k:
        Bo_pk = [];
        for i in Rad:
            Vop=Vi*j
            Bo_pk.append(Boc_pk(Vop=Vop))
        limit.append([xlimit, ylimit])
        df_dict.update({'dBoc=%.1f' % j: Bo_pk})
        legend.append('d=%.1f' %j)
        data_sets.append([Rad, Bo_pk])

    #df.set_index(deg)
    ff.plot(data_sets,  title='Boc_pk', combine=True, limit=limit,legend=legend)
    df = pd.DataFrame(df_dict)
    df.to_csv('data_dab2.csv')


    return df




    ''' read file'''
    read(filepath='', filename='data_%s' % (spec))

if __name__ == '__main__':
    df=main()



