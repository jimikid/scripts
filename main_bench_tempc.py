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
    log +="\n\n save and close at"+time.strftime(" %m/%d/%Y %I:%M \n")  
    text_file = open(para['data_path']+"/log_%sV.txt" %para['SAS_volt'], "w")
    text_file.write(log)
    text_file.close()    

def main(name='name', P_rated=280, SAS_volt=32, mode='LL'):
    exe, para, eq = OrderedDict(), OrderedDict(), OrderedDict()
    para['model'], para['SN'], para['pcb']='Hornet', name, '800-00521 0601 1397'
    log ="\n\n Start at"+time.strftime(" %m/%d/%Y %I:%M \n\n")    
    log +="\n Description : Hornet P2T, temperature measurements at 280W with Lr 82uH\n"    

    para['data_file_name'] ='data'  
    para['ac_mode']=mode   #'LN' : (120.0 ,120.0 ,120.0), 'LL':(120.0 120.0) 

    para['p_rated'] = P_rated
    para['folder_name']=para['SN']+'_%s_%sW' %(para['ac_mode'], para['p_rated'])
    para['data_path']= ff.create_path_dir(name=para['folder_name'], path = dirname(dirname(__file__))+'/data') 
    para['source_path']=dirname(dirname(__file__))+'/source_files'           
    para['SAS_volt'] =  SAS_volt
    para['Load_pts'] =  [1.0]    
    para['results'] = pd.DataFrame([])
    file_name='summary_%s_%.0fW_%sV' %(para['ac_mode'], para['p_rated'], para['SAS_volt'] )        
    
    eq=initialize()               
    m1=mm.Measurement(para, eq)
    print m1            
    
    m1.do_measure_tempc(time_step=2, duration=40, SAT='On')    #in minute 
    results=pd.DataFrame(m1.results)                                #m1.results is list with elements in dict, [{ : },{ : }...]
  
    para['results']=results.set_index([range(len(results))])
    para['results'].to_csv(para['data_path']+'/'+file_name+'.csv')
    eq['SERIAL'].close()
    m1.shutdown()             
    save_log(exe, para, log)    
    
           
if __name__ == '__main__':
    Vdc=[28, 36, 44]
    for i in Vdc:        
        main(name='121610019482_82u_tempc' , P_rated=280, SAS_volt=i, mode='LL')
        print ' cool down..\n'
        time.sleep(60*60)   #cool down 40 min 
    

    
        
  