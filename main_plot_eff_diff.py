
"""
Created on 08/03/2015, @author: sbaek
  - initial release

    V01 : 08/24/2015
     - format changes
 
    V02 : 01/20/2016
     - dict()

    V03 : 03/25/2016
     - use sort() from library 'analysis'
     - def save_fig()
     - ff.sort_index
"""

import sys, time
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append('%s/analysis' % (dirname(dirname(__file__))))

from collections import OrderedDict

from math import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import analysis.figure_functions as ff
import pandas as pd
data=OrderedDict()
para=OrderedDict()

    
def data_eff(data1, name):
    Load1, Load2, Load3= data1.keys()[0], data1.keys()[1], data1.keys()[2]    
    df1, df2, df3 = data1.values()[0], data1.values()[1], data1.values()[2]    
    eff=[]    
    for i in range(len(df1)):    
        a=(0.21*df1['eff'][i]+0.53*df2['eff'][i]+0.05*df3['eff'][i])/(0.21+0.53+0.05)
        #b=(0.48*df1['eff'][i]+0*df2['eff'][i]+0.2*df3['eff'][i])/(0.48+0+0.2)
        eff.append(a)        
    return df1.volt_in, eff

def save_fig(filename):
    print 'save : %s\n' %filename
    plt.savefig(filename)
    plt.close()

def plot_eff(data1, name):
    Load1, Load2, Load3= data1.keys()[0], data1.keys()[1], data1.keys()[2]    
    df1, df2, df3 = data1.values()[0], data1.values()[1], data1.values()[2]    
    fig = plt.figure(1)   
    ax1 = fig.add_subplot(111)    
    markersize=6
    l1=ax1.plot(df1.volt_in, df1['eff'], '-bx', markersize=markersize, label='Unit Eff. load %s%%' %Load1)
    l2=ax1.plot(df2.volt_in, df2['eff'], '-gx', markersize=markersize, label='Unit Eff. load %s%%' %Load2)
    l3=ax1.plot(df3.volt_in, df3['eff'], '-rx', markersize=markersize, label='Unit Eff. load %s%%' %Load3)
    
    lns = l1+l2+l3
    labs = [l.get_label() for l in lns]
    
    ax1.set_xlim(26, 46)  
    ax1.set_ylim(94.5, 97.5)
    ax1.set_xlabel('Vdc[V]')    
    ax1.set_ylabel('Eff.[%]')
    ax1.legend(lns, labs, loc='upper left')
    ax1.grid()

    plt.title('P_rated= %sW, %s, %s' %(para['p_rated'], para['mode'], name))
    filename=para['data_path']+'fig_%s_%.0fW_%s.png' %(para['mode'], para['p_rated'], name)
    save_fig(filename)
    
    
def main():        
    para['data_path']=dirname(dirname(__file__))+'/data/'
    #para['source_path']=dirname(dirname(__file__))+'/source_files/'
    
    para['p_rated']=280 # the amount of the power transfer from DC to AC
    para['data_file_name']='data'
    para['mode']='LL'
    #index=[0,1,2]
      
    name='14044'
    df=pd.read_csv('../data/summary_%s_%.0fW_%s.csv' %(para['mode'], para['p_rated'], name))          
    data.update({name:ff.sort_index(df)})
    plot_eff(data[name], name)  

    name='15044'
    df=pd.read_csv('../data/summary_%s_%.0fW_%s.csv' %(para['mode'], para['p_rated'], name))
    data.update({name:ff.sort_index(df)})
    plot_eff(data[name], name)

    name='17544'
    df=pd.read_csv('../data/summary_%s_%.0fW_%s.csv' %(para['mode'], para['p_rated'], name))          
    data.update({name:ff.sort_index(df)})
    plot_eff(data[name], name) 
    
    name='22044'
    df=pd.read_csv('../data/summary_%s_%.0fW_%s.csv' %(para['mode'], para['p_rated'], name))          
    data.update({name:ff.sort_index(df)})
    plot_eff(data[name], name) 


    ''' differences '''
    for Load in ('50','75','100'):  #input the Load and label to plot
        fig = plt.figure(1)
        ax1 = fig.add_subplot(111)
        markersize=6
        plts=[]

        marker='rx'
        plts.append(ax1.plot(data['14044'][Load]['volt_in'], data['15044'][Load]['eff']-data['14044'][Load]['eff'], marker,
                             markersize=markersize, label='15044-14044'))
        marker='gx'
        plts.append(ax1.plot(data['14044'][Load]['volt_in'], data['17544'][Load]['eff']-data['14044'][Load]['eff'], marker,
                             markersize=markersize, label='17544-14044'))
        marker='bx'
        plts.append(ax1.plot(data['14044'][Load]['volt_in'], data['22044'][Load]['eff']-data['14044'][Load]['eff'], marker,
                             markersize=markersize, label='22044-14044'))

        ax1.set_xlim(26, 46)
        ax1.set_ylim(-0.5, 0.5)
        ax1.set_xlabel('Vdc[V]')
        ax1.set_ylabel('Eff.[%]')

        lns=[]
        for i in range(len(plts)):
            lns=lns+plts[i]

        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')
        ax1.grid()
        plt.title('Unit Eff. difference, %s' %(para['mode']))

        filename=para['data_path']+'fig_%s_%s_%s.png' %(para['mode'], 'eff_diff', Load)
        save_fig(filename)


    ''' differences '''
    for Load in ('50','75','100'):  #input the Load and label to plot
        fig = plt.figure(2)
        ax1 = fig.add_subplot(111)
        markersize=6
        plts=[]

        marker='rx'
        plts.append(ax1.plot(data['14044'][Load]['volt_in'],
                             (data['15044'][Load]['p_in']-data['15044'][Load]['p_ac_out'])-(data['14044'][Load]['p_in']-data['14044'][Load]['p_ac_out']),
                              marker, markersize=markersize, label='15044-14044'))
        marker='gx'
        plts.append(ax1.plot(data['14044'][Load]['volt_in'],
                             (data['17544'][Load]['p_in']-data['17544'][Load]['p_ac_out'])-(data['14044'][Load]['p_in']-data['14044'][Load]['p_ac_out']),
                              marker, markersize=markersize, label='17544-14044'))
        marker='bx'
        plts.append(ax1.plot(data['14044'][Load]['volt_in'],
                             (data['22044'][Load]['p_in']-data['22044'][Load]['p_ac_out'])-(data['14044'][Load]['p_in']-data['14044'][Load]['p_ac_out']),
                              marker, markersize=markersize, label='22044-14044'))

        ax1.set_xlim(26, 46)
        ax1.set_ylim(-1, 1)
        ax1.set_xlabel('Vdc[V]')
        ax1.set_ylabel('Loss[W]')

        lns=[]
        for i in range(len(plts)):
            lns=lns+plts[i]

        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')
        ax1.grid()
        plt.title('Unit Eff. difference, %s' %(para['mode']))

        filename=para['data_path']+'fig_%s_%s_%s.png' %(para['mode'], 'loss_diff', Load)
        save_fig(filename)

        
if __name__ == '__main__':
    main()
   
    
        
  
