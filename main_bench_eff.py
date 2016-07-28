"""
Created on 07/06/2016, @author: sbaek
  V00
  - initial release

  V01 07/06/2016
  - move plot_eff() to figure_functions.py
  - para['Load_pts'], para['SAS_pts'] are given in list [] now.

  V02 07/27/2016
  - bootup process is moved to main script.  It needs to be there to change registers.

"""

import sys, time
from os.path import abspath, dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append('%s/data_aq_lib' % (dirname(dirname(__file__))))

import pandas as pd
from collections import OrderedDict
from data_aq_lib.equipment import equipment
import data_aq_lib.equipment.sas as sas
import data_aq_lib.equipment.ac_source as ac

import data_aq_lib.measurement.measurements as mm
import data_aq_lib.analysis.figure_functions as ff
from data_aq_lib.equipment import serialcom


def initialize():
    print 'initialize..\n'
    eq=equipment.Equip()
    list_equip=eq.get_equip()
    return list_equip

def write_flash(cmd, delay=0):
    '''
       - to change values on registers
       - need to boot up by setting a DC voltage
    :param cmd: a pair with write and read e.g. ('wl f60A 00\r', 'rl f60A 1\r')
    :param delay:
    :return:
    '''
    time.sleep(delay)
    try:
        ser=serialcom.SerialCom()
        ser.write(cmd='%s' %cmd[0])
        ser.write(cmd='%s' %cmd[1])
        id=cmd[1].split(' ')[1] #cmd[1].split(' ')[1] is the address of the register
        #print id
        ser.read_F(id=id)
        ser.close()
    except:pass

def save_log(exe, para):
    #for i in range(exe.__len__()):
    #    para['log'] += ' '+exe.keys()[i]+': '+str(exe.values()[i])+'\n'
    for i in range(para.__len__()):
        if para.keys()[i] is not 'log': # to avoid duplication, i is Int
            para['log'] += ' '+para.keys()[i]+': '+str(para.values()[i])+'\n'
    para['log'] +="\n\n save and close at"+time.strftime(" %m/%d/%Y %I:%M \n")  
    text_file = open(para['data_path']+"/log.txt", "w")
    text_file.write(para['log'])
    text_file.close()    

def measurements(para, eq, delay=4, cmd=None):
    data=[]
    fault = True
    for pts in para['SAS_pts']:
        ''' boot up '''
        if fault :  #only first time and when fault occurs,
            ac.set_ac_source(eq, mode=para['ac_mode'], freq=60.0)
            sas.sas_pcu_boot(eq, para, CURR=14, VOLT=36, boot_up=1.0)
            if cmd is not None:
                for i in cmd:
                    write_flash(cmd=i, delay=1) # need around 20sec to boot up
                    para['log'] += ' %s %s\n'%i # i is always in a pair with write and read

        '''SAS '''
        para['SAS_volt']=pts
        sas.sas_fixed_adj(eq, CURR=14, VOLT=para['SAS_volt'])

        m1=mm.Measurement(para, eq)
        fault= m1.flag
        print m1
        m1.do_measure_pm(delay=delay, adj=False, show=True, boot_up=1.0)
        data=data+m1.results
        time.sleep(4)
        results=pd.DataFrame(data) # update often, no harm, so that reduce a chance to lose data
    return results, m1


def main(name='name', P_rated=280, mode='LL',Mnt='On', cmd=None):
    '''
    :param name:
    :param P_rated:
    :param mode:
    :param Mnt:
    :param cmd:
    :return:
    '''
    ''' set parameters'''
    exe, para, eq = OrderedDict(), OrderedDict(), OrderedDict()
    para['model'], para['SN'], para['pcb']='Hornet_P3', name, '800-00504 05'
    para['log'] ="\n\n start at"+time.strftime(" %m/%d/%Y %I:%M \n\n")
    para['log'] +="\n Description : \n 121629026777  \n check operating range with 110uH, parm-NA-hornet1-S290-72-p540-00118-r01-v01.04.60.tch \n\n"

    exe['measurement']=Mnt #'On'        
    para['data_file_name'] ='data'
    para['ac_mode'], para['p_rated']=mode, P_rated   #'LN' : (120.0 ,120.0 ,120.0), 'LL':(120.0 120.0)
    para['folder_name']=para['SN']+'_%s_%sW' %(para['ac_mode'], para['p_rated'])
    para['data_path']= ff.create_path_dir(name=para['folder_name'], path = dirname(dirname(__file__))+'/data') 
    para['source_path']=dirname(dirname(__file__))+'/source_files'
    para['cmd']= cmd
    file_name='summary_%s_%.0fW' %(para['ac_mode'], para['p_rated'])

    para['Load_pts'] =  [i*0.01 for i in range(50,70,10)]+[i*0.01 for i in range(70,90,5)]+[i*0.01 for i in range(90,103,2)]
    para['SAS_pts'] =   [i*0.1 for i in range(450,350,-40)]+[i*0.1 for i in range(350,260,-20)]

    ''' do measurements'''
    eq=initialize()
    results, m1=measurements(para, eq, delay=3, cmd=cmd)
    results=results.set_index([range(len(results))])


    print '\n save data to %s' %(para['data_path']+'/'+file_name+'.csv')
    results.to_csv(para['data_path']+'/'+file_name+'.csv')
    save_log(exe, para)    
    
    try:
        ff.plot_eff(para, file_name)        
    except:pass
    return eq, para, m1


if __name__ == '__main__':
    cmd=(('wl F60A 00\r', 'rl F60A 1\r'), ('wl F612 11\r', 'rl F612 1\r'))  #F has to be capital F, string read from serial starts with a capital letter.
    for i in range(1, 3):
        eq, para, m1=main(name='f60A00_f61211_%s' %i, P_rated=300, mode='LL', cmd=cmd)

    cmd=(('wl F60A 01\r', 'rl F60A 1\r'), ('wl F612 10\r', 'rl F612 1\r'))
    for i in range(1, 3):
        eq, para, m1=main(name='f60A01_f61210_%s' %i, P_rated=300, mode='LL', cmd=cmd)

    cmd=(('wl f60A 00\r', 'rl F60A 1\r'), ('wl F612 10\r', 'rl f612 1\r'))
    for i in range(1, 3):
        eq, para, m1=main(name='f60A00_f61210_%s' %i, P_rated=300, mode='LL', cmd=cmd)

    cmd=(('wl f60A 01\r', 'rl F60A 1\r'), ('wl F612 11\r', 'rl f612 1\r'))
    for i in range(1, 3):
        eq, para, m1=main(name='f60A01_f61211_%s' %i, P_rated=300, mode='LL', cmd=cmd)

    m1.shutdown()

  