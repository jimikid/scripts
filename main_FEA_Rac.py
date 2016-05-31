"""
Created on 03/18/2016, @author: sbaek
  V00
    - initial release

  V01 : 05/05/2016
     - AnsysElectronicsDesktop
     - 'para' and 'init' are located ouside main()

  V02 : 05/12/2016
     - 'oEditor.GetObjectsByMaterial('copper')' to read copper objects
     - Objects that needs to be ruled out for Rac calculation is named with 'del_' and automatically removed by a script. 
     - No need to change a script.
     - form="Data Table" is added on report(), table is now default
     - Lac(oDesign) : assuming excitation is 1Arms

  V03 : 05/26/2016
     - Solid and Sheet are devided.
     - Current calculation. 
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


def loss(oDesign, Solid):
    oModule = oDesign.GetModule("FieldsReporter")
    name=Solid+'_loss' 
    oModule.EnterQty("OhmicLoss")
    oModule.EnterVol(Solid)
    oModule.CalcOp("Integrate")
    oModule.AddNamedExpression(name, "Fields")
    return name

def J_real(oDesign, Sheet):
    oModule = oDesign.GetModule("FieldsReporter")
    name=Sheet+'_J_real'     
    oModule.EnterQty("J")
    oModule.CalcOp("Real")
    oModule.EnterSurf(Sheet)
    oModule.CalcOp("NormalComponent")
    oModule.CalcOp("Integrate")
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
          
def unit_loss(oDesign, Solid):
    oModule = oDesign.GetModule("FieldsReporter")
    name=Solid+'_unit_loss'
    oModule.CopyNamedExprToStack(Solid+"_loss")
    oModule.CopyNamedExprToStack(Solid+"_vol")
    oModule.CalcOp("/")
    oModule.AddNamedExpression(name, "Fields")  
    return name    

def I_peak(oDesign, list_sheets):
    print '\n %s ' %time.strftime("%d/%m/%Y %I:%M")
    oModule = oDesign.GetModule("FieldsReporter")
    oModule.CopyNamedExprToStack(list_sheets[0])
    print "\n Ipeak \n %s" %list_sheets[0]
    for i  in list_sheets:
        if i is not list_sheets[0]:                
            oModule.CopyNamedExprToStack(i)
            oModule.CalcOp("+")
            print " +%s" %(i)       
    oModule.AddNamedExpression("I_peak", "Fields")



def Rac(oDesign, list_subt):
    print '\n %s ' %time.strftime("%d/%m/%Y %I:%M")
    oModule = oDesign.GetModule("FieldsReporter")
    oModule.CopyNamedExprToStack("AllObjects_Loss")
    print "\n Rac = \n AllObjects_Loss"
    for i in list_subt:
        oModule.CopyNamedExprToStack(i+'_loss')
        oModule.CalcOp("-")
        print " -%s" %(i+'_loss')       
    oModule.AddNamedExpression("Rac", "Fields")

def Lac(oDesign):
    print '\n %s ' %time.strftime("%d/%m/%Y %I:%M")
    oModule = oDesign.GetModule("FieldsReporter")
    oModule.EnterQty("energy")
    oModule.EnterVol("AllObjects")
    oModule.CalcOp("Integrate")
    oModule.AddNamedExpression("Lac", "Fields")

    
def report(oDesign, item, name="XY Plot 1", form="Data Table"):  #form :"Rectangular Plot", "Data Table"
    print '\n %s ' %time.strftime("%d/%m/%Y %I:%M")
    oModule = oDesign.GetModule("ReportSetup")
    oModule.CreateReport(name, "Fields", form, "Setup1 : LastAdaptive", 
    	[
    		"Domain:="		, "Sweep"
    	], 
    	[
    		"Freq:="		, ["All"],
    		"Phase:="		, ["0deg"],
    	], 
    	[
    		"X Component:="		, "Freq",
                #"Y Component:="		, ["Rac","Lac"]
                "Y Component:="		, item
    	], [])     
  

def main():      
    init['save_name']=init['save_path']+init['ProjectName']    
    ''' Initiation, solution type'''
    oProject, oDesign=initiation()


    ''' Build lists of objects '''    
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    SolidList= oEditor.GetObjectsByMaterial('copper')  #SolidList is in list
    #oEditor.GetObjectsInGroup('solids')
    SheetList=oEditor.GetObjectsInGroup('sheets')
    
    init['Solid']=['AllObjects']
    init['Sheet']=[]
    init['Solid_plot']=[]    
    init['Sheet_plot']=[]    
    
    init['Solid_vias']=[]        
    init['Solid_del']=[]
     
    if  SolidList:
        for i in SolidList:
            #if not ('via' in i):
                init['Solid'].append(i)       
        for i in SolidList:
            #if ('del_' in i) or ('via_' in i):
            if ('del' in i) :
                init['Solid_del'].append(i)                    
            if ('via' in i) :
                init['Solid_vias'].append(i)    
        
        print ' copper items including AllObjects : %.0f '  %len(init['Solid'])
        print ' copper vias : %.0f '  %len(init['Solid_vias'])
        print ' rule out %.0f items from Rac calculation'  %len(init['Solid_del'])        
    else: pass
    
    if SheetList:
        for i in SheetList:
            if 'Section1' in i:
                init['Sheet'].append(i)                         

                
    ''' Delete previous set-up '''    
    try:
        oModule = oDesign.GetModule("FieldsReporter")
        oModule.CalcStack("clear")
        oModule.ClearAllNamedExpr()
        print '\n Delete expressions in a calculator'
    
        oModule = oDesign.GetModule("ReportSetup")
        oModule.DeleteAllReports()
        print ' Delete plots'
    except:pass

    
    ''' filed reporter'''
    loss_list, unit_loss_list=[], []
    for i in init['Solid']:       
        name=loss(oDesign, i)
        if ('All' not in i) and ('del' not in i):
            init['Solid_plot'].append(name)  
        print '\n ohmic loss of %s'%(name)        

    for i in init['Sheet']:       
        name=J_real(oDesign, i)
        init['Sheet_plot'].append(name)  
        print '\n J_real of %s'%(name)        
          
    Rac(oDesign, init['Solid_del'])
    I_peak(oDesign, init['Sheet_plot'])
    Lac(oDesign)

    ''' plot'''
    report(oDesign, ['Rac', 'Lac', 'I_peak'])    #put a list of feild parameters in string format, form :"Rectangular Plot", "Data Table"    
    if init['Solid_plot']: 
        report(oDesign, init['Solid_plot'], form="Rectangular Plot", name='Loss')
    if init['Sheet_plot']:     
        report(oDesign, init['Sheet_plot'], form="Rectangular Plot", name='J_real')

    ''' save'''
    oProject.SaveAs(init['save_name']+'.aedt', True)
    #oProject.Save()
    if init['Close']=='On': 
        print '\n Close at %s ' %time.strftime("%d/%m/%Y %I:%M")  
        oProject.close()
    
    
    
if __name__ == '__main__':        
    
    names=[["620_00504r03_Q14_100k", "pcb_v01_Q14"], ["620_00504r03_Q14_100k", "pcb_v02_Q14"]]

    for name in names:        
        init['ProjectName'], init['DesignName']=name[0], name[1]
        init['Open'], init['Close']='Off', 'Off'
        init['save_path']="C:/Users/sbaek/Documents/Ansoft/"
        print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")
        main()            

