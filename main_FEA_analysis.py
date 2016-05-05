"""
Created on 03/18/2016, @author: sbaek
  V00
    - initial release
    
  V01 : 05/05/2016
     - AnsysElectronicsDesktop
"""
from __future__ import division 
from math import *
import win32com.client 

def main(it, names):    
    ProjectName=names[0]
    DesignName=names[1]
    
    oAnsoftApp = win32com.client.Dispatch("Ansoft.ElectronicsDesktop")
    oDesktop = oAnsoftApp.GetAppDesktop()        
    oDesktop.RestoreWindow()  
    oProject = oDesktop.SetActiveProject(ProjectName)
    oDesign = oProject.SetActiveDesign(DesignName)

    oDesign.AnalyzeAll()

    oProject.Save()
    oProject.close()

   
if __name__ == '__main__':            
    names=[["620-00504r03_0504", "pcb_v01_Q14" ]]
    for it in range(len(names)):
        main(it, names[it])

