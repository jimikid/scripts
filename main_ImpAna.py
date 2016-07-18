
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

data= OrderedDict()
figsize=(8,6)
xlim=(0.1,10)
xtick=[i for i in range(100,600,100)]
xtick=[0.1,1,10]
xtick_label=[str(i) for i in range(100,600,100)]
xtick_label=['0.1','1','10']

for i in range(1,7):       
    filename="C%s_open(1)timestested_" %i
    print filename
    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")    
    save_path=""    
    #df=pd.read_csv(folderpath+'/'+filename+'/'+filename+'.csv')                
    df=pd.read_csv('C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0715_Payton/T1/'+filename+'/'+filename+'.csv')                
    data.update({filename:df})

limit=[]
legend=[]
data_list=[]

for i in data.keys():
    print i
    data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE A'][:200]*1E3))
    limit.append((xlim,(0, 4)))
    print i , i.split('_')[0]
    legend.append(i.split('_')[0])

ff.plot(
    data=data_list,
    label=[('Freq [kHz]','L [mH]')],
    limit=limit,
    title='L open_circuit' ,
    fig_num=1, hold=True, combine=True, legend=legend, figsize=figsize,
    xtick=xtick, xtick_label=xtick_label)

data_list=[]; limit=[]; legend=[]

for i in data.keys():
    print i
    data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE B'][:200]))
    limit.append((xlim,(0, 1)))
    print i , i.split('_')[0]
    legend.append(i.split('_')[0])

ff.plot(
        data=data_list,
        label=[('Freq [kHz]','R [ohm]')],
        limit=limit,
        title='R open_circuit' ,
        fig_num=2, hold=True, combine=True, legend=legend, figsize=figsize,
        xtick=xtick, xtick_label=xtick_label)


#############


data= OrderedDict()


for i in range(1,7):       
    filename="C%s_short(1)timestested_" %i
    print filename
    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")    
    save_path=""    
    #df=pd.read_csv(folderpath+'/'+filename+'/'+filename+'.csv')                
    df=pd.read_csv('C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0715_Payton/T1/'+filename+'/'+filename+'.csv')                
    data.update({filename:df})

data_list=[]
limit=[]
legend=[]
for i in data.keys():
    print i
    data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE A'][:200]*1E3))
    limit.append((xlim,(0, 0.15)))
    print i , i.split('_')[0]
    legend.append(i.split('_')[0])


ff.plot(
    data=data_list,
    label=[('Freq [kHz]','L [mH]')],
    limit=limit,
    title='L short_circuit' ,
    fig_num=1, hold=True, combine=True, legend=legend, figsize=figsize,
    xtick=xtick, xtick_label=xtick_label)


data_list=[]
limit=[]
legend=[]

for i in data.keys():
    print i
    data_list.append((data[i]['FREQ (HZ)'][:200]/1E3, data[i]['TRACE B'][:200]))
    limit.append((xlim,(0, 0.2)))
    print i , i.split('_')[0]
    legend.append(i.split('_')[0])


ff.plot(
    data=data_list,
    label=[('Freq [kHz]','R [ohm]')],
    limit=limit,
    title='R short_circuit' ,
    fig_num=2, hold=True, combine=True, legend=legend, figsize=figsize,
    xtick=xtick, xtick_label=xtick_label)


