
"""
@author: sbaek
  V00 06/01/2016
    - initial release
    - plot and save : ff.plot, ff.plot_bar for .csv files.

"""
import sys, time
from os.path import abspath, dirname
folderpath=dirname(__file__)
print folderpath
sys.path.append('%s/analysis' % (dirname(dirname(__file__))))
print 'add path %s/analysis' % (dirname(dirname(__file__)))
from collections import OrderedDict

print sys.path
import matplotlib.pyplot as plt
import pandas as pd
import figure_functions as ff
import pandas as pd




def main_L(filename, data, terminal, scale, xlim, ylim, xtick,xtick_label):
    figsize = (8, 6)

    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")
    save_path=""
    data_list=[]; limit=[]; legend=[]


    for i in data.keys():
        print i
        data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE A'][:200]*1E3))
        limit.append((xlim,ylim))
        print i , i.split('_')[0]
        legend.append(i.split('_')[0])

    ff.plot(
        data=data_list,
        label=[('Freq [kHz]','L [mH]')],
        limit=limit,
        title='L_%s_circuit' %terminal ,
        fig_num=1, hold=True, combine=True, legend=legend, figsize=figsize,
        xtick=xtick, xtick_label=xtick_label, scale=scale)\




def main_R(filename, data, terminal, scale, xlim, ylim, xtick,xtick_label):
    figsize = (8, 6)
    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")
    save_path=""

    data_list=[]; limit=[]; legend=[]

    for i in data.keys():
        print i
        data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE B'][:200]))
        limit.append((xlim,ylim))
        print i , i.split('_')[0]
        legend.append(i.split('_')[0])

    ff.plot(
            data=data_list,
            label=[('Freq [kHz]','R [ohm]')],
            limit=limit,
            title='R_%s_circuit'%terminal ,
            fig_num=2, hold=True, combine=True, legend=legend, figsize=figsize,
            xtick=xtick, xtick_label=xtick_label, scale=scale)


def main_G(filename, data, terminal, scale, xlim, ylim, xtick,xtick_label):
    figsize = (8, 6)
    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")
    save_path=""

    data_list=[]; limit=[]; legend=[]

    for i in data.keys():
        print i
        data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE B'][:200]))
        limit.append((xlim,ylim))
        print i , i.split('_')[0]
        legend.append(i.split('_')[0])

    ff.plot(
            data=data_list,
            label=[('Freq [kHz]','G [S]')],
            limit=limit,
            title='G_%s_circuit'%terminal ,
            fig_num=2, hold=True, combine=True, legend=legend, figsize=figsize,
            xtick=xtick, xtick_label=xtick_label, scale=scale)



if __name__ == '__main__':
    data = OrderedDict()
    xlim = (100, 300)
    #xlim = (1, 3)
    xtick = [i for i in range(100, 400, 100)]
    #xtick = [1, 2, 3]
    xtick_label = [str(i) for i in range(100, 600, 100)]
    xtick_label = ['1', '2', '3']

    terminal = 'open'

    for i in range(1,7):
        filename="C%s_%s(1)timestested_" %(i, terminal)
        df=pd.read_csv('C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0718_Payton/T1/'+filename+'/'+filename+'.csv')
        data.update({filename:df})
    main_L(filename, data, terminal, scale='log', xlim=xlim, ylim = (0, 4),  xtick=xtick, xtick_label=xtick_label)
    #main_L(filename, data, terminal, scale='loglog', xlim=xlim, ylim = (0, 4),xtick=xtick, xtick_label=xtick_label)
    main_G(filename, data, terminal, scale='log', xlim=xlim, ylim = (0, 2E-3), xtick=xtick, xtick_label=xtick_label)
    #main_G(filename, data, terminal, scale='loglog', xlim=xlim, ylim = (0, 1E-5), xtick=xtick, xtick_label=xtick_label)


    data = OrderedDict()
    terminal = 'short'

    for i in range(1, 7):
        filename = "C%s_%s(1)timestested_" % (i, terminal)
        df = pd.read_csv('C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0718_Payton/T1/' + filename + '/' + filename + '.csv')

        data.update({filename: df})
    main_L(filename, data, terminal, scale='log', xlim=xlim, ylim = (0, 0.14), xtick=xtick, xtick_label=xtick_label)
    #main_L(filename, data, terminal, scale='loglog', xlim=xlim, ylim = (0, 0.14), xtick=xtick, xtick_label=xtick_label)
    main_R(filename, data, terminal, scale='log', xlim=xlim, ylim = (0.15, 0.45),xtick=xtick, xtick_label=xtick_label)
    #main_R(filename, data, terminal, scale='loglog', xlim=xlim,  ylim = (0, 0.5),xtick=xtick, xtick_label=xtick_label)
