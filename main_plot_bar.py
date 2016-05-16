
"""
Created on 05/16/2016, @author: sbaek
  V00
    - initial release
    
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
import pandas as pd

para, init = OrderedDict(), OrderedDict()
para, init = OrderedDict(), OrderedDict()

def main(filename, it):
    print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")    
    save_path="C:/Users/sbaek/Documents/Ansoft/"    
    df=pd.read_csv(save_path+filename+'.csv')
    
    
    plt.figure(it)
    labels=[]
    values=[]
    for i in range(1, len(df.loc[0])-1):
        labels.append(df.loc[0].index[i].split('_loss')[0])
        values.append(df.loc[0][i])
        
    objects = labels
    y_pos = np.arange(len(objects))
    performance = values
     
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.show()   
            
    labels=[]
    values=[]
    for i in range(1, len(df.loc[1])-1):
        labels.append(df.loc[1].index[i].split('_loss')[0])
        values.append(df.loc[1][i])
        
    
    objects = labels
    y_pos = np.arange(len(objects))
    performance = values
     
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    xticks=[i*0.0005 for i in range(6)]  #xlimit can be set by ticks.
    plt.xticks(xticks)
    plt.yticks(y_pos, objects)
    plt.xlabel('Rac[Ohm]')
    plt.title(filename )
    plt.show()   
            
          
if __name__ == '__main__':
    filename="pcb_v01_Q14"
    main(filename, 1)
   
    filename="pcb_v01_Q23"
    main(filename, 2)
    
    filename="pcb_v02_Q14"
    main(filename, 3)
       
    filename="pcb_v02_Q23"
    main(filename, 4)
    
        
  
