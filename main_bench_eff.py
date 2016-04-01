"""
Created on 02/05/2016, @author: sbaek
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

def measurements(para, eq):
    data=[]
    for SAS_volt in range(para['SAS_volt_min'], para['SAS_volt_max'], para['SAS_volt_step']):  # DC voltage sweep
        '''SAS '''         
        para['SAS_volt']=SAS_volt
        m1=mm.Measurement(para, eq)
        print m1            
        
        m1.do_measure()   
        data=data+m1.results
    results=pd.DataFrame(data)        
    return results
   
def plot(para, file_name):    
    df=pd.read_csv(para['data_path']+'/'+file_name+'.csv')          
    data1=ff.sort(df, index=[j  for j in range(len(para['Load_pts']))])    
    Load, data = [], []    
    for key in data1.keys():
        Load.append(key)
        data.append(data1[key])

    fig = plt.figure(1)   
    ax1 = fig.add_subplot(111)    
    markersize=6
    plots, labels=[], []    
    for key in data1.keys():
        l1,=ax1.plot(data1[key].volt_in, data1[key].eff, '-x', markersize=markersize)
        plots.append(l1)
        labels.append('Unit Eff. load %s%%' %key)
     
    ax1.legend(plots, labels)    
    ax1.set_xlim(26, 46)  
    ax1.set_ylim(94.0, 97.0)       
    ax1.set_xlabel('Vdc[V]')    
    ax1.set_ylabel('Eff.[%]')
    ax1.grid()     
    plt.title('P_rated= %sW, %s' %(para['p_rated'], para['ac_mode']))  
    name=para['data_path']+'/fig_%s_%.0fW_%s.png' %(para['ac_mode'], para['p_rated'], file_name)
    plt.savefig(name)
    plt.close()

def main(name='name', P_rated=280, mode='LL', Tb='On', Mnt='On'):      
    exe, para, eq = OrderedDict(), OrderedDict(), OrderedDict()
    para['model'], para['SN'], para['pcb']='Hornet', name, '800-00521 0601 1397'
    log ="\n\n Start at"+time.strftime(" %m/%d/%Y %I:%M \n\n")    
    log ="\n Description : litz wire, comparison between 150/44 and 250??/44 \n"    
    
    exe['table']=Tb #'On'
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
    ac.set_ac_source(eq, mode=mode, freq=60.0)
    
    if exe['table']=='On':
        table_gen1=tg.table_gen(para, eq)
        table_gen1.generate(SAS_volt=30, show='On', max_power=290)
        
    if exe['measurement']=='On':
        para['Load_pts'] =  [0.5,0.75, 1.0]           #para['p_rated'], para['Load_pts'] = P_rated, [0.5+i*0.05 for i in range(11)]
        para['SAS_volt_min'], para['SAS_volt_max'], para['SAS_volt_step']= 27,46,3
        #para['Load_pts']=[round(i*0.01, 2) for i in range(50,100+1,10)]    # choose load condition as reference 1 at full-load, para['p_rated']  

        results=measurements(para, eq)
        results=results.set_index([range(len(results))])
        results.to_csv(para['data_path']+'/'+file_name+'.csv')
        
    eq['SERIAL'].close()
  
    try:
            plot(para, file_name)
            save_log(exe, para, log)    
    except:pass     
    return eq, para
           
if __name__ == '__main__':
    for i in range(2):
        eq, para=main(name='12160500032_110u_17544_%s' %i, P_rated=280, mode='LL', Tb='Off', Mnt='On')
    
        
  