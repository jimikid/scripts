"""
Created on 07/06/2016, @author: sbaek
  V00
  - initial release

  V01 07/06/2016
  - move plot_eff() to figure_functions.py
  - para['Load_pts'], para['SAS_pts'] are given in list [] now. 
"""

import sys, time
from os.path import abspath, dirname

import sys, time
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append('%s/data_aq_lib' % (dirname(dirname(__file__))))

import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from data_aq_lib.equipment import equipment
import data_aq_lib.measurement.measurements as mm
import data_aq_lib.analysis.figure_functions as ff


def initialize():
    print 'initialize..\n'
    eq=equipment.Equip()
    list_equip=eq.get_equip()
    return list_equip
                    
def save_log(exe, para):
    for i in range(exe.__len__()):     
        para['log'] += ' '+exe.keys()[i]+': '+str(exe.values()[i])+'\n'   
    for i in range(para.__len__()):   
        para['log'] += ' '+para.keys()[i]+': '+str(para.values()[i])+'\n'
    para['log']=para['log'].split('SAS_volt:')[0]  #SAS_volt keeps changing..
    para['log'] +="\n\n save and close at"+time.strftime(" %m/%d/%Y %I:%M \n")  
    text_file = open(para['data_path']+"/log.txt", "w")
    text_file.write(para['log'])
    text_file.close()    

def measurements(para, eq, delay=4):
    data=[]
    for i in para['SAS_pts']:
        '''SAS '''         
        para['SAS_volt']=i
        m1=mm.Measurement(para, eq)
        print m1            
        
        m1.do_measure_pm(delay=delay, adj=False)
        data=data+m1.results
        m1.shutdown()   
        time.sleep(2)
    results=pd.DataFrame(data)  
    #m1.shutdown()             
    return results
 

def main(name='name', P_rated=280, mode='LL',Mnt='On'):
    exe, para, eq = OrderedDict(), OrderedDict(), OrderedDict()
    para['model'], para['SN'], para['pcb']='Hornet', name, '800-00521 0601 1397'
    para['log'] ="\n\n Start at"+time.strftime(" %m/%d/%Y %I:%M \n\n")    
    para['log'] ="\n Description : 121610019482 800-00504 P2T \n Lr=110uH (0.95mm), Sec winding is in outer window \n"    

    exe['measurement']=Mnt #'On'        
    para['data_file_name'] ='data'
    para['ac_mode']=mode   #'LN' : (120.0 ,120.0 ,120.0), 'LL':(120.0 120.0) 

    para['p_rated'] = P_rated
    para['folder_name']=para['SN']+'_%s_%sW' %(para['ac_mode'], para['p_rated'])
    para['data_path']= ff.create_path_dir(name=para['folder_name'], path = dirname(dirname(__file__))+'/data') 
    para['source_path']=dirname(dirname(__file__))+'/source_files'       
    para['results'] = pd.DataFrame([])  
    file_name='summary_%s_%.0fW' %(para['ac_mode'], para['p_rated'])    
    eq=initialize()    

    #para['Load_pts'] =  [i*0.01 for i in range(94,102,2)]+[i*0.01 for i in range(102,125,1)]
    #para['SAS_pts'] =   [i*0.1 for i in range(300,255,-10)]
    para['Load_pts'] =  [i*0.01 for i in range(84,94,2)]+[i*0.01 for i in range(94,126,1)]
    para['SAS_pts'] =   [i*0.1 for i in range(260,305,10)]


    results=measurements(para, eq, delay=3)
    results=results.set_index([range(len(results))])
    print '%s save data to ' %(para['data_path']+'/'+file_name+'.csv')
    results.to_csv(para['data_path']+'/'+file_name+'.csv')    
    eq['SERIAL'].close()
    save_log(exe, para)    
    
    try:
        ff.plot_eff(para, file_name)        
    except:pass
    
    return eq, para
           
if __name__ == '__main__':
    for i in range(1, 6):
        eq, para=main(name='Hornet_110uH_%s' %i, P_rated=300, mode='LL')
    
   
        
        
  