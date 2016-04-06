"""
Created on 04/05/2016, @author: sbaek
  V00
    - initial release
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
import data_aq_lib.measurement.table_generator as tg
import data_aq_lib.analysis.figure_functions as ff

import data_aq_lib.equipment.sas as sas
import data_aq_lib.equipment.ac_source as ac


def initialize():
    print 'initialize..\n'
    eq=equipment.Equip()
    list_equip=eq.get_equip()
    return list_equip
                    
def save_log(exe, para, log):
    for i in range(exe.__len__()):     
        log += ' '+exe.keys()[i]+': '+str(exe.values()[i])+'\n'   
    for i in range(para.__len__()):   
        log += ' '+para.keys()[i]+': '+str(para.values()[i])+'\n'
    log=log.split('SAS_volt:')[0]  #SAS_volt keeps changing..
    log +="\n\n save and close at"+time.strftime(" %m/%d/%Y %I:%M \n")  
    text_file = open(para['data_path']+"/log.txt", "w")
    text_file.write(log)
    text_file.close()    


def main(name='name', P_rated=280, Vdc=32, mode='LL'):
    exe, para, eq = OrderedDict(), OrderedDict(), OrderedDict()
    para['model'], para['SN'], para['pcb']='Hornet', name, '800-00521 0601 1397'
    log ="\n\n Start at"+time.strftime(" %m/%d/%Y %I:%M \n\n")    
    log ="\n Description : \n"    

    para['data_file_name'] ='data'
    para['ac_mode']=mode   #'LN' : (120.0 ,120.0 ,120.0), 'LL':(120.0 120.0) 

    para['p_rated'] = P_rated
    para['folder_name']=para['SN']+'_%s_%sW' %(para['ac_mode'], para['p_rated'])
    para['data_path']= ff.create_path_dir(name=para['folder_name'], path = dirname(dirname(__file__))+'/data') 
    para['source_path']=dirname(dirname(__file__))+'/source_files'       
    para['results'] = pd.DataFrame([])
    para['Load_pts'] =  [1.0]

    file_name='summary_%s_%.0fW' %(para['ac_mode'], para['p_rated'])        
    
    eq=initialize()
    ac.set_ac_source(eq, mode=mode, freq=60.0)
    sas.pcu_boot(eq, CURR=14, VOLT=Vdc, ADJ='On')

    para['Load_pts'] =  [1.0]         
    data=[]
    m1=mm.Measurement(para, eq)
    print m1            
    
    m1.do_measure_tempc(time_step=1, duration=10) #in minute
    data=data+m1.results
    results=pd.DataFrame(data)    
    
    results=results.set_index([range(len(results))])
    results.to_csv(para['data_path']+'/'+file_name+'.csv')
    eq['SERIAL'].close()

           
if __name__ == '__main__':
    main(name='test' , P_rated=280, Vdc=32, mode='LL')
    
        
  