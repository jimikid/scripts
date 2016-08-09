"""
Created on 07/06/2016, @author: sbaek
  V00
  - initial release

  V01 07/06/2016
  - move plot_eff() to figure_functions.py
  - para['Load_pts'], para['SAS_pts'] are given in list [] now.

  V02 07/27/2016
  - bootup process is moved to main script.  It needs to be there to change registers.

  V03 08/9/2016
  - 'code_update_heron_mode' is included in data_aq_lib.  Now plant firmware automatically from a specificed folder para['firmware_path']
  - if para['firmware_path'] is none, pass
  - def write_flash is added to change registers

"""

import sys, time
from os.path import abspath, dirname
import os
sys.path.append(dirname(dirname(__file__)))
sys.path.append('%s/data_aq_lib' % (dirname(dirname(__file__))))

import pandas as pd
from collections import OrderedDict
from data_aq_lib.equipment import equipment
import data_aq_lib.equipment.sas as sas
import data_aq_lib.equipment.ac_source as ac
import data_aq_lib.equipment.code_update_heron_mod as firm

import data_aq_lib.measurement.measurements as mm
import data_aq_lib.analysis.figure_functions as ff
from data_aq_lib.equipment import serialcom
import data_aq_lib.equipment.dvm as dvm

import data_aq_lib.analysis.eff_func as ef

def initialize():
    print ' initialize..\n'
    eq=equipment.Equip()
    list_equip=eq.get_equip()
    return list_equip

def firmware(para, eq):
    """ To load code into Heron board.
     - there should not be Vdc when starting.
     - there should be two files (procload and parameter table)
     - Board needs to be booted, serial cable attached, uses COM5.
     - Copy procload & parameter table files to a directory on local drive, and pass the
    directiry name on command line.
    """
    print ' set firmware..'
    dir = para['firmware_path']
    files = os.listdir(para['firmware_path'])
    pl_file, pt_file = None, None

    for name in files:
        if name.find("parm") != -1:pt_file = "%s/%s" %  (dir, name)
        if name.find("procload-") != -1: pl_file = "%s/%s" %  (dir, name)

    sas.sas_fixed(eq, CURR=14, VOLT=20)
    x = firm.PCUProgrammer()
    x.connect(comport=5)
    x.enter_flasher_mode()
    x.erase_procload_and_parm()

    para['log'] += pl_file+'\n'+pt_file+'\n'
    print ' pl_file : %s' %pl_file
    print ' pt_file : %s' %pt_file

    for bank in (0,1):
        x.program_file('pci%i'% bank,pl_file)
        x.program_file('ppi%i' % bank, pt_file)
    sas.sas_off(eq)
    time.sleep(20)

def write_flash(cmd, delay=0):
    '''
       - to change values on registers
       - need to boot up by setting a DC voltage
    :param cmd: a pair with write and read e.g. ('wl f60A 00\r', 'rl f60A 1\r')
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
    para['log'] += '\n'
    for i in range(para.__len__()):
        if para.keys()[i] is not 'log': # to avoid duplication, i is Int
            para['log'] += ' '+para.keys()[i]+': '+str(para.values()[i])+'\n'
    para['log'] +="\n\n save and close at"+time.strftime(" %m/%d/%Y %I:%M \n")
    text_file = open(para['data_path']+"/log.txt", "w")
    text_file.write(para['log'])
    text_file.close()

def measurements(para, eq, delay=4, cmd=None, adj=False):
    data=[]
    fault = True

    ''' wait til reach to temperature set '''
    if para['set_temp'] is not None:
        print ' set temperature : %s' %para['set_temp']
        temp=None
        while not (temp < (para['set_temp'] +1.0) and temp > (para['set_temp'] -1.0)):
            time.sleep(30)
            temp=dvm.measure_tempc(eq)


    for pts in para['SAS_pts']:
        ''' boot up '''
        if fault :  #only first time and when fault occurs,
            ac.set_ac_source(eq, mode=para['ac_mode'], freq=60.0)
            sas.sas_pcu_boot(eq, para, CURR=18, VOLT=30, boot_up=1.0)
            if cmd is not None:
                for i in cmd:
                    write_flash(cmd=i, delay=1) # need around 20sec to boot up
                    para['log'] += ' %s %s\n'%i # i is always in a pair with write and read


        para['SAS_volt']=pts
        m1=mm.Measurement(para, eq)
        fault= m1.flag
        print m1
        m1.do_measure_pm(delay=delay, adj=adj, show=True, boot_up=1.0)
        data=data+m1.results
        time.sleep(4)
        results=pd.DataFrame(data) # update often, no harm, so that reduce a chance to lose data
    return results, m1


def main(foldername, P_rated, mode, Mnt=True, Firm=False, Plt=True, cmd=None, Load_pts=None, SAS_pts=None, adj=False):
    ''' set parameters'''
    exe, para, eq = OrderedDict(), OrderedDict(), OrderedDict()
    results, m1= None, None
    para['log']= "\n\n start at"+time.strftime(" %m/%d/%Y %I:%M \n\n")

    ####################################################################################################################
    para['Description'] = "\n\n check operating range and eff with Lr 110uH (Pri in) and temperature \n\n"
    para['ac_mode'], para['p_rated']=mode, P_rated   #'LN' : (120.0 ,120.0 ,120.0), 'LL':(120.0 120.0), 'LL_HVRT' :'LL':(132.0 132.0)
    para['model'], para['SN'], para['pcb']='Hornet_P3', '121629026786', '800-00504 05'
    para['firmware_path']='C:/Users/sbaek/WorkSpace/firmware/P3_110uH_wide' #default None
    para['Load_pts'] =  [i*0.01 for i in range(50,70,10)]+[i*0.01 for i in range(70,90,5)]+[i*0.01 for i in range(90,107,2)]
    para['SAS_pts'] =   [i*0.1 for i in range(450,350,-40)]+[i*0.1 for i in range(350,260,-20)]
    para['set_temp'] = None #default : None, measure temperature before boot up and start at the set_temp
    ####################################################################################################################

    exe['measurement']=Mnt #'On'
    para['data_file_name'] ='data'
    para['folder_name']=foldername+para['SN']+'_%s_%sW' %(para['ac_mode'], para['p_rated'])
    para['data_path']= ff.create_path_dir(name=para['folder_name'], path = dirname(dirname(__file__))+'/data')
    para['cmd']= cmd
    file_name='summary_%s_%.0fW' %(para['ac_mode'], para['p_rated'])
    if Load_pts is not None:
        para['Load_pts'] =Load_pts
    if SAS_pts is not None:
        para['SAS_pts'] = SAS_pts

    eq=initialize()
    ''' firmwares'''
    if (Firm) and (para['firmware_path'] is not None): # to plant firmware, pcu should start without Vdc!
        firmware(para, eq)
    else:pass

    ''' measurements '''
    if Mnt:
        results, m1=measurements(para, eq, delay=3, cmd=cmd, adj=adj)
        results=results.set_index([range(len(results))])
        print '\n save data to %s' %(para['data_path']+'/'+file_name+'.csv')
        results.to_csv(para['data_path']+'/'+file_name+'.csv')
        save_log(exe, para)
    else: pass

    ''' plots '''
    if Plt:
        try:
            ef1=ef.eff(file_name=file_name, para=para)
            ef1.plot_map()
            ef1.plot_eff(xlim=(26, 46), ylim=(95.0, 97.5))
        except:pass
    else: pass

    return m1


if __name__ == '__main__':
    temp='25'

    mode='LL'
    for i in range(1, 4):
        m1=main(foldername='%sC_%s_' %(temp,i), P_rated=300, mode=mode, Firm=True)
    for i in range(1, 4):
        m1=main(foldername='%sC_%s_' %(temp,i), P_rated=290, mode=mode, Load_pts=[0.5, 0.75, 1.0], SAS_pts=[27.0, 36.0, 45.0], adj=True)

    mode='LL_HVRT'
    for i in range(1, 4):
        m1=main(foldername='%sC_%s_' %(temp,i), P_rated=300, mode=mode)
    for i in range(1, 4):
        m1=main(foldername='%sC_%s_' %(temp,i), P_rated=290, mode=mode, Load_pts=[0.5, 0.75, 1.0], SAS_pts=[27.0, 36.0, 45.0], adj=True)

    mode='LN'
    for i in range(1, 4):
        m1=main(foldername='%sC_%s_' %(temp,i), Mnt=False, P_rated=300, mode=mode)
    for i in range(1, 4):
        m1=main(foldername='%sC_%s_' %(temp,i), Mnt=False, P_rated=290, mode=mode, Load_pts=[0.5, 0.75, 1.0], SAS_pts=[27.0, 36.0, 45.0], adj=True)

    m1.shutdown()
