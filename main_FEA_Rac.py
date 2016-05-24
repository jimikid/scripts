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


def loss(oDesign, Object):
    oModule = oDesign.GetModule("FieldsReporter")
    name=Object+'_loss' 
    oModule.EnterQty("OhmicLoss")
    oModule.EnterVol(Object)
    oModule.CalcOp("Integrate")
    oModule.AddNamedExpression(name, "Fields")
    return name

def volume(oDesign, Object):
    '''
    object : list of the names in Maxwell in string format
    name_list : list of the names in calculator in Maxwell
    '''
    oModule = oDesign.GetModule("FieldsReporter")
    name=Object+'_vol'
    oModule.EnterScalar(1)
    oModule.EnterVol(Object)
    oModule.CalcOp("Integrate")    
    oModule.AddNamedExpression(name, "Fields")    
    return name
          
def unit_loss(oDesign, Object):
    oModule = oDesign.GetModule("FieldsReporter")
    name=Object+'_unit_loss'
    oModule.CopyNamedExprToStack(Object+"_loss")
    oModule.CopyNamedExprToStack(Object+"_vol")
    oModule.CalcOp("/")
    oModule.AddNamedExpression(name, "Fields")  
    return name    
                                                                       
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
    ObList= oEditor.GetObjectsByMaterial('copper')
    
    init['Object']=['AllObjects']
    init['Object_vias']=[]        
    init['Object_del']=[]
    init['Object_plot']=[]    
      
    for i in ObList:
        #if not ('via' in i):
            init['Object'].append(i)            
            
    for i in ObList:
        #if ('del_' in i) or ('via_' in i):
        if ('del_' in i) :
            init['Object_del'].append(i)    
        else:        # plot every item that does not have '_del'
            init['Object_plot'].append(i+'_loss')  # to plot loss of the items, they are named with _loss in calculator
            
        if ('via' in i) :
            init['Object_vias'].append(i)    
    
    print ' copper items including AllObjects : %.0f '  %len(init['Object'])
    print ' copper vias : %.0f '  %len(init['Object_vias'])
    print ' rule out %.0f items from Rac calculation'  %len(init['Object_del'])
    print ' plot %.0f copper items'  %len(init['Object_plot'])
         
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
    for i in init['Object']:       
        name=loss(oDesign, i)
        loss_list.append(name)
        print '\n Set ohmic loss of %s'%(name)    
        
        #name=volume(oDesign, i)
        #print '\n Set volume of %s'%(name)
        
        #name=unit_loss(oDesign, i)
        #unit_loss_list.append(name)
        #print '\n Set unit_loss of %s'%(name)
          
    Rac(oDesign, init['Object_del'])
    Lac(oDesign)

    ''' plot'''
    report(oDesign, ['Rac', 'Lac'])    #put a list of feild parameters in string format, form :"Rectangular Plot", "Data Table"
    
    report(oDesign, init['Object_plot'], form="Rectangular Plot", name='Loss')
    #report(oDesign, unit_loss_list, name='Unit_Loss')

    ''' save'''
    oProject.SaveAs(init['save_name']+'.aedt', True)
    #oProject.Save()
    if init['Close']=='On': 
        print '\n Close at %s ' %time.strftime("%d/%m/%Y %I:%M")  
        oProject.close()
    
    
    
if __name__ == '__main__':         
    names=[["620_00504r03_sp", "pcb_v01_Q14"]]
    for name in names:        
        init['ProjectName'], init['DesignName']=name[0], name[1]
        init['Open'], init['Close']='Off', 'Off'
        init['save_path']="C:/Users/sbaek/Documents/Ansoft/"
        print '\n Start at %s ' %time.strftime("%d/%m/%Y %I:%M")
        main()            
    main()



