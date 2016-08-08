
"""
Created on 08/03/2015
    - initial release
@author: sbaek
    V01 : 08/24/2015
     - format changes

    V02 : 01/21/2016
     - oveall changes with dict()
     - check load conditions and pu weight into account

    V03 : 03/16/2016
     - link to analysis folder
     - namesof valuables in a summary file changed.  -> volt_in, eff

"""

import sys, time
from os.path import abspath, dirname
print dirname(dirname(__file__))
sys.path.append(dirname(dirname(__file__)))
#print '%s/analysis' % (dirname(dirname(__file__)))
#sys.path.append('%s/analysis' % (dirname(dirname(__file__))))

from collections import OrderedDict

from math import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import analysis.figure_functions as ff


data_w=OrderedDict()
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


def weight_eff(data1, name):
    ''' check load conditions and pu weight into account '''
    for i in range(len(data1)):
        if (int(data1.keys()[i])>98 and int(data1.keys()[i])<102):
            weight1=0.05
            print 'Load :100, weight :%s' %weight1
            L100= data1.values()[i]['eff']*weight1

        if (int(data1.keys()[i])>73 and int(data1.keys()[i])<77):
            weight2=0.53
            print 'Load :75, weight :%s' %weight2
            L75= data1.values()[i]['eff']*weight2

        if (int(data1.keys()[i])>48 and int(data1.keys()[i])<52):
            weight3=0.21
            print 'Load :50, weight :%s \n' %weight3
            L50= data1.values()[i]['eff']*weight3
    eff=(L100+L75+L50)/(weight1+weight2+weight3)
    return (data1.values()[0]['volt_in'], eff)



def main():
    data = OrderedDict()
    names=['C4_1', 'C4_2', 'C5_1', 'C5_2']
    for name in names:
        foldername = "%s_LL_290W" % (name)
        path = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/%s/%s/' % (name.split('_')[0], foldername)
        # para['data_path']=dirname(dirname(__file__))+'/data/'
        para['data_path'] = path
        para['p_rated'] = 290  # the amount of the power transfer from DC to AC
        #para['data_file_name'] = 'data'
        #para['mode'] = 'LL'
        # index=[0,1,2]
        print path+"summary_LL_290W.csv"
        df=pd.read_csv(path+"summary_LL_290W.csv")
        data.update({name:ff.sort_index(df)})
        #print data[name]
        print data[name].keys() # e.g. ['49', '74', '99']
        #print data[name].values()
        print [float(i) for i in data[name].keys()]
        para['Load_pts']= [float(i) for i in data[name].keys()]

        #ff.plot_eff(para, df= data[name], file_name=name, limit=[(26,46),(95.5, 97.5)])
        Load=data[name].keys()
        data=data[name].values()
        print name
        print data[name]
               #     para, file_name, Load, data, df = None, limit = None
        ff.plot_eff(para, file_name=name, Load=Load, data=data[name] ,  limit=[(26,46),(95.5, 97.5)])
        data_w.update({name:weight_eff(data[name], name)})


    ''' plot based on load conditions '''
    for n in range(len(data[name].values())):   #len(data[name].values()) : # of sorted load condtions
        fig = plt.figure(n+1)
        ax1 = fig.add_subplot(111)
        markersize=6
        plts=[]
        for key1 in data:
            '''data is in dict()
               key1 is the name ' ',
               data[key1].keys() : 'load condition in str' in list []
               data[key1].values() : 'measured values in dataframe' in list[]
               n indicates load condition
            '''
            plts.append(ax1.plot(data[key1].values()[n]['volt_in'], data[key1].values()[n]['eff'], '-x',
                                 markersize=markersize, label='Unit Eff. '+key1))

        ax1.set_xlim(26, 46)
        ax1.set_ylim(94.5, 97.5)
        ax1.set_xlabel('Vdc[V]')
        ax1.set_ylabel('Eff.[%]')

        lns=[]
        for i in range(len(plts)):
            lns=lns+plts[i]

        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')
        ax1.grid()
        plt.title('Load= %s%%, %s' %(data.values()[n].keys()[n], para['mode']))
        filename=para['data_path']+'fig_%s_%s.png' %(para['mode'], data.values()[n].keys()[n])
        save_fig(filename)


    ''' weighted eff
    fig = plt.figure(1)
    ax1 = fig.add_subplot(111)
    markersize=6
    plts=[]
    for key1 in data_w:
        if '140' in key1:
            plts.append(ax1.plot(data_w[key1][0], data_w[key1][1], '-x',
                             markersize=markersize, label='Unit Eff. '+key1))
        if '150' in key1:
            plts.append(ax1.plot(data_w[key1][0], data_w[key1][1], '-x',
                             markersize=markersize, label='Unit Eff. '+key1))
        if '175' in key1:
            plts.append(ax1.plot(data_w[key1][0], data_w[key1][1], '-x',
                             markersize=markersize, label='Unit Eff. '+key1))
        if '220' in key1:
            plts.append(ax1.plot(data_w[key1][0], data_w[key1][1], '-x',
                             markersize=markersize, label='Unit Eff. '+key1))

    ax1.set_xlim(26, 46)
    ax1.set_ylim(95.6, 97.0)
    ax1.set_xlabel('Vdc[V]')
    ax1.set_ylabel('Eff.[%]')

    lns=[]
    for i in range(len(plts)):
        lns=lns+plts[i]

    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left')
    ax1.grid()
    plt.title('Weighted Eff., Po=%s, %s' %(para['p_rated'], para['mode']))
    filename=para['data_path']+'fig_weighted_eff_%s_%s.png' %(para['mode'], para['p_rated'])
    save_fig(filename)
    '''

        
if __name__ == '__main__':
    main()
   
    
        
  
