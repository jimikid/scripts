import pandas as pd
from os.path import abspath, dirname, exists
print (dirname(dirname(__file__)))
from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np

x, y, z=[], [], []
figsize=(10,7); xlim=(27, 45); ylim=(160, 305); Ind=[96, 103, 110]

for j in Ind:        
    for i in range(3,6):
        plt.figure(1, figsize=figsize)
        foldername="Payton_%s_LL_300W" %(i)
        path = 'C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0718_Payton/Payton_LL_300W/%s/' % foldername
        df=pd.read_csv(path+"summary_LL_300W.csv")
        p_ac_out = df['p_ac_out']
        eff = df['eff']
        #volt_in = df['volt_in']
        volt_in = df['Vdc'] # there are cases fail to boot up
        fault_=df['fault']

        # make up data.
        #npts = int(raw_input('enter # of random points to plot:'))
        seed(0)
        npts = 400
        x, y, z = volt_in, p_ac_out, eff
        
        # define grid.
        xi = np.linspace(33, 45, 100)
        yi = np.linspace(150,310,100)
        # grid the data.
        zi = griddata(x, y, z, xi, yi, interp='linear')
        # contour the gridded data, plotting dots at the nonuniform data points.
        CS = plt.contour(xi, yi, zi, 10, linewidths=0.1, colors='k')
        CS = plt.contourf(xi, yi, zi, 10, cmap=plt.cm.rainbow, vmax=zi.max(), vmin=zi.min(), alpha=0.3)

        plt.colorbar()  # draw colorbar
        #bar=plt.colorbar(ticks=[i for i in range(90, 98, 2)], orientation='vertical') # draw colorbar
        # plot data points.
        plt.scatter(x, y, marker='o', c='b', s=30, zorder=20, alpha=0.9)
        for j in range(len(fault_)):
            if fault_[j] ==True:
                plt.scatter(x[j-1], y[j-1]+3, marker='o', c='r', s=60, zorder=20, alpha=1)
                        
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.title("Eff. [%]" )
        plt.xlabel('Vdc [V]')
        plt.ylabel('P_ac_out [W]')
        plt.savefig(path+'/Eff_'+foldername+'.png')
        plt.close()




        '''
        plt.figure(2, figsize=figsize)
        p_ac_out = df['p_ac_out']
        eff = df['eff']
        Temp = df['Temp']

        from numpy.random import uniform, seed
        from matplotlib.mlab import griddata
        import matplotlib.pyplot as plt
        import numpy as np
        # make up data.
        #npts = int(raw_input('enter # of random points to plot:'))
        seed(0)
        npts = 400
        x = volt_in
        y = p_ac_out
        z = Temp
        # define grid.

        xi = np.linspace(25,30.5,100)
        yi = np.linspace(220,310,100)
        # grid the data.
        zi = griddata(x, y, z, xi, yi, interp='linear')
        # contour the gridded data, plotting dots at the nonuniform data points.
        CS = plt.contour(xi, yi, zi, 5, linewidths=0.1, colors='k')
        CS = plt.contourf(xi, yi, zi, 5, cmap=plt.cm.rainbow,
                          vmax=zi.max(), vmin=zi.min(), alpha=0.3)


        plt.colorbar()  # draw colorbar
        #bar=plt.colorbar(ticks=[i for i in range(90, 98, 2)], orientation='vertical') # draw colorbar
        # plot data points.
        plt.scatter(x, y, marker='o', c='b', s=30, zorder=20, alpha=0.9)
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.title("Temp. %suH [C]" %(j) )
        plt.xlabel('Vdc [V]')
        plt.ylabel('P_ac_out [W]')
        plt.savefig(path+'/Temp_'+foldername+'.png')
        plt.savefig('C:/Users/sbaek/WorkSpace/2016_Hornet_Bench/0708_T1_sat_limit/Temp_'+foldername+'.png')

        plt.close()
        '''
