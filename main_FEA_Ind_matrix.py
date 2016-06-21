"""
    V00 : 06/20/2016
    - initial release
    - init['solver'] has to be set either "Magnetostatic" , "EddyCurrent"
    - init['currents'] init['turns']  has to be given, which is set in Ansys parameters
"""

import win32com.client
import sys
from os.path import abspath, dirname, exists
from collections import OrderedDict
import time
para, init = OrderedDict(), OrderedDict()

def initiation():
    oAnsoftApp = win32com.client.Dispatch("Ansoft.ElectronicsDesktop")
    oDesktop = oAnsoftApp.GetAppDesktop()
    print ' ProjectName : %s, DesignName : %s' %(init['ProjectName'], init['DesignName'])
    if init['Open'] =='On':
        oDesktop.RestoreWindow()
        print init['save_name']+'.aedt'
        oDesktop.OpenProject(init['save_name']+'.aedt')
        oProject = oDesktop.SetActiveProject(init['ProjectName'])
        oDesign = oProject.SetActiveDesign(init['DesignName'])
    else:
        oDesktop.RestoreWindow()
        oProject = oDesktop.SetActiveProject(init['ProjectName'])
        oDesign = oProject.SetActiveDesign(init['DesignName'])
    return oProject, oDesign


def inductances(oDesign, currents=['Current1','Current2'], turns=['turn1','turn2']):
    oModule = oDesign.GetModule("OutputVariable")
    L11="Matrix1.L("+currents[0]+","+currents[0]+")"
    L22="Matrix1.L("+currents[1]+","+currents[1]+")"
    L12="Matrix1.L("+currents[0]+","+currents[1]+")"

    oModule = oDesign.GetModule("OutputVariable")
    oModule.CreateOutputVariable("L1",
                                 L11+"*"+turns[0]+"^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("L2",
                                 L22+"*"+turns[1]+"^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Lm_to_1",
                                 L12+"*"+turns[0]+"^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Lm_to_2",
                                 L12 + "*" + turns[1] + "^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Lleak1_to_1",
                                 "(" + L11 + "-" + L12 + ")" + "*" + turns[0] + "^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Lleak2_to_1",
                                 "(" + L22 + "-" + L12 + ")" + "*" + turns[0] + "^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Lleak1_to_2",
                                 "(" + L11 + "-" + L12 + ")" + "*" + turns[1] + "^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Lleak2_to_2",
                                 "(" + L22 + "-" + L12 + ")" + "*" + turns[1] + "^2",
                                 "Setup1 : LastAdaptive", init['solver'], [])

    oModule.CreateOutputVariable("Ls_to_1", "Lleak1_to_1+Lleak2_to_1",
    							 "Setup1 : LastAdaptive", init['solver'], [])
    oModule.CreateOutputVariable("Ls_to_2", "Lleak1_to_2+Lleak2_to_2",
    							 "Setup1 : LastAdaptive", init['solver'], [])


def main():
    print '\n Start at %s ' % time.strftime("%d/%m/%Y %I:%M")

    init['save_name']=init['save_path']+init['ProjectName']
    ''' Initiation, solution type'''
    oProject, oDesign=initiation()

    inductances(oDesign, currents=init['currents'], turns=init['turns'])


if __name__ == '__main__':
    names = [["422_00148_flux", "Ind_Eddy"]]

    for name in names:
        init['ProjectName'], init['DesignName'] = name[0], name[1]
        init['solver']= "EddyCurrent"   #"Magnetostatic" , "EddyCurrent"
        init['Open'], init['Close'] = 'Off', 'Off'
        init['save_path']="C:/Users/sbaek/Documents/Ansoft/"

        init['currents'] = ['Current_In', 'Current_Out']
        init['turns'] = ['turn_in', 'turn_out']



        main()


