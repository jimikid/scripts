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

    V04 : 08/05/2016
     - overall change.
     - main_plot_sat_limit.py and map plots are combined with eff_func.py.
"""

import sys, time
from os.path import abspath, dirname
print dirname(dirname(__file__))
sys.path.append(dirname(dirname(__file__)))
from collections import OrderedDict
from math import *
import matplotlib.pyplot as plt
import analysis.eff_func as ef

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


def weight_eff(data1):
    ''' check load conditions and put weight into account '''
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
    ''' eff plots '''
    results, names = OrderedDict(), []
    figsize = (5, 7)
    for i in range(3, 6):
        for j in range(1, 5):
            names.append('C%s_%s' % (i, j))

    for name in names:
        para['p_rated'], para['ac_mode'] = 290, 'LL'
        foldername = "%s_LL_%sW" % (name, para['p_rated'])
        file_name='summary_%s_%.0fW' % (para['ac_mode'], para['p_rated'])
        para['data_path'] = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/%s/%s/' % (name.split('_')[0], foldername)
        para['name'] = name

        ef1=ef.eff(file_name=file_name, para=para)
        ef1.plot_eff(limit=[(26, 46), (95.5, 97.5)], marker='o', figsize=figsize)
        results.update({name: ef1.sort_index()})


    ''' weighted eff '''
    # for 50%, 75% and 100% measurements only!
    for i in range(3, 6):
        for j in range(1, 5):
            names.append('C%s_%s' % (i, j))

    plts = [] #put ;lots in this list
    for name in names:
        para['p_rated'], para['ac_mode'] = 290, 'LL'
        foldername = "%s_LL_%sW" % (name, para['p_rated'])
        file_name='summary_%s_%.0fW' % (para['ac_mode'], para['p_rated'])
        para['data_path'] = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/%s/%s/' % (name.split('_')[0], foldername)
        #para['name'] = name

        results[name]
        volt_in, eff = weight_eff(results[name])
        fig = plt.figure(1)
        ax1 = fig.add_subplot(111)
        markersize=6
        plts.append(ax1.plot(volt_in, eff, '-x', markersize=markersize, label='Eff. %s' %name))
        #ax1.set_xlim(26, 46)
        #ax1.set_ylim(95.6, 97.0)
        #ax1.set_xlabel('Vdc[V]')
        #ax1.set_ylabel('Eff.[%]')
        #ax1.grid()
        #plt.title('Weighted Eff., Po=%s, %s' %(para['p_rated'], para['ac_mode']))
        filename=para['data_path']+'fig_weighted_eff_%s_%s.png' %(para['ac_mode'], para['p_rated'])
        #save_fig(filename) # if save here cannot produce a combined plot


    ax1.set_xlim(26, 46)
    ax1.set_ylim(95.6, 97.0)
    ax1.set_xlabel('Vdc[V]')
    ax1.set_ylabel('Eff.[%]')
    #combine all weighted eff plots.
    lns=[]
    for i in range(len(plts)):
        lns=lns+plts[i]

    print lns

    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left')
    ax1.grid()
    plt.title('Weighted Eff., Po=%s, %s' %(para['p_rated'], para['ac_mode']))
    filename='fig_weighted_eff_%s_%s.png' %(para['ac_mode'], para['p_rated'])
    save_fig(filename)


    ''' map and 3d plots '''
    names = []
    for i in range(1, 6):
        for j in range(1, 3):
            names.append('C%s_%s' % (i, j))
    for name in names:
        para['p_rated'], para['ac_mode'] = 300, 'LL'
        foldername = "%s_LL_%sW" % (name, para['p_rated'])
        file_name='summary_%s_%.0fW' % (para['ac_mode'], para['p_rated'])
        para['data_path'] = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/%s/%s/' % (name.split('_')[0], foldername)
        #para['name'] = name

        ef2=ef.eff(file_name=file_name, para=para)
        ef2.plot_eff(limit=[(26, 46), (95.5, 97.5)], marker='o', figsize=figsize)
        ef2.plot_3d(zlim=(95.5, 97.5))
        ef2.plot_map()


    ''' plot based on load conditions '''
    for n in range(len(results[name].values())):   #len(data[name].values()) : # of sorted load condtions
        fig = plt.figure(n+1)
        ax1 = fig.add_subplot(111)
        markersize=6
        plts=[]
        for key1 in results:
            '''data is in dict()
               key1 is the name ' ',
               data[key1].keys() : 'load condition in str' in list []
               data[key1].values() : 'measured values in dataframe' in list[]
               n indicates load condition
            '''
            plts.append(ax1.plot(results[key1].values()[n]['volt_in'], results[key1].values()[n]['eff'], '-x',
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
        plt.title('Load= %s%%, %s' %(results.values()[n].keys()[n], para['ac_mode']))
        #filename=para['data_path']+'fig_%s_%s.png' %(para['mode'], results.values()[n].keys()[n])
        filename = 'fig_%s_%s.png' % (para['ac_mode'], results.values()[n].keys()[n])
        save_fig(filename)

    figsize = (5, 7)
    for p_rated in [270, 280, 290, 300]:
        para['p_rated'] = p_rated  # the amount of the power transfer from DC to AC
        para['ac_mode'] = 'LL'
        foldername = "C4_eff_1_LL_%sW" % (para['p_rated'])
        file_name = 'summary_%s_%.0fW' % (para['ac_mode'], para['p_rated'])
        para['data_path'] = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0803_Horent_Sat/C4_eff/%s/' %foldername

        ef3=ef.eff(file_name=file_name, para=para)
        ef3.plot_eff(limit=[(26, 46), (95.5, 97.5)], marker='o', figsize=figsize)


if __name__ == '__main__':
    main()




