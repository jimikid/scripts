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
from collections import OrderedDict

from math import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import analysis.figure_functions as ff

data_w = OrderedDict()
para = OrderedDict()


def data_eff(data1, name):
    Load1, Load2, Load3 = data1.keys()[0], data1.keys()[1], data1.keys()[2]
    df1, df2, df3 = data1.values()[0], data1.values()[1], data1.values()[2]
    eff = []
    for i in range(len(df1)):
        a = (0.21 * df1['eff'][i] + 0.53 * df2['eff'][i] + 0.05 * df3['eff'][i]) / (0.21 + 0.53 + 0.05)
        # b=(0.48*df1['eff'][i]+0*df2['eff'][i]+0.2*df3['eff'][i])/(0.48+0+0.2)
        eff.append(a)
    return df1.volt_in, eff


def save_fig(filename):
    print 'save : %s\n' % filename
    plt.savefig(filename)
    plt.close()


def weight_eff(data1, name):
    ''' check load conditions and pu weight into account '''
    for i in range(len(data1)):
        if (int(data1.keys()[i]) > 98 and int(data1.keys()[i]) < 102):
            weight1 = 0.05
            print 'Load :100, weight :%s' % weight1
            L100 = data1.values()[i]['eff'] * weight1

        if (int(data1.keys()[i]) > 73 and int(data1.keys()[i]) < 77):
            weight2 = 0.53
            print 'Load :75, weight :%s' % weight2
            L75 = data1.values()[i]['eff'] * weight2

        if (int(data1.keys()[i]) > 48 and int(data1.keys()[i]) < 52):
            weight3 = 0.21
            print 'Load :50, weight :%s \n' % weight3
            L50 = data1.values()[i]['eff'] * weight3
    eff = (L100 + L75 + L50) / (weight1 + weight2 + weight3)
    return (data1.values()[0]['volt_in'], eff)


def main():
    results = OrderedDict()
    '''
    names=[]
    figsize = (5, 7)
    for i in range(1,6):
        for j in range(1,3):
            names.append('C%s_%s' %(i,j))
    print names
    #names = ['C4_1', 'C4_2']
    for name in names:
        para['p_rated'] = 300  # the amount of the power transfer from DC to AC
        para['ac_mode'] = 'LL'

        foldername = "%s_LL_%sW" % (name, para['p_rated'])
        path = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/%s/%s/' % (name.split('_')[0], foldername)
        # para['data_path']=dirname(dirname(__file__))+'/data/'
        para['data_path'] = path
        # index=[0,1,2]

        df = pd.read_csv(path + "summary_LL_%sW.csv" %para['p_rated'])
        results.update({name: ff.sort_index(df)})  # results[name].keys()  # e.g. ['49', '74', '99']
        Load = results[name].keys()
        data = results[name].values()
        ff.plot_eff(para, file_name=name, data=results[name], limit=[(26, 46), (95.5, 97.5)],
                    marker='o', figsize=figsize, add_labels =False)

    '''

    names = []
    figsize = (5, 7)
    for i in range(1, 6):
        for j in range(1, 5):
            names.append('C%s_%s' % (i, j))
    print names
    for name in names:
        try:

            para['p_rated'] = 290  # the amount of the power transfer from DC to AC
            para['ac_mode'] = 'LL'

            foldername = "%s_LL_%sW" % (name, para['p_rated'])
            path = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/%s/%s/' % (name.split('_')[0], foldername)
            # para['data_path']=dirname(dirname(__file__))+'/data/'
            para['data_path'] = path
            para['name'] = name
            # index=[0,1,2]

            df = pd.read_csv(path + "summary_LL_%sW.csv" % para['p_rated'])
            results.update({name: ff.sort_index(df)})  # results[name].keys()  # e.g. ['49', '74', '99']
            Load = results[name].keys()
            data = results[name].values()
            #ff.plot_eff(para, data=results[name], limit=[(26, 46), (95.5, 97.5)], marker='o',figsize = figsize)
            ff.plot_eff(para, data=results[name], limit=[(26, 46), (95.5, 97.5)], marker='o', figsize=figsize)
        except:pass


    #name = 'C4_eff_1'
    figsize = (5, 7)
    for p_rated in [270, 280, 290, 300]:
        para['p_rated'] = p_rated  # the amount of the power transfer from DC to AC
        para['ac_mode'] = 'LL'
        para['name'] = 'C4_eff_1'

        foldername = "%s_LL_%sW" % (para['name'], para['p_rated'])
        path = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/C4_eff/%s/' %foldername
        # para['data_path']=dirname(dirname(__file__))+'/data/'
        para['data_path'] = path
        # index=[0,1,2]

        df = pd.read_csv(path + "summary_LL_%sW.csv" % para['p_rated'])
        results.update({para['name']: ff.sort_index(df)})  # results[name].keys()  # e.g. ['49', '74', '99']
        Load = results[para['name']].keys()
        data = results[para['name']].values()
        ff.plot_eff(para, data=results[name], limit=[(27, 45), (95.7, 97.3)], marker='o', figsize=figsize)

if __name__ == '__main__':
    main()




