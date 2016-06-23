"""
@author: sbaek
  V00 06/21/2016
    - initial release
    - standalone script for transient solver
    - surfaces have to be set in Ansys with a specific name convention. such as all sheets have 'path'
    - finds all sheets by itself.
    - report is B flux on sheets with time
    - volume and surface calculation for calculator is included.
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


def reset_cal(oDesign):
    try:
        oModule = oDesign.GetModule("FieldsReporter")
        oModule.CalcStack("clear")
        oModule.ClearAllNamedExpr()
        print '\n Delete expressions in a calculator'
    except:
        pass


def B_normal(oDesign, Sheet):
    oModule = oDesign.GetModule("FieldsReporter")
    name_B=Sheet+'_Bl_Int'
    oModule.EnterQty("B")
    oModule.EnterSurf(Sheet)
    oModule.CalcOp("NormalComponent")
    oModule.CalcOp("Integrate")
    oModule.AddNamedExpression(name_B, "Fields")  #add '_Bl_Int' : integration of B normal

    name_suf=surface(oDesign, Sheet)

    oModule.CopyNamedExprToStack(name_B)
    oModule.CopyNamedExprToStack(name_suf)
    oModule.CalcOp("/")
    name=Sheet+'_B'
    oModule.AddNamedExpression(name, "Fields")
    return name


def volume(oDesign, Solid):
    '''
    Solid : list of the names in Maxwell in string format
    name_list : list of the names in calculator in Maxwell
    '''
    oModule = oDesign.GetModule("FieldsReporter")
    name=Solid+'_vol'
    oModule.EnterScalar(1)
    oModule.EnterVol(Solid)
    oModule.CalcOp("Integrate")    
    oModule.AddNamedExpression(name, "Fields")    
    return name


def surface(oDesign, Sheet):
    '''
    Sheet : list of the names in Maxwell in string format
    name_list : list of the names in calculator in Maxwell
    '''
    oModule = oDesign.GetModule("FieldsReporter")
    name = Sheet + '_Ac'
    oModule.EnterScalar(1)
    oModule.EnterScalar(1)
    oModule.EnterSurf(Sheet)
    oModule.CalcOp("Integrate")
    oModule.AddNamedExpression(name, "Fields")
    return name

def report_t(oDesign, item, name="XY Plot 1", form="Rectangular Plot"):  #form :"Rectangular Plot", "Data Table"
    '''
    - report for transient solver with time
    :return: None
    '''

    print '\n %s ' %time.strftime("%d/%m/%Y %I:%M")
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(name, "Fields", form, "Setup1 : Transient",
                         [
                             "Domain:="	, "Sweep"
                         ],
                         [
                             "Time:="		, ["All"],
                         ],
                         [
                             "X Component:="		, "Time",
                             #"Y Component:="		, ["path_02_B" ,"path_04_B" ,"path_01_B" ,"path_03_B" ,"path_06_B" ,"path_05_B"]
                             "Y Component:="	, item
                         ], [])
    oModule.AddTraceCharacteristics(name, "pk2pk", [], ["Full"])
  

def main():      
    init['save_name']=init['save_path']+init['ProjectName']

    ''' Initiation, solution type'''
    oProject, oDesign=initiation()

    ''' Build lists of objects '''
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    SolidList = oEditor.GetObjectsByMaterial('copper')  # SolidList is in list
    # oEditor.GetObjectsInGroup('solids')
    SheetList = oEditor.GetObjectsInGroup('sheets')

    init['Solid'] = ['AllObjects']
    init['Sheet'] = []
    init['Solid_plot'] = []
    init['Sheet_plot'] = []

    init['Solid_vias'] = []
    init['Solid_del'] = []

    if SolidList:
        for i in SolidList:
            init['Solid'].append(i)
    else:
        pass

    if SheetList:
        for i in SheetList:
            if 'path' in i:
                init['Sheet'].append(i)

    ''' Delete previous set-up '''
    reset_cal(oDesign)

    ''' filed reporter'''
    loss_list, unit_loss_list=[], []

    for i in init['Sheet']:       
        name=B_normal(oDesign, i)
        init['Sheet_plot'].append(name)  
        print '\n B_normal of %s'%(name)

    ''' plot'''
    if init['Sheet_plot']:
        report_t(oDesign, init['Sheet_plot'], form="Rectangular Plot", name='plot')

    ''' export plot'''
    oModule = oDesign.GetModule("ReportSetup")  #have all names of reports
    names= oModule.GetAllREportNames()
    for i in names:
        oModule.ExportToFile(i, init['save_path']+init['ProjectName']+'_'+init['DesignName']+'_'+i+".csv")

    ''' save'''
    oProject.SaveAs(init['save_name']+'.aedt', True)
    #oProject.Save()
    if init['Close']=='On': 
        print '\n Close at %s ' %time.strftime("%d/%m/%Y %I:%M")  
        oProject.close()
    
    
    
if __name__ == '__main__':
    names=[["422_00157_flux_Sec_In", "flux_Tran_82"], ["422_00157_flux_Sec_In", "flux_Tran_110"],
           ["422_00157_flux_Sec_Out", "flux_Tran_82"],["422_00157_flux_Sec_Out", "flux_Tran_110"]]

    for name in names:        
        init['ProjectName'], init['DesignName']=name[0], name[1]
        init['Open'], init['Close']='Off', 'Off'
        init['save_path']="C:/Users/sbaek/Documents/Ansoft/"
        print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")
        main()            

