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
oAnsoftApp = win32com.client.Dispatch("Ansoft.ElectronicsDesktop")
oDesktop = oAnsoftApp.GetAppDesktop()
    
def main(name):    
    ProjectName=name[0]
    DesignName=name[1]
    
   
    oDesktop.RestoreWindow()  
    oProject = oDesktop.SetActiveProject(ProjectName)
    oDesign = oProject.SetActiveDesign(DesignName)

    oDesign.AnalyzeAll()
    oProject.Save()

   
if __name__ == '__main__':            
    names=[["620_00504r03_Q14", "pcb_v01_Q14"],
           ["620_00504r03_Q14", "pcb_v02_Q14"]]
    for name in names:
        try:
            main(name)
        except:
            pass

