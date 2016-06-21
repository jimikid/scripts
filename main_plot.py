
"""
@author: sbaek
  V00 06/01/2016
    - initial release

"""
import sys, time
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append('%s/analysis' % (dirname(dirname(__file__))))
print 'add path %s/analysis' % (dirname(dirname(__file__)))
from collections import OrderedDict

from math import *
import pandas as pd
import matplotlib.pyplot as plt
import analysis.figure_functions as ff
import pandas as pd
para, init = OrderedDict(), OrderedDict()

def main():
    filename = "data_270W_27V_100_DC2AC"
    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")    
    save_path="C:/Users/sbaek/WorkSpace/2016_Hornet/data/New folder/"    
    try:
        df=pd.read_csv(save_path+filename+'.csv')
    except:
        print ' check if your file exists in the folder'

    ff.plot_bar(df, xticks=[0,100000,200000], title=filename)


    ff.plot(
        data=[(df['phase'], df['I_hv_rms']*5),
              (df['phase'], df['freq'] / 1000)],
        label=[('phase','I_hv [Arms]'),
               ('phase','freq[kHz]')],
        limit=[((0,90),(0,50)),
               ((0,90),(0,400))],
        title=filename,
        fig_num=10
    )


if __name__ == '__main__':
    main()