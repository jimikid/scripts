
"""
@author: sbaek
  V00 06/01/2016
    - initial release
    - scripted for waveforms of .csv file
    - waveform_func.py converts the file in the following form(a key 't' : time x axis)
     t	    i_pri   	i_sec
0	        7.17E-15	1.43E-15
2.00E-08	0.745617959	0.149123592
4.00E-08	1.491114875	0.298222975

  V01 06/28/2016
    - convert_1st_key_t() to change a key of the first column to 't'
    - returns w in list
"""
import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))
sys.path.append('%s/analysis' % (dirname(dirname(__file__))))
print 'add path %s/analysis' % (dirname(dirname(__file__)))

import pandas as pd
import analysis.waveform_func as wf

def convert_1st_key_t(df):
    '''
    :param df: DataFrame
    :return: DataFrame
    '''
    # the first key(column) is changed to 't' to use waveform_func.py
    new_keys=['t']
    for i in range(1, len(df.keys())):
        print i, df.keys()[i]
        new_keys.append(df.keys()[i])
    df.columns=new_keys
    return df


def main(filepath, filename):
    '''
    :param filepath:str()
    :param filename:str()
    :return: []
    '''
    file=filepath + filename + '.csv'
    print ' read file %s' %file
    df = pd.read_csv(file)
    df=convert_1st_key_t(df)  #change the first key(column) to 't' which is compatible with waveform_func.py

    waves=wf.waveforms(filename=filename, filepath=filepath, df=df)

    waves.get_rms()
    waves.get_avg()
    waves.get_pkpk()
    zeros= waves.get_zero_crossing(waves.get_labels()[0])
    freq = waves.get_freq(waves.get_labels()[0], zeros)
    print ' %.1f kHz' %(freq/1000)

    print waves
    waves.plot_all()

    return waves


if __name__ == '__main__':
    filepath = "C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0701_T1_saturation/"

    # waveforms from Epics
    w=dict()
    filename = "Ls_87_Vdc_27_Vac_240_Pac_300_dt_10ns_fsw_117835.099Hz"  # .csv is excluded to avoid .csv when saved.
    w.update({filename:main(filepath, filename)})
    filename = "Ls_92_Vdc_27_Vac_240_Pac_300_dt_10ns_fsw_114028.872Hz"  # . csv is in wf.
    w.update({filename: main(filepath, filename)})
    filename = "Ls_98_Vdc_27_Vac_240_Pac_300_dt_10ns_fsw_109891.095Hz"  # .csv is excluded to avoid .csv when saved.
    w.update({filename: main(filepath, filename)})
    filename = "Ls_105_Vdc_27_Vac_240_Pac_300_dt_10ns_fsw_105563.831Hz"  # . csv is in wf.
    w.update({filename: main(filepath, filename)})


    # reports from Ansys
    names=['087u', '092u','098u', '105u']
    B_pkpk, B_rms, B_avg = dict(), dict(), dict()
    F_pkpk, F_rms, F_avg = dict(), dict(), dict()
    W_pkpk, W_rms, W_avg = dict(), dict(), dict()

    for i in names:
        filename = "Hornet_00157_"+i+"_Pri_in_B"  # . csv is in wf.
        print ' %s ' %filename
        wave = main(filepath, filename)
        B_pkpk.update({filename: wave.get_pkpk()})
        B_rms.update({filename: wave.get_rms()})
        B_avg.update({filename: wave.get_avg()})
        w.update({filename: wave})

        filename = "Hornet_00157_"+i+"_Pri_out_B"  # . csv is in wf.
        wave = main(filepath, filename)
        B_pkpk.update({filename: wave.get_pkpk()})
        B_rms.update({filename: wave.get_rms()})
        B_avg.update({filename: wave.get_avg()})
        w.update({filename: wave})

    df_pk = pd.DataFrame(B_pkpk, index=wave.get_labels())
    df_rms = pd.DataFrame(B_rms, index=wave.get_labels())
    df_avg = pd.DataFrame(B_avg, index=wave.get_labels())

    df_pk.to_csv(filepath+'B_pkpk.csv')
    df_rms.to_csv(filepath+'B_rms.csv')
    df_avg.to_csv(filepath+'B_avg.csv')


    for i in names:
        filename = "Hornet_00157_"+i + "_Pri_in_fluxlinkage"  # . csv is in wf.
        wave = main(filepath, filename)
        F_pkpk.update({filename: wave.get_pkpk()})
        F_rms.update({filename: wave.get_rms()})
        F_avg.update({filename: wave.get_avg()})
        w.update({filename: wave})

        filename = "Hornet_00157_"+ i + "_Pri_out_fluxlinkage"  # . csv is in wf.
        wave = main(filepath, filename)
        F_pkpk.update({filename: wave.get_pkpk()})
        F_rms.update({filename: wave.get_rms()})
        F_avg.update({filename: wave.get_avg()})
        w.update({filename: wave})

    df_pk = pd.DataFrame(F_pkpk, index=wave.get_labels())
    df_rms = pd.DataFrame(F_rms, index=wave.get_labels())
    df_avg = pd.DataFrame(F_avg, index=wave.get_labels())

    df_pk.to_csv(filepath+'F_pkpk.csv')
    df_rms.to_csv(filepath+'F_rms.csv')
    df_avg.to_csv(filepath+'F_avg.csv')


    for i in names:
        filename = "Hornet_00157_"+ i + "_Pri_in_winding"  # . csv is in wf.
        wave = main(filepath, filename)
        W_pkpk.update({filename: wave.get_pkpk()})
        W_rms.update({filename: wave.get_rms()})
        W_avg.update({filename: wave.get_avg()})
        w.update({filename: wave})

        filename = "Hornet_00157_"+i + "_Pri_out_winding"  # . csv is in wf.
        wave = main(filepath, filename)
        W_pkpk.update({filename: wave.get_pkpk()})
        W_rms.update({filename: wave.get_rms()})
        W_avg.update({filename: wave.get_avg()})
        w.update({filename: wave})

    df_pk = pd.DataFrame(W_pkpk, index=wave.get_labels())
    df_rms = pd.DataFrame(W_rms, index=wave.get_labels())
    df_avg = pd.DataFrame(W_avg, index=wave.get_labels())

    df_pk.to_csv(filepath+'W_pkpk.csv')
    df_rms.to_csv(filepath+'W_rms.csv')
    df_avg.to_csv(filepath+'W_avg.csv')


