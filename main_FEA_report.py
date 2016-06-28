"""
@author: sbaek
  V00 06/28/2016
    - initial release
    - finds all reports by itself and export .csv files.
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
    print ' ProjectName : %s, DesignName : %s' % (init['ProjectName'], init['DesignName'])
    if init['Open'] == 'On':
        oDesktop.RestoreWindow()
        print init['save_name'] + '.aedt'
        oDesktop.OpenProject(init['save_name'] + '.aedt')
        oProject = oDesktop.SetActiveProject(init['ProjectName'])
        oDesign = oProject.SetActiveDesign(init['DesignName'])
    else:
        oDesktop.RestoreWindow()
        oProject = oDesktop.SetActiveProject(init['ProjectName'])
        oDesign = oProject.SetActiveDesign(init['DesignName'])
    return oProject, oDesign


def main():
    init['save_name' ] =init['save_path' ] +init['ProjectName']

    ''' Initiation, solution type'''
    oProject, oDesign= initiation()

    ''' export plot'''
    oModule = oDesign.GetModule("ReportSetup")  # have all names of reports
    names = oModule.GetAllREportNames()
    for i in names:
        print ' export reports %s' % i
        oModule.ExportToFile(i, init['save_path'] + init['ProjectName'] + '_' + init['DesignName'] + '_' + i + ".csv")

    ''' save'''
    oProject.SaveAs(init['save_name'] + '.aedt', True)
    # oProject.Save()
    if init['Close'] == 'On':
        print '\n Close at %s ' % time.strftime("%d/%m/%Y %I:%M")
        oProject.close()


if __name__ == '__main__':
    names = [["Hornet_00157", "087u_Pri_in"], ["Hornet_00157", "087u_Pri_out"],
             ["Hornet_00157", "092u_Pri_in"], ["Hornet_00157", "092u_Pri_out"],
             ["Hornet_00157", "098u_Pri_in"], ["Hornet_00157", "098u_Pri_out"],
             ["Hornet_00157", "105u_Pri_in"], ["Hornet_00157", "105u_Pri_out"]]

    for name in names:
        init['ProjectName'], init['DesignName'] = name[0], name[1]
        init['Open'], init['Close'] = 'Off', 'Off'
        init['save_path'] = "C:/Users/sbaek/Documents/Ansoft/"
        print '\n Start at %s ' % time.strftime("%d/%m/%Y %I:%M")
        main()





